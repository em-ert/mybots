import constants as c
import numpy as np
from pyglet.resource import media
import pyrosim.pyrosim as pyrosim


class METRONOME:
    def __init__(self, tempo=120, timeSignature=[4,4], sonify=False):
        self.tempo = tempo
        self.timeSignature = timeSignature

        self.beat = 0
        self.subdivision = 0
        self.framesPerBeat = (60/self.tempo)/c.FRAME_RATE
        self.sonify = sonify

        if self.sonify:
            self.click = media("sounds/metronome.mp3", streaming=False)
            self.clickLow = media("sounds/metronome_low.mp3", streaming=False)

        
        self.CLICK = 1
        self.NO_CLICK = 0
    
    
    def StepFunction(self):
        # Increment subdivision with each step
        self.subdivision += 1
        # Click if number of subdivision reaches limit
        if self.framesPerBeat - self.subdivision < 0:
            self.__Click()
            return [self.CLICK, self.framesPerBeat]
        else: 
            return [self.NO_CLICK, self.framesPerBeat]
        
        
    def __Click(self):
        # Reset subdivision count
        self.subdivision = 1
        # If on last beat, wrap around to 1
        if self.beat == self.timeSignature[0]:
            self.beat = 1
        else:
            self.beat += 1
        # If a sound should be made, make it    
        if self.sonify:
            if self.beat == 1:
                self.click.play()
            else:
                self.clickLow.play()

          
    def Reset(self, tempo, timesignature=[4,4]):
        self.beat = 1
        self.subdivision = 1
        self.tempo = tempo
        self.timesignature = timesignature
        self.framesPerBeat = (60/self.tempo)/c.FRAME_RATE