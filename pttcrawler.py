#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
from requests_html import HTML
import pandas as pd
import re

def fetch(url):
    response = requests.get(url)
    # response = requests.get(url, cookies={'over18': '1'})  # 一直向 server 回答滿 18 歲了 !
    return response

def parse_article_entries(doc):
    html = HTML(html=doc)
    post_entries = html.find('div.r-ent')
    return post_entries

def parse_article_meta(entry):
    '''
    每筆資料都存在 dict() 類型中：key-value paird data
    '''
    
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

url = 'https://www.ptt.cc/bbs/e-shopping/index.html'
key_words = ['折扣', '打折', '優惠', '降價', '免運']

controls = html.find('.action-bar a.btn.wide')# 控制頁面選項: 最舊/上頁/下頁/最新
link = controls[1].get('href')
page_url = urllib.parse.urljoin('https://www.ptt.cc/', link)

resp = fetch(url)  # step-1
post_entries = parse_article_entries(resp.text)  # step-2

print(post_entries)  # result of setp-2

def get_metadata_from(url):

    def parse_next_link(doc):
        html = HTML(html=doc)
        controls = html.find('.action-bar a.btn.wide')
        link = controls[1].attrs.get('href')
        return urllib.parse.urljoin(domain, link)

    resp = fetch(url)
    post_entries = parse_article_entries(resp.text)
    next_link = parse_next_link(resp.text)

    metadata = [parse_article_meta(entry) for entry in post_entries]
    return metadata, next_link

def get_paged_meta(url, num_pages):
    collected_meta = []

    for page_n in range(num_pages):
        posts, link = get_metadata_from(url)
        collected_meta += posts
        url = urllib.parse.urljoin(domain, link)

    return collected_meta

start_url = 'https://www.ptt.cc/bbs/movie/index.html'
metadata = get_paged_meta(start_url, num_pages=5)

post_meta_dicts = []
for entry in post_entries:
    meta_article = parse_article_meta(entry)
    post_meta_dicts.append(meta_article)
    print(meta_article)  # result of setp-3
article_df = pd.DataFrame(post_meta_dicts)
print(article_df)

