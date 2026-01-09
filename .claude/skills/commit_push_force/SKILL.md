---
name: commit_push_force
description: AI 自动分析代码变更并推送。支持 "!" 模式跳过交互，实现全自动执行。
parameters:
  - name: query
    type: string
    required: false
    description: 用户指令。如果包含 "!" 符号（例如 "/smart_commit_push !"），将开启全自动静默执行模式，跳过所有人工确认。
returns:
  type: object
  description: 包含最终生成的 Commit 信息、分支名及执行状态。
---

# 技能实现细节

## 模式判定逻辑
1. **静默模式检测**：检查 `query` 参数。如果包含 `!` 字符，或者用户明确表示“直接推”、“不需要确认”，则将 `SILENT_MODE` 设为 `true`。
2. **静默模式行为**：在 `SILENT_MODE` 为 `true` 时，严禁中途停顿或询问，必须根据 AI 分析结果直接完成所有 Git 操作。

## 第一阶段：环境与变更分析 (Win11)
1. **暂存全部**：执行 `git add -A`。
2. **状态核查**：执行 `git status --porcelain`。
   - 如果为空，终止并告知用户：“工作区无变更”。
3. **读取差异**：执行 `git diff --cached`。AI 必须阅读此 diff 以理解代码逻辑。

## 第二阶段：AI 自动生成 Commit 信息
根据 diff 内容，生成一个极其简练且符合 **Conventional Commits** 规范的标题：
- **格式**：`<type>(<scope>): <subject>`
- **Type 选择**：根据改动本质选择 `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `chore`。
- **内容要求**：使用英文祈使句，描述“为什么改”而非“改了哪个文件”。

## 第三阶段：原子化执行序列
> [!IMPORTANT]
> 在 Windows 11 环境下，请按顺序执行以下指令，不要使用复杂的 Shell 嵌套。

1. **执行提交**：
   - 如果 `SILENT_MODE` 是 `false`：展示生成的信息，询问用户“是否执行提交并推送？”。
   - 如果 `SILENT_MODE` 是 `true`：直接运行 `git commit -m "<AI_Generated_Message>"`。
2. **识别分支**：运行 `git branch --show-current`。获取输出结果（如 `main`）。
3. **推送远程**：使用获取到的分支名，运行 `git push origin <branch_name>`。

## 异常处理 (Win11 优化)
- **推送冲突**：若提示 `non-fast-forward`，立即停止并建议用户执行 `git pull --rebase`，不要强推。
- **身份验证**：若在推送阶段卡住或报错，提醒用户检查 Win11 的 Git 凭据管理器。

## 成功反馈
- ✨ **Commit**: <AI_Generated_Message>
- 🚀 **Push**: 已成功推送到 <branch_name> 分支
- 💡 **Mode**: <Silent/Interactive>