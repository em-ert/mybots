# All code marked with "from Repeated_Timer" is from the python-repeated-timer library, which can be be accessed at https://github.com/takhyun12/python-repeated-timer/tree/main
# This library can be installed with the command: pip install python-repeated-timer
# Copyright (c) 2021-2025 Tackhyun Jung and Jongsung Yoon.

# The rest of the code was written by Emily Ertle but is based on the Metronome object within music.py in the jythonMusic library, which can be accessed at https://github.com/manaris/jythonMusic/blob/21dd2f5297552f15510361b93a7d288739f42c6c/library/music.py#L2837

import constants as c
import synthesizer
from threading import Thread
from time import sleep
from typing import Callable
from repeatedTimer import REPEATED_TIMER

class METRONOME:
    def __init__(self, stepFunction: Callable, tempo=120, timeSignature=[4,4], realtime=False):
        self.stepFunction = stepFunction
        self.tempo = tempo
        self.timeSignature = timeSignature
        self.realtime = realtime

        # Lists working in parallel - 1 index for each function to call
        self.functions        = []      
        self.parameters       = [] 
        self.desiredBeats     = []      # What beat to call fn on (0 means now)
        self.repeatFlags      = []      # Whether calls are repeated
        self.beatCountdowns   = []      # Steps until needs to be called

        # TODO: Create timer for non-discrete runs
        self.currentBeat = 1
        self.timer = None
        self.running = False

        if self.realtime:
            self.sonify = True
        else:
            self.sonify = False
        
        self.pitchStrong = "E5"
        self.pitchStandard = "F5"
        self.volume = 100

        self.synth = synthesizer.Create_Synth()
        
    
    def Start(self, interval, duration):
        self.timer = REPEATED_TIMER(interval=interval, duration=duration, function=self.Control)
        self.intervalBeatRatio = (60/self.tempo)/c.FRAME_RATE
        self.timer.start()


    def Control(self, numTicks):
        self.numTicks = numTicks
        if numTicks % self.intervalBeatRatio == 0:
            self.__Call_Functions()
            self.stepFunction(numTicks, 1)
        else:
            self.stepFunction(numTicks, -1)


    def Stop(self):
        self.timer.stop()


    def Set_Realtime(self, isRealtime):
        if isRealtime:
            self.realtime = True
        else:
            self.realtime = False


    def Add(self, function, parameters=[], desiredBeat=0, repeatFlag=False):
        """
        Adds call to a desired function to a metronome-based scheduler.
        For desiredBeat:
            0: Now regardless of current beat
            1 to max in time signature: called every measure on indicated beat
            Numbers > max in t.s.: allows for calls every 2+ measures on a specific beat
        """

        # Add all parameters @ same index in parallel lists
        self.functions.append(function)
        self.parameters.append(parameters)
        self.desiredBeats.append(desiredBeat)
        self.repeatFlags.append(repeatFlag)
        
        # calculate beat countdown
        beatCountdown = self.__Calculate_Countdown(desiredBeat)              
            
        # store beat countdown for this function
        self.beatCountdowns.append(beatCountdown)


    def Remove(self, function):
        # Removes function from list. If more than one has this name, the first is removed. If such a function does not exist, an exception is thrown.
        index = self.functions.index(function)  # Finds earliest if multiple
        self.functions.pop(index)
        self.parameters.pop(index)
        self.desiredBeats.pop(index)
        self.repeatFlags.pop(index)
        self.beatCountdowns.pop(index)


    def Remove_All(self):
        # All functions removed

        self.functions        = []    
        self.parameters       = []  
        self.desiredBeats     = []   
        self.repeatFlags      = []  
        self.beatCountdowns   = []   


    def Set_Tempo(self, tempo):

        self.tempo = tempo


    def Get_Tempo(self):

        return self.tempo
    

    def Set_Time_Signature(self, timeSignature):  

        self.timeSignature = timeSignature
        self.currentBeat = 0


    def Get_Time_Signature(self):

        return self.timeSignature

    
    def __Call_Functions(self):

        if self.sonify:
            if self.currentBeat == 1:
                self.synth.play_note(self.pitchStrong)
            else:
                self.synth.play_note(self.pitchStandard)

        nonRepeatedFunctions = []   # Non-repeated function indices held here for easy removal after functionexecution
        for i in range(len(self.functions)):
        
            # Check if function at index i should be called immediately
            if self.beatCountdowns[i] == 0:
                self.functions[i](*(self.parameters[i]))
                

            # If function is non-repeated, add to non-repeated list
            if not self.repeatFlags[i]:
                nonRepeatedFunctions.append(i)
        
        # Remove all executed non-repeated functions from the list
        for i in nonRepeatedFunctions:
            self.functions.pop(i)   
            self.parameters.pop(i) 
            self.desiredBeats.pop(i) 
            self.repeatFlags.pop(i) 
            self.beatCountdowns.pop(i)

        # Advance metronome by one beat
        self.currentBeat = (self.currentBeat % self.timeSignature[0]) + 1

        # Update beat countdowns for all functions
        for i in range(len(self.functions)):
            
            # If function was just called, recalculate countdowns
            if self.beatCountdowns[i] == 0:
                self.beatCountdowns[i] = self.__calculateCountdown(self.desiredBeats[i])              

            # If some waiting must still be done, update coundowns
            else:
                self.beatCountdowns[i] = self.beatCountdowns[i] - 1


    def __Calculate_Countdown(self, desiredBeat):   
    
        # Call now regardless of beat
        if desiredBeat == 0:
            beatCountdown = 0 
        
        # If beat has not occurred yet within current measure
        elif self.currentBeat <= desiredBeat <= self.timeSignature[0]:
            beatCountdown = desiredBeat - self.currentBeat

        # If beat already passed in the current measure
        elif 1 <= desiredBeat < self.currentBeat:
            beatCountdown = (desiredBeat + self.timeSignature[0]) - self.currentBeat

        # If beat is greater than the length of a measure, meaning the function may occur every 2+ measures - ex: beat "7" in 4/4 = beat 3 every other measure
        elif self.timeSignature[0] < desiredBeat:
            beatCountdown = desiredBeat - self.currentBeat + self.timeSignature[0]
        else:  # we cannot handle negative beats
            raise ValueError("Beat value '" + desiredBeat + "' is invalid.")
            
        return beatCountdown

