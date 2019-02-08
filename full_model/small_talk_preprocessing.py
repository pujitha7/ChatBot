
# coding: utf-8

# In[1]:


import random
import numpy as np
import pickle

file = open("small_talk_data.txt",'r')

data = [i for i in file]

ques = []
ans = []

for i in range(len(data)):
    if data[i][0:3] == '- -':
        ques.append(data[i])
        ans.append(data[i+1])
        i = i + 1

import re
for i in range(len(ques)):
    ques[i] = re.sub('\W+',' ', ques[i] )
    ans[i] = re.sub('\W+',' ', ans[i] )
    ques[i] = ques[i][1:-1]
    ans[i] = ans[i][1:-1]


# In[2]:


with open('questions.pkl', 'wb') as cpickle:
    pickle.dump(ques, cpickle, protocol=pickle.HIGHEST_PROTOCOL)

