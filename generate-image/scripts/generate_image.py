#!/usr/bin/env python3
"""
使用 Gemini 官方 API 生成图片。
"""

import sys
import io
import base64
import argparse
import os
import re
from pathlib import Path

# 修复 Windows 控制台编码问题
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

MODEL = "gemini-3-pro-image-preview"
TRANSLATE_MODEL = "gemini-2.0-flash"

# 系统指令：引导模型生成高质量图片
SYSTEM_INSTRUCTION = """You are an expert image generator. Create visually stunning images with:
- Professional composition and framing
- Realistic lighting, shadows and depth
- Sharp details and proper focus
- Harmonious colors and appropriate contrast
Always match the exact description provided by the user."""


def get_api_key() -> str:
    """获取 Gemini API Key。"""
    key = os.environ.get('GEMINI_API_KEY')
    if key:
        return key

    for parent in [Path.cwd()] + list(Path.cwd().parents):
        env_file = parent / ".env"
        if env_file.exists():
            for line in env_file.read_text(encoding='utf-8').splitlines():
                line = line.strip()
                if line and not line.startswith('#') and line.startswith('GEMINI_API_KEY='):
                    key = line.split('=', 1)[1].strip().strip('"\'')
                    if key:
                        return key

    print("❌ 未找到 GEMINI_API_KEY")
    print("   请创建 .env 文件: GEMINI_API_KEY=your-api-key")
    print("   获取: https://aistudio.google.com/apikey")
    sys.exit(1)


def has_chinese(text: str) -> bool:
    """检测文本是否包含中文。"""
    return bool(re.search(r'[\u4e00-\u9fff]', text))


def translate_to_english(text: str, api_key: str) -> str:
    """使用 Gemini 将中文翻译为英文。"""
    try:
        import requests
    except ImportError:
        return text

    url = f"https://generativelanguage.googleapis.com/v1beta/models/{TRANSLATE_MODEL}:generateContent?key={api_key}"

    resp = requests.post(
        url,
        headers={"Content-Type": "application/json"},
        json={
            "contents": [{
                "parts": [{
                    "text": f"Translate the following image generation prompt to English. Only output the translation, nothing else:\n\n{text}"
                }]
            }]
        },
        timeout=30
    )

    if resp.status_code == 200:
        result = resp.json()
        candidates = result.get("candidates", [])
        if candidates:
            parts = candidates[0].get("content", {}).get("parts", [])
            if parts and "text" in parts[0]:
                return parts[0]["text"].strip()

    return text


def load_image(path: str) -> tuple[str, str]:
    """加载图片，返回 (base64数据, mime类型)。"""
    p = Path(path)
    if not p.exists():
        print(f"❌ 图片不存在: {path}")
        sys.exit(1)

    mime = {
        '.png': 'image/png',
        '.jpg': 'image/jpeg',
        '.jpeg': 'image/jpeg',
        '.webp': 'image/webp',
        '.gif': 'image/gif',
    }.get(p.suffix.lower(), 'image/png')

    data = base64.b64encode(p.read_bytes()).decode()
    return data, mime


def save_image(base64_data: str, output: str, mime_type: str = None) -> str:
    """保存图片到文件。"""
    out_path = Path(output)
    if out_path.parent and str(out_path.parent) != '.':
        out_path.parent.mkdir(parents=True, exist_ok=True)

    # 根据实际 mime_type 调整扩展名
    if mime_type == 'image/jpeg' and output.endswith('.png'):
        output = output[:-4] + '.jpg'
    elif mime_type == 'image/webp' and output.endswith('.png'):
        output = output[:-4] + '.webp'

    Path(output).write_bytes(base64.b64decode(base64_data))
    return output


def generate(prompt: str, output: str, input_image: str = None,
             aspect_ratio: str = None, resolution: str = None):
    """调用 Gemini API 生成图片。"""
    try:
        import requests
    except ImportError:
        print("❌ 请安装 requests: pip install requests")
        sys.exit(1)

    api_key = get_api_key()

    # 中文提示词自动翻译为英文
    final_prompt = prompt
    if has_chinese(prompt):
        print(f"🔤 检测到中文，正在翻译...")
        final_prompt = translate_to_english(prompt, api_key)
        print(f"🔤 翻译结果: {final_prompt}")

    # 构建用户请求
    parts = []

    if input_image:
        print(f"✏️  编辑图片: {input_image}")
        img_data, mime_type = load_image(input_image)
        parts.append({
            "inlineData": {
                "mimeType": mime_type,
                "data": img_data
            }
        })

    # 将宽高比和分辨率信息加入提示词（作为备用）
    if aspect_ratio or resolution:
        extra_info = []
        if aspect_ratio:
            extra_info.append(f"aspect ratio {aspect_ratio}")
        if resolution:
            extra_info.append(f"{resolution} resolution")
        final_prompt = f"{final_prompt}, {', '.join(extra_info)}"

    parts.append({"text": final_prompt})

    print(f"📝 {prompt}")
    if aspect_ratio:
        print(f"📐 宽高比: {aspect_ratio}")
    if resolution:
        print(f"🖼️  分辨率: {resolution}")
    print(f"⏳ 生成中...")

    # 构建生成配置
    generation_config = {
        "responseModalities": ["IMAGE", "TEXT"]
    }

    # 添加图像配置（宽高比和分辨率）
    if aspect_ratio or resolution:
        image_config = {}
        if aspect_ratio:
            image_config["aspectRatio"] = aspect_ratio
        if resolution:
            image_config["imageSize"] = resolution
        generation_config["imageConfig"] = image_config

    # 构建请求体
    request_body = {
        "contents": [{"parts": parts}],
        "generationConfig": generation_config,
        "systemInstruction": {
            "parts": [{"text": SYSTEM_INSTRUCTION}]
        }
    }

    # 调用 API
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent?key={api_key}"

    try:
        resp = requests.post(
            url,
            headers={"Content-Type": "application/json"},
            json=request_body,
            timeout=180
        )
    except requests.exceptions.Timeout:
        print("❌ 请求超时，请重试")
        sys.exit(1)
    except requests.exceptions.RequestException as e:
        print(f"❌ 网络错误: {e}")
        sys.exit(1)

    # 解析响应
    if resp.status_code != 200:
        try:
            error_msg = resp.json().get("error", {}).get("message", resp.text)
        except:
            error_msg = resp.text
        print(f"❌ API 错误 ({resp.status_code}): {error_msg}")
        sys.exit(1)

    result = resp.json()

    if "error" in result:
        print(f"❌ {result['error'].get('message', result['error'])}")
        sys.exit(1)

    # 检查是否被阻止
    if "promptFeedback" in result and "blockReason" in result["promptFeedback"]:
        print(f"❌ 请求被阻止: {result['promptFeedback']['blockReason']}")
        sys.exit(1)

    candidates = result.get("candidates", [])
    if not candidates:
        print("❌ 无响应内容")
        sys.exit(1)

    candidate = candidates[0]
    if candidate.get("finishReason") == "SAFETY":
        print("❌ 内容被安全过滤器阻止")
        sys.exit(1)

    # 提取图片
    parts = candidate.get("content", {}).get("parts", [])
    for part in parts:
        inline_data = part.get("inlineData") or part.get("inline_data")
        if inline_data:
            img_data = inline_data.get("data")
            mime_type = inline_data.get("mimeType") or inline_data.get("mime_type", "image/png")
            if img_data:
                saved_path = save_image(img_data, output, mime_type)
                print(f"✅ 已保存: {saved_path}")
                return

    # 未找到图片
    for part in parts:
        if "text" in part:
            print(f"⚠️  模型返回文本: {part['text'][:200]}")
    print("❌ 响应中未找到图片")
    sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="Gemini 文生图",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python generate_image.py "一只橘猫在阳光下睡觉"
  python generate_image.py "cyberpunk city" -r 16:9 -s 4K
  python generate_image.py "把背景换成海滩" -i photo.jpg
        """
    )
    parser.add_argument("prompt", help="图片描述（支持中英文，中文会自动翻译）")
    parser.add_argument("-o", "--output", default="generated.png", help="输出路径（默认项目根目录）")
    parser.add_argument("-i", "--input", help="输入图片（编辑模式）")
    parser.add_argument("-r", "--ratio", help="宽高比 (1:1, 16:9, 9:16, 4:3, 3:4, 3:2, 2:3)")
    parser.add_argument("-s", "--size", help="分辨率 (1K, 2K, 4K)")

    args = parser.parse_args()
    generate(args.prompt, args.output, args.input, args.ratio, args.size)


if __name__ == "__main__":
    main()
