---
name: awesome-ai-research-writing
description: "论文写作 Prompt 模板库与技能导航：翻译/润色/去 AI 味/逻辑检查/Reviewer 视角审视/图表标题/实验分析等。适合在不同写作任务间快速选用成熟模板。"
---

# Awesome AI Research Writing（模板库导航技能）

本技能本质上是一个“科研写作 Prompt 模板库 + 使用教程”的本地镜像，适合在你不确定该如何下指令、或需要更强约束的写作场景下使用。

## 何时使用
- 你想快速套用成熟模板（翻译、润色、去 AI 味、逻辑检查、Reviewer 视角审视、图表标题、实验分析等）。
- 你需要“强约束输出协议”（例如：必须输出纯文本可粘贴 Word、或必须输出 LaTeX 源码且转义特殊字符）。

## 使用方法（最小工作流）
1. 打开本技能同目录下的 `README.md`，按目录定位到对应场景（如“去 AI 味”“逻辑检查”“Reviewer 视角”）。
2. 复制相应 Prompt（或根据你的场景做最小改动：替换输入区、字数/风格约束）。
3. 将你的原文粘贴到 Prompt 的 Input 区执行。

## 与 `academic-bilingual-polishing` 的协同建议
- 想要“最终可直接进论文的文本”：优先使用 `academic-bilingual-polishing` 的 `academic-polish/ai-rewrite/format-optimize`。
- 想要“模板化强约束/审稿人视角/诊断型输出”：先用本技能在 `README.md` 里挑模板做一次诊断/改写，再把结果交给 `academic-bilingual-polishing` 做最终定稿与格式统一。

