# -*- coding: utf-8 -*-
from __future__ import print_function
import sys
sys.path.insert(0, '../api')
import reverso_api
import requests

reverso=reverso_api.ReversoContextApi('en','ru')
word_data, example = reverso.send_request('Hello hack')

for word in word_data:
    print(word,end=': ')
    print(', '.join(word_data[word]),end='\n')
