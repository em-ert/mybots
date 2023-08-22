from bots.capsuleBot import CAPSULE_BOT
import constants as c
import math
import numpy as np
import os
import pybullet as p
import pyrosim.pyrosim as pyrosim
import random
import time


class SOLUTION:
    def __init__(self, ID):
        # Sensor to hidden weights
        self.s_h_Weights = np.random.rand(c.NUM_SENSOR_NEURONS, c.NUM_HIDDEN_NEURONS)
        self.s_h_Weights = (self.s_h_Weights * 2) - 1

        # Auditory to hidden weights
        self.a_h_Weights = np.random.rand(c.NUM_AUDITORY_NEURONS, c.NUM_HIDDEN_NEURONS)
        self.a_h_Weights = (self.a_h_Weights * 2) - 1

        # Hidden to hidden weights
        self.h_h_Weights = np.random.rand(c.NUM_HIDDEN_NEURONS, c.NUM_HIDDEN_NEURONS)
        self.h_h_Weights = (self.h_h_Weights * 2) - 1

        # Hidden to motor weights
        self.h_m_Weights = np.random.rand(c.NUM_HIDDEN_NEURONS, c.NUM_MOTOR_NEURONS)
        self.h_m_Weights = (self.h_m_Weights * 2) - 1

        """
        # Auditory to motor weights
        self.a_m_Weights = np.random.rand(c.NUM_AUDITORY_NEURONS, c.NUM_MOTOR_NEURONS)
        self.a_m_Weights = (self.a_m_Weights * 2) - 1
        """

        """
        # Auditory to motor weights
        self.a_m_Weights = np.ones((c.NUM_AUDITORY_NEURONS, c.NUM_MOTOR_NEURONS), float)
        # self.a_m_Weights = (self.a_m_Weights * 2) - 1
        """

        self.myID = ID
        self.age = 1
        self.wasSimulated = False
        self.links = []
        self.joints = []
        # self.fitness (set in self.Wait_For_Simulation_To_End())

    @staticmethod
    def Create_World():
        pyrosim.Start_SDF("world.sdf")
        pyrosim.Send_Cube(name="Box", pos=[-4, 4, 0.5], size=[1, 1, 1])
        # pyrosim.Send_Capsule(name="Capsule", pos=[-2, 4, 2], size=[.2,1])
        pyrosim.End()

    @staticmethod
    def Create_Body(start_x, start_y, start_z):
        bot = CAPSULE_BOT()
        bot.Create_Body(start_x, start_y, start_z)

    # Produces an nndf file given the weights of the solution
    def Create_Brain(self):
        bot = CAPSULE_BOT()
        self.joints = bot.joints
        self.links = bot.links

        pyrosim.Start_NeuralNetwork("brain" + str(self.myID) + ".nndf")

        neuronCount = 0

        if not c.INCLUDE_UPPER_LINKS:
            linkSensorStart = 4
        else:
            linkSensorStart = 0
    
        # Sensor Neurons
        for sensor in range(c.NUM_SENSOR_NEURONS):
            pyrosim.Send_Sensor_Neuron(name=neuronCount, linkName=self.links[linkSensorStart + sensor])
            neuronCount += 1
        
        # Auditory Neurons
        for auditory in range(c.NUM_AUDITORY_NEURONS):
            pyrosim.Send_Auditory_Neuron(name=neuronCount)
            neuronCount += 1
        
        # Hidden Neurons
        for hidden in range(c.NUM_HIDDEN_NEURONS):
            pyrosim.Send_Hidden_Neuron(name=neuronCount)
            neuronCount += 1

        """
        # Auditory Neurons
        for auditory in range(c.NUM_AUDITORY_NEURONS):
            pyrosim.Send_Auditory_Neuron(name=neuronCount)
            neuronCount += 1
        """

        # Motor Neurons
        for motor in range(c.NUM_MOTOR_NEURONS):
            pyrosim.Send_Motor_Neuron(name=neuronCount, jointName=self.joints[motor].name)
            neuronCount += 1

        # Randomize sensor to hidden
        for currentRow in range(c.NUM_SENSOR_NEURONS):
            for currentColumn in range(c.NUM_HIDDEN_NEURONS):
                pyrosim.Send_Synapse(
                    sourceNeuronName=currentRow, 
                    targetNeuronName=currentColumn + c.NUM_SENSOR_NEURONS, 
                    weight=self.s_h_Weights[currentRow][currentColumn]
                    )
        
        # Randomize auditory to hidden
        for currentRow in range(c.NUM_AUDITORY_NEURONS):
            for currentColumn in range(c.NUM_HIDDEN_NEURONS):
                pyrosim.Send_Synapse(
                    sourceNeuronName=currentRow + c.NUM_SENSOR_NEURONS, 
                    targetNeuronName=currentColumn + c.NUM_SENSOR_NEURONS + c.NUM_AUDITORY_NEURONS, 
                    weight=self.a_h_Weights[currentRow][currentColumn]
                    )
        
        # Randomize hidden to hidden
        for currentRow in range(c.NUM_HIDDEN_NEURONS):
            for currentColumn in range(c.NUM_HIDDEN_NEURONS):
                pyrosim.Send_Synapse(
                    sourceNeuronName=currentRow + c.NUM_SENSOR_NEURONS, 
                    targetNeuronName=currentColumn + c.NUM_SENSOR_NEURONS, 
                    weight=self.h_h_Weights[currentRow][currentColumn]
                    )
        
        # Randomize hidden to motor
        for currentRow in range(c.NUM_HIDDEN_NEURONS):
            for currentColumn in range(c.NUM_MOTOR_NEURONS):
                pyrosim.Send_Synapse(
                    sourceNeuronName=currentRow + c.NUM_SENSOR_NEURONS, 
                    targetNeuronName=currentColumn + c.NUM_SENSOR_NEURONS + c.NUM_HIDDEN_NEURONS + c.NUM_AUDITORY_NEURONS,
                    weight=self.h_m_Weights[currentRow][currentColumn]
                    )
        """        
        # Randomize auditory to motor
        for currentRow in range(c.NUM_AUDITORY_NEURONS):
            for currentColumn in range(c.NUM_MOTOR_NEURONS):
                pyrosim.Send_Synapse(
                    sourceNeuronName=currentRow + c.NUM_SENSOR_NEURONS + c.NUM_HIDDEN_NEURONS, 
                    targetNeuronName=currentColumn + c.NUM_SENSOR_NEURONS + c.NUM_HIDDEN_NEURONS + c.NUM_AUDITORY_NEURONS, 
                    weight=self.a_m_Weights[currentRow][currentColumn]
                    )
        """        
        
        pyrosim.End()

    def Mutate(self):
        randomLayer = random.randint(0, 3)
        if randomLayer == 0:
            # Mutate S - H
            randomRow = random.randint(0, c.NUM_SENSOR_NEURONS - 1)
            randomColumn = random.randint(0, c.NUM_HIDDEN_NEURONS - 1)
            self.s_h_Weights[randomRow,randomColumn] = (random.random() * 2) - 1
        
        
        elif randomLayer == 1:
            # Mutate H - H
            randomRow = random.randint(0, c.NUM_HIDDEN_NEURONS - 1)
            randomColumn = random.randint(0, c.NUM_HIDDEN_NEURONS - 1)
            self.h_h_Weights[randomRow,randomColumn] = (random.random() * 2) - 1
        
        elif randomLayer == 2:
            # Mutate H - M
            randomRow = random.randint(0, c.NUM_HIDDEN_NEURONS - 1)
            randomColumn = random.randint(0, c.NUM_MOTOR_NEURONS - 1)
            self.h_m_Weights[randomRow,randomColumn] = (random.random() * 2) - 1

        
        elif randomLayer == 3:
            # Mutate A - M
            randomRow = random.randint(0, c.NUM_AUDITORY_NEURONS - 1)
            randomColumn = random.randint(0, c.NUM_MOTOR_NEURONS - 1)
            self.a_m_Weights[randomRow,randomColumn] = (random.random() * 2) - 1

        
        else:
            raise Exception("Random choice error!")

    def Reset_Simulation_State(self):
        self.wasSimulated = False

    def Set_ID(self, ID):
        self.myID = ID

    def Start_Simulation(self, directOrGUI, showBest):
        self.Create_Brain()
        if not showBest:
            os.system("python3 simulate.py " + directOrGUI + " " + str(self.myID) + " False 2&>1 &")
            
        # Note: Without "&" best runs are shown serially
        else:
            os.system("python3 simulate.py " + directOrGUI + " " + str(self.myID) + " True 2&>1")

    def Wait_For_Simulation_To_End(self):
        fitnessFileName = "fitness" + str(self.myID) + ".txt"
        while not os.path.exists(fitnessFileName):
            time.sleep(0.001)
        fitnessFile = open(fitnessFileName, "r")
        self.fitness = float(fitnessFile.read())
        fitnessFile.close()
        os.system("rm " + fitnessFileName)

        if c.OPTIMIZE_AGE == False:
            fitnessFileName2 = "fitnessb" + str(self.myID) + ".txt"
            while not os.path.exists(fitnessFileName2):
                time.sleep(0.001)
            fitnessFile2 = open(fitnessFileName2, "r")
            self.fitness2 = float(fitnessFile2.read())
            fitnessFile2.close()
            os.system("rm " + fitnessFileName2)
        
        self.wasSimulated = True