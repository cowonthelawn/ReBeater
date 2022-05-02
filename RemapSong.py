# -*- coding: utf-8 -*-
"""
Created on Sun Mar 13 11:24:42 2022

@author: allen
"""
from __future__ import annotations
from pathlib import Path
import json
import ReBeater as rb

# Open the beat map files
f = open(Path.cwd() / 'Test Song' / 'HardStandard.dat')
beat_map = json.load(f)
f.close()

f = open(Path.cwd() / 'Test Song' / 'info.dat')
info = json.load(f)
f.close()

# Get a list of times notes are present on the map
beat_states = []
for beat in beat_map['_notes']:            
    if beat['_time'] not in beat_states:
        beat_states.append(beat['_time'])

# Walk the Markov chain and get a list of Beat_States
steps = len(beat_states)
walk = rb.random_walk(steps)

# Modify the beat map meta data
info['_levelAuthorName'] = 'ReBeater'
info['_difficultyBeatmapSets'][0]['_beatmapCharacteristicName'] = 'OneSaber'

# Remove all obstacles and notes from the beat map
beat_map['_notes'] = []
beat_map['_obstacles'] = []

# Repopulate the beat map notes with the results of walking the Markov chain
for index in range(len(walk)):
    for note in walk[index].beat_notes:
        new_note = {}
        new_note['_time'] = beat_states[index]
        new_note['_lineIndex'] = note.x
        new_note['_lineLayer'] = note.y
        new_note['_type'] = 1
        new_note['_cutDirection'] = note.direction
        beat_map['_notes'].append(new_note)
                
# Write the re-mapped files
map_path =  Path.cwd() / 'Test Song' / 'ReBeated' / 'HardStandard.dat'
info_path = Path.cwd() / 'Test Song' / 'ReBeated' / 'info.dat'
with open(map_path, "w") as write_file:
    json.dump(beat_map, write_file)
with open(info_path, "w") as write_file:
    json.dump(info, write_file)
    


