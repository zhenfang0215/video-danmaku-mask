import base64
import os
from PIL import Image
import svglib
import io


def decode_save_svg(data, output_path):
    # 去除data:image/svg+xml;base64,前缀，并解码Base64
    header, encoded = data.split(',')
    svg_data = base64.b64decode(encoded)

    with open(output_path, "wb") as svg_file:
        svg_file.write(svg_data)

    print(f"图片已保存为 {output_path}")


def process_file(input_file, output_dir):
    # 确保输出目录存在
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 打开文本文件并处理每一行
    with open(input_file, 'r') as file:
        count = 0
        for i, line in enumerate(file, start=1):
            if line.strip() == "":
                continue
            if line.find("data:image/svg+xml") <0:
                continue
            count += 1
            # 为每一行生成一个唯一的文件名
            output_path = os.path.join(output_dir, f"image_{count:0>5}.svg")
            decode_save_svg(line.strip(), output_path)

def process_file_v2(input_file, output_file):
    # 打开文本文件并处理每一行
    with open(input_file, 'r') as file:
        content = ""
        for i, line in enumerate(file, start=1):
            if line.strip() == "":
                continue
            if line.find("data:image/svg+xml") <0:
                continue
            # 为每一行生成一个唯一的文件名
            content = content + f"\"{line.strip()}\",\n"
        
        with open(output_file, "w") as svg_file:
            result = f"var masksvgList = [{content}]"
            svg_file.write(result)

        


if __name__ == "__main__":
    input_file = 'svg.txt'  # 这里替换成你的文件名
    output_dir = 'imgs'  # 输出目录
    # process_file(input_file, output_dir)

    output_file = 'masksvg.js'
    process_file_v2(input_file, output_file)
