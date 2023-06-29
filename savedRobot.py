import constants as c
import os
import pickle
import pybullet as p
from pyrosim.neuralNetwork import NEURAL_NETWORK
import pyrosim.pyrosim as pyrosim
from sensor import SENSOR
from metronomeSensor import METRONOME_SENSOR
from motor import MOTOR


class SAVED_ROBOT:
    def __init__(self, solutionID):
        self.robotId = p.loadURDF("body.urdf")
        self.motors = {}

        self.nn = NEURAL_NETWORK("brain" + str(solutionID) + ".nndf")

        pyrosim.Prepare_To_Simulate(self.robotId)
        self.Prepare_To_Act()

        os.system("rm brain" + str(solutionID) + ".nndf")


    def Prepare_To_Act(self):
        self.motors = {}
        if os.path.exists("motorValues.bin") and os.path.exists("sensorValues.bin"):
            with open("motorValues.bin", "rb") as f:
                motorValues = pickle.load(f)
            with open("sensorValues.bin", "rb") as f:
                sensorValues = pickle.load(f)
            for jointName in pyrosim.jointNamesToIndices:
                self.motors[jointName] = MOTOR(jointName)
                self.motors[jointName].Load_Value_Array(motorValues[jointName])
                if jointName.decode("utf8") in sensorValues:
                    self.motors[jointName].Load_Sensor_Array(sensorValues[jointName.decode("utf8")])
            

    def Act(self, timestep):
        for neuronName in self.nn.Get_Neuron_Names():
            if self.nn.Is_Motor_Neuron(neuronName):
                jointName = self.nn.Get_Motor_Neurons_Joint(neuronName)
                jointName = bytes(jointName, 'UTF-8')
                self.motors[jointName].Set_Stored_Value(self, timestep)
                

    def Think(self, click):
        self.nn.Update(click)
        # self.nn.Print()