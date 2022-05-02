# -*- coding: utf-8 -*-
"""
Created on Sat Apr 23 17:34:27 2022

@author: allen
"""
import pandas as pd
from sklearn.metrics import cohen_kappa_score
from sklearn.metrics import precision_score, recall_score, accuracy_score
from sklearn.naive_bayes import GaussianNB

df = pd.read_csv('flow_expert_balanced.csv')
df = df[df['Time'] >= 0]

df = df.drop(columns=['Unnamed: 0', 'Side'])
print(len(df[df['Flow'] == False]))
print(len(df[df['Flow'] == True]))

training = df.sample(frac=.5, random_state=42)
test = df.drop(training.index)

training_y = training['Flow']
training_x = training.drop(columns=['Flow'])

test_y = test['Flow']
test_x = test.drop(columns=['Flow'])

gnb = GaussianNB()
gnb.fit(training_x, training_y)

gnb_predictions = gnb.predict(test_x)
print('Guassian Niave Bayes Accuracy: %.3f' % accuracy_score(test_y, gnb_predictions))
print('Guassian Niave Bayes Precision: %.3f' % precision_score(test_y, gnb_predictions))
print('Guassian Niave Bayes Recall: %.3f' % recall_score(test_y, gnb_predictions))
print("Guassian Naive Bayes Cohens Kappa: ", cohen_kappa_score(test_y, gnb_predictions))