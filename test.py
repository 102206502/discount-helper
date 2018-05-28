#!/usr/bin/env python
# -*- coding: utf-8 -*-
date_str = '12/28'
import datetime
now_time = datetime.datetime.now()
print(now_time.month)
date_arr = date_str.split('/')
post_month = int(date_arr[0])

print(post_month, type(post_month))