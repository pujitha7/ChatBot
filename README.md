# ChatBot
Bot for students to query about their classes, timings, remainders for quizzes, assignments etc

Chatbot built end to end from intent classification to entity extraction to core model. It is also has small talk functionality.

# Natural Language Understanding
Built Custom NLU model to detect the intent of the question and also extract the entities from the question. For training the NLU model data is created using Chatito.

Intent classification: A shallow neural network is built to classify the intent.

Intents are: 'check_all_classes' ,'check_assignment_due', 'check_when_class', 'check_particular_class' , 'check_where_class' , 'add_reminder'

Entity exctraction: A sequence to sequence neural network model is built tagging each word in the question as entity or not as sequence tagging.

Entities are: Day or date, subject, ordinal numbers.

Spelling correction is performed using edit distance to extract entities.

# Core Engine

The core of the model is used to decide upon which action need to be performed by the chatbot. Based on the intent and entities extracted an action is performed. Core engine of the chatbot is currently written using functional algorithm but working to convert the core of chatbot to learning capable.

Some functions are: date_missing(), subject_missing(), check_for_remainders() etc.

When all the required entities are obtained for an intent Database call is made using SQLite.
Two databases are created one to store time table and other to store remainders.

# Small Talk

Its always fun to have the chatbot do small talk. A small talk database is used to train the model to do small talk with cosine similarity question matching on a TFIDF matrix.


![image](https://user-images.githubusercontent.com/16939123/52484790-30eb3b00-2bdd-11e9-804a-f5e2c4f3be14.png)
