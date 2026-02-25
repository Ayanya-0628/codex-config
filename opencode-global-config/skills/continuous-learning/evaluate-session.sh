#!/bin/bash
# Continuous Learning - OpenCode Session Evaluator
#
# Goal:
# - detect repeated user corrections / preference signals
# - append durable notes to learned files

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONFIG_FILE="$SCRIPT_DIR/config.json"

DEFAULT_LEARNED="${HOME}/.config/opencode/skills/learned"
DEFAULT_PREFERENCES="${DEFAULT_LEARNED}/user-preferences.md"
DEFAULT_MIN=6

read_config() {
  local key="$1"
  local fallback="$2"
  python - "$CONFIG_FILE" "$key" "$fallback" <<'PY'
import json, os, sys
cfg, key, fallback = sys.argv[1], sys.argv[2], sys.argv[3]
val = fallback
try:
    with open(cfg, "r", encoding="utf-8") as f:
        data = json.load(f)
    v = data.get(key, fallback)
    if isinstance(v, (dict, list)):
        print(fallback)
    else:
        print(str(v))
except Exception:
    print(fallback)
PY
}

LEARNED_SKILLS_PATH="$(read_config "learned_skills_path" "$DEFAULT_LEARNED")"
PREFERENCES_PATH="$(read_config "preferences_path" "$DEFAULT_PREFERENCES")"
MIN_SESSION_LENGTH="$(read_config "min_session_length" "$DEFAULT_MIN")"

LEARNED_SKILLS_PATH="${LEARNED_SKILLS_PATH/#\~/$HOME}"
PREFERENCES_PATH="${PREFERENCES_PATH/#\~/$HOME}"

mkdir -p "$LEARNED_SKILLS_PATH"
mkdir -p "$(dirname "$PREFERENCES_PATH")"

transcript_path="${OPENCODE_TRANSCRIPT_PATH:-${CLAUDE_TRANSCRIPT_PATH:-${TRANSCRIPT_PATH:-}}}"

if [ -z "$transcript_path" ] || [ ! -f "$transcript_path" ]; then
  echo "[ContinuousLearning] No transcript path provided, skip extraction." >&2
  exit 0
fi

message_count=$(python - "$transcript_path" <<'PY'
import json, sys
path = sys.argv[1]
count = 0
with open(path, "r", encoding="utf-8", errors="ignore") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        try:
            obj = json.loads(line)
        except Exception:
            continue
        role = obj.get("role")
        if role == "user":
            count += 1
            continue
        msg = obj.get("message", {})
        if msg.get("role") == "user":
            count += 1
print(count)
PY
)

if [ "${message_count:-0}" -lt "$MIN_SESSION_LENGTH" ]; then
  echo "[ContinuousLearning] Session too short ($message_count < $MIN_SESSION_LENGTH), skipping." >&2
  exit 0
fi

python - "$transcript_path" "$PREFERENCES_PATH" <<'PY'
import json
import os
import re
import sys
from datetime import datetime

transcript_path, out_path = sys.argv[1], sys.argv[2]

signals = []
patterns = [
    r"必须",
    r"不要",
    r"每次",
    r"默认",
    r"请始终",
    r"改成",
    r"优化一下",
    r"记得",
]

with open(transcript_path, "r", encoding="utf-8", errors="ignore") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        try:
            obj = json.loads(line)
        except Exception:
            continue
        text = ""
        role = obj.get("role")
        if role == "user":
            content = obj.get("content", "")
            if isinstance(content, str):
                text = content
            elif isinstance(content, list):
                text = "\n".join(str(x.get("text", "")) for x in content if isinstance(x, dict))
        else:
            msg = obj.get("message", {})
            if msg.get("role") != "user":
                continue
            content = msg.get("content", [])
            if isinstance(content, list):
                text = "\n".join(str(x.get("text", "")) for x in content if isinstance(x, dict))
        if not text:
            continue
        lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
        for ln in lines:
            if any(re.search(p, ln) for p in patterns):
                signals.append(ln)

signals = signals[-8:]
if not signals:
    sys.exit(0)

os.makedirs(os.path.dirname(out_path), exist_ok=True)
ts = datetime.now().strftime("%Y-%m-%d %H:%M")
with open(out_path, "a", encoding="utf-8") as f:
    f.write(f"\n## {ts}\n")
    f.write(f"- Source: {transcript_path}\n")
    for s in signals:
        f.write(f"- Preference signal: {s}\n")

print(f"[ContinuousLearning] Appended {len(signals)} preference signals to {out_path}")
PY

echo "[ContinuousLearning] Session has ${message_count} user messages. Learned notes updated." >&2
