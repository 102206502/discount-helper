#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pandas as pd
discount_df = pd.read_csv('discount info.csv')
discount_info = discount_df[['title','link']]
print(str(discount_info))