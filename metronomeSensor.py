import constants as c
import numpy as np
import pyrosim.pyrosim as pyrosim


class METRONOME_SENSOR:
    def __init__(self, name):
        self.name = name
        self.Prepare_To_Sense()

    def Get_Value(self, timestep, click):
        self.values[timestep] = click

    def Prepare_To_Sense(self):
        self.values = np.zeros(sum(c.FRAMES_PER_TEMPO))

    def Save_Values(self, path):
        fullPath = path + "data/metronome_sensor_values.npy"
        np.save(fullPath, self.values)
        print("Data saved to " + fullPath)