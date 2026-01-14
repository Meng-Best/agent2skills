# 论文来源解析指南

本文档指导如何解析和获取不同来源的论文内容。

## 来源类型识别

根据用户输入识别论文来源类型：

```
输入格式                              → 来源类型
─────────────────────────────────────────────────────
D:\papers\xxx.pdf                    → LOCAL_PDF
/home/user/papers/xxx.pdf            → LOCAL_PDF
C:/papers/xxx.pdf                    → LOCAL_PDF
arxiv:2301.00001                     → ARXIV_ID
arXiv:2301.00001                     → ARXIV_ID
https://arxiv.org/abs/2301.00001     → ARXIV_URL
https://arxiv.org/pdf/2301.00001     → ARXIV_URL
doi:10.1234/xxxxx                    → DOI
https://doi.org/10.1234/xxxxx        → DOI
```

## 解析规则

### 1. 本地 PDF 文件

**识别特征：**
- 以盘符开头 (Windows): `C:\`, `D:\` 等
- 以 `/` 开头 (Unix): `/home/`, `/Users/` 等
- 以 `./` 或 `../` 开头 (相对路径)
- 文件扩展名为 `.pdf`

**处理流程：**
```
1. 验证文件路径是否存在
2. 使用 Read 工具直接读取 PDF 文件
   - Claude 原生支持 PDF 视觉读取
3. 如果读取失败，提示用户检查文件路径
```

**输出文件位置：** 与原 PDF 同目录

### 2. arXiv 论文

**识别特征：**
- 前缀 `arxiv:` 或 `arXiv:`（不区分大小写）
- URL 包含 `arxiv.org`

**arXiv ID 格式：**
- 新格式: `YYMM.NNNNN` (如 `2301.00001`)
- 旧格式: `category/YYMMNNN` (如 `cs.AI/0701001`)

**处理流程：**
```
1. 提取 arXiv ID
   - 从 arxiv:2301.00001 提取 → 2301.00001
   - 从 URL 提取 → https://arxiv.org/abs/2301.00001 → 2301.00001

2. 构建 PDF 下载 URL
   - https://arxiv.org/pdf/{arxiv_id}.pdf

3. 使用 WebFetch 获取论文页面信息
   - https://arxiv.org/abs/{arxiv_id}
   - 提取标题、作者、摘要等元信息

4. 直接使用 WebFetch 获取 PDF 内容
   - 或提示用户下载 PDF 后使用本地路径
```

**输出文件位置：** 当前工作目录，文件名使用 arXiv ID

### 3. DOI 链接

**识别特征：**
- 前缀 `doi:`
- URL 包含 `doi.org`
- 格式: `10.XXXX/XXXXX`

**处理流程：**
```
1. 提取 DOI
   - 从 doi:10.1234/example 提取 → 10.1234/example
   - 从 URL 提取 → https://doi.org/10.1234/example → 10.1234/example

2. 尝试获取开放获取版本
   a. 查询 Unpaywall API (如果可用)
      - https://api.unpaywall.org/v2/{doi}?email=user@example.com

   b. 尝试常见开放获取来源
      - arXiv (很多论文有预印本)
      - PubMed Central
      - 作者个人主页

3. 如果无法获取全文
   - 提示用户："该论文可能在付费墙后，请提供本地 PDF 文件"
   - 给出可能的获取途径建议
```

**输出文件位置：** 当前工作目录

## PDF 内容解析

### 优先方案：Claude 原生 PDF 读取

Claude 具备原生的 PDF 视觉读取能力，可以直接理解 PDF 内容：

```
使用 Read 工具读取 PDF 文件
- 自动识别文本、公式、表格
- 保持文档结构
- 识别图片（但不翻译图片上的文字）
```

### 回退方案：Python 库解析

如果原生读取效果不佳，可使用 Python 库：

```python
# 方案 1: pdfplumber (推荐，表格支持好)
import pdfplumber

with pdfplumber.open(pdf_path) as pdf:
    for page in pdf.pages:
        text = page.extract_text()
        tables = page.extract_tables()

# 方案 2: PyMuPDF (速度快)
import fitz  # PyMuPDF

doc = fitz.open(pdf_path)
for page in doc:
    text = page.get_text()
```

## 元信息提取

无论何种来源，都应尝试提取以下元信息：

| 字段 | 说明 | 来源 |
|------|------|------|
| title | 论文标题 | PDF 首页 / arXiv 页面 / DOI 元数据 |
| authors | 作者列表 | PDF 首页 / arXiv 页面 |
| abstract | 摘要 | PDF Abstract 章节 / arXiv 页面 |
| year | 发表年份 | arXiv ID / DOI |
| venue | 发表会议/期刊 | DOI 元数据 |

## 错误处理

### 文件不存在
```
❌ 错误：找不到文件 D:\papers\example.pdf
💡 请检查文件路径是否正确
```

### arXiv ID 无效
```
❌ 错误：无效的 arXiv ID 格式
💡 正确格式示例：arxiv:2301.00001 或 https://arxiv.org/abs/2301.00001
```

### DOI 无法获取全文
```
⚠️ 该论文可能在付费墙后，无法直接获取全文

可尝试以下方式获取：
1. 通过学校/机构图书馆访问
2. 在 Google Scholar 搜索开放获取版本
3. 联系论文作者获取预印本
4. 下载 PDF 后使用本地路径：/read_paper D:\papers\xxx.pdf
```

### PDF 解析失败
```
⚠️ PDF 解析遇到问题，部分内容可能无法正确提取

正在尝试备用解析方案...
[如果仍失败] 建议使用其他工具将 PDF 转换为文本格式后重试
```
