#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
import pandas as pd
import urllib.parse
# import pttcrawler
# crawler = pttcrawler.PttBoardCrawleer()
    
# discount_df = pd.read_csv('discount info.csv')
# discount_info = discount_df[['date','title','link']]
# message = ''
# for i in range(len(discount_info)):
#     info_meta = discount_info.iloc[i,:]
#     link_str = urllib.parse.urljoin(crawler.domain, info_meta['link'])
#     message += info_meta['date']+'\n'+info_meta['title']+'\n'+link_str+'\n'
# print(message)
last_crawl = datetime.datetime.now()

def check_crawl():
    re_crawl = True
    cur_time = datetime.datetime.now()
    if cur_time.date() != last_crawl.date():
        print()
    elif cur_time.hour() - last_crawl.hour() > 4:
        print()
    else:
        re_crawl = False
    return re_crawl
check_crawl()