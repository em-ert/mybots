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
        #REVIEW - [2] Edit fitness function here

        if c.FIT_FUNCTION == "COS":
            # Increment subdivision with each step
            self.subdivision += 1
            # Click if number of subdivision reaches limit
            if self.framesPerBeat - self.subdivision < 0:
                self.__Click()
                return [self.CLICK, self.framesPerBeat, self.subdivision]
            else: 
                return [self.NO_CLICK, self.framesPerBeat, self.subdivision]


        if c.FIT_FUNCTION == "BIN":
            # Increment subdivision with each step
            self.subdivision += 1
            # Click if number of subdivision reaches limit
            if self.framesPerBeat - self.subdivision < 0:
                self.__Click()
                return [self.CLICK, self.framesPerBeat, self.subdivision]
            else: 
                return [self.NO_CLICK, self.framesPerBeat, self.framesPerBeat/self.subdivision]    
        

        if c.FIT_FUNCTION == "EXP":
            # Increment subdivision with each step
            self.subdivision += 1
            # Click if number of subdivision reaches limit
            if self.framesPerBeat - self.subdivision < 0:
                self.__Click()
                return [self.CLICK, self.framesPerBeat, 0]
            
            # Return distance from click if <= 2 from click on either end
            elif self.subdivision <= 2:
                return [self.NO_CLICK, self.framesPerBeat, self.subdivision]
            
            elif self.framesPerBeat - self.subdivision <= 2:
                return [self.NO_CLICK, self.framesPerBeat, self.framesPerBeat - self.subdivision]
            
            # Otherwise return -1 for distance from click
            else: 
                return [self.NO_CLICK, self.framesPerBeat, -1]
            
        
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

          
    def Reset(self, tempo, timeSignature=[4,4]):
        self.tempo = tempo
        self.timeSignature = timeSignature
        self.framesPerBeat = (60/self.tempo)/c.FRAME_RATE
        # Maximize these so all simulations begin with a click
        self.beat = self.timeSignature[0]
        self.subdivision = self.framesPerBeat + 1

        # Garbage collection / reset for sound if sonify is true
        if self.sonify:
            del self.click
            del self.clickLow
            self.click = media("sounds/metronome.mp3", streaming=False)
            self.clickLow = media("sounds/metronome_low.mp3", streaming=False)