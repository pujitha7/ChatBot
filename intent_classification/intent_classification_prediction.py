
# coding: utf-8

# In[1]:


from keras.models import load_model
from gensim.models import Word2Vec
import editdistance
import numpy as np
import editdistance


target_classes = ['check_all_classes' ,'check_assignment_due', 'check_when_class', 'check_particular_class' , 'check_where_class' , 'add_reminder']
model_inf = load_model('intent_model.h5')
w2v = Word2Vec.load('w2v_model_for_intent_classification.model')

def intent_classifier(sent):
    
    def unk_words(unk):
        mini = 10
        for i in range(len(w2v.wv.vocab)):
            dist = editdistance.eval(unk,list(w2v.wv.vocab)[i])
            unk_closet=""
            if list(w2v.wv.vocab)[i][0] == unk[0]:
                if dist < mini:
                    mini = dist
                    unk_closest = list(w2v.wv.vocab)[i]
        if unk_closet=="":
            return 'pad_word'
        else:
            return unk_closest


    sent = sent.split(" ")
    a = []
    for i in range(len(sent)):
        try:
            a.append(w2v.wv[sent[i]])
        except KeyError:
            sent[i] = unk_words(sent[i])
            a.append(w2v.wv[sent[i]])
    for i in range(10 - len(a)):
        a.append(w2v.wv['pad_word'])
    a = np.array(a)
    a = a.reshape([1,len(a),20])
    
    pred=model_inf.predict(a)
    confidence=pred[0][np.argmax(pred)]
    
    if confidence>0.78:
        return target_classes[np.argmax(pred)]
    else:
        return 'bad intent'

