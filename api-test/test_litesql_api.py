# -*- coding: utf-8 -*-
from __future__ import print_function
import sys
sys.path.insert(0, '../api')
import litesql_api


litesql=litesql_api.LiteSQLApi('en','ru')
word_data = litesql.send_request('Hello')

for word in word_data:
    print(word,end=': ')
    print(', '.join(word_data[word]))
