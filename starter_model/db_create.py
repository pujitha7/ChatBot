
# coding: utf-8

# In[3]:


import sqlite3


# In[4]:


def database_create(no_of_subjects,mon,tues,wed,thurs,fri,sat,sun,locations,c,c2,conn):
    working_days=[]
    all_classes=[]
    if len(mon)!=0:
        all_classes.append(mon)
        working_days.append('monday')
    if len(tues)!=0:
        all_classes.append(tues)
        working_days.append('tuesday')
    if len(wed)!=0:
        all_classes.append(wed)
        working_days.append('wednesday')
    if len(thurs)!=0:
        all_classes.append(thurs)
        working_days.append('thursday')
    if len(fri)!=0:
        all_classes.append(fri)
        working_days.append('friday')
    if len(sat)!=0:
        all_classes.append(sat)
        working_days.append('saturday')
    if len(sun)!=0:
        all_classes.append(sun)
        working_days.append('sunday')
        
    
    c.execute("""CREATE TABLE timetable('subject' text,
                                    'monday' text DEFAULT noclass,
                                    tuesday text DEFAULT noclass,
                                    wednesday text DEFAULT noclass,
                                    thursday text DEFAULT noclass,
                                    friday text DEFAULT noclass,
                                    saturday text DEFAULT noclass,
                                    sunday text DEFAULT noclass,
                                    location text DEFAULT notspecified)""")
    
    for i in range(0,len(no_of_subjects)):
        with conn:
            try:
                locate=locations[no_of_subjects[i]]
            except:
                locate='notspecified'
            c.execute("INSERT INTO timetable(subject,location) VALUES(:sub,:loc)",{'sub':no_of_subjects[i],
                                                                               'loc':locate})
            
    for i in range(0,len(working_days)):
        for j in range(0,len(all_classes[i])):
            with conn:
                c.execute("""UPDATE timetable SET %s=? WHERE subject=?"""% working_days[i],
                                                      (all_classes[i][j][1],all_classes[i][j][0]))
                
    
    c2.execute("""CREATE TABLE remainders(subject text DEFAULT 'NA',
                                     date DATE,
                                     remainder text)""")
    

