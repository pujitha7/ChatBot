
# coding: utf-8

# In[3]:


import random
import numpy as np
import pickle
import re
from sklearn.feature_extraction.text import TfidfVectorizer


file = open("small_talk_data.txt",'r')
data = [i for i in file]
ques = []
ans = []
for i in range(len(data)):
    if data[i][0:3] == '- -':
        ques.append(data[i])
        ans.append(data[i+1])
        i = i + 1

for i in range(len(ques)):
    ques[i] = re.sub('\W+',' ', ques[i] )
    ans[i] = re.sub('\W+',' ', ans[i] )
    ques[i] = ques[i][1:-1]
    ans[i] = ans[i][1:-1]


tfidf = TfidfVectorizer()

tfidf.fit(ques)
transf=tfidf.transform(ques)

with open('small_talk_model.pkl', 'wb') as pickle_file:
        pickle.dump(tfidf, pickle_file, protocol=pickle.HIGHEST_PROTOCOL)  

with open('sparse_small_transformed.pkl', 'wb') as pickle_file:
        pickle.dump(transf, pickle_file, protocol=pickle.HIGHEST_PROTOCOL) 

with open('small_talk_answers.pkl', 'wb') as pickle_file:
        pickle.dump(ans, pickle_file, protocol=pickle.HIGHEST_PROTOCOL) 

