# TextCrawler.py
# encoding: utf-8
# 本代码用来获取作业所需要的中英文文本数据，主要是利用Wikipedia的随机词条这一功能，实现语料的收集，最终中英文各爬取10000条词条，保存为jsonl文件，方便后续处理
import requests
from bs4 import BeautifulSoup
import time
import json
import os

class TextCrawler:
    '''
    定义一个用于爬取Wikipedia随机词条的类，包括初始化、获取随机词条、爬取并保存词条等功能
    '''
    def __init__(self, lang):
        self.lang = lang
        if lang == 'zh':
            self.base_url = "https://zh.wikipedia.org/wiki/Special:Random?variant=zh-cn"    # 细节，加上cn确保爬下来的是简体中文大陆
        elif lang == 'en':
            self.base_url = "https://en.wikipedia.org/wiki/Special:Random"
        self.seen_urls = set()

    def fetch_random_article(self):
        try:
            headers = {
                'User-Agent': 'TextCrawler/1.0 (yaoxianglin21@mails.ucas.ac.cn)'
            }   # Wikipedia要求请求中包含User-Agent头
            response = requests.get(self.base_url, timeout=10, headers=headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            title_tag = soup.find('title')  # 通过直接查找title标签来获取该词条的标题
            title = title_tag.text.strip()
            content_div = soup.select_one('#mw-content-text > div.mw-parser-output')    # 经过对维基百科词条网页的分析，发现正文内容都在这个div之下
            paragraphs = content_div.find_all('p')  # 选择在段落中的内容
            content = ' '.join([
                ''.join(p.stripped_strings) for p in paragraphs if p.get_text(strip=True)
            ])  # 提取出对应正文段落中的主要文本内容，忽略掉那些没有实际文本信息的HTML部分，只选择我们真正需要的部分
            url = response.url
            return {'title': title, 'content': content, 'url': url} # 返回一个包含标题、内容和URL的字典，这是三个我们主要关心的内容
        except Exception as e:
                print(f"[ERROR] {self.lang} fetch failed: {e}")
                return None
            
    def load_existing_data(self, jsonl_path):
        """
        加上这个是避免程序中途中断，count清零，并且可能出现重复爬取的情况，这里通过读取jsonl文件（如果存在）来确认目前已经爬取的词条数
        """
        count = 0
        if not os.path.exists(jsonl_path): return count # 如果jsonl文件不存在说明程序第一次启动
        with open(jsonl_path, 'r', encoding='utf-8') as f:
            for line in f:
                data = json.loads(line)
                if 'url' in data:
                    self.seen_urls.add(data['url'])
                    count += 1
        return count

    def crawl_and_save(self, num_articles, jsonl_path):
        count = self.load_existing_data(jsonl_path)   # 从目前已经爬取的jsonl文件中确认已经爬取的词条数量
        with open(jsonl_path, 'a', encoding='utf-8') as f:  #细节，追加模式a，惨痛的教训
            while count < num_articles:
                article = self.fetch_random_article()
                if article['url'] not in self.seen_urls:    # 通过词条的URL来判断是否重复，只要没爬过的
                    self.seen_urls.add(article['url'])
                    f.write(json.dumps(article, ensure_ascii=False) + '\n')
                    count += 1
                time.sleep(1)

def crawl_both_languages(num_articles, zh_jsonl, en_jsonl):
    '''
    分别进行中文和英文的词条的爬取工作，并保存为jsonl文件，方便后续处理
    '''
    zh_crawler = TextCrawler('zh')
    zh_crawler.crawl_and_save(num_articles, zh_jsonl)
    en_crawler = TextCrawler('en')
    en_crawler.crawl_and_save(num_articles, en_jsonl)
    
if __name__ == "__main__":
    num_articles = 10000  # 每种语言爬取的词条数量，暂时定为10000条
    crawl_both_languages(num_articles, 'zh_wikipedia.jsonl', 'en_wikipedia.jsonl')