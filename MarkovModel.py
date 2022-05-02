# -*- coding: utf-8 -*-
"""
Created on Sat Apr 23 17:34:27 2022

@author: allen
"""
import pandas as pd
import numpy as np
import statistics as st
from datetime import datetime

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

# Build the state indexes for keys in the Markov Chain
states = {}
unique_keys = df_keys['Key'].to_list()
num_keys = len(df_keys['Key'])
for i in range(num_keys):
    states[i] = unique_keys[i]
print()
print('States:')
print(states)

# Reverse states dictionary it for quick access to the key from the state
keys = {}
for state in states.keys():
    keys[states[state]] = state
print()
print('Keys:')
print(keys)

# Create empty probability dictionary
probabilities = {}
total_transitions = {}
for index, row in df_main.iterrows():
    prev_key = row['Prev_Key']
    next_key = row['Curr_Key']
    
    if prev_key not in total_transitions.keys():
        total_transitions[prev_key] = 1
    else:
        total_transitions[prev_key] += 1
        
    if prev_key not in probabilities.keys():
        probabilities[prev_key] = {}
        probabilities[prev_key][next_key] = 1
    elif next_key not in probabilities[prev_key].keys():
        probabilities[prev_key][next_key] = 1
    else:
        probabilities[prev_key][next_key] += 1

print()
print("Total Transitions:")
print(total_transitions)

# Populate the actual percentage per transition
for prev_key in unique_keys:
    if prev_key not in probabilities.keys():
        probabilities[prev_key] = {}
    for next_key in unique_keys:
        if next_key not in probabilities[prev_key].keys():
            probabilities[prev_key][next_key] = 0
        else:
            probabilities[prev_key][next_key] /= total_transitions[prev_key]
            
print()
print('Probabilities:')
print(probabilities)

transition_matrix = np.zeros((num_keys, num_keys))
for prev_key in probabilities.keys():
    for next_key in probabilities[prev_key].keys():
        prev_state = keys[prev_key]
        next_state = keys[next_key]
        transition_matrix[prev_state, next_state] = probabilities[prev_key][next_key]

print()
print('Transition Matrix:')
print(transition_matrix)

print()
print('Beginning random walk')
# Average number of states per song is around 824
start_time = datetime.now()
n = 824
start_state = 0
print(states[start_state], '--->', end=' ')
prev_state = start_state

while n > 0:
    curr_state = np.random.choice(range(num_keys), p=transition_matrix[prev_state])
    print(states[curr_state], '--->', end= ' ')
    prev_state = curr_state
    n -= 1
print('stop')
print("Walk generation time: " + str((datetime.now() - start_time).microseconds / 1000) + 'ms')

print()
print('Calculating stationary distribution')
steps = 10**3
A_n = transition_matrix
i = 0
while i < steps:
    A_n = np.matmul(A_n, transition_matrix)
    i += 1

total_states = 0
used_states = 0
print(A_n[0])
for state in A_n[0]:
    if state > 0:
        used_states += 1
    total_states += 1
print("Number of total states:", total_states)
print("Number of used states:", used_states)
print("Mean percentage per state:", st.mean(A_n[0]))
print("Max percentage:", max(A_n[0]))
print("Min percentage:", min([percent for percent in A_n[0] if percent > 0]))
print("Standard Deviation: ", st.stdev(A_n[0]))
# The average number of states per song is around 824
# The lowest percentage likely to get seen in a song is 1/824 or around .1%
print("States likely to get placed in a song:", len([percent for percent in A_n[0] if percent >= .001]))
        






    
    