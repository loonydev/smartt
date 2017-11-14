# -*- coding: utf-8 -*- 
import reverso_api
import requests

reverso=reverso_api.ReversoContextApi('en','ru')
word_data, example = reverso.send_request('Hello')
