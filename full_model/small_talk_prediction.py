
# coding: utf-8

# In[3]:


import pickle
import random
import numpy as np
with open('small_talk_model.pkl', 'rb') as pickle_load:
    tfidf1 = pickle.load(pickle_load)
    
with open('sparse_small_transformed.pkl', 'rb') as pickle_load:
    a1 = pickle.load(pickle_load)
    
with open('small_talk_answers.pkl', 'rb') as pickle_load:
    ans1 = pickle.load(pickle_load)
    
from sklearn.metrics.pairwise import cosine_similarity

exit_words = ['quit','end','bye','stop','exit']

def small_talk(sen):
    
    if sen in exit_words:
        return print("bot: bye bye")
    
    b1 = tfidf1.transform([sen])
    z1 = cosine_similarity(a1,b1)
    
    print("bot: ",ans1[random.choice([i for i in range(len(z1)) if z1[i] == z1[np.argmax(z1)][0]])])
    
    return

