#h coding: utf-8

# In[ ]:


import core_part

current_dict={'subject':'NA','count':'NA','content':'NA','date':'NA'}
prev_dict={'subject':'NA','count':'NA','content':'NA','date':'NA'}

print('hello')

sentence=input()
while(sentence not in ['bye','goodbye']):
    current_dict,prev_dict=core_part.output(sentence,current_dict,prev_dict)
    sentence=input()

