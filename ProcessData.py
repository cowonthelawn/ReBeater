# -*- coding: utf-8 -*-
"""
Created on Sun Mar 13 11:24:42 2022

@author: allen
"""
from __future__ import annotations
import json
import copy
import math
import os
from pathlib import Path
import pandas as pd
import ReBeater as rb

maps_path = Path.cwd() / 'Test Maps'
directories = [x[0] for x in os.walk(maps_path) if 'Test Maps\\' in x[0] ]

df_2sides = pd.DataFrame(columns = ['Beat_ID', 'Prev_Beat_ID',
                                    'Curr0-0', 'Curr0-1', 'Curr0-2', 'Curr0-3',
                                    'Curr1-0', 'Curr1-1', 'Curr1-2', 'Curr1-3',
                                    'Curr2-0', 'Curr2-1', 'Curr2-2', 'Curr2-3',
                                    'Prev0-0', 'Prev0-1', 'Prev0-2', 'Prev0-3',
                                    'Prev1-0', 'Prev1-1', 'Prev1-2', 'Prev1-3',
                                    'Prev2-0', 'Prev2-1', 'Prev2-2', 'Prev2-3',
                                    'Flow'
                                    ])
df_single = pd.DataFrame(columns = ['Side', 'Beat_ID', 'Prev_Beat_ID',
                                    'Curr0-0', 'Curr0-1', 'Curr0-2', 'Curr0-3',
                                    'Curr1-0', 'Curr1-1', 'Curr1-2', 'Curr1-3',
                                    'Curr2-0', 'Curr2-1', 'Curr2-2', 'Curr2-3',
                                    'Prev0-0', 'Prev0-1', 'Prev0-2', 'Prev0-3',
                                    'Prev1-0', 'Prev1-1', 'Prev1-2', 'Prev1-3',
                                    'Prev2-0', 'Prev2-1', 'Prev2-2', 'Prev2-3',
                                    'Flow'
                                    ])
df_flow = pd.DataFrame(columns = ['Side', 'Direction', 'Magnitude', 'Horizontal',
                                  'Vertical', 'Start Direction', 'End Direction',
                                  'Direction Delta', 'Time', 'Flow'
                                  ])

# Traverse the directories to populate the song states in beat_states
beat_states = {}
current_Beat = 0
total_songs = 0
total_beats = 0
for directory in directories:
    if os.path.exists(directory + '//ExpertPlus.dat'):
        map_path = directory + '//ExpertPlus.dat'
    elif os.path.exists(directory + '//Expert.dat'):
        map_path = directory + '//Expert.dat'
    else:
        continue
    
    info_path = directory + '//info.dat'
    if 'bennydabeast' in directory.lower():
        flow = True
    else:
        flow = False
    
    f = open(map_path)
    beat_map = json.load(f)
    f.close()
    
    f = open(info_path)
    info = json.load(f)
    f.close()
    
    song_beat_states = {}
    for beat in beat_map['_notes']:
        if beat['_lineIndex'] > 3 or beat['_lineLayer'] > 2:
            print(directory)
            continue
                
        if (beat['_lineLayer'] == 2):
            row = 0
        elif (beat['_lineLayer'] == 0):
            row = 2
        else:
            row = beat['_lineLayer']
        curr_note = rb.Beat_Note(beat['_type'], 
                              beat['_cutDirection'], 
                              beat['_lineIndex'], 
                              row)
        
        if beat['_time'] is not current_Beat:
            current_Beat = beat['_time']
        
        if current_Beat not in song_beat_states.keys():
            if beat['_type'] <= 1:
                curr_state = rb.Beat_State()
                curr_state.add_note(curr_note)
                song_beat_states[current_Beat] = curr_state
            else:
                continue
        else:
            if beat['_type'] <= 1:
                song_beat_states[current_Beat].add_note(curr_note)
        total_beats += 1
    
    beat_states[directory] = song_beat_states
    total_songs += 1
print("Total Songs:", total_songs)
print("Total Beat States:", total_beats)
print("Average Beat States per Song:", total_beats / total_songs)
    
# Identify the total number of states and the number of unique states
total_states = 0
unique_states = []
for song in beat_states.keys():
    # print(song)
    for beat in beat_states[song].keys():
        total_states += 1
        if beat_states[song][beat].get_uid() not in unique_states:
            unique_states.append(beat_states[song][beat].get_uid())
        if beat_states[song][beat].is_empty():
            print(beat_states[song][beat].get_uid())
           
print('Total States: ', total_states)
print('Unique States: ', len(unique_states))

# Traverse the songs to populate the dataframes
prev_beat = -1
prev_beat_left = -1
prev_beat_right = -1
for song in beat_states.keys():
    for beat in beat_states[song].keys():
        if 'bennydabeast' in song:
            flow = True
        else:
            flow = False
            
        # Populate the 2sides dataframe
        curr_state = copy.deepcopy(beat_states[song][beat])
        if prev_beat < 0 or beat - prev_beat > 5:
            prev_state = copy.deepcopy(curr_state)
            prev_beat = beat
            continue
        else:
            beat_id = curr_state.get_uid()
            prev_beat_id = prev_state.get_uid()
            df_2sides = df_2sides.append({'Beat_ID': beat_id,
                                          'Prev_Beat_ID': prev_beat_id, 
                                          'Curr0-0': curr_state.beat_grid[0,0],
                                          'Curr0-1': curr_state.beat_grid[0,1],
                                          'Curr0-2': curr_state.beat_grid[0,2],
                                          'Curr0-3': curr_state.beat_grid[0,3],
                                          'Curr1-0': curr_state.beat_grid[1,0],
                                          'Curr1-1': curr_state.beat_grid[1,1],
                                          'Curr1-2': curr_state.beat_grid[1,2],
                                          'Curr1-3': curr_state.beat_grid[1,3],
                                          'Curr2-0': curr_state.beat_grid[2,0],
                                          'Curr2-1': curr_state.beat_grid[2,1],
                                          'Curr2-2': curr_state.beat_grid[2,2],
                                          'Curr2-3': curr_state.beat_grid[2,3],
                                          'Prev0-0': prev_state.beat_grid[0,0],
                                          'Prev0-1': prev_state.beat_grid[0,1],
                                          'Prev0-2': prev_state.beat_grid[0,2],
                                          'Prev0-3': prev_state.beat_grid[0,3],
                                          'Prev1-0': prev_state.beat_grid[1,0],
                                          'Prev1-1': prev_state.beat_grid[1,1],
                                          'Prev1-2': prev_state.beat_grid[1,2],
                                          'Prev1-3': prev_state.beat_grid[1,3],
                                          'Prev2-0': prev_state.beat_grid[2,0],
                                          'Prev2-1': prev_state.beat_grid[2,1],
                                          'Prev2-2': prev_state.beat_grid[2,2],
                                          'Prev2-3': prev_state.beat_grid[2,3],
                                          'Flow': flow
                                          }, ignore_index=True)
        
        # Populate a state that only has left blocks
        if rb.get_block(curr_state, rb.Sides.LEFT).direction != -1:
            curr_state_left = copy.deepcopy(curr_state)
            # Clear any blocks that aren't on the left side
            for y in range(3):
                for x in range(4):
                    if curr_state_left.beat_grid[y,x] > 8:
                        curr_state_left.beat_grid[y,x] = -1
            if curr_state_left.is_empty():
                print(curr_state.get_uid(), 'LEFT ' + str(beat))
            # Identify first block in a song
            if prev_beat_left < 0 or beat - prev_beat_left > 10:
                # Don't populate first block as it has no previous state
                prev_state_left = copy.deepcopy(curr_state_left)
                prev_beat_left = beat
                prev_block_left = rb.get_block(curr_state, rb.Sides.LEFT)
                continue
            else:
                # Populate previous and current state
                beat_id = curr_state_left.get_uid()
                prev_beat_id = prev_state_left.get_uid()
                side = rb.Sides.LEFT
                df_single = df_single.append({'Side': side,
                                              'Beat_ID': beat_id,
                                              'Prev_Beat_ID': prev_beat_id, 
                                              'Curr0-0': curr_state_left.beat_grid[0,0],
                                              'Curr0-1': curr_state_left.beat_grid[0,1],
                                              'Curr0-2': curr_state_left.beat_grid[0,2],
                                              'Curr0-3': curr_state_left.beat_grid[0,3],
                                              'Curr1-0': curr_state_left.beat_grid[1,0],
                                              'Curr1-1': curr_state_left.beat_grid[1,1],
                                              'Curr1-2': curr_state_left.beat_grid[1,2],
                                              'Curr1-3': curr_state_left.beat_grid[1,3],
                                              'Curr2-0': curr_state_left.beat_grid[2,0],
                                              'Curr2-1': curr_state_left.beat_grid[2,1],
                                              'Curr2-2': curr_state_left.beat_grid[2,2],
                                              'Curr2-3': curr_state_left.beat_grid[2,3],
                                              'Prev0-0': prev_state_left.beat_grid[0,0],
                                              'Prev0-1': prev_state_left.beat_grid[0,1],
                                              'Prev0-2': prev_state_left.beat_grid[0,2],
                                              'Prev0-3': prev_state_left.beat_grid[0,3],
                                              'Prev1-0': prev_state_left.beat_grid[1,0],
                                              'Prev1-1': prev_state_left.beat_grid[1,1],
                                              'Prev1-2': prev_state_left.beat_grid[1,2],
                                              'Prev1-3': prev_state_left.beat_grid[1,3],
                                              'Prev2-0': prev_state_left.beat_grid[2,0],
                                              'Prev2-1': prev_state_left.beat_grid[2,1],
                                              'Prev2-2': prev_state_left.beat_grid[2,2],
                                              'Prev2-3': prev_state_left.beat_grid[2,3],
                                              'Flow': flow
                                          }, ignore_index=True)
            
                # Populate the flow data
                curr_block = rb.get_block(curr_state, rb.Sides.LEFT)
                bpm = info['_beatsPerMinute']
                time = (beat / bpm - prev_beat_left / bpm) * 60
                side = rb.Sides.LEFT
                start_direction = rb.get_angle(prev_block_left.direction)
                end_direction = rb.get_angle(curr_block.direction)
                direction_delta = start_direction - end_direction
                horizontal = curr_block.x - prev_block_left.x
                vertical = curr_block.y - prev_block_left.y
                magnitude = math.sqrt(horizontal**2 + vertical**2)
                if (horizontal != 0):
                    direction = math.atan(vertical / horizontal)
                    if (horizontal > 0 and vertical > 0) or (horizontal < 0 and vertical < 0):
                        direction += 180
                elif (vertical > 0):
                    direction = 0
                elif (vertical < 0):
                    direction = 180
                else:
                    direction = 0
                
                df_flow = df_flow.append({'Side': side,
                                          'Direction': direction, 
                                          'Magnitude': magnitude,
                                          'Horizontal': horizontal, 
                                          'Vertical': vertical,
                                          'Start Direction': start_direction, 
                                          'End Direction': end_direction, 
                                          'Direction Delta': direction_delta, 
                                          'Time': time,
                                          'Flow': flow
                                          }, ignore_index=True)
                
        # Populate a state that only has right blocks
        if rb.get_block(curr_state, rb.Sides.RIGHT).direction != -1:
            curr_state_right = copy.deepcopy(curr_state)
            # Clear any blocks that aren't on the right side
            for y in range(3):
                for x in range(4):
                    if curr_state_right.beat_grid[y,x] < 9:
                        curr_state_right.beat_grid[y,x] = -1
            if curr_state_right.is_empty():
                print(curr_state.get_uid(), 'RIGHT ' + str(beat))
            # Identify first block in a song
            if prev_beat_right < 0 or beat - prev_beat_right > 10:
                # Don't populate first block as it has no previous state
                prev_state_right = copy.deepcopy(curr_state_right)
                prev_beat_right = beat
                prev_block_right = rb.get_block(curr_state, rb.Sides.RIGHT)
                continue
            else:
                # Populate previous and current state
                beat_id = curr_state_right.get_uid()
                prev_beat_id = prev_state_right.get_uid()
                side = rb.Sides.RIGHT
                df_single = df_single.append({'Side': side,
                                              'Beat_ID': beat_id,
                                              'Prev_Beat_ID': prev_beat_id, 
                                              'Curr0-0': curr_state_right.beat_grid[0,0],
                                              'Curr0-1': curr_state_right.beat_grid[0,1],
                                              'Curr0-2': curr_state_right.beat_grid[0,2],
                                              'Curr0-3': curr_state_right.beat_grid[0,3],
                                              'Curr1-0': curr_state_right.beat_grid[1,0],
                                              'Curr1-1': curr_state_right.beat_grid[1,1],
                                              'Curr1-2': curr_state_right.beat_grid[1,2],
                                              'Curr1-3': curr_state_right.beat_grid[1,3],
                                              'Curr2-0': curr_state_right.beat_grid[2,0],
                                              'Curr2-1': curr_state_right.beat_grid[2,1],
                                              'Curr2-2': curr_state_right.beat_grid[2,2],
                                              'Curr2-3': curr_state_right.beat_grid[2,3],
                                              'Prev0-0': prev_state_right.beat_grid[0,0],
                                              'Prev0-1': prev_state_right.beat_grid[0,1],
                                              'Prev0-2': prev_state_right.beat_grid[0,2],
                                              'Prev0-3': prev_state_right.beat_grid[0,3],
                                              'Prev1-0': prev_state_right.beat_grid[1,0],
                                              'Prev1-1': prev_state_right.beat_grid[1,1],
                                              'Prev1-2': prev_state_right.beat_grid[1,2],
                                              'Prev1-3': prev_state_right.beat_grid[1,3],
                                              'Prev2-0': prev_state_right.beat_grid[2,0],
                                              'Prev2-1': prev_state_right.beat_grid[2,1],
                                              'Prev2-2': prev_state_right.beat_grid[2,2],
                                              'Prev2-3': prev_state_right.beat_grid[2,3],
                                              'Flow': flow
                                          }, ignore_index=True)

                # Populate the flow data
                curr_block = rb.get_block(curr_state, rb.Sides.RIGHT)
                bpm = info['_beatsPerMinute']
                time = (beat / bpm - prev_beat_right / bpm) * 60
                side = rb.Sides.RIGHT
                start_direction = rb.get_angle(prev_block_right.direction)
                end_direction = rb.get_angle(curr_block.direction)
                direction_delta = start_direction - end_direction
                horizontal = curr_block.x - prev_block_right.x
                vertical = curr_block.y - prev_block_right.y
                magnitude = math.sqrt(horizontal**2 + vertical**2)
                if (horizontal != 0):
                    direction = math.atan(vertical / horizontal)
                    if (horizontal > 0 and vertical > 0) or (horizontal < 0 and vertical < 0):
                        direction += 180
                elif (vertical > 0):
                    direction = 0
                elif (vertical < 0):
                    direction = 180
                else:
                    direction = 0
                
                df_flow = df_flow.append({'Side': side,
                                          'Direction': direction, 
                                          'Magnitude': magnitude,
                                          'Horizontal': horizontal, 
                                          'Vertical': vertical,
                                          'Start Direction': start_direction, 
                                          'End Direction': end_direction, 
                                          'Direction Delta': direction_delta, 
                                          'Time': time,
                                          'Flow': flow
                                          }, ignore_index=True)                
                
    # Reset previous state variables to prepare for next song
    prev_beat = -1
    prev_beat_left = -1
    prev_beat_right = -1
                
    print(song, "completed!")

df_2sides.to_csv(Path.cwd() / '2sides_expert.csv')
df_single.to_csv(Path.cwd() / 'single_expert.csv')
df_flow.to_csv(Path.cwd() / 'flow_expert.csv')
        
        
# # print (json.dumps(info, ensure_ascii=False, indent=4))


