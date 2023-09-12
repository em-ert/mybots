import constants as c
import numpy as np
import pyrosim.pyrosim as pyrosim


class SENSOR:
    def __init__(self, linkName, name):
        self.linkName = linkName
        self.name = name
        self.Prepare_To_Sense()
        self.numSteps = 0

    def Get_Value(self, timestep):
        self.values[timestep] = pyrosim.Get_Touch_Sensor_Value_For_Link(self.linkName)

    def Get_Step(self, timestep):
        if self.values[timestep] > self.values[timestep - 1]:
            self.numSteps += 1
            return 1
        else:
            return 0

    def Prepare_To_Sense(self):
        self.values = np.zeros(c.SIM_STEPS * len(c.TEMPOS))

    def Save_Values(self, path):
        fullPath = path + "data/" + self.linkName + "_sensor_values.npy"
        np.save(fullPath, self.values)
        print("Data saved to " + fullPath)