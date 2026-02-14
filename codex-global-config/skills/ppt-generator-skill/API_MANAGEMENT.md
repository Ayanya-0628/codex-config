# API 密钥管理规范

## 📋 当前配置

### API 存储位置

所�?API 密钥现在统一存储在：

```
📁 ppt-generator/.env
```

### �?安全验证

- �?`.env` 文件已创�?
- �?已被 `.gitignore` 保护（第15行规则）
- �?不会被提交到 Git
- �?`run.sh` 可以正确加载

### 🎯 使用方法

**无需任何额外配置�?* 直接使用即可�?

```bash
./run.sh --plan slides_plan.json --style styles/gradient-glass.md --resolution 2K
```

输出显示�?
```
📌 �?.env 文件加载API密钥
```

---

## 🔐 API 管理规范

### 1️⃣ 添加新的 API 密钥

编辑 `.env` 文件�?

```bash
# 使用编辑器打开
nano .env

# 或使�?VS Code
code .env
```

按照以下格式添加�?

```bash
# API 名称说明
# 用途：描述这个 API 的用�?
# 获取地址：https://...
API_NAME=your-api-key-here
```

**示例**�?

```bash
# OpenAI API
# 用途：未来可能用于文档分析
# 获取地址：https://platform.openai.com/api-keys
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxx
```

### 2️⃣ 在代码中使用 API 密钥

**�?错误做法**（硬编码）：

```python
# 绝对不要这样做！
api_key = "AIzaSyAfHE4vctPhMF2mVn96aEZZp8WuURlaGpM"
```

**�?正确做法**（从环境变量读取）：

```python
import os

# 从环境变量读�?
api_key = os.environ.get("GEMINI_API_KEY")

# 或带默认�?
api_key = os.getenv("GEMINI_API_KEY", "")

# 检查是否存�?
if not api_key:
    raise ValueError("未找�?GEMINI_API_KEY 环境变量")
```

### 3️⃣ 环境变量加载优先�?

`run.sh` 的加载逻辑�?

```
1. 系统环境变量（~/.zshrc 等）
   �?如果没有
2. .env 文件
   �?如果都没�?
3. 报错提示用户配置
```

这意味着�?
- �?CI/CD 环境可以使用系统环境变量
- �?本地开发使�?.env 文件
- �?灵活切换不同环境的密�?

### 4️⃣ 多环境管�?

如果需要管理多个环境（开�?测试/生产）：

```bash
# 开发环�?
.env.development

# 测试环境
.env.test

# 生产环境
.env.production
```

使用时指定：

```bash
# 复制对应环境的配�?
cp .env.development .env

# 或使用符号链�?
ln -sf .env.development .env
```

---

## 📝 .env 文件结构

### 当前结构

```bash
.env
├─ [注释区域]
�? ├─ 安全提醒
�? ├─ 使用说明
�? └─ 加载优先级说�?
�?
├─ [主要 API 密钥]
�? └─ GEMINI_API_KEY (已配�?
�?
├─ [备用 API 密钥]
�? ├─ OPENAI_API_KEY (注释状�?
�? ├─ ANTHROPIC_API_KEY (注释状�?
�? └─ STABILITY_API_KEY (注释状�?
�?
└─ [项目配置]
   ├─ DEFAULT_RESOLUTION (注释状�?
   ├─ DEFAULT_STYLE (注释状�?
   └─ OUTPUT_DIR (注释状�?
```

### 字段说明

| 变量�?| 状�?| 用�?| 获取地址 |
|--------|------|------|----------|
| `GEMINI_API_KEY` | �?已配�?| Nano Banana Pro 图像生成 | [Google AI Studio](https://makersuite.google.com/app/apikey) |
| `OPENAI_API_KEY` | 💤 预留 | 未来可能用于文档分析 | [OpenAI Platform](https://platform.openai.com/api-keys) |
| `ANTHROPIC_API_KEY` | 💤 预留 | 未来可能用于Claude API | [Anthropic Console](https://console.anthropic.com/) |
| `STABILITY_API_KEY` | 💤 预留 | 未来可能用于其他图像模型 | [Stability AI](https://platform.stability.ai/) |

---

## 🚨 安全检查清�?

### 开发时

- [ ] 从不在代码中硬编�?API 密钥
- [ ] 使用 `os.environ.get()` �?`os.getenv()` 读取
- [ ] 添加密钥缺失时的错误提示
- [ ] 在函�?类初始化时读取，不要每次请求都读

### 提交�?

- [ ] 运行 `git status` 确认 .env 不在列表�?
- [ ] 运行 `grep -r "AIzaSy" --exclude-dir=.git .` 无输�?
- [ ] 检�?`.gitignore` 包含 `.env`
- [ ] 代码中无任何硬编码的密钥

### 分享项目�?

- [ ] 提供 `.env.example` 作为模板
- [ ] �?README 中说明如何配�?
- [ ] 不要通过聊天/邮件发�?.env 文件
- [ ] 建议用户使用自己�?API 密钥

---

## 💡 最佳实�?

### 1. 密钥轮换

定期更新 API 密钥（建�?3-6 个月）：

```bash
# 1. �?API 平台生成新密�?
# 2. 更新 .env 文件
# 3. 测试功能正常
# 4. 撤销旧密�?
```

### 2. 密钥权限

为不同用途创建不同的 API 密钥�?

```bash
# 开发用（限制配额）
GEMINI_API_KEY_DEV=...

# 生产用（完整权限�?
GEMINI_API_KEY_PROD=...
```

### 3. 错误处理

代码中添加友好的错误提示�?

```python
import os
import sys

def get_api_key(key_name):
    """安全获取 API 密钥"""
    api_key = os.getenv(key_name)

    if not api_key:
        print(f"�?错误: 未找�?{key_name} 环境变量")
        print("")
        print("请配�?API 密钥�?)
        print("1. 编辑 .env 文件")
        print("2. 添加：{key_name}=your-key")
        print("3. 保存并重新运�?)
        sys.exit(1)

    return api_key

# 使用
gemini_key = get_api_key("GEMINI_API_KEY")
```

### 4. 日志安全

不要在日志中输出完整密钥�?

```python
# �?危险
print(f"Using API key: {api_key}")

# �?安全
print(f"Using API key: {api_key[:8]}...{api_key[-4:]}")
# 输出: Using API key: AIzaSyAf...GpM
```

---

## 🔄 迁移指南

### 从系统环境变量迁移到 .env

如果您之前在 `~/.zshrc` 中配置了密钥�?

**步骤1**: �?.zshrc 删除

```bash
# 编辑配置文件
nano ~/.zshrc

# 删除这一�?
export GEMINI_API_KEY="..."

# 重新加载
source ~/.zshrc
```

**步骤2**: 添加�?.env

```bash
# .env 文件已包含密钥，无需额外操作
```

**步骤3**: 测试

```bash
./run.sh --help
# 应该显示：�?�?.env 文件加载API密钥
```

### �?.env 迁移到系统环境变�?

如果您想使用系统环境变量（跨项目共享）：

```bash
# 1. 复制 .env 中的密钥
cat .env | grep GEMINI_API_KEY

# 2. 添加�?.zshrc
echo 'export GEMINI_API_KEY="..."' >> ~/.zshrc

# 3. 重新加载
source ~/.zshrc

# 4. 测试
./run.sh --help
# 应该显示：✅ 使用系统环境变量中的API密钥
```

---

## 📚 相关文档

- **SECURITY.md** - 完整的安全指�?
- **ENV_SETUP.md** - 环境变量配置详解
- **.env.example** - 配置模板
- **README.md** - 项目使用说明

---

## 🆘 常见问题

### Q: .env 文件在哪里？

A: 在项目根目录 `ppt-generator/.env`

### Q: 如何查看我的 API 密钥�?

A:
```bash
cat .env | grep GEMINI_API_KEY
```

### Q: 可以提交 .env 文件吗？

A: **绝对不可以！** .env 文件包含敏感信息，已�?.gitignore 保护�?

### Q: 团队协作时如何共享配置？

A:
1. 提交 `.env.example` 模板
2. 团队成员复制�?`.env`
3. 各自填入自己�?API 密钥

### Q: 如何知道密钥是从哪里加载的？

A: 运行任何命令时查看输出：
- `�?使用系统环境变量中的API密钥` - 从系统加�?
- `📌 �?.env 文件加载API密钥` - �?.env 加载

---

## �?总结

### 当前配置

�?**API 密钥统一管理**
- 存储位置：`ppt-generator/.env`
- 安全保护：`.gitignore` 规则
- 自动加载：`run.sh` 脚本

�?**开发规�?*
- 不在代码中硬编码
- 使用 `os.getenv()` 读取
- 添加错误处理
- 日志中不输出完整密钥

�?**安全保证**
- .env 不会提交�?Git
- .env.example 作为模板
- 定期轮换密钥
- 不同环境使用不同密钥

### 立即可用

现在您可以直接开始迭代功能，所�?API 配置都已就绪�?

```bash
# 直接使用
./run.sh --plan your_plan.json --style styles/gradient-glass.md
```

---

**创建日期**: 2026-01-11
**最后更�?*: 2026-01-11
**创作�?*: 歸藏
