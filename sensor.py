import constants as c
import numpy
import pyrosim.pyrosim as pyrosim


class SENSOR:
    def __init__(self, linkName):
        self.linkName = linkName
        self.Prepare_To_Sense()

    def Get_Value(self, timestep):
        self.values[timestep] = pyrosim.Get_Touch_Sensor_Value_For_Link(self.linkName)

    def Prepare_To_Sense(self):
        self.values = numpy.zeros(c.SIM_STEPS)

    def Save_Values(self):
        numpy.save("data/" + self.linkName + "_sensor_values.npy", self.values)
        print("Data saved to /data/" + self.linkName + "_sensor_values.npy")