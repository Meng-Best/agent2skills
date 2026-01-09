# .claude 目录结构说明

此目录是 **Claude Code** 的项目级配置目录，用于存放自定义代理、技能、命令和设置文件。

## 目录结构概览

```
.claude/
├── README.md              # 本说明文件
├── settings.json          # 项目级设置（可提交到 Git）
├── settings.local.json    # 本地设置（不应提交到 Git）
├── agents/                # 自定义代理定义
│   └── tech-docs-writer.md
├── commands/              # 自定义命令（斜杠命令）
└── skills/                # 自定义技能
    ├── commit_push/
    │   └── SKILL.md
    └── commit_push_force/
        └── SKILL.md
```

---

## 文件说明

### `settings.json`
**作用**：项目级别的 Claude Code 配置文件，可提交到版本控制。

**当前配置**：
- 启用了 `code-review@claude-plugins-official` 插件

**示例内容**：
```json
{
  "enabledPlugins": {
    "code-review@claude-plugins-official": true
  }
}
```

---

### `settings.local.json`
**作用**：本地专用设置文件，用于存放不应提交到 Git 的个人配置（如权限白名单）。

**当前配置**：
- 定义了一系列允许自动执行的 Bash 命令权限

> ⚠️ **注意**：此文件应添加到 `.gitignore`，避免泄露本地环境信息。

---

## 文件夹说明

### `agents/` - 自定义代理

存放自定义的 AI 代理定义文件，每个 `.md` 文件定义一个代理。

#### `tech-docs-writer.md`
| 属性 | 值 |
|------|-----|
| **名称** | tech-docs-writer |
| **模型** | opus |
| **用途** | 技术文档编写专家代理 |

**功能特性**：
- 创建和维护 README 文件
- 编写 API 文档
- 生成架构设计文档
- 编写安装和配置指南
- 创建变更日志和发布说明

**调用方式**：Claude Code 会在需要创建或更新技术文档时自动调用此代理。

---

### `commands/` - 自定义命令

存放自定义的斜杠命令，当前为空目录。

**用途**：可在此目录创建 `.md` 文件来定义自定义命令，通过 `/命令名` 方式调用。

---

### `skills/` - 自定义技能

存放可通过 `/技能名` 调用的自定义技能。

#### `commit_push/SKILL.md`
| 属性 | 值 |
|------|-----|
| **名称** | commit_push |
| **调用方式** | `/commit_push` |

**功能描述**：
AI 自动分析代码变更，生成符合 **Conventional Commits** 规范的提交信息，并一键推送到远程仓库。

**执行流程**：
1. 暂存所有变更 (`git add -A`)
2. 读取差异 (`git diff --cached`)
3. AI 分析并生成 Commit Message
4. 执行提交 (`git commit`)
5. 识别当前分支并推送 (`git push`)

**参数**：
- `additional_context` (可选): 辅助信息，如关联的 Issue 编号

---

#### `commit_push_force/SKILL.md`
| 属性 | 值 |
|------|-----|
| **名称** | commit_push_force |
| **调用方式** | `/commit_push_force` 或 `/commit_push_force !` |

**功能描述**：
与 `commit_push` 类似，但支持 **静默模式**。在指令中添加 `!` 符号可跳过所有交互确认，实现全自动执行。

**模式说明**：
- **交互模式**（默认）：生成信息后询问用户确认
- **静默模式**（添加 `!`）：直接执行所有操作，无需确认

---

## 扩展指南

### 添加新代理
在 `agents/` 目录创建 `.md` 文件，格式如下：
```markdown
---
name: 代理名称
description: 代理描述
model: sonnet/opus/haiku
---

代理的系统提示词内容...
```

### 添加新技能
在 `skills/` 目录创建子文件夹，并在其中创建 `SKILL.md` 文件：
```
skills/
└── 技能名称/
    └── SKILL.md
```

### 添加新命令
在 `commands/` 目录创建 `.md` 文件，文件名即为命令名。

---

## 相关文档

- [Claude Code 官方文档](https://docs.anthropic.com/claude-code)
- [Conventional Commits 规范](https://www.conventionalcommits.org/)
