
# coding: utf-8

# In[1]:


import sys
import os
working_directory=os.path.abspath(os.path.join(os.getcwd(), os.pardir))
sys.path.insert(0, working_directory+'/intent_classification/')
import intent_classification_prediction
working_directory=os.path.abspath(os.path.join(os.getcwd(), os.pardir))
sys.path.insert(0, working_directory+'/entity_extraction/')
import crf_model_prediction
from nltk.corpus import stopwords
import pickle

def nlu(sent,intention='NA'):
    if intention!='NA':
        intent=intention
    
    else:
        intent=intent_classification_prediction.intent_classifier(sent)
    
        if intent == 'bad intent':
            return 'bad intent'
    
    entities = crf_model_prediction.entity_pred(sent)
    
    entities_list=[]
    for i in range(0,len(entities[1])):
        if entities[1][i]!='0':
            entities_list.append(entities[2][0][i])
        
    if intent=='add_reminder':
        sentence=entities[2][0]
        content_str=reminder_content(sentence,entities_list)
        if content_str=='':
            content_str='NA'
        
    else:
        content_str="NA"
    
    
    if intention!='NA':
        return content_str
    
    current_nlu_values = {}
    
    current_nlu_values['intent'] = intent
    current_nlu_values['entities'] = entities[0]
    current_nlu_values['content'] = content_str

    
    
    return current_nlu_values

def reminder_content(sentence,entities_list):
    stop = set(stopwords.words('english'))
    sentence=[i for i in sentence if i not in stop]
    content=[]
    for word in sentence:
        if word not in entities_list+['remind']+['remaind']:
            content.append(word)
    
    content_str=" ".join(word for word in content)
    return content_str

