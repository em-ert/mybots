#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 11 21:22:00 2024

@author: eertle
"""
import math
import numpy as np
import time
from numba import jit

SIM_STEPS = 50
C_TEMPOS = np.array([220, 180, 200])
FRAME_RATE = 0.0250
C_FRAMES_PER_BEAT = np.array([math.ceil((60/tempo)/FRAME_RATE) for tempo in C_TEMPOS])
C_CLICKS_PER_TEMPO : int = math.ceil(SIM_STEPS/min(C_FRAMES_PER_BEAT))
C_FRAMES_PER_TEMPO = np.array([numFrames * C_CLICKS_PER_TEMPO for numFrames in C_FRAMES_PER_BEAT])

print(C_FRAMES_PER_BEAT)
print(C_CLICKS_PER_TEMPO)
print(C_FRAMES_PER_TEMPO)

@jit
def func(FRAMES_PER_BEAT, CLICKS_PER_TEMPO, FRAMES_PER_TEMPO, TEMPOS):
    steps = np.zeros(sum(FRAMES_PER_TEMPO))
    
    curr = 0
    for i in range(3):
        for j in range(CLICKS_PER_TEMPO):
            steps[curr] = 1
            curr += FRAMES_PER_BEAT[i]
      
            
    fitness = 0
    frameStartIndex = 0     
    for i in range(TEMPOS.size):
        framesPerBeat = FRAMES_PER_BEAT[i]
        
        currentTempoData = steps[frameStartIndex : frameStartIndex + FRAMES_PER_TEMPO[i]]
        currentTempoData = np.reshape(currentTempoData, (CLICKS_PER_TEMPO, framesPerBeat))
        pointsArray = np.linspace(0, framesPerBeat, framesPerBeat + 1)
        pointsArray = pointsArray[0: framesPerBeat]
        # Generate the sine wave 
        pointsArray = framesPerBeat * np.cos(((2*np.pi)/framesPerBeat) * pointsArray)
        currentTempoData = np.multiply(currentTempoData, pointsArray)
        currentTempoData = currentTempoData.flatten()
        
        # Iterate through the arrays to find points values
        remaining = FRAMES_PER_TEMPO[i]
        startIndex = 0
        fitness += np.max(currentTempoData[startIndex : math.ceil(framesPerBeat/2)])
        startIndex = math.ceil(framesPerBeat/2)
        remaining -= (startIndex - 1)
        while remaining > 0:
            if remaining < framesPerBeat:
                fitness += np.max(currentTempoData[startIndex : startIndex + remaining])
            else:
                fitness += np.max(currentTempoData[startIndex : startIndex + framesPerBeat])
            startIndex += framesPerBeat
            remaining -= framesPerBeat
            
            
         
start = time.time()
func(C_FRAMES_PER_BEAT, C_CLICKS_PER_TEMPO, C_FRAMES_PER_TEMPO, C_TEMPOS)
end = time.time()
print(f"First: {end - start}")

start = time.time()
func(C_FRAMES_PER_BEAT, C_CLICKS_PER_TEMPO, C_FRAMES_PER_TEMPO, C_TEMPOS)
end = time.time()
print(f"Second: {end - start}")

start = time.time()
func(C_FRAMES_PER_BEAT, C_CLICKS_PER_TEMPO, C_FRAMES_PER_TEMPO, C_TEMPOS)
end = time.time()
print(f"Third: {end - start}")
            
        
        
    
    
    
    
