# TextCrawler.py
# encoding: utf-8
# 用来获取作业所需要的中英文文本数据，主要是利用Wikipedia的随机词条这一功能，来获取一定量的中英文文本数据
import requests
from bs4 import BeautifulSoup
import time
import json

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
            paragraphs = content_div.find_all('p')  # 选择在段落中的内容，但是忽略所有HTML标签和超链接，仅保留段落中的文本内容，这才是我们真正想要的
            content = ' '.join([
                ''.join(p.stripped_strings) for p in paragraphs if p.get_text(strip=True)
            ])
            url = response.url
            return {'title': title, 'content': content, 'url': url} # 返回一个包含标题、内容和URL的字典，这是三个我们主要关心的内容
        except Exception as e:
                print(f"[ERROR] {self.lang} fetch failed: {e}")
                return None

    def crawl_and_save(self, num_articles, jsonl_path):
        count = 0
        with open(jsonl_path, 'w', encoding='utf-8') as f:
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