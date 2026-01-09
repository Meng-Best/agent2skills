# git-init

一键完成项目首次 Git 仓库初始化、提交并推送到 GitHub。

## 触发方式

```
/git-init <GitHub仓库URL>
```

**示例：**
```
/git-init https://github.com/username/my-project
/git-init git@github.com:username/my-project.git
```

## 功能说明

此 skill 执行以下操作（全自动，无交互）：

1. **Git 初始化** - 如果当前目录不是 git 仓库，执行 `git init`
2. **检测项目类型** - 自动识别 Node.js/TypeScript、Python、Go 项目
3. **生成 .gitignore** - 根据项目类型生成合适的 .gitignore（已存在则智能合并）
4. **创建 README.md** - 如果不存在，使用项目名生成基础 README
5. **创建 LICENSE** - 如果不存在，创建 Apache-2.0 许可证
6. **首次提交** - `git add .` 并生成描述性 commit message
7. **关联远程** - `git remote add origin <URL>`
8. **推送** - `git push -u origin <branch>`

## 执行步骤

当用户调用 `/git-init <URL>` 时，按以下步骤执行：

### Step 1: 验证参数
- 检查 URL 参数是否提供
- 验证 URL 格式是否为有效的 GitHub 仓库地址

### Step 2: Git 初始化
```bash
# 检查是否已是 git 仓库
git rev-parse --git-dir 2>/dev/null

# 如果不是，初始化
git init
```

### Step 3: 检测项目类型
检测以下文件确定项目类型：

| 项目类型 | 检测文件 |
|----------|----------|
| Node.js/TypeScript | `package.json`, `tsconfig.json` |
| Python | `requirements.txt`, `pyproject.toml`, `setup.py`, `Pipfile` |
| Go | `go.mod` |

### Step 4: 生成 .gitignore
根据检测到的项目类型，生成或合并 .gitignore：

**Node.js/TypeScript:**
```gitignore
node_modules/
dist/
build/
.env
.env.local
*.log
npm-debug.log*
.DS_Store
coverage/
.nyc_output/
```

**Python:**
```gitignore
__pycache__/
*.py[cod]
*$py.class
.venv/
venv/
env/
.env
*.egg-info/
dist/
build/
.pytest_cache/
.coverage
htmlcov/
```

**Go:**
```gitignore
bin/
*.exe
*.exe~
*.dll
*.so
*.dylib
*.test
*.out
vendor/
.env
```

### Step 5: 创建 README.md（如不存在）
使用当前目录名作为项目名，生成：

```markdown
# {项目名}

## 简介

[项目描述待补充]

## 安装

[安装说明待补充]

## 使用

[使用说明待补充]

## 许可证

Apache-2.0
```

### Step 6: 创建 LICENSE（如不存在）
创建 Apache-2.0 许可证文件，自动填充：
- 当前年份
- 用户名（从 `git config user.name` 获取）

### Step 7: 首次提交
```bash
git add .
git commit -m "🎉 Initial commit: {项目类型} project

- 初始化项目结构
- 添加 .gitignore
- 添加 README.md
- 添加 LICENSE (Apache-2.0)"
```

### Step 8: 关联远程并推送
```bash
git remote add origin <URL>
git branch -M main
git push -u origin main
```

## 输出格式

执行过程中输出调试级信息：

```
══════════════════════════════════════════════════════════
                    🚀 git-init
══════════════════════════════════════════════════════════

[1/6] Git 初始化...
      $ git init
      ✓ 完成

[2/6] 检测项目类型...
      ✓ Node.js/TypeScript

[3/6] 生成 .gitignore...
      ✓ 已创建 (Node.js 模板)

[4/6] 创建 README.md...
      ✓ 已创建

[5/6] 创建 LICENSE...
      ✓ 已创建 (Apache-2.0)

[6/6] 提交并推送...
      $ git add .
      $ git commit -m "🎉 Initial commit..."
      $ git remote add origin https://github.com/user/repo
      $ git push -u origin main
      ✓ 完成

══════════════════════════════════════════════════════════
✅ 初始化完成!
   仓库: https://github.com/user/repo
   分支: main
══════════════════════════════════════════════════════════
```

## 错误处理

| 错误场景 | 处理方式 |
|----------|----------|
| 未提供 URL | 报错：请提供 GitHub 仓库 URL |
| URL 格式无效 | 报错：URL 格式不正确 |
| git 未安装 | 报错：请先安装 git |
| 远程已存在 | 跳过 remote add，直接 push |
| push 失败 | 显示错误信息，提示手动处理 |

## 注意事项

- 此 skill 会自动执行 git push，请确保 URL 对应的仓库已在 GitHub 上创建
- 如果本地已有提交历史，会推送所有现有提交
- LICENSE 默认使用 Apache-2.0，如需其他许可证请手动修改
