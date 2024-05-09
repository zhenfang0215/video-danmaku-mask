import os
import requests
import time

def save_response_as_file(url, directory):
    # 确保输出目录存在
    if not os.path.exists(directory):
        os.makedirs(directory)

    # 发送 GET 请求
    response = requests.get(url)
    
    if response.status_code == 200:
        # 提取文件名
        # 生成时间戳作为文件名
        timestamp = int(time.time())
        filename = f"{timestamp}"
        filepath = os.path.join(directory, filename)
        
        # 写入文件
        with open(filepath, 'wb') as f:
            f.write(response.content)
        
        print(f"文件已保存至 {filepath}")
    else:
        print("请求失败")

def get_mask_url(filename):
    result = []
    with open(filename, 'r') as f:
        for line in f:
            if line.strip() == "":
                continue
            result.append(line.strip())
    return result

if __name__ == "__main__":
    mask_file = './maskurl.txt'
    directory = './maskfile'

    mask_url_list = get_mask_url(mask_file)
    print(mask_url_list)

    # 调用函数保存文件
    for url in mask_url_list:
        save_response_as_file(url, directory)
