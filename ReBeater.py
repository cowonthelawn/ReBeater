# -*- coding: utf-8 -*-
"""
Created on Fri Apr 22 15:12:32 2022

@author: allen
"""

import numpy as np
import pandas as pd
import copy


UID_ARRAY = np.array([[0, 1, 2, 3, 4, 5, 6, 7, 8],
                      [9,10,11,12,13,14,15,16,17]])
        
class Sides:
    LEFT = 0
    RIGHT = 1

class Directions:
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3
    UP_LEFT = 4
    UP_RIGHT = 5
    DOWN_LEFT = 6
    DOWN_RIGHT = 7
    ANY = 8
    
def get_block(state, side):
    # Get only blocks for one side
    blocks = [note for note in state.beat_notes if note.side == side]
    if len(blocks) > 0:
        x_list = [block.x for block in blocks]
        y_list = [block.y for block in blocks]
        direction = blocks[0].direction
        # Select the block location at the start of a swing
        if direction == Directions.UP:
            y = min(y_list)
            x = min(x_list)
        elif direction == Directions.DOWN:
            y = max(y_list)
            x = max(x_list)
        elif direction == Directions.LEFT:
            y = max(y_list)
            x = min(x_list)
        elif direction == Directions.RIGHT:
            y = max(y_list)
            x = max(x_list)
        elif direction == Directions.UP_LEFT:
            y = min(y_list)
            x = max(x_list)
        elif direction == Directions.UP_RIGHT:
            y = min(y_list)
            x = min(x_list)
        elif direction == Directions.DOWN_LEFT:
            y = max(y_list)
            x = min(x_list)
        elif direction == Directions.DOWN_RIGHT:
            y = max(y_list)
            x = max(x_list)
        else:
            y = blocks[0].y
            x = blocks[0].x
    else:
        note = Beat_Note(-1, -1, -1, -1)
        return note
        
    note = Beat_Note(side, direction, x, y)
    return note

def get_angle(direction):
    if direction == Directions.UP:
        return 0
    elif direction == Directions.DOWN:
        return 180
    elif direction == Directions.LEFT:
        return 270
    elif direction == Directions.RIGHT:
        return 90
    elif direction == Directions.UP_LEFT:
        return 315
    elif direction == Directions.UP_RIGHT:
        return 45
    elif direction == Directions.DOWN_LEFT:
        return 225
    elif direction == Directions.DOWN_RIGHT:
        return 135
    else:
        return -1
        

class Beat_Note:    
    def __init__(self, side=0, direction=0, x=0, y=0):
        self.side = side
        self.direction = direction
        if self.direction > 8:
            self.direction -= 8
        self.x = x
        self.y = y
        
    def to_string(self):
# =============================================================================
#         result = { 
#             str(self.side),
#             str(self.direction),
#             str(self.x),
#             str(self.y)
#             }
#         return ':'.join(result)
# =============================================================================
        return str(self.x) + ':' + str(self.y)
    
    def get_uid(self):
        if self.side <= 1:
            return UID_ARRAY[self.side,self.direction]
        else:
            return -1
    
class Beat_State:  
    def __init__(self):
        self.beat_notes = []
        self.beat_grid = np.array([[-1, -1, -1, -1],
                                   [-1, -1, -1, -1],
                                   [-1, -1, -1, -1]])
        
    def add_note(self, note):
        self.beat_notes.append(note)
        # print('y: ' + str(note.y) + ' x: ' + str(note.x) + ' direction: ' + str(note.direction))
        self.beat_grid[note.y, note.x] = note.get_uid()
        
    def to_string(self):
        result = []
        for note in self.beat_notes:
            result.append(note.to_string())
        return result
    
    def get_uid(self):
        uid = '*'
        for y in range(3):
            for x in range(4):
                if self.beat_grid[y,x] >= 0:
                    uid += '+'
                uid += str(self.beat_grid[y,x])
        uid += '*'
        return uid
    
    def equals(self, state):
        return self.beat_grid == state.beat_grid
    
    def is_empty(self):
        empty = True
        for y in range(3):
            for x in range(4):
                if self.beat_grid[y,x] != -1:
                    empty = False
                    break
        return empty
    
    def from_UID(self, uid):
        self.beat_notes = []
        self.beat_grid = np.array([[-1, -1, -1, -1],
                                   [-1, -1, -1, -1],
                                   [-1, -1, -1, -1]])
        
        uid = str(uid).replace('*', '')
        index = 0
        start_index = 0
        end_index = 0
        num_found = 0
        found_start = False
        found_end = False
        while index < len(uid):
            if uid[index] == '-' or uid[index] == '+' or index == len(uid) - 1:
                if found_start:
                    found_end = True
                    end_index = index
                else:   
                    found_start = True
                    start_index = index
                    index += 1
                    continue
            if found_start and found_end:
                num_found += 1
                if end_index == len(uid) - 1:
                    note_string = uid[start_index:]
                else:
                    note_string = uid[start_index:end_index]
                note_num = int(note_string)
                if note_num >= 0:
                    side = Sides.RIGHT
                    if (note_num <= 8):
                        direction = note_num
                    else:
                        note_num -= 9
                        direction = note_num
                    if num_found <= 4:
                        y = 0
                        x = num_found - 1
                    elif num_found <= 8:
                        y = 1
                        x = num_found - 5
                    else:
                        y = 2
                        x = num_found - 9
                    note = Beat_Note(side, direction, x, y)
                    self.add_note(note)
                    # print('note_added!')
                found_start = False
                found_end = False
                continue
            else:
                index += 1
                continue
        return copy.deepcopy(self)

def random_walk(steps):
    # Read in the data and filter to only good flow songs
    df_main = pd.read_csv('single_expert_cleaned.csv')
    df_main = df_main[df_main['Flow'] == True]
    df_main = df_main.drop(columns=['Unnamed: 0'])
    
    df_keys = pd.read_csv('single_expert_beat_keys.csv')
    
    # Build the dictionary to store the key to Beat_ID table
    beat_IDs = {}
    for index, row in df_keys.iterrows():
        beat_IDs[row['Key']] = row['Beat_ID']
    
    # Build the state indexes for keys in the Markov Chain
    states = {}
    unique_keys = df_keys['Key'].to_list()
    num_keys = len(df_keys['Key'])
    for i in range(num_keys):
        states[i] = unique_keys[i]
    
    # Reverse states dictionary it for quick access to the key from the state
    keys = {}
    for state in states.keys():
        keys[states[state]] = state
    
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
    
    # Populate the actual percentage per transition
    for prev_key in unique_keys:
        if prev_key not in probabilities.keys():
            probabilities[prev_key] = {}
        for next_key in unique_keys:
            if next_key not in probabilities[prev_key].keys():
                probabilities[prev_key][next_key] = 0
            else:
                probabilities[prev_key][next_key] /= total_transitions[prev_key]
    
    transition_matrix = np.zeros((num_keys, num_keys))
    for prev_key in probabilities.keys():
        for next_key in probabilities[prev_key].keys():
            prev_state = keys[prev_key]
            next_state = keys[next_key]
            transition_matrix[prev_state, next_state] = probabilities[prev_key][next_key]
    
    start_state = 0
    prev_state = start_state
    result = []
    
    while steps > 0:
        curr_state = np.random.choice(range(num_keys), p=transition_matrix[prev_state])
        uid = beat_IDs[states[curr_state]].replace('*', '')
        # print('uid:', uid)
        beat_state = Beat_State().from_UID(uid)
        result.append(beat_state)
        prev_state = curr_state
        steps -= 1
        
    return result