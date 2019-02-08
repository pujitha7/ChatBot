
# coding: utf-8

# In[1]:


import pickle
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
import sys
import os
working_directory=os.path.abspath(os.path.join(os.getcwd(), os.pardir))

# In[2]:


def training():
    with open(working_directory+'/data/total_data.pkl', 'rb') as pickle_load:
        data = pickle.load(pickle_load)
    with open('questions.pkl','rb') as pickle_load:
        small_talk_data=pickle.load(pickle_load)
    
    
    for i in range(0,len(small_talk_data)):
        small_talk_data[i]=small_talk_data[i].lower()
    rand_ints=np.random.randint(len(data),size=1500)
    chopped_data=[]
    for i in range(0,len(rand_ints)):
        chopped_data.append(data[rand_ints[i]])
    tot_data=chopped_data+small_talk_data
    target=len(chopped_data)*[0]+len(small_talk_data)*[1]
    tfidf_model=TfidfVectorizer()
    tfidf_model.fit(tot_data)
    tfidf=tfidf_model.transform(tot_data)
    x_train,x_test,y_train,y_test=train_test_split(tfidf,target,random_state=123,stratify=target)
    logreg=LogisticRegression()
    logreg.fit(x_train,y_train)
    with open('tfidf_model.pkl', 'wb') as pickle_file:
        pickle.dump(tfidf_model, pickle_file, protocol=pickle.HIGHEST_PROTOCOL)
    with open('classify_sentence_model.pkl', 'wb') as pickle_file:
        pickle.dump(logreg, pickle_file, protocol=pickle.HIGHEST_PROTOCOL)


# In[3]:


training()

