import constants as c
import pybullet as p
import pyrosim.pyrosim as pyrosim
from sensor import SENSOR
from motor import MOTOR


class ROBOT:
    def __init__(self):
        self.robotId = p.loadURDF("body.urdf")
        self.motors = {}
        self.sensors = {}

        pyrosim.Prepare_To_Simulate(self.robotId)
        self.Prepare_To_Sense()
        self.Prepare_To_Act()

    def Prepare_To_Sense(self):
        self.sensors = {}
        for linkName in pyrosim.linkNamesToIndices:
            self.sensors[linkName] = SENSOR(linkName)

    def Prepare_To_Act(self):
        self.motors = {}
        for jointName in pyrosim.jointNamesToIndices:
            self.motors[jointName] = MOTOR(jointName)

    def Sense(self, timestep):
        for sensor in self.sensors:
            self.sensors[sensor].Get_Value(timestep)

    def Act(self, timestep):
        for motor in self.motors:
            self.motors[motor].SetValue(self, timestep)