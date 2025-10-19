# Preprocess.py
# encoding: utf-8
# 本代码用于对爬取到的文本进行预处理，主要包括去除非中文/英文字符、去除多余空白符号以及将分条的jsonl文件内容整理成后续可直接进行统计分析的纯文本txt文件，中文就只保留中文字符，英文就只保留英文字符和空格（确保单词与单词之间还是要划分）

import json
import re

class TextPreprocessor: 
    '''
    构建一个用于将jsonl文件中每个json中的content字段进行清洗预处理并保存为纯文本的txt文件的类
    '''
    def __init__(self, lang):
        self.lang = lang
        if lang == 'zh':
            self.pattern = re.compile(r'[^\u4e00-\u9fa5]')  # 只保留中文字符
        elif lang == 'en':
            self.pattern = re.compile(r'\b[a-zA-Z]+(?:-[a-zA-Z]+)*\b')  # 删除包含非英文字母字符的单词，一定程度上避免将词条中出现的部分诸如法语、德语等其他语言的单词混入英文单词进行统计，但是也只能把那些单词中含有非英文26个字母的单词给剔除掉

    def clean(self, input_path, output_path):
        cleaned_lines = []  # 用于存储清洗后的文本
        with open(input_path, 'r', encoding = 'utf-8') as f:
            for line in f:
                data = json.loads(line) # 一个json一个json地读入
                clean_text = self.pattern.sub('', data['content'])  # 只对content字段进行清洗
                cleaned_lines.append(clean_text)
    
        with open(output_path, 'w', encoding = 'utf-8') as f:
            f.write("".join(cleaned_lines))

if __name__ == "__main__":
    zh_preprocessor = TextPreprocessor('zh')
    zh_preprocessor.clean('HW1/zh_wikipedia.jsonl', 'HW1/zh_wikipedia.txt')
    
    en_preprocessor = TextPreprocessor('en')
    en_preprocessor.clean('HW1/en_wikipedia.jsonl', 'HW1/en_wikipedia.txt')