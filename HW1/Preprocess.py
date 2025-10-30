# Preprocess.py
# encoding: utf-8
# 本代码用于对爬取到的文本进行预处理，主要包括去除非中文/英文字符、去除多余空白符号以及将分条的jsonl文件内容整理成后续可直接进行统计分析的纯文本txt文件，中文就只保留中文字符，英文就只保留英文字符和空格（确保单词与单词之间还是要划分）

import json
import re

class ZhCleaner:
    '''
    专门用来处理中文文本的清洗类
    该类会去除所有非中文字符，只保留中文字符
    '''
    def __init__(self):
        self.pattern = re.compile(r'[^\u4e00-\u9fa5]')  # 选中非中文字符以便后续去除

    def clean(self, input_path, output_path):
        cleaned_lines = []  # 用于存储清洗后的文本
        with open(input_path, 'r', encoding = 'utf-8') as f:
            for line in f:
                data = json.loads(line) # 一个json一个json地读入
                clean_text = self.pattern.sub('', data['content'])  # 只对content内容进行处理，匹配到的非中文字符替换为空
                cleaned_lines.append(clean_text)
    
        with open(output_path, 'w', encoding = 'utf-8') as f:
            f.write("".join(cleaned_lines))
            
class EnCleaner:
    '''
    专门用来处理英文文本的清洗类
    该类会去除所有非英文字符，只保留英文字符和空格（确保单词与单词之间还是要划分）
    '''
    def __init__(self):
        self.pattern = re.compile(r'\b[a-zA-Z]+(?:-[a-zA-Z]+)*\b')  # 选中英文单词（保留连字符）以后续进行拼接保留

    def clean(self, input_path, output_path):
        cleaned_lines = []  # 用于存储清洗后的文本
        with open(input_path, 'r', encoding = 'utf-8') as f:
            for line in f:
                data = json.loads(line) # 一个json一个json地读入
                clean_text = ' '.join(self.pattern.findall(data['content']))  # 只对content字段进行处理，将匹配到的单词用空格连接起来
                clean_text = re.sub(r'\s+', ' ', clean_text).strip()  # 去除多余空格
                clean_text = clean_text.lower()  # 转为小写
                cleaned_lines.append(clean_text)
    
        with open(output_path, 'w', encoding = 'utf-8') as f:
            f.write("".join(cleaned_lines))

if __name__ == "__main__":
    zh_cleaner = ZhCleaner()
    zh_cleaner.clean('HW1/zh_wikipedia.jsonl', 'HW1/zh_wikipedia.txt')

    en_cleaner = EnCleaner()
    en_cleaner.clean('HW1/en_wikipedia.jsonl', 'HW1/en_wikipedia.txt')