
# coding: utf-8

# In[1]:


import pickle
import numpy as np
from sklearn_crfsuite import CRF
import re
import editdistance


# In[2]:


ordinal_num={'first':1,'second':2,'third':3,'fourth':4,'fifth':5,'sixth':6,'seventh':7,'eight':8,'ninth':9,
            'tenth':10}

vocab=['first','second','third','fourth','fifth','sixth','seventh','eight','ninth','tenth']

with open('crf_model.pkl', 'rb') as pickle_load:
    crf = pickle.load(pickle_load)
with open('subjects.pkl','rb') as pickle_load:
    subjects=pickle.load(pickle_load)

def edit_dis(word):
    ordinals=re.findall(r'\d+',word)
    if len(ordinals)==0:
        dist=[]
        for i in range(0,len(vocab)):
            if word[0]==vocab[i][0]:
                dist.append(editdistance.eval(word,vocab[i]))
            else:
                dist.append(100)
        return ordinal_num[vocab[dist.index(min(dist))]]   
    
    else:
        return int(ordinals[0])
    
def edit_dis_subject(subject):
    dist=[]
    for i in range(0,len(subjects)):        
        dist.append((editdistance.eval(subject,subjects[i]))/len(subjects[i]))
    return subjects[dist.index(min(dist))]


# In[3]:


def entity_pred(sen):
    
    sen=[sen.split()]
    predic=crf.predict(sen)
    predic=predic[0]
    entities=[]
    subj=""
    day=""
    for i in range(0,len(predic)):
        if predic[i]=='count':
            num=edit_dis(sen[0][i])
            entities.append((num,predic[i]))
        elif predic[i]=='subject':
            subj=subj+sen[0][i]+" "
        elif predic[i]=='day':
            day=day+sen[0][i]+" "
        elif predic[i]!='0':
            entities.append((sen[0][i],predic[i]))
    if subj!="":
        entities.append((edit_dis_subject(subj[:-1]),'subject'))
    if day!="":
        entities.append((day[:-1],'day'))
    
    return (entities,predic,sen)

