# 翻译工作流程指南

本文档详细说明论文翻译的具体流程和规范。

## 翻译流程概览

```
┌──────────────────────────────────────────────────────────────┐
│                      翻译工作流程                             │
├──────────────────────────────────────────────────────────────┤
│  Phase 1: 预处理                                              │
│  ├─ 识别论文结构（章节划分）                                  │
│  ├─ 提取元信息（标题、作者、摘要）                            │
│  └─ 标记特殊内容（公式、表格、图片、代码）                    │
├──────────────────────────────────────────────────────────────┤
│  Phase 2: 逐段翻译                                            │
│  ├─ 按章节顺序翻译                                            │
│  ├─ 保持英文原文 + 中文译文对照                               │
│  ├─ 术语首次出现时标注中英对照                                │
│  └─ 跳过参考文献和图片文字                                    │
├──────────────────────────────────────────────────────────────┤
│  Phase 3: 润色优化                                            │
│  ├─ 检查译文流畅度                                            │
│  ├─ 确保中文学术表达习惯                                      │
│  └─ 标注重点内容（加粗）                                      │
├──────────────────────────────────────────────────────────────┤
│  Phase 4: 附加内容生成                                        │
│  ├─ 生成论文摘要（要点提炼）                                  │
│  ├─ 生成术语对照表                                            │
│  └─ 撰写深度分析                                              │
├──────────────────────────────────────────────────────────────┤
│  Phase 5: 组装输出                                            │
│  └─ 按模板格式组装 Markdown 文件                              │
└──────────────────────────────────────────────────────────────┘
```

## Phase 1: 预处理

### 1.1 识别论文结构

典型学术论文结构：

```
Title                 → 标题（必译）
Authors               → 作者（保留原文）
Abstract              → 摘要（必译）
1. Introduction       → 引言（必译）
2. Related Work       → 相关工作（必译）
3. Method/Approach    → 方法（必译）
4. Experiments        → 实验（必译）
5. Results            → 结果（必译）
6. Discussion         → 讨论（必译）
7. Conclusion         → 结论（必译）
Acknowledgments       → 致谢（可选）
References            → 参考文献（跳过）
Appendix              → 附录（可选）
```

### 1.2 特殊内容标记

在翻译前识别并标记：

| 内容类型 | 识别特征 | 处理方式 |
|----------|----------|----------|
| 数学公式 | `$...$`, `$$...$$`, `\begin{equation}` | 保留 LaTeX 格式 |
| 表格 | `\begin{table}`, HTML `<table>` | 翻译内容，保持结构 |
| 图片说明 | `Figure X:`, `Fig. X` | 翻译说明文字 |
| 图片内文字 | 嵌入图片中的文字 | 不翻译 |
| 代码块 | `\begin{lstlisting}`, ``` | 保留代码，翻译注释 |
| 算法伪代码 | `\begin{algorithm}` | 翻译注释和说明 |
| 引用 | `[1]`, `(Author, 2023)` | 保留原样 |

## Phase 2: 逐段翻译

### 2.1 翻译格式

采用逐段对照格式：

```markdown
## 1. Introduction / 引言

> Original English paragraph here. This is the source text that needs
> to be translated. It may contain technical terms and formulas.

这里是中文翻译段落。技术术语如 **变换器** (Transformer) 会在首次出现时
标注英文原文。数学公式如 $E = mc^2$ 保持 LaTeX 格式。
```

### 2.2 术语处理规范

**首次出现：** 中文 (English, 缩写)
```
自注意力机制 (Self-Attention) 是 Transformer 的核心组件...
大语言模型 (Large Language Model, LLM) 近年来取得了显著进展...
```

**后续出现：** 可直接使用中文或缩写
```
基于自注意力机制，模型能够捕捉长距离依赖...
LLM 在各种下游任务中表现优异...
```

**常见 AI/ML 术语对照参考：**

| 英文 | 中文 | 缩写 |
|------|------|------|
| Transformer | 变换器 | - |
| Attention | 注意力机制 | - |
| Self-Attention | 自注意力 | - |
| Multi-Head Attention | 多头注意力 | MHA |
| Feed-Forward Network | 前馈网络 | FFN |
| Layer Normalization | 层归一化 | LayerNorm |
| Embedding | 嵌入/向量表示 | - |
| Fine-tuning | 微调 | - |
| Pre-training | 预训练 | - |
| Prompt | 提示/提示词 | - |
| In-context Learning | 上下文学习 | ICL |
| Chain-of-Thought | 思维链 | CoT |
| Reinforcement Learning | 强化学习 | RL |
| Reinforcement Learning from Human Feedback | 人类反馈强化学习 | RLHF |
| Retrieval-Augmented Generation | 检索增强生成 | RAG |
| Knowledge Distillation | 知识蒸馏 | - |
| Gradient Descent | 梯度下降 | - |
| Backpropagation | 反向传播 | - |
| Overfitting | 过拟合 | - |
| Regularization | 正则化 | - |
| Dropout | Dropout | - |
| Batch Normalization | 批归一化 | BN |
| Convolutional Neural Network | 卷积神经网络 | CNN |
| Recurrent Neural Network | 循环神经网络 | RNN |
| Long Short-Term Memory | 长短期记忆 | LSTM |
| Graph Neural Network | 图神经网络 | GNN |
| Generative Adversarial Network | 生成对抗网络 | GAN |
| Variational Autoencoder | 变分自编码器 | VAE |
| Diffusion Model | 扩散模型 | - |
| Benchmark | 基准测试 | - |
| State-of-the-Art | 最先进的/当前最优 | SOTA |
| Ablation Study | 消融实验 | - |

### 2.3 数学公式处理

**行内公式：** 使用单个 `$`
```markdown
损失函数定义为 $L = -\sum_{i} y_i \log(\hat{y}_i)$，其中 $y_i$ 是真实标签。
```

**行间公式：** 使用双 `$$`
```markdown
注意力机制的计算公式如下：

$$
\text{Attention}(Q, K, V) = \text{softmax}\left(\frac{QK^T}{\sqrt{d_k}}\right)V
$$

其中 $Q$、$K$、$V$ 分别表示查询、键、值矩阵。
```

### 2.4 翻译风格要求

**✅ 推荐：**
- 使用学术论文的正式语体
- 句式符合中文表达习惯
- 适当调整语序使译文通顺
- 关键结论使用 **加粗** 标记

**❌ 避免：**
- 逐词直译导致的翻译腔
- 过于口语化的表达
- 丢失原文的逻辑关系
- 过度意译改变原意

**示例对比：**

| 原文 | ❌ 直译 | ✅ 润色后 |
|------|--------|----------|
| We propose a novel approach... | 我们提出一个新颖的方法... | 本文提出了一种新方法... |
| It is worth noting that... | 值得注意的是... | 需要指出的是... |
| Our experiments demonstrate... | 我们的实验证明... | 实验结果表明... |
| To the best of our knowledge | 据我们所知 | 据我们了解 |

## Phase 3: 润色优化

### 3.1 流畅度检查

检查以下问题：
- [ ] 是否有不通顺的句子
- [ ] 是否有重复啰嗦的表达
- [ ] 术语使用是否一致
- [ ] 逻辑连接是否清晰

### 3.2 重点标注

使用 **加粗** 标记：
- 论文的核心创新点
- 关键实验结论
- 重要的性能数据
- 显著的发现或观点

```markdown
实验结果表明，本文提出的方法在 GLUE 基准测试上取得了 **89.3%** 的平均分数，
**相比基线模型提升了 4.2 个百分点**。
```

## Phase 4: 附加内容生成

### 4.1 论文摘要（要点提炼）

在文档开头生成 3-5 个核心要点：

```markdown
## 论文摘要

📌 **核心要点：**
1. 提出了 XXX 方法，解决了 YYY 问题
2. 引入了 AAA 机制，实现了 BBB 效果
3. 在 N 个基准数据集上取得了 SOTA 性能
4. 关键创新：CCC 技术的首次应用
5. 局限性：DDD 场景下性能有所下降
```

### 4.2 术语对照表

提取论文中出现的专业术语：

```markdown
## 术语表

| 英文术语 | 中文翻译 | 首次出现 |
|----------|----------|----------|
| Transformer | 变换器 | 摘要 |
| Self-Attention | 自注意力机制 | 第2节 |
| ... | ... | ... |
```

### 4.3 深度分析

撰写深入浅出的分析，包含以下部分：

```markdown
## 论文深度分析

### 🎯 核心创新点
[用通俗语言解释本文的主要贡献]

### 📊 研究现状对比
[与同期/前期工作的对比分析]

### ✅ 优势
- 优势1：...
- 优势2：...

### ⚠️ 局限性
- 局限1：...
- 局限2：...

### 🔬 可行性评估
[从工程实现和实际应用角度分析]

### 💡 未来价值与追踪建议

**推荐追踪程度：** ⭐⭐⭐⭐☆ (4/5)

[给出追踪建议的理由]
```

**追踪程度评级标准：**

| 评级 | 含义 | 适用情况 |
|------|------|----------|
| ⭐ | 了解即可 | 增量改进，无重大突破 |
| ⭐⭐ | 选择性关注 | 特定领域有价值 |
| ⭐⭐⭐ | 建议阅读 | 有一定创新，值得学习 |
| ⭐⭐⭐⭐ | 重点追踪 | 重要突破，可能成为新范式 |
| ⭐⭐⭐⭐⭐ | 必读 | 里程碑式工作，定义新方向 |

## Phase 5: 组装输出

按照 `output_template.md` 中的模板格式组装最终文件。

## 质量检查清单

在输出前进行最终检查：

- [ ] 所有章节都已翻译（参考文献除外）
- [ ] 术语使用一致
- [ ] 数学公式格式正确
- [ ] 中英对照格式统一
- [ ] 重点内容已加粗
- [ ] 摘要准确概括论文要点
- [ ] 术语表完整
- [ ] 深度分析客观全面
- [ ] 文件命名正确（原文件名_翻译.md）
- [ ] 保存位置正确
