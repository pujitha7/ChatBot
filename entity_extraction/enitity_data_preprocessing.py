
# coding: utf-8

# In[1]:


import warnings
warnings.filterwarnings("ignore")
import json
import codecs
from sklearn.model_selection import train_test_split
import pandas as pd
import numpy as np
from string import ascii_letters
from string import printable
import os
working_directory = os.path.abspath('..')


# In[2]:


def preprocessing(js):
    temp = []
    final = []
    for i in range(len(js[list(js.keys())[0]])):
        for j in range(len(js[list(js.keys())[0]][i])):
            if js[list(js.keys())[0]][i][j]['type'] == 'Text':
                temp = temp + [(k,0) for k in js[list(js.keys())[0]][i][j]['value'].split(" ") if k != '']
            else:
                temp = temp + [(k,js[list(js.keys())[0]][i][j]['slot']) for k in js[list(js.keys())[0]][i][j]['value'].split(" ") if k != '']

        final.append(temp)
        temp = []
        
    return final


# In[3]:


js=json.load(codecs.open(working_directory+'/data/all_classes.json', 'r', 'utf-8-sig'))
check_all_classes = preprocessing(js)
js=json.load(codecs.open(working_directory+'/data/check_assignment_due.json', 'r', 'utf-8-sig'))
check_assignment_due = preprocessing(js)
js=json.load(codecs.open(working_directory+'/data/find_whether_a_class.json', 'r', 'utf-8-sig'))
check_when_class_is = preprocessing(js)
js=json.load(codecs.open(working_directory+'/data/find_what_is_particular_class.json', 'r', 'utf-8-sig'))
check_what_lecture = preprocessing(js)
js=json.load(codecs.open(working_directory+'/data/where_class.json', 'r', 'utf-8-sig'))
where_class = preprocessing(js)

js=json.load(codecs.open(working_directory+'/data/add_reminder_1.json', 'r', 'utf-8-sig'))
ad1 = preprocessing(js)
js=json.load(codecs.open(working_directory+'/data/add_reminder_2.json', 'r', 'utf-8-sig'))
ad2 = preprocessing(js)
js=json.load(codecs.open(working_directory+'/data/add_reminder_3.json', 'r', 'utf-8-sig'))
ad3 = preprocessing(js)
js=json.load(codecs.open(working_directory+'/data/add_reminder_4.json', 'r', 'utf-8-sig'))
ad4 = preprocessing(js)
js=json.load(codecs.open(working_directory+'/data/add_reminder_5.json', 'r', 'utf-8-sig'))
ad5 = preprocessing(js)

add_reminder = ad1 + ad2 + ad3 + ad4 + ad5


add_reminder=ad1+ad2+ad3+ad4+ad5

final_data = check_all_classes  + check_assignment_due + check_when_class_is + check_what_lecture + add_reminder + where_class
max_len = len(max(final_data,key = len))

for i in range(len(final_data)):
    for j in range(max_len-len(final_data[i])):
        final_data[i] = final_data[i] + [("pad_word",'0')]
        
        
words=[]
tags=[]
for i in range(0,len(final_data)):
    for j in range(0,len(final_data[i])):
        words.append(final_data[i][j][0])
        tags.append(final_data[i][j][1])
        
        
words = list(set(words))
tags=list(set(tags))

n_words=len(words)
n_tags=len(tags)

word2idx = {w: i for i, w in enumerate(words)}
tag2idx = {t: i for i, t in enumerate(tags)}


def sent2features(sent):
    return [token for token,label in sent]

def sent2labels(sent):
    return [label for token,label in sent]

X = [sent2features(s) for s in final_data]
y = [sent2labels(s) for s in final_data]

for i in range(0,len(y)):
    for j in range(0,len(y[i])):
        if y[i][j]==0:
            y[i][j]='0'
            
import pickle

with open(working_directory+'/starter_model/entity_data_X.pkl', 'wb') as pickle_file:
    pickle.dump(X, pickle_file, protocol=pickle.HIGHEST_PROTOCOL)
with open(working_directory+'/starter_model/entity_data_y.pkl', 'wb') as pickle_file:
    pickle.dump(y, pickle_file, protocol=pickle.HIGHEST_PROTOCOL)

