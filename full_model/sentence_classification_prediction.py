
# coding: utf-8

# In[1]:


import pickle
import numpy as np


# In[2]:


def prediction(sen):
    with open('classify_sentence_model.pkl','rb') as pickle_load:
        log_reg_model=pickle.load(pickle_load)
    with open('tfidf_model.pkl','rb') as pickle_load:
        tfidf_model=pickle.load(pickle_load)
    
    sen=[sen]
    transf=tfidf_model.transform(sen)
    pred=log_reg_model.predict(transf)
    if pred[0]==0:
        return "not_small_talk"
    else:
        return "small_talk"

