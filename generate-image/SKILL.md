---
name: generate-image
description: 使用 Gemini 生成图片。文生图、图生图。
---

# 文生图技能

使用 Google Gemini 3 Pro Image Preview 生成高质量图片。

## 触发方式

```
generate-image 提示词 宽高比 分辨率
```

### 参数说明

| 参数 | 必需 | 说明 | 示例 |
|------|------|------|------|
| 提示词 | 是 | 图片描述，支持中英文（中文自动翻译） | `赛博朋克城市` |
| 宽高比 | 否 | 图片比例 | `16:9`, `1:1`, `9:16` |
| 分辨率 | 否 | 图片精度 | `1K`, `2K`, `4K` |

### 触发示例

```
generate-image 一只橘猫在阳光下睡觉
generate-image 赛博朋克城市夜景 16:9 4K
generate-image 极简风格logo 1:1 2K
```

## 脚本调用

```bash
！python scripts/generate_image.py "提示词" -r 宽高比 -s 分辨率
```

### 完整参数

| 参数 | 说明 |
|------|------|
| `prompt` | 图片描述（必需，中文自动翻译为英文） |
| `-o` | 输出路径（默认当前目录 `generated.png`） |
| `-i` | 输入图片路径（启用编辑模式） |
| `-r` | 宽高比：`1:1`, `16:9`, `9:16`, `4:3`, `3:4`, `3:2`, `2:3` |
| `-s` | 分辨率：`1K`, `2K`, `4K` |

### 脚本示例

```bash
# 基础生成（输出到当前目录）
python scripts/generate_image.py "一只橘猫在阳光下睡觉"

# 指定比例和分辨率
python scripts/generate_image.py "cyberpunk city" -r 16:9 -s 4K

# 图生图（编辑现有图片）
python scripts/generate_image.py "把天空换成星空" -i photo.jpg

# 指定输出路径
python scripts/generate_image.py "森林小屋" -o images/cabin.png
```

## API Key 配置

在 `.env` 文件中配置：

```
GEMINI_API_KEY=your-api-key
```

获取地址：https://aistudio.google.com/apikey

## 特性

- **中文自动翻译**：检测到中文提示词时自动翻译为英文
- **高质量系统指令**：内置优化指令，引导生成专业构图、光影、色彩
- **灵活宽高比**：支持多种常见比例
- **高清输出**：支持最高 4K 分辨率（4096x4096）

## 提示词技巧

### 结构化描述

按 **主体 → 场景 → 风格 → 细节** 组织：

```
一只橘猫趴在窗台上，午后阳光透过纱帘，暖色调，摄影风格
```

### 常用风格词

| 类型 | 关键词 |
|------|--------|
| 摄影 | `photography`, `cinematic`, `bokeh`, `8K` |
| 插画 | `illustration`, `concept art`, `anime` |
| 艺术 | `oil painting`, `watercolor`, `minimalist` |
| 3D | `3D render`, `octane render`, `isometric` |

### 光照词

- `golden hour` - 黄金时段
- `soft light` - 柔光
- `dramatic lighting` - 戏剧光
- `neon glow` - 霓虹
