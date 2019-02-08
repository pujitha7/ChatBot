
# coding: utf-8

# In[6]:


import pickle
import os
import numpy as np
from sklearn_crfsuite import CRF

with open('entity_data_X.pkl', 'rb') as pickle_load:
    X = pickle.load(pickle_load)
with open('entity_data_y.pkl', 'rb') as pickle_load:
    y = pickle.load(pickle_load)


# In[7]:


def entity_crf_train(my_subjects):
    for i in range(0,len(X)):
        for j in range(0,len(X[i])):
            if 'sub' in X[i][j]:
                subj=my_subjects[np.random.randint(len(my_subjects))]
                subj=subj.split()
                X[i]=X[i][:j]+subj+X[i][j+1:]
                y[i]=y[i][:j]+['subject']*len(subj)+y[i][j+1:]
        X[i]=X[i][0:10]  
        y[i]=y[i][0:10]
        
    crf = CRF(c1=0.1,
          c2=0.01,
          max_iterations=200,
          all_possible_transitions=True)
    
    print(".....Training entity extraction model.....")
    crf.fit(X, y)
    print(".....Trained entity extraction model.....")
    
    working_directory=os.path.abspath(os.path.join(os.getcwd(), os.pardir))
    with open(working_directory+'/full_model/crf_model.pkl', 'wb') as pickle_file:
        pickle.dump(crf, pickle_file, protocol=pickle.HIGHEST_PROTOCOL)
    with open(working_directory+'/full_model/subjects.pkl','wb') as pickle_file:
        pickle.dump(my_subjects,pickle_file,protocol=pickle.HIGHEST_PROTOCOL)

