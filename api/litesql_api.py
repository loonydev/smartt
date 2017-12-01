# -*- coding: utf-8 -*-
from __future__ import print_function
import os.path
import sqlite3
import re
class LiteSQLApi:

    def __init__(self,source_language, target_language,dictionary_directory='../dictionary/',database_name='dictionary',key_word='KEY',key_ans='ANS'):
        file_name=dictionary_directory+source_language+"_"+target_language+".db"

        self.database_name=database_name
        self.key_word=key_word
        self.key_ans=key_ans


        if(os.path.isfile(file_name)):
            #print("Yeah,find file")
            self.connect_to_db(file_name)
        else:
            raise ValueError("Can't find dictionary file. Check language or add file to @dictionary_path")

    def connect_to_db(self,file_name):
        self.db_connection = sqlite3.connect(file_name,check_same_thread=False)
    	self.db_cursor = self.db_connection.cursor()
    	#return con,cur

    def send_request(self,text):
        #Yes i know about sql injection
        word_array=self.getWords(text)
        result_dict={}
        for word in word_array:
            self.db_cursor.execute("SELECT "+self.key_ans+" FROM "+self.database_name+" WHERE "+self.key_word+" LIKE '"+word+"'")
            time_text=self.parse_result(self.db_cursor.fetchall())
            result_dict[time_text[0]]=time_text[1:]
            #print(', '.join(result_dict[time_text[0]]))
    	return (result_dict)

    def parse_result(self,result):
        time_array=[]
        # Need test for 0,0 result. Maybe we find 0,2.
        time_str=result[0][0]
        time_str=self.remove_number(time_str)
        #TODO: Add parser for example
        return self.getWords(time_str)


    def remove_number(self,text):
        return ''.join([i for i in text if not i.isdigit()])

    def getWords(self,text):
        time_text=re.compile('\w+',re.UNICODE).findall(text)
        #print(', '.join(time_text))
        return time_text
    #def parse_result(self,result):
