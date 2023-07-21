from bots.capsuleBot import CAPSULE_BOT
import constants as c
import os
import pickle
import pybullet as p
from pyrosim.neuralNetwork import NEURAL_NETWORK
import pyrosim.pyrosim as pyrosim
from sensor import SENSOR
from metronomeSensor import METRONOME_SENSOR
from motor import MOTOR
import numpy as np


class ROBOT:
    def __init__(self, solutionID):
        self.robotId = p.loadURDF("body.urdf")
        self.motors = {}
        self.sensors = {}

        bot = CAPSULE_BOT()
        self.joints = bot.joints

        self.nn = NEURAL_NETWORK("brain" + str(solutionID) + ".nndf")

        self.fitness = 0

        pyrosim.Prepare_To_Simulate(self.robotId)
        self.Prepare_To_Act()
        self.Prepare_To_Sense()
        self.Prepare_To_Sense_Audio()
        os.system("rm brain" + str(solutionID) + ".nndf")

    
    def Get_Fitness(self, solutionID):
        """
        stateOfLinkZero = p.getLinkState(self.robotId, 0)
        positionOfLinkZero = stateOfLinkZero[0]
        xCoordinateOfLinkZero = positionOfLinkZero[0]
        """
        # Define tmp and true fitness file names
        tmpFitnessFileName = "tmp" + str(solutionID) + ".txt"
        fitnessFileName = "fitness" + str(solutionID) + ".txt"
        # Write to temp file so reading doesn't occur before writing concludes
        tmpFitnessFile = open(tmpFitnessFileName, "w")
        tmpFitnessFile.write(str(self.fitness))
        tmpFitnessFile.close()
        os.system("mv " + tmpFitnessFileName + " " + fitnessFileName)


    def Prepare_To_Sense(self):
        self.sensors = {}
        sensor_name = 0
        for linkName in pyrosim.linkNamesToIndices:
            self.sensors[linkName] = SENSOR(linkName, sensor_name)
            sensor_name += 1


    def Prepare_To_Sense_Audio(self):
        self.metronomeSensor = METRONOME_SENSOR(0)


    def Prepare_To_Act(self):
        self.motors = {}
        for jointName in pyrosim.jointNamesToIndices:
            self.motors[jointName] = MOTOR(jointName, hollow=False)


    def Sense(self, timestep):
        stepValue = 0
        for sensor in self.sensors:
            curr_sensor = self.sensors[sensor]
            curr_sensor.Get_Value(timestep)
            step = curr_sensor.Get_Step(timestep)
            stepValue += step
        self.fitness += stepValue * (np.sin((2*np.pi)/c.MET_FRAME_RATIO)+0.5)
        
            
    def Sense_Rhythm(self, timestep, click):
        self.metronomeSensor.Get_Value(timestep, click)
        
        """
        for link in ["FrontLower", "BackLower", "LeftLower", "RightLower"]:
            linkIndex = pyrosim.linkNamesToIndices[link]
            linkState = p.getLinkState(self.robotId, linkIndex, 1)
            linkVelocities = linkState[6]
            totalChange = 0
            for velocity in linkVelocities:
                totalChange += velocity
            self.fitness += totalChange * click
        """    

    def Act(self):
        for neuronName in self.nn.Get_Neuron_Names():
            if self.nn.Is_Motor_Neuron(neuronName):
                jointName = self.nn.Get_Motor_Neurons_Joint(neuronName)
                jointName = bytes(jointName, 'UTF-8')
                desiredAngle = self.nn.Get_Value_Of(neuronName) * c.MOTOR_JOINT_RANGE
                self.motors[jointName].Set_Value(self, desiredAngle)


    def Act_And_Save(self, timestep):
        for neuronName in self.nn.Get_Neuron_Names():
            if self.nn.Is_Motor_Neuron(neuronName):
                jointName = self.nn.Get_Motor_Neurons_Joint(neuronName)
                jointName = bytes(jointName, 'UTF-8')
                desiredAngle = self.nn.Get_Value_Of(neuronName) * c.MOTOR_JOINT_RANGE
                self.motors[jointName].Set_And_Save_Value(self, desiredAngle, timestep)
            
                # print("Name=" + neuronName + ", Joint=" + jointName  + ", Angle=" + str(desiredAngle))


    def Save_Motor_Values(self):
        motorValues = {}
        for neuronName in self.nn.Get_Neuron_Names():
            if self.nn.Is_Motor_Neuron(neuronName):
                jointName = self.nn.Get_Motor_Neurons_Joint(neuronName)
                jointName = bytes(jointName, 'UTF-8')
                motorValues[jointName] = self.motors[jointName].storedValues
        with open("pickles/motorValues.pickle", "wb") as f:
            pickle.dump(motorValues, f)

    def Save_Sensor_Values(self):
        sensorValues = {}
        for neuronName in self.nn.Get_Neuron_Names():
            if self.nn.Is_Sensor_Neuron(neuronName):
                linkName = self.nn.Get_Sensor_Neurons_Link(neuronName)
            for joint in self.joints:
                if joint.child == linkName:
                    joint_for_sensor = joint.name
                    sensorValues[joint_for_sensor] = self.sensors[linkName].values
                    self.sensors[linkName].Save_Values()
        with open("pickles/sensorValues.pickle", "wb") as f:
            pickle.dump(sensorValues, f)

    def Save_Metronome_Sensor_Values(self):
        self.metronomeSensor.Save_Values()


    def Think(self, click):
        self.nn.Update(click)
        # self.nn.Print()