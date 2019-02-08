
# coding: utf-8

# In[58]:


import warnings
warnings.filterwarnings("ignore")
import json
import codecs
import pandas as pd
import numpy as np
import editdistance
import keras
import pickle
import os
from sklearn.model_selection import train_test_split

working_directory=os.path.abspath(os.path.join(os.getcwd(), os.pardir))


# In[29]:


js=json.load(codecs.open(working_directory+'/data/all_classes.json', 'r', 'utf-8-sig'))
check_all_classes = []
tmp = []
for i in range(len(js['what_class_day'])):
    for j in range(len(js['what_class_day'][i])):
        tmp.append(js['what_class_day'][i][j]['value'])
    tmp = ''.join(tmp)
    check_all_classes.append(tmp)
    tmp = []


# In[30]:


js=json.load(codecs.open(working_directory+'/data/check_assignment_due.json', 'r', 'utf-8-sig'))
check_assignment_due=[]
tmp = []
for i in range(len(js['check_assignemnt_for_particular_subject'])):
    for j in range(len(js['check_assignemnt_for_particular_subject'][i])):
        tmp.append(js['check_assignemnt_for_particular_subject'][i][j]['value'])
    tmp = ''.join(tmp)
    check_assignment_due.append(tmp)
    tmp = []


# In[31]:


js=json.load(codecs.open(working_directory+'/data/find_whether_a_class.json', 'r', 'utf-8-sig'))
check_when_class=[]
tmp = []
for i in range(len(js['find_when_lecture_is'])):
    for j in range(len(js['find_when_lecture_is'][i])):
        tmp.append(js['find_when_lecture_is'][i][j]['value'])
    tmp = ''.join(tmp)
    check_when_class.append(tmp)
    tmp = []


# In[32]:


js=json.load(codecs.open(working_directory+'/data/find_what_is_particular_class.json', 'r', 'utf-8-sig'))
check_particular_class=[]
tmp = []
for i in range(len(js['find_what_lecture'])):
    for j in range(len(js['find_what_lecture'][i])):
        tmp.append(js['find_what_lecture'][i][j]['value'])
    tmp = ''.join(tmp)
    check_particular_class.append(tmp)
    tmp = []


# In[33]:


js=json.load(codecs.open(working_directory+'/data/where_class.json', 'r', 'utf-8-sig'))
check_where_class=[]
tmp = []
for i in range(len(js['where_class'])):
    for j in range(len(js['where_class'][i])):
        tmp.append(js['where_class'][i][j]['value'])
    tmp = ''.join(tmp)
    check_where_class.append(tmp)
    tmp = []


# In[34]:


js=json.load(codecs.open(working_directory+'/data/add_reminder_1.json', 'r', 'utf-8-sig'))
ad1=[]
tmp = []
for i in range(len(js['add_remainder'])):
    for j in range(len(js['add_remainder'][i])):
        tmp.append(js['add_remainder'][i][j]['value'])
    tmp = ''.join(tmp)
    ad1.append(tmp)
    tmp = []
js=json.load(codecs.open(working_directory+'/data/add_reminder_2.json', 'r', 'utf-8-sig'))
ad2=[]
tmp = []
for i in range(len(js['add_remainder'])):
    for j in range(len(js['add_remainder'][i])):
        tmp.append(js['add_remainder'][i][j]['value'])
    tmp = ''.join(tmp)
    ad2.append(tmp)
    tmp = []
js=json.load(codecs.open(working_directory+'/data/add_reminder_3.json', 'r', 'utf-8-sig'))
ad3=[]
tmp = []
for i in range(len(js['add_remainder'])):
    for j in range(len(js['add_remainder'][i])):
        tmp.append(js['add_remainder'][i][j]['value'])
    tmp = ''.join(tmp)
    ad3.append(tmp)
    tmp = []
js=json.load(codecs.open(working_directory+'/data/add_reminder_4.json', 'r', 'utf-8-sig'))
ad4=[]
tmp = []
for i in range(len(js['add_remainder'])):
    for j in range(len(js['add_remainder'][i])):
        tmp.append(js['add_remainder'][i][j]['value'])
    tmp = ''.join(tmp)
    ad4.append(tmp)
    tmp = []
js=json.load(codecs.open(working_directory+'/data/add_reminder_5.json', 'r', 'utf-8-sig'))
ad5=[]
tmp = []
for i in range(len(js['add_remainder'])):
    for j in range(len(js['add_remainder'][i])):
        tmp.append(js['add_remainder'][i][j]['value'])
    tmp = ''.join(tmp)
    ad5.append(tmp)
    tmp = []
    
add_remainder=ad1+ad2+ad3+ad4+ad5


# In[35]:


final_data=check_all_classes+check_assignment_due+check_when_class+check_particular_class+check_where_class+add_remainder


# In[36]:


with open(working_directory+'/data/total_data.pkl', 'wb') as pickle_file:
    pickle.dump(final_data, pickle_file, protocol=pickle.HIGHEST_PROTOCOL)


# In[37]:


for i in range(0,len(final_data)):
    final_data[i]=final_data[i].lower()
    final_data[i]=final_data[i].split()


# In[38]:


max_len = len(max(final_data,key = len))


# In[39]:


for i in range(len(final_data)):
    temp = final_data[i]
    for j in range(max_len-len(temp)):
        final_data[i] = final_data[i] + ['pad_word']


# In[40]:


from gensim.models import Word2Vec


# In[41]:


w2v = Word2Vec(final_data,size=20)


# In[42]:


w2v.save(working_directory+'/full_model/w2v_model_for_intent_classification.model')


# In[43]:


print("word2vec done .. next training model")


# In[44]:


target  = len(check_all_classes) * [0] + len(check_assignment_due)* [1] + len(check_when_class) * [2] + len(check_particular_class) * [3] + len(check_where_class) * [4] + len(add_remainder) * [5]
target_classes = ['check_all_classes' ,'check_assignment_due', 'check_when_class', 'check_particular_class' , 'check_where_class' , 'add_reminder']


# In[45]:


for i in range(len(final_data)):
    for j in range(len(final_data[i])):
        final_data[i][j] = w2v.wv[final_data[i][j]]


# In[46]:


np.shape(final_data)


# In[47]:


len(target)


# In[48]:


x_train,x_test,y_train,y_test = train_test_split(final_data,target,test_size = 0.2,stratify = target,random_state = 1234)


# In[49]:


y_train = pd.get_dummies(y_train)
y_test = pd.get_dummies(y_test)


# In[50]:


x_train = np.array(x_train)
y_train = np.array(y_train)
x_test = np.array(x_test)
y_test = np.array(y_test)


# In[51]:


np.shape(x_test)


# In[52]:


inp = keras.layers.Input(shape=[None,20])
lstm=keras.layers.LSTM(16)(inp)
out = keras.layers.Dense(6,activation='softmax')(lstm)


# In[53]:


model = keras.Model(inputs = inp,outputs=out)


# In[54]:


model.compile(optimizer='Adam',loss='categorical_crossentropy',metrics=['accuracy'])


# In[55]:


model.summary()


# In[56]:


model.fit(x = x_train,y = y_train,batch_size = 32,epochs=1,verbose =1,validation_data = [x_test,y_test],shuffle = True)


# In[57]:


model.save(working_directory+"/full_model/intent_model.h5")

