import constants as c
import math
import numpy
import os
import pyrosim.pyrosim as pyrosim
import random
import time


class SOLUTION:
    def __init__(self, ID):
        self.weights = numpy.random.rand(c.NUM_SENSOR_NEURONS, c.NUM_MOTOR_NEURONS)
        self.weights = (self.weights * 2) - 1
        self.myID = ID
        self.age = 1
        self.wasSimulated = False
        # self.fitness (set in self.Wait_For_Simulation_To_End())

    @staticmethod
    def Create_World():
        pyrosim.Start_SDF("world.sdf")
        pyrosim.Send_Cube(name="Box", pos=[-4, 4, 0.5], size=[1, 1, 1])
        # pyrosim.Send_Capsule(name="Capsule", pos=[-2, 4, 2], size=[.2,1])
        pyrosim.End()

    @staticmethod
    def Create_Body(start_x, start_y, start_z):
        pyrosim.Start_URDF("body.urdf")

        pyrosim.Send_Cube(name="Torso", pos=[start_x, start_y, start_z], size=[1,1,1])

        # Front leg
        pyrosim.Send_Joint(
            name="Torso_FrontLeg", 
            parent="Torso", 
            child="FrontLeg", 
            type="revolute", 
            position=[start_x, start_y+0.5, start_z], 
            jointAxis="1 0 1")
        pyrosim.Send_Capsule(
            name="FrontLeg", 
            pos=[0, 0.5, 0], 
            size=[0.2, 1],
            rpy=[0,(math.pi/2),(math.pi/2)])
        pyrosim.Send_Joint(
            name="FrontLeg_FrontLower", 
            parent="FrontLeg", 
            child="FrontLower", 
            type="revolute", 
            position=[0, 1, 0], 
            jointAxis="1 0 1")
        pyrosim.Send_Capsule(
            name="FrontLower", 
            pos=[0, 0, -0.5], 
            size=[0.2, 1])

        # Back leg
        pyrosim.Send_Joint(
            name="Torso_BackLeg", 
            parent="Torso", 
            child="BackLeg", 
            type="revolute", 
            position=[start_x, start_y-0.5, start_z], 
            jointAxis="1 0 1")
        pyrosim.Send_Capsule(
            name="BackLeg", 
            pos=[0, -0.5, 0],
            size=[0.2, 1],
            rpy=[0,(math.pi/2),(math.pi/2)])
        pyrosim.Send_Joint(
            name="BackLeg_BackLower", 
            parent="BackLeg", 
            child="BackLower", 
            type="revolute", 
            position=[0, -1, 0], 
            jointAxis="1 0 1")
        pyrosim.Send_Capsule(
            name="BackLower", 
            pos=[0, 0, -0.5], 
            size=[0.2, 1])

        # Left leg
        pyrosim.Send_Joint(
            name="Torso_LeftLeg",
            parent="Torso",
            child="LeftLeg",
            type="revolute",
            position=[start_x-0.5, start_y, start_z], 
            jointAxis="0 1 1")
        pyrosim.Send_Capsule(
            name="LeftLeg", 
            pos=[-0.5, 0, 0], 
            size=[0.2, 1],
            rpy=[0,(math.pi/2),0])
        pyrosim.Send_Joint(
            name="LeftLeg_LeftLower", 
            parent="LeftLeg", 
            child="LeftLower", 
            type="revolute", 
            position=[-1, 0, 0], 
            jointAxis="0 1 1")
        pyrosim.Send_Capsule(
            name="LeftLower", 
            pos=[0, 0, -0.5], 
            size=[0.2, 1])

        # Right leg
        pyrosim.Send_Joint(
            name="Torso_RightLeg", 
            parent="Torso", 
            child="RightLeg", 
            type="revolute", 
            position=[start_x+0.5, start_y, start_z], 
            jointAxis="0 1 1")
        pyrosim.Send_Capsule(
            name="RightLeg", 
            pos=[0.5, 0, 0], 
            size=[0.2, 1],
            rpy=[0,(math.pi/2),0])
        pyrosim.Send_Joint(
            name="RightLeg_RightLower", 
            parent="RightLeg", 
            child="RightLower", 
            type="revolute", 
            position=[1, 0, 0], 
            jointAxis="0 1 1")
        pyrosim.Send_Capsule(
            name="RightLower", 
            pos=[0, 0, -0.5], 
            size=[0.2, 1])

        pyrosim.End()

    def Create_Brain(self):
        pyrosim.Start_NeuralNetwork("brain" + str(self.myID) + ".nndf")

        # Sensor Neurons
        """pyrosim.Send_Sensor_Neuron(name=0, linkName="Torso")
        pyrosim.Send_Sensor_Neuron(name=1, linkName="BackLeg")
        pyrosim.Send_Sensor_Neuron(name=2, linkName="FrontLeg")
        pyrosim.Send_Sensor_Neuron(name=3, linkName="LeftLeg")
        pyrosim.Send_Sensor_Neuron(name=4, linkName="RightLeg")"""

        pyrosim.Send_Sensor_Neuron(name=0, linkName="BackLower")
        pyrosim.Send_Sensor_Neuron(name=1, linkName="FrontLower")
        pyrosim.Send_Sensor_Neuron(name=2, linkName="LeftLower")
        pyrosim.Send_Sensor_Neuron(name=3, linkName="RightLower")
        

        # Motor Neurons
        pyrosim.Send_Motor_Neuron(name=4, jointName="Torso_BackLeg")
        pyrosim.Send_Motor_Neuron(name=5, jointName="Torso_FrontLeg")
        pyrosim.Send_Motor_Neuron(name=6, jointName="Torso_LeftLeg")
        pyrosim.Send_Motor_Neuron(name=7, jointName="Torso_RightLeg")
        pyrosim.Send_Motor_Neuron(name=8, jointName="BackLeg_BackLower")
        pyrosim.Send_Motor_Neuron(name=9, jointName="FrontLeg_FrontLower")
        pyrosim.Send_Motor_Neuron(name=10, jointName="LeftLeg_LeftLower")
        pyrosim.Send_Motor_Neuron(name=11, jointName="RightLeg_RightLower")

        for currentRow in range(c.NUM_SENSOR_NEURONS):
            for currentColumn in range(c.NUM_MOTOR_NEURONS):
                pyrosim.Send_Synapse(
                    sourceNeuronName=currentRow, 
                    targetNeuronName=currentColumn + c.NUM_SENSOR_NEURONS, 
                    weight=self.weights[currentRow][currentColumn]
                    )

        pyrosim.End()

    def Mutate(self):
        randomRow = random.randint(0, c.NUM_SENSOR_NEURONS - 1)
        randomColumn = random.randint(0, c.NUM_MOTOR_NEURONS - 1)
        self.weights[randomRow,randomColumn] = (random.random() * 2) - 1

    def Reset_Simulation_State(self):
        self.wasSimulated = False

    def Set_ID(self, ID):
        self.myID = ID

    def Start_Simulation(self, directOrGUI, showBest):
        self.Create_Brain()
        if not showBest:
            os.system("python3 simulate.py " + 
                    directOrGUI + " " +
                    str(self.myID) +
                    " False 2&>1 &")
            
        # Note: Without "&" best runs are shown serially
        else:
            os.system("python3 simulate.py " + 
                    directOrGUI + " " +
                    str(self.myID) +
                    " True 2&>1")

    def Wait_For_Simulation_To_End(self):
        fitnessFileName = "fitness" + str(self.myID) + ".txt"
        while not os.path.exists(fitnessFileName):
            time.sleep(0.01)
        fitnessFile = open(fitnessFileName, "r")
        self.fitness = float(fitnessFile.read())
        fitnessFile.close()
        os.system("rm " + fitnessFileName)
        self.wasSimulated = True