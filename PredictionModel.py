# -*- coding: utf-8 -*-
"""
Created on Sat Apr 23 17:34:27 2022

@author: allen
"""
import pandas as pd
from sklearn.metrics import cohen_kappa_score
from sklearn.metrics import precision_score, recall_score, accuracy_score
from sklearn.naive_bayes import GaussianNB
from sklearn import svm

transitions = {}

def find_key(beat_ID, states_dict):
    for i in range(len(states_dict)):
        if states_dict[i] == beat_ID:
            return i
        
def display_transitions(truth, predictions):
    transitions = {}
    prev_keys = truth['Prev_Key'].to_list()
    for index in range(len(predictions)):  
        if prev_keys[index] not in transitions:
            transitions[prev_keys[index]] = []
            transitions[prev_keys[index]].append(predictions[index])
        elif predictions[index] not in transitions[prev_keys[index]]:
                transitions[prev_keys[index]].append(predictions[index])
    print(transitions)

def score_predictions(truth, predictions, transitions):
    total = len(predictions)
    correct = 0
    
    print("Processing " + str(total) + " Predictions")
    truth_key = truth['Prev_Key'].to_list()
    matched = False
    num_processed = 0
 
    for index in range(len(predictions)):
        matched = False
        prev_key = truth_key[index]
        prediction = predictions[index]
        for index, row in transitions.iterrows():
            if row['Prev_Key'] == prev_key and row['Next_Key'] == prediction:
                matched = True
                break
        if matched:
            correct += 1
        num_processed += 1
        print("Processed Prediction " + str(num_processed) + ' ' + str(matched))
        
    return correct / total

# Read in the data and filter to only good flow songs
df_main = pd.read_csv('single_expert_cleaned.csv')
df_main = df_main[df_main['Flow'] == True]
df_main = df_main.drop(columns=['Unnamed: 0'])
print(df_main.columns)

# Read in the key translation table and transitions data
df_transitions = pd.read_csv('single_expert_transitions.csv')
print(df_transitions.columns)

df_keys = pd.read_csv('single_expert_beat_keys.csv')
print(df_keys.columns)

        
print()
print("Total Number of Transitions: ", len(df_main['Beat_ID']))
print("Number of Unique Beat States: ", len(df_keys['Key']))

training = df_main.sample(frac=.5, random_state=42)
test = df_main.drop(training.index)

training_y = training['Curr_Key']
training_x = training.drop(columns=['Side', 'Beat_ID', 'Prev_Beat_ID', 'Curr_Key', 'Prev_Key', 'Flow', 'Curr0-0', 'Curr0-1', 'Curr0-2', 'Curr0-3',
                                    'Curr1-0', 'Curr1-1', 'Curr1-2', 'Curr1-3',
                                    'Curr2-0', 'Curr2-1', 'Curr2-2', 'Curr2-3'])
test_y = test['Curr_Key']
test_x = test.drop(columns=['Side', 'Beat_ID', 'Prev_Beat_ID', 'Curr_Key', 'Prev_Key', 'Flow', 'Curr0-0', 'Curr0-1', 'Curr0-2', 'Curr0-3',
                            'Curr1-0', 'Curr1-1', 'Curr1-2', 'Curr1-3',
                            'Curr2-0', 'Curr2-1', 'Curr2-2', 'Curr2-3'])
test_x_with_prev_key = test.drop(columns=['Side', 'Beat_ID', 'Prev_Beat_ID', 'Curr_Key', 'Flow', 'Curr0-0', 'Curr0-1', 'Curr0-2', 'Curr0-3',
                            'Curr1-0', 'Curr1-1', 'Curr1-2', 'Curr1-3',
                            'Curr2-0', 'Curr2-1', 'Curr2-2', 'Curr2-3'])

print(test_x)
print(test_x_with_prev_key)

# gnb = GaussianNB()
# gnb.fit(training_x, training_y)

# gnb_predictions = gnb.predict(test_x)
# print(score_predictions(test_x_with_prev_key, gnb_predictions, df_transitions))

svm_model = svm.SVC()
svm_model.fit(training_x, training_y)

svm_predictions = svm_model.predict(test_x)
# print(accuracy_score(test_y, svm_predictions))
print(score_predictions(test_x_with_prev_key, svm_predictions, df_transitions))
display_transitions(test_x_with_prev_key, svm_predictions)

# num_empty = 0
# columns = test_x.columns
# for index, row in test_x.iterrows():
#     empty = True
#     for column in columns:
#         if str(row[column]) != '-1' and '*' not in str(row[column]) and column != 'Side':
#             # print(column, row['Side'])
#             empty = False
#     if empty is True:
#         print(row['Side'])
#         num_empty += 1
    
# print(len(test_x['Prev0-1']))
# print(num_empty)



