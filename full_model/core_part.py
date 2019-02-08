
# coding: utf-8

# In[14]:

import nlu_modified
import datetime
import sqlite3
import dateutil.parser
import calendar
import os

import sys
working_directory=os.path.abspath(os.path.join(os.getcwd(), os.pardir))
sys.path.insert(0, working_directory+'/entity_extraction/')
import crf_model_prediction


import sentence_classification_prediction
import small_talk_prediction


def all_classes(day):
    conn=sqlite3.Connection("timetable.db")
    c=conn.cursor()
    c.execute("SELECT subject,(%s) FROM timetable WHERE  (%s)!='noclass'" % (day,day))
    return c.fetchall()

def check_what_lecture(value,day):
    conn=sqlite3.Connection("timetable.db")
    c=conn.cursor()
    c.execute("SELECT subject,(%s) FROM timetable WHERE (%s)!='noclass'" % (day,day))
    timings=c.fetchall()
    start_time={}
    for i in range(0,len(timings)):
        start_time[timings[i][0]]=int(timings[i][1][0:2])
    sorted_start_time = sorted(start_time.items(), key=lambda kv: kv[1])
    return sorted_start_time[value-1][0]

def check_when_lecture(subject,day):
    conn=sqlite3.Connection("timetable.db")
    c=conn.cursor()
    c.execute("SELECT subject,(%s) FROM timetable WHERE subject=?" % (day),(subject,))
    return c.fetchall()

def where_class(subject):
    conn=sqlite3.Connection("timetable.db")
    c=conn.cursor()
    c.execute("SELECT subject,location FROM timetable WHERE subject=?",(subject,))
    return c.fetchall()

def remainder_add(date,remainder,subject='not_specified'):
    conn2=sqlite3.Connection("remainders.db")
    c2=conn2.cursor()
    c2.execute("""INSERT INTO remainders(subject,date,remainder) VALUES(?,?,?)""",(subject,date,remainder))
    conn2.commit()

def check_for_remainders(date='NA',subject='NA'):
    conn2=sqlite3.Connection("remainders.db")
    c2=conn2.cursor()
    if subject=='NA' and date!='NA':
        c2.execute("SELECT DISTINCT date,subject,remainder FROM remainders WHERE date=?",(date,))
    elif date=='NA' and subject!='NA':
        c2.execute("SELECT DISTINCT date,subject,remainder FROM remainders WHERE subject=?",(subject,))
    elif date!='NA' and subject!='NA':
        c2.execute("SELECT DISTINCT date,subject,remainder FROM remainders WHERE date=? AND subject=?",(date,subject))
    else:
        c2.execute("SELECT DISTINCT date,subject,remainder FROM remainders WHERE date>=DATE() ORDER BY date ASC LIMIT 5")
    return c2.fetchall()

def date_missing():
    sen=input("bot: Enter the date")
    date=crf_model_prediction.entity_pred(sen)[0][0][0]
    return date

def subject_missing():
    sen=input("bot: Enter for which subject")
    subject=crf_model_prediction.entity_pred(sen)[0][0][0]
    return subject

def count_missing():
    sen=input("bot: Enter is first, second or what?")
    count=crf_model_prediction.entity_pred(sen)[0][0][0]
    return count

def content_missing():
    sentence=input("bot: What to remind about")
    content=nlu_modified.nlu(sentence,'add_reminder')
    subject=crf_model_prediction.entity_pred(sentence)[0]
    if len(subject)==0:
        return content,'NA'
    else:
        return content,subject[0][0]

def flush_all(dictionary):
    dictionary['subject']='NA'
    dictionary['date']='NA'
    dictionary['count']=0
    dictionary['content']='NA'
    return dictionary

def copy_data(dictionary1,dictionary2):
    dictionary2['subject']=dictionary1['subject']
    dictionary2['date']=dictionary1['date']
    dictionary2['count']=dictionary1['count']
    return dictionary2

def all_classes_core(current_dict,prev_dict):
    global base_time
    
    #Time difference to check context
    time_now=datetime.datetime.now()
    time_diff = time_now - base_time
    diff=time_diff.total_seconds()
    base_time=datetime.datetime.now()
    
    #formatting date
    if current_dict['date']!='NA':
        current_dict['date']=date_formatting(current_dict['date'],'DAY')
    if prev_dict['date']!='NA':
        prev_dict['date']=date_formatting(prev_dict['date'],'DAY')
    
    #if time diff is less than 120 sec taking previous entities
    if current_dict['date'] == 'NA' and diff <60:
        if prev_dict['date']!='NA':
            current_dict['date']=previous_dict['date']
    
    if diff>60:
        prev_dict=flush_all(prev_dict)
        
    #if date is missing
    if current_dict['date'] == 'NA':
            current_dict['date']=date_missing()
            current_dict['date']=date_formatting(current_dict['date'],'DAY')
        
    #making db call        
    if current_dict['date']!='NA':
        res=all_classes(current_dict['date'])
        for i in range(0,len(res)):
            print("bot: You have "+res[i][0]+" at "+res[i][1])
        if len(res)==0:
            print("bot: No classes today")
    
    #storing in prev_dict
    prev_dict=copy_data(current_dict,prev_dict)
    
    return current_dict,prev_dict
def check_for_reminders_core(current_dict,prev_dict):
    global base_time
    
    #time differnece to check context
    time_now=datetime.datetime.now()
    time_diff = time_now - base_time
    diff=time_diff.total_seconds()
    base_time=datetime.datetime.now()
    
    #time formatting
    if current_dict['date']!='NA':
        current_dict['date']=date_formatting(current_dict['date'],'DATE')
    if prev_dict['date']!='NA':
        prev_dict['date']=date_formatting(prev_dict['date'],'DATE')
    
    #taking context
    if current_dict['date'] == 'NA' and current_dict['subject'] == 'NA' and diff < 60:
        if prev_dict['date']!='NA':
            current_dict['date']=prev_dict['date']
        if prev_dict['subject']!='NA':
            current_dict['subject']=prev_dict['subject']
    
    #flushing
    if diff >60:
        prev_dict=flush_all(prev_dict)
      
    #making db call
    remainds=check_for_remainders(current_dict['date'],current_dict['subject'])
    
    
    #storing in prev_data
    prev_dict=copy_data(current_dict,prev_dict)
    
    
    #printing result
    if len(remainds)==0:
        print("bot: You dont have any remainders")
    else:
        for i in range(0,len(remainds)):
            if remainds[i][1]=='not_specified':
                print('bot: You have '+remainds[i][2]+' on'+remainds[i][0])
            else:
                print('bot: You have '+remainds[i][1]+' '+remainds[i][2]+' on'+remainds[i][0])
                prev_dict['subject']=remainds[i][1]
    
    return current_dict,prev_dict            
def check_when_class_is_core(current_dict,prev_dict):
    
    global base_time
    
    #time differnece to check context
    time_now=datetime.datetime.now()
    time_diff = time_now - base_time
    diff=time_diff.total_seconds()
    base_time=datetime.datetime.now()
        
    #date formatting
    if current_dict['date']!='NA':
        current_dict['date']=date_formatting(current_dict['date'],'DAY')
    if prev_dict['date']!='NA':
        prev_dict['date']=date_formatting(prev_dict['date'],'DAY')
        
    #time diff
    if current_dict['date'] == 'NA' and current_dict['subject'] == 'NA' and diff <60:
        #use previous entities
        if prev_dict['date']!='NA':
            current_dict['date']=prev_dict['date']
        if prev_dict['subject']!='NA':
            current_dict['subject']=prev_dict['subject']
            
    #flushing
    if diff >60:
        prev_dict=flush_all(prev_dict)
    
    #Missing
    if current_dict['subject'] == 'NA':
            current_dict['subject']=subject_missing()
    if current_dict['date']=='NA':  
            current_dict['date']=date_missing()
            current_dict['date']=date_formatting(current_dict['date'],'DAY')
    
    #storing in prev_data
    prev_dict=copy_data(current_dict,prev_dict)
    
    #Make DB call
    if current_dict['date'] != 'NA' and current_dict['subject']!='NA':
        res=check_when_lecture(current_dict['subject'],current_dict['date'])
        if res[0][1]!='noclass':
            print("bot: You have "+res[0][0]+" at "+res[0][1])
            prev_dict['subject']=res[0][0]
        else:
            print("bot: You have no class")
            
    return current_dict,prev_dict

def check_what_lecture_core(current_dict,prev_dict):
    global base_time
    
    #time differnece to check context
    time_now=datetime.datetime.now()
    time_diff = time_now - base_time
    diff=time_diff.total_seconds()
    base_time=datetime.datetime.now()
    
    #date formatting
    if current_dict['date']!='NA':
        current_dict['date']=date_formatting(current_dict['date'],'DAY')
    if prev_dict['date']!='NA':
        prev_dict['date']=date_formatting(prev_dict['date'],'DAY')
    
    #if time diff
    if current_dict['date'] == 'NA' and current_dict['count'] == 0 and diff <60:
        if prev_dict['date']!='NA':
            current_dict['date']=prev_dict['date']
        if prev_dict['date']!=0:
            current_dict['count']=prev_dict['count']
    
    #flushing
    if diff >60:
        prev_dict=flush_all(prev_dict)        
    
    #Missing
    if current_dict['count'] == 0:
            current_dict['count']=count_missing()
    if current_dict['date']=='NA':  
            current_dict['date']=date_missing()
            current_dict['date']=date_formatting(current_dict['date'],'DAY')
  
    #storing in prev_data
    prev_dict=copy_data(current_dict,prev_dict)
    
    #DB call
    if current_dict['date'] != 'NA' and current_dict['count']!=0:            
            try:
                res=check_what_lecture(current_dict['count'],current_dict['date'])
                print("bot: You have "+res+" on "+current_dict['date'])
                prev_dict['subject']=res
            except:
                print("bot: You have no class")
                
    return current_dict,prev_dict
def remainder_add_core(current_dict,prev_dict,content='NA'):
    global base_time
    
    #time differnece to check context
    time_now=datetime.datetime.now()
    time_diff = time_now - base_time
    diff=time_diff.total_seconds()
    base_time=datetime.datetime.now()
    
    #date formatting
    if current_dict['date']!='NA':
        current_dict['date']=date_formatting(current_dict['date'],'DATE')
    
    #if content not specified    
    if content=='NA':
        content,subject=content_missing()
        current_dict['content']=content
        if subject!='NA':
            current_dict['subject']=subject
        
    #Date missing 
    if current_dict['date'] == 'NA':
        current_dict['date']=date_missing()
        current_dict['date']=date_formatting(current_dict['date'],'DATE')
        
    #DB call    
    if current_dict['date'] != 'NA' and current_dict['subject']!='NA':
        remainder_add(current_dict['date'],content,current_dict['subject'])
        print("bot: remainder added")
    
    else:
        remainder_add(current_dict['date'],content)
        print("bot: remainder added")
    
    #storing in prev_data
    prev_dict=copy_data(current_dict,prev_dict)
    
    return current_dict,prev_dict
def where_class_core(current_dict,prev_dict):
    global base_time
    
    #time differnece to check context
    time_now=datetime.datetime.now()
    time_diff = time_now - base_time
    diff=time_diff.total_seconds()
    base_time=datetime.datetime.now()
    
    #time diff
    if current_dict['subject'] == 'NA' and diff <60:
        if prev_dict['subject']!='NA':
            current_dict['subject']=prev_dict['subject']
    
    #flushing
    if diff >60:
        prev_dict=flush_all(prev_dict)
        
           
    #Missing call
    if current_dict['subject'] == 'NA':
            current_dict['subject']=subject_missing()
    
    #storing in prev_data
    prev_dict=copy_data(current_dict,prev_dict)
    
    #DB call
    if current_dict['subject']!='NA':
        out=where_class(current_dict['subject'])
        if out[0][1]!='notspecified':
            print("bot: You have "+out[0][0]+" at "+out[0][1])
        else:
            print("bot: No info")
    
    return current_dict,prev_dict  
def date_formatting(date1,type_required):
    if type_required=='DATE':
        if date1 in ['today','tdy','tod']:
            return str(datetime.date.today())
        if date1 in ['tommorrow','tmrw','tomorow','tom','tomorrow','tmrww']:
            return str(datetime.date.today() + datetime.timedelta(1))
        if 'next' in date1 and 'mon' in date1:
            today = datetime.date.today()
            return str(today + datetime.timedelta( (0-today.weekday()) % 7 ))
        if 'next' in date1 and 'tue' in date1:
            today = datetime.date.today()
            return str(today + datetime.timedelta( (1-today.weekday()) % 7 ))
        if 'next' in date1 and 'wed' in date1:
            today = datetime.date.today()
            return str(today + datetime.timedelta( (2-today.weekday()) % 7 ))
        if 'next' in date1 and 'thu' in date1:
            today = datetime.date.today()
            return str(today + datetime.timedelta( (3-today.weekday()) % 7 ))
        if 'next' in date1 and 'fri' in date1:
            today = datetime.date.today()
            return str(today + datetime.timedelta( (4-today.weekday()) % 7 ))
        if 'next' in date1 and 'sat' in date1:
            today = datetime.date.today()
            return str(today + datetime.timedelta( (5-today.weekday()) % 7 ))
        if 'next' in date1 and 'sun' in date1:
            today = datetime.date.today()
            return str(today + datetime.timedelta( (6-today.weekday()) % 7 ))
        
        if 'mon' in date1:
            return str(dateutil.parser.parse("mon"))[0:10]
        if 'tue' in date1:
            return str(dateutil.parser.parse("tue"))[0:10]
        if 'wed' in date1:
            return str(dateutil.parser.parse("wed"))[0:10]
        if 'thu' in date1:
            return str(dateutil.parser.parse("thu"))[0:10]
        if 'fri' in date1:
            return str(dateutil.parser.parse("fri"))[0:10]
        if 'sat' in date1:
            return str(dateutil.parser.parse("sat"))[0:10]
        if 'sun' in date1:
            return str(dateutil.parser.parse("sun"))[0:10]
        
        try:
            return str(dateutil.parser.parse(date1))[0:10]
        except:
            return 'NA'
            
    if type_required=='DAY':
        if date1 in ['today','tdy','tod']:
            my_date = datetime.date.today()
            return calendar.day_name[my_date.weekday()].lower()
        if date1 in ['tommorrow','tmrw','tomorow','tom','tomorrow','tmrww']:
            today = datetime.date.today()
            my_date=today + datetime.timedelta(1)
            return calendar.day_name[my_date.weekday()].lower()
        
        if 'mon' in date1:
            return 'monday'
        if 'tue' in date1:
            return 'tuesday'
        if 'wed' in date1:
            return 'wednesday'
        if 'thu' in date1:
            return 'thursday'
        if 'fri' in date1:
            return 'friday'
        if 'sat' in date1:
            return 'saturday'
        if 'sun' in date1:
            return 'sunday'
        try:
            my_date=dateutil.parser.parse(date1)
            return calendar.day_name[my_date.weekday()].lower()
        except:
            return 'NA'
        

base_time=datetime.datetime.now()

def output(ques,current_dict,prev_dict):
    global base_time
    
    if sentence_classification_prediction.prediction(ques)=='small_talk':
        small_talk_prediction.small_talk(ques)
        return current_dict,prev_dict
        
    
    int_ent=nlu_modified.nlu(ques)
        
    if int_ent=='bad intent':
        print('bot: oops unable to understand the sentence please renter')
        return current_dict,prev_dict
        
    entitiies=int_ent['entities']
    
    
    current_dict=flush_all(current_dict)
    
    
    for i in range(0,len(entitiies)):
        if entitiies[i][1]=='day':
            current_dict['date']=entitiies[i][0]
        elif entitiies[i][1]=='count':
            current_dict['count']=entitiies[i][0]
        elif entitiies[i][1]=='subject':
            current_dict['subject']=entitiies[i][0]
    
    if int_ent['content']!='NA':
        current_dict['content']=int_ent['content']
        
    intent=int_ent['intent']
    
    if intent=='check_all_classes':
        current_dict,prev_dict=all_classes_core(current_dict,prev_dict)
    elif intent=='check_assignment_due':
        current_dict,prev_dict=check_for_reminders_core(current_dict,prev_dict)
    elif intent=='check_when_class':
        current_dict,prev_dict=check_when_class_is_core(current_dict,prev_dict)
    elif intent=='check_particular_class':
        current_dict,prev_dict=check_what_lecture_core(current_dict,prev_dict)
    elif intent=='check_where_class':
        current_dict,prev_dict=where_class_core(current_dict,prev_dict)
    elif intent=='add_reminder':
        current_dict,prev_dict=remainder_add_core(current_dict,prev_dict,current_dict['content'])
    else:
        print("bot: Not understood")
    
    return current_dict,prev_dict

