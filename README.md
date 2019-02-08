 # Student Time-table query ChatBot
Bot for students to query about their classes, timings, remainders for quizzes, assignments etc
Chatbot built end to end from intent classification to entity extraction to core model. It also has small talk functionality.

## Natural Language Understanding
* Built Custom NLU model to detect the intent of the question and also extract the entities from the question. For training the NLU model data is created using Chatito.

### Intent classification: 
* A shallow neural network is built to classify the intent.
* Intents are: 'check_all_classes' ,'check_assignment_due', 'check_when_class','check_particular_class' , 'check_where_class' , 'add_reminder'       

### Entity exctraction:
* A sequence to sequence neural network model is built tagging each word in the question as entity or not as sequence tagging.
* Entities are: Day or date, subject, ordinal numbers.
* Spelling correction is performed using edit distance to extract entities.

## Core Engine

* The core of the model is used to decide upon which action need to be performed by the chatbot. Based on the intent and entities extracted an action is performed. Core engine of the chatbot is currently written using functional algorithm but working to convert the core of chatbot to learning capable.
* Some functions are: date_missing(), subject_missing(), check_for_remainders() etc.
* When all the required entities are obtained for an intent Database call is made using SQLite.
* Two databases are created one to store time table and other to store remainders.

## Small Talk

* Its always fun to have the chatbot do small talk. A small talk database is used to train the model to do small talk with cosine similarity question matching on a TFIDF matrix.

## TOOLS USED:
SKLearn ,Keras, Tensorflow, Gensim, SQLite3, NLTK
Numpy, Pandas, sklearn_crfsuite, OS, JSON, re
Pickle, editdistance, warnings, calender, random
Chatito - Online tool to generate datasets for Chatbot training.

## BUILD YOUR CUSTOM BOT INSTRUCTIONS: (Command-Line)
* Clone or Download the repository.
* cd ChatBot
* cd intent_classification
* python intent_classifier_training.py 
* cd ../entity_extraction
* python enitity_data_preprocessing.py
* cd ../starter_model
* python starter_code.py
** Then enter your time-table including all the subjects, their timings, location. If no classes on that day just click enter without typing anything.
* cd ../full_model
* python small_talk_preprocessing.py
* python small_talk_classification_training.py

* python small_talk_training.py
* python prediction.py
** Test the bot.
* To stop the bot type "bye".

## DEMO:
![image](https://user-images.githubusercontent.com/16939123/52484790-30eb3b00-2bdd-11e9-804a-f5e2c4f3be14.png)


## Work in progress:
Trying to use machine learning in Core engine also.
