import constants as c
import numpy
import os
import pyrosim.pyrosim as pyrosim
import random
import time


class SOLUTION:
    def __init__(self, ID):
        self.weights = numpy.random.rand(3,2)
        self.weights = (self.weights * 2) - 1
        self.myID = ID

    @staticmethod
    def Create_World():
        pyrosim.Start_SDF("world.sdf")
        pyrosim.Send_Cube(name="Box", pos=[-4, 4, 0.5], size=[1, 1, 1])
        pyrosim.End()

    @staticmethod
    def Create_Body(start_x, start_y, start_z):
        pyrosim.Start_URDF("body.urdf")

        pyrosim.Send_Cube(name="Torso", pos=[start_x, start_y, start_z], size=[1, 1, 1])
        pyrosim.Send_Joint(name="Torso_FrontLeg", parent="Torso", child="FrontLeg", type="revolute", position=[start_x, start_y-0.5, start_z], jointAxis="0 1 0")
        pyrosim.Send_Cube(name="FrontLeg", pos=[0, 0.5, 0], size=[0.2, 1, 0.2])

        pyrosim.Send_Joint(name="Torso_BackLeg", parent="Torso", child="BackLeg", type="revolute", position=[start_x, start_y+0.5, start_z], jointAxis="0 1 0")
        pyrosim.Send_Cube(name="BackLeg", pos=[0, -0.5, 0], size=[0.2, 1, 0.2])

        pyrosim.End()

    def Create_Brain(self):
        pyrosim.Start_NeuralNetwork("brain" + str(self.myID) + ".nndf")

        # Sensor Neurons
        pyrosim.Send_Sensor_Neuron(name=0, linkName="Torso")
        pyrosim.Send_Sensor_Neuron(name=1, linkName="BackLeg")
        pyrosim.Send_Sensor_Neuron(name=2, linkName="FrontLeg")

        # Motor Neurons
        pyrosim.Send_Motor_Neuron(name=3, jointName="Torso_BackLeg")
        pyrosim.Send_Motor_Neuron(name=4, jointName="Torso_FrontLeg")

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

    def Set_ID(self, ID):
        self.myID = ID

    def Start_Simulation(self, directOrGUI, showBest):
        self.Create_Brain()
        if not showBest:
            os.system("python3 simulate.py " + 
                    directOrGUI + " " +
                    str(self.myID) +
                    " False 2&>1 &")
        else:
            os.system("python3 simulate.py " + 
                    directOrGUI + " " +
                    str(self.myID) +
                    " True 2&>1 &")

    def Wait_For_Simulation_To_End(self):
        fitnessFileName = "fitness" + str(self.myID) + ".txt"
        while not os.path.exists(fitnessFileName):
            time.sleep(0.01)
        fitnessFile = open(fitnessFileName, "r")
        self.fitness = float(fitnessFile.read())
        fitnessFile.close()
        os.system("rm " + fitnessFileName)