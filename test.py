#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pandas as pd
import urllib.parse
import pttcrawler
crawler = pttcrawler.PttBoardCrawleer()
discount_df = pd.read_csv('discount info.csv')
discount_info = discount_df[['date','title','link']]
# print(discount_info)
for i in range(len(discount_info)):
	info_meta = discount_info.iloc[i,:]
	link_str = urllib.parse.urljoin(crawler.domain, info_meta['link'])
	message = info_meta['date']+'\n'+info_meta['title']+'\n'+link_str
	print(message)