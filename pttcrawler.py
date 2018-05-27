#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
from requests_html import HTML
import pandas as pd
import re
import urllib.parse



class PttBoardCrawleer(object):
    """docstring for PttBoardCrawleer"""
    def __init__(self):
        self.domain = 'https://www.ptt.cc/'

    def crawl_discount_info(self, board_name):
        
        start_url = 'https://www.ptt.cc/bbs/' + board_name + '/index.html'
        key_words = ['折扣', '打折', '優惠', '降價', '免運']
        num_pages = 5

        collected_meta = self.get_paged_meta(start_url, num_pages)
        article_df = pd.DataFrame(collected_meta)
        print(article_df)
        

    def fetch(self, url):
        response = requests.get(url)
        # response = requests.get(url, cookies={'over18': '1'})  # 一直向 server 回答滿 18 歲了 !
        return response

    def parse_article_meta(self, ent):
        ''' Step-3 (revised): parse the metadata in article entry '''
        # 基本要素都還在
        meta = {
            'title': ent.find('div.title', first=True).text,
            'push': ent.find('div.nrec', first=True).text,
            'date': ent.find('div.date', first=True).text,
        }

        try:
            # 正常狀況取得資料
            meta['author'] = ent.find('div.author', first=True).text
            meta['link'] = ent.find('div.title > a', first=True).attrs['href']
        except AttributeError:
            # 但碰上文章被刪除時，就沒有辦法像原本的方法取得 作者 跟 連結
            if '(本文已被刪除)' in meta['title']:
                # e.g., "(本文已被刪除) [haudai]"
                match_author = re.search(r'\[(\w*)\]', meta['title'])
                if match_author:
                    meta['author'] = match_author.group(1)
            elif re.search(r'已被\w*刪除', meta['title']):
                # e.g., "(已被cappa刪除) <edisonchu> op"
                match_author = re.search(r'\<(\w*)\>', meta['title'])
                if match_author:
                    meta['author'] = match_author.group(1)
        return meta

        # 最終仍回傳統一的 dict() 形式 paired data
        return meta

    def get_metadata_from(self, url):

        def parse_next_link(doc):
            html = HTML(html=doc)
            print('html type:', type(html))
            controls = html.find('.action-bar a.btn.wide')
            link = controls[1].attrs.get('href')
            return urllib.parse.urljoin(self.domain, link)

        resp = self.fetch(url)
        post_entries = self.parse_article_entries(resp.text)
        next_link = parse_next_link(resp.text)

        metadata = [self.parse_article_meta(entry) for entry in post_entries]
        return metadata, next_link

    def parse_article_entries(self, doc):
        html = HTML(html=doc)
        post_entries = html.find('div.r-ent')
        return post_entries

    def get_paged_meta(self, url, num_pages):
        collected_meta = []

        for page in range(num_pages):
            print('parsing page', page)
            print('page url:', url)
            posts, link = self.get_metadata_from(url)
            collected_meta += posts
            url = urllib.parse.urljoin(self.domain, link)

        return collected_meta

if __name__ == "__main__":
    crawler = PttBoardCrawleer()
    crawler.crawl_discount_info('e-shopping')




