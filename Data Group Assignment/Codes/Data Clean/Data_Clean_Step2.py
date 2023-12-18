import re

def remove_non_chinese_characters(file_path, output_file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # 保留中文字符和换行符，移除其他所有字符
    cleaned_content = re.sub(r'[^\u4e00-\u9fff\n]', '', content)

    with open(output_file_path, 'w', encoding='utf-8') as file:
        file.write(cleaned_content)

# 调用函数
remove_non_chinese_characters('keyword_黔东南2.txt', 'keyword_黔东南3.txt')
