# -*- coding: utf-8 -*-
"""
Created on Sat Apr 23 17:34:27 2022

@author: allen
"""
import pandas as pd

# Method to obtain a beat ID's key value
def find_key(beat_ID, states_dict):
    for i in range(len(states_dict)):
        if states_dict[i] == beat_ID:
            return i

print('Loading data')
# Read in the data and filter to only good flow songs
df = pd.read_csv('single_expert.csv')
df = df[df['Flow'] == True]
df = df.drop(columns=['Unnamed: 0'])

# Get unique states
print('Identifying unique beat states')
unique_states = {}
state_index = 0
complete_states = df['Beat_ID']
for state in complete_states:
    if state not in unique_states.values():
        unique_states[state_index] = state
        state_index += 1
complete_states = df['Prev_Beat_ID']
for state in complete_states:
    if state not in unique_states.values():
        unique_states[state_index] = state
        state_index += 1
        
print('Assigning keys to beat IDs')
# Add the numeric keys for each unique state
df['Prev_Key'] = [find_key(x, unique_states) for x in df['Prev_Beat_ID']]
df['Curr_Key'] = [find_key(x, unique_states) for x in df['Beat_ID']]
        
print('Building transition dictionary')
# Identify next states for each individual previous state
transition_dict = {}
for state in unique_states:
    if state not in transition_dict.keys():
        transition_dict[state] = []
    for index, row in df.iterrows():
        if row['Prev_Key'] == state and row['Curr_Key'] not in transition_dict[state]:
            transition_dict[state].append(row['Curr_Key'])

print('Removing invalid transitions')
# Identify states with no transitions and remove the entries in the main dataframe
to_remove = []
for state in transition_dict.keys():
    if len(transition_dict[state]) == 0:
        to_remove.append(state)
        df = df.drop(df[df.Prev_Key == state].index)
        df = df.drop(df[df.Curr_Key == state].index)
for state in to_remove:
    transition_dict.pop(state)

# Remove the states with no transition from the list of eligable states
for state in transition_dict.keys():
    for x in to_remove:
        if x in transition_dict[state]:
            transition_dict[state].remove(x)
            
print('Saving cleaned data')
# Build beat ID key translation table and save it
df_beat_keys = pd.DataFrame()
keys = {}
for index, row in df.iterrows():
    if row['Prev_Beat_ID'] not in keys.keys():
        keys[row['Prev_Key']] = row['Prev_Beat_ID']
    if row['Beat_ID'] not in keys.keys():
        keys[row['Curr_Key']] = row['Beat_ID']

df_beat_keys['Key'] = keys.keys()
df_beat_keys['Beat_ID'] = keys.values()
df_beat_keys.to_csv("single_expert_beat_keys.csv")

# Build beat ID key transition data and save it
df_transitions = pd.DataFrame()
prev_keys = []
next_keys = []
for prev_key in transition_dict.keys():
    for next_key in transition_dict[prev_key]:
        prev_keys.append(prev_key)
        next_keys.append(next_key)
df_transitions['Prev_Key'] = prev_keys
df_transitions['Next_Key'] = next_keys
df_transitions.to_csv('single_expert_transitions.csv')

# Save cleaned training data
df.to_csv('single_expert_cleaned.csv')

print("Total transitions: ", len(df['Beat_ID']))
print("Total unique beat states: ", len(df_beat_keys['Key']))



