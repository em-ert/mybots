import constants as c
import numpy
import pyrosim.pyrosim as pyrosim


class METRONOME_SENSOR:
    def __init__(self, name):
        self.name = name
        self.Prepare_To_Sense()

    def Get_Value(self, timestep, click):
        self.values[timestep] = click

    def Prepare_To_Sense(self):
        self.values = numpy.zeros(c.SIM_STEPS)

    def Save_Values(self):
        numpy.save("data/" + self.linkName + "_sensor_values.npy", self.values)
        print("Data saved to /data/" + self.linkName + "_sensor_values.npy")