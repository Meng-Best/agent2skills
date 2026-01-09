---
name: commit_push
description: AI 自动分析代码变更，生成符合 Conventional Commits 规范的提交信息，并在 Win11 环境下一键推送。
parameters:
  - name: additional_context
    type: string
    required: false
    description: 辅助信息（例如关联的 Issue 编号），AI 将其结合到自动生成的总结中。
returns:
  type: object
  description: 包含最终生成的 Commit Message 和推送状态。
---

# 技能实现细节

## 第一阶段：深度代码分析 (AI 核心任务)
1. **暂存变更**：运行 `git add -A` 以确保所有改动都在暂存区。
2. **读取差异**：运行 `git diff --cached`。
3. **意图推理**：
   - AI 必须阅读 diff 内容，识别改动的是逻辑、样式、文档还是配置。
   - **严禁** 生成模糊的描述（如 "update files"）。
   - **必须** 识别核心改动（例如：如果改动了 `auth.ts` 里的逻辑，总结应聚焦于“认证逻辑”而非“修改文件”）。



## 第二阶段：消息构建规范
生成的提交信息必须遵循以下结构：
- **格式**：`<type>(<scope>): <subject>`
- **Type 准则**：
  - `feat`: 新功能
  - `fix`: 修复 Bug
  - `docs`: 文档更新
  - `refactor`: 重构（既不修复 Bug 也不添加功能的代码更改）
  - `chore`: 构建流程或辅助工具的变动
- **Subject 准则**：
  - 使用祈使句（例如 "add" 而不是 "added"）。
  - 全长度建议控制在 50 个字符以内。
  - 如果提供了 `additional_context`，将其整合在描述中。

## 第三阶段：Win11 原子化执行序列
> [!IMPORTANT]
> 请按顺序逐条执行，确保在 Windows 终端（PowerShell/CMD）中路径和分支识别准确。

1. **执行提交**：使用 AI 总结的信息运行 `git commit -m "<AI_Generated_Message>"`。
2. **识别分支**：运行 `git branch --show-current` 并捕获输出。
3. **执行推送**：使用捕获的分支名运行 `git push origin <branch_name>`。

## 错误处理
- **无变更**：若 `git diff --cached` 为空，告知用户“没有检测到需要提交的变更”。
- **推送冲突**：若发生冲突，停止并提示用户手动解决，不要尝试强推。

## 成功总结
- ✨ **AI 总结**: <Generated_Message>
- 🚩 **推送分支**: <branch_name>
- 🔗 **状态**: 成功同步至 GitHub