import constants as c
import numpy
import pyrosim.pyrosim as pyrosim


class SENSOR:
    def __init__(self, linkName, name):
        self.linkName = linkName
        self.name = name
        self.Prepare_To_Sense()
        self.currValue = 0

    def Get_Value(self, timestep):
        self.values[timestep] = pyrosim.Get_Touch_Sensor_Value_For_Link(self.linkName)
        self.currValue = self.values[timestep]

    def Prepare_To_Sense(self):
        self.values = numpy.zeros(c.SIM_STEPS)

    def Save_Values(self):
        numpy.save("data/" + self.linkName + "_sensor_values.npy", self.values)
        print("Data saved to /data/" + self.linkName + "_sensor_values.npy")