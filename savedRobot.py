import constants as c
from glob import glob
import os
import pickle
import pybullet as p
from pyrosim.neuralNetwork import NEURAL_NETWORK
import pyrosim.pyrosim as pyrosim
from sensor import SENSOR
from motor import MOTOR


class SAVED_ROBOT:
    def __init__(self, uniqueID):
        self.root = "bestRuns/{}sols_{}gens/run{}".format(c.POPULATION_SIZE, c.NUMBER_OF_GENERATIONS, uniqueID) + "/"

        self.robotId = p.loadURDF("body.urdf")
        self.motors = {}

        brains = glob(self.root + "brain?.nndf")
        if len(brains) == 1:
            self.nn = NEURAL_NETWORK(brains[0])

        pyrosim.Prepare_To_Simulate(self.robotId)
        self.Prepare_To_Act()



    def Prepare_To_Act(self):
        self.motors = {}
        if os.path.exists(self.root + "pickles/motorValues.pickle") and os.path.exists(self.root + "pickles/sensorValues.pickle"):
            with open(self.root + "pickles/motorValues.pickle", "rb") as f:
                motorValues = pickle.load(f)
            with open(self.root + "pickles/sensorValues.pickle", "rb") as f:
                sensorValues = pickle.load(f)
            for jointName in pyrosim.jointNamesToIndices:
                self.motors[jointName] = MOTOR(jointName, hollow=True)
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