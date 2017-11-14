# -*- coding: utf-8 -*- 

from __future__ import print_function

import sqlite3
import pyxhook
import time
import pyperclip
import requests
from lxml import html
import time
def create_db_file(db_name):
	con = sqlite3.connect(db_name,check_same_thread=False)
	cur = con.cursor()
	return con,cur
def get_word(word,cursor):
	cursor.execute("SELECT ANS FROM dictionary WHERE KEY LIKE '"+word+"'")
	result=cursor.fetchall()
	return (result)

def get_word_api_reverso(word):
	url = 'http://context.reverso.net/%D0%BF%D0%B5%D1%80%D0%B5%D0%B2%D0%BE%D0%B4/%D0%B0%D0%BD%D0%B3%D0%BB%D0%B8%D0%B9%D1%81%D0%BA%D0%B8%D0%B9-%D1%80%D1%83%D1%81%D1%81%D0%BA%D0%B8%D0%B9/'+word+'%3F'

	headers = {
		'Host': 'context.reverso.net',
		'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',
		'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
		'Accept-Language': 'en-US,en;q=0.5',
		'Accept-Encoding': 'gzip, deflate',
		'Connection': 'close',
		'Upgrade-Insecure-Requests': '1'
	}
	sta=time.time()
	response = requests.get(url, headers=headers)
	print(time.time()-sta)
	tree = html.fromstring(response.content)
	word_list = tree.xpath('//div[@class = "translation ltr dict no-pos"]')
	example_list_en = tree.xpath('.//div[@class="example"]/div[@class="src ltr"]/span[@class="text"]')#.find('//span[@class="text"]')
	example_list_ru = tree.xpath('.//div[@class="example"]/div[@class="trg ltr"]/span[@class="text"]')
	print(word_list)
	for i in range(len(example_list_en)):
		
		#print('-----')
		print(str(example_list_en[i].text)+str(example_list_en[i].find('em').text))
		print(str(example_list_ru[i].text)+str(example_list_ru[i].find('a').find('em').text))
		#print(ell.find('em').text)
	# out_test=open('out_test.txt','w')
	# out_test.write(response.content)
	# out_test.close()
	#return (result)

# def get_all_ans(string):
# 	all_answer=[]
# 	index=0
# 	len_ex=1
# 	while index<len(string):
# 		index=string.find('>',index)
# 		if index ==-1:
# 			break
# 		index_next_ex=string.find('\n',index+len_ex)
# 		if(index_next_ex==-1):
# 			all_example.append(string[index+len_ex:])
# 		else:
# 			all_example.append(string[index+len_ex:index_next_ex])
# 		index=index+len_ex

def get_all_by_word(string,req,next):
	all_answer=[]
	index=0
	len_ex=len(req)
	while index<len(string):
		index=string.find(req,index)
		if index ==-1:
			break
		index_next_ex=string.find(next,index+len_ex)
		if(index_next_ex==-1):
			all_answer.append(string[index+len_ex:])
		else:
			all_answer.append(string[index+len_ex:index_next_ex])
		index=index+len_ex
	return all_answer

# def get_all_ex(string):
# 	all_example=[]
# 	index=0
# 	len_ex=5
# 	len_an=2
# 	while index<len(string):

# 		index=string.find('_Ex:\n',index)
# 		if index ==-1:
# 			break

# 		index_next_ex=string.find('\n',index+len_ex)
# 		#index_next_an=string.find('>',index+len_ex)
# 		if(index_next_ex==-1):
# 			all_example.append(string[index+len_ex:])
# 		else:
# 			all_example.append(string[index+len_ex:index_next_ex])
# 		index=index+len_ex
# 	for i in all_example:
# 		print('-----')
# 		print(i)
def clear_line(data,req):
	out_data=[]
	len_req=len(req)
	for line in data:
		index=line.find(req)
		if(index!=-1):
			out_data.append(line[index+len_req:])
		else:
			out_data.append(line)
	return out_data

def pretty_string_gen(string):
	synonims=[]
	print('---------------------------------------------')

	all_example=get_all_by_word(string,'_Ex:\n       ','\n')
	all_answer=get_all_by_word(string,'> ','\n')
	print("Ответы")
	for i in range(len(all_answer)):
		print(all_answer[i])

	print("\nПримеры")
	for i in range(len(all_example)):
		print(all_example[i])
def kbevent(event):
	global running,prev_key,cursor
	# print key info
	#print(event.Ascii)
	if((prev_key==227) and(event.Ascii==99)):
		# result=get_word(pyperclip.paste(),cursor)
		# for res in result:
		# 	print('##')
		# 	for i in res:
		# 		#print(i)
		# 		pretty_string_gen(i)
		get_word_api_reverso(pyperclip.paste())
		print('------------------------------------------------------------')
		#pyperclip.copy('')


	prev_key=event.Ascii

	# If the ascii value matches spacebar, terminate the while loop
	if event.Ascii == 32:
		running = False


prev_key=0

connection,cursor=create_db_file("test.db")
# Create hookmanager
hookman = pyxhook.HookManager()
# Define our callback to fire when a key is pressed down
hookman.KeyDown = kbevent
# Hook the keyboard
hookman.HookKeyboard()
# Start our listener
hookman.start()

# Create a loop to keep the application running
running = True
while running:
	time.sleep(0.1)

# Close the listener when we are done
hookman.cancel()