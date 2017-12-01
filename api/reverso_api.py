# -*- coding: utf-8 -*-
from __future__ import print_function
from lxml import html
import requests

class ReversoContextApi:

	def __init__(self, source_language, target_language):
		language_to_reverso_name={
		'ar':'арабский',
		'de':'немецкий',
		'en':'английский',
		'es':'испанский',
		'fr':'французкий',
		'he':'иврит',
		'it':'итальянский',
		'ja':'японский',
		'nl':'голландский',
		'pl':'польский',
		'pt':'португальский',
		'ro':'румынский',
		'ru':'русский',
		}
		self.url="http://context.reverso.net/перевод/"+language_to_reverso_name[source_language]+'-'+language_to_reverso_name[target_language]+"/"

		self.headers = {
			'Host': 'context.reverso.net',
			'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',
			'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
			'Accept-Language': 'en-US,en;q=0.5',
			'Accept-Encoding': 'gzip, deflate',
			'Connection': 'close',
			'Upgrade-Insecure-Requests': '1'
		}

	def send_request(self,word):
		return self.parse_result(requests.get(self.get_url_with_word(word), headers=self.get_headers()))

	def get_url_with_word(self,word):
		return self.url+word

	def get_headers(self):
		return self.headers

	def parse_result(self,result):
		tree = html.fromstring(result.content)
		# word_list = tree.xpath('.//div[@id ="translations-content"]').text_content().split("\n")


		tree_word=tree.xpath('.//div[@id ="translations-content"]')
		#print(tree_word)
		if(len(tree_word)==0):
			tree_word=tree.xpath('.//div[@id ="splitting-content"]/div[@class="split wide-container"]')
		#print(tree_word)
		word_dictionary={}
		for current_tree in tree_word:
			time_list=[]
			for i in current_tree.text_content().split("\n"):
				i=i.replace('  ','')
				if(len(i)>2):
					time_list.append(i)
			word_dictionary[time_list[0]]=time_list[1:]

		# for key in word_dictionary:
		# 	print(key,end=": ")
		# 	for item in word_dictionary[key]:
		# 		print(item,end=', ')
		example_list_source = tree.xpath('.//div[@class="example"]/div[@class="src ltr"]/span[@class="text"]')#.find('//span[@class="text"]')
		example_list_target = tree.xpath('.//div[@class="example"]/div[@class="trg ltr"]/span[@class="text"]')
		example_list=[]
		# for i in range(len(example_list_source)):
		# 	example_list.append(example_list_source[i].text.encode('utf-8')+'\n'+example_list_source[i].find('em').text.encode('utf-8')+'\n'+example_list_target[i].text.encode('utf-8')+'\n'+example_list_target[i].find('a').find('em').text.encode('utf-8'))

		return word_dictionary,example_list
