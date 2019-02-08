
# coding: utf-8

# In[6]:

import sys,os
working_directory=os.path.abspath(os.path.join(os.getcwd(), os.pardir))
sys.path.insert(0, working_directory+'/entity_extraction/')
import crf_model_training
import db_create
import sqlite3
import shutil



# In[1]:


subs=input('Enter all subjects separated by comma')
no_of_subjects=subs.split(',')


# In[2]:


mon_classes=input('Classes on monday in the format (subject_name(space)time) for all subjects separated by comma time in hh:mm-hh:mm format')
if mon_classes=='':
    mon_classes=[]
else:
    mon_classes=mon_classes.split(',')
    for i in range(0,len(mon_classes)):
        mon_classes[i]=mon_classes[i].rsplit(' ',1)
        mon_classes[i]=[mon_classes[i][0][1:],mon_classes[i][1][:-1]]
        
tues_classes=input('Classes on tuesday in the format (subject_name(space)time) for all subjects separated by comma time in hh:mm-hh:mm format')
if tues_classes=='':
    tues_classes=[]
else:
    tues_classes=tues_classes.split(',')
    for i in range(0,len(tues_classes)):
        tues_classes[i]=tues_classes[i].rsplit(' ',1)
        tues_classes[i]=[tues_classes[i][0][1:],tues_classes[i][1][:-1]]

wed_classes=input('Classes on wednesday in the format (subject_name(space)time) for all subjects separated by comma time in hh-mm format')
if wed_classes=='':
    wed_classes=[]
else:
    wed_classes=wed_classes.split(',')
    for i in range(0,len(wed_classes)):
        wed_classes[i]=wed_classes[i].rsplit(' ',1)
        wed_classes[i]=[wed_classes[i][0][1:],wed_classes[i][1][:-1]]
        
        
thurs_classes=input('Classes on thursday in the format (subject_name(space)time) for all subjects separated by comma time in hh-mm format')
if thurs_classes=='':
    thurs_classes=[]
else:
    thurs_classes=thurs_classes.split(',')
    for i in range(0,len(thurs_classes)):
        thurs_classes[i]=thurs_classes[i].rsplit(' ',1)
        thurs_classes[i]=[thurs_classes[i][0][1:],thurs_classes[i][1][:-1]]
        
fri_classes=input('Classes on friday in the format (subject_name(space)time) for all subjects separated by comma time in hh-mm format')
if fri_classes=='':
    fri_classes=[]
else:
    fri_classes=fri_classes.split(',')
    for i in range(0,len(fri_classes)):
        fri_classes[i]=fri_classes[i].rsplit(' ',1)
        fri_classes[i]=[fri_classes[i][0][1:],fri_classes[i][1][:-1]]
        
sat_classes=input('Classes on saturday in the format (subject_name(space)time) for all subjects separated by comma time in hh-mm format')
if sat_classes=='':
    sat_classes=[]
else:
    sat_classes=sat_classes.split(',')
    for i in range(0,len(sat_classes)):
        sat_classes[i]=sat_classes[i].rsplit(' ',1)
        sat_classes[i]=[sat_classes[i][0][1:],sat_classes[i][1][:-1]]
        
sun_classes=input('Classes on sunday in the format (subject_name(space)time) for all subjects separated by comma time in hh-mm format')
if sun_classes=='':
    sun_classes=[]
else:
    sun_classes=sun_classes.split(',')
    for i in range(0,len(sun_classes)):
        sun_classes[i]=sun_classes[i].rsplit(' ',1)
        sun_classes[i]=[sun_classes[i][0][1:],sun_classes[i][1][:-1]]


# In[4]:


inp=input("Do you wanna save location of your classes also? Y/N")
locations={}
if inp=='Y' or inp=='y':
    for i in range(0,len(no_of_subjects)):
        locations[no_of_subjects[i]]=input("where is {} class".format(no_of_subjects[i]))


# In[7]:


conn=sqlite3.Connection("timetable.db")
c=conn.cursor()
conn2=sqlite3.Connection("remainders.db")
c2=conn2.cursor()

db_create.database_create(no_of_subjects,mon_classes,tues_classes,wed_classes,thurs_classes,fri_classes,sat_classes,sun_classes,locations,c,c2,conn)


# In[8]:


crf_model_training.entity_crf_train(no_of_subjects)


files = ['timetable.db', 'remainders.db']
for f in files:
    shutil.copy(f, working_directory+'/full_model/')

