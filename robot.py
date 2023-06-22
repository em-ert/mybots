import constants as c
import os
from playsound import playsound
import pybullet as p
from pyrosim.neuralNetwork import NEURAL_NETWORK
import pyrosim.pyrosim as pyrosim
from sensor import SENSOR
from motor import MOTOR


class ROBOT:
    def __init__(self, solutionID):
        self.robotId = p.loadURDF("body.urdf")
        self.motors = {}
        self.sensors = {}

        self.nn = NEURAL_NETWORK("brain" + str(solutionID) + ".nndf")

        pyrosim.Prepare_To_Simulate(self.robotId)
        self.Prepare_To_Act()
        self.Prepare_To_Sense()
        self.Prepare_For_Contact()
        os.system("rm brain" + str(solutionID) + ".nndf")

    def Get_Fitness(self, solutionID):
        stateOfLinkZero = p.getLinkState(self.robotId, 0)
        positionOfLinkZero = stateOfLinkZero[0]
        xCoordinateOfLinkZero = positionOfLinkZero[0]
        # Define tmp and true fitness file names
        tmpFitnessFileName = "tmp" + str(solutionID) + ".txt"
        fitnessFileName = "fitness" + str(solutionID) + ".txt"
        # Write to temp file so reading doesn't occur before writing concludes
        tmpFitnessFile = open(tmpFitnessFileName, "w")
        tmpFitnessFile.write(str(xCoordinateOfLinkZero))
        tmpFitnessFile.close()
        os.system("mv " + tmpFitnessFileName + " " + fitnessFileName)

    def Prepare_To_Sense(self):
        self.sensors = {}
        sensor_name = 0
        for linkName in pyrosim.linkNamesToIndices:
            self.sensors[linkName] = SENSOR(linkName, sensor_name)
            sensor_name += 1


    def Prepare_To_Act(self):
        self.motors = {}
        for jointName in pyrosim.jointNamesToIndices:
            self.motors[jointName] = MOTOR(jointName)

 
    def Prepare_For_Contact(self):
        self.linksInContact = {}
        for linkIndex in range(0, p.getNumJoints(self.robotId)):
            self.linksInContact[linkIndex] = False


    def Sense(self, timestep):
        for sensor in self.sensors:
            curr_sensor = self.sensors[sensor]
            curr_sensor.Get_Value(timestep)


    def Sense_And_Sound(self, timestep):
        for sensor in self.sensors:
            curr_sensor = self.sensors[sensor]
            oldValue = curr_sensor.currValue
            oldValue2 = curr_sensor.values[timestep - 2]
            curr_sensor.Get_Value(timestep)
            if oldValue < curr_sensor.currValue and oldValue2 < curr_sensor.currValue and timestep != 0:
                playsound("sounds/simple_step.mp3", block=False)
            

    def Step_Audio(self, timestep, curr_sensor):
        old_value_1 = curr_sensor.values[timestep - 1]
        old_value_2 = curr_sensor.values[timestep - 2]
        new_value = curr_sensor.values[timestep]
        if new_value == 1 and new_value != old_value:
            """
            print("playing sound")
            print(curr_sensor.name)
            print(old_value)
            print(new_value)
            """
            playsound("sounds/simple_step.mp3", block=False)


    def Act(self, timestep):
        for neuronName in self.nn.Get_Neuron_Names():
            if self.nn.Is_Motor_Neuron(neuronName):
                jointName = self.nn.Get_Motor_Neurons_Joint(neuronName)
                jointName = bytes(jointName, 'UTF-8')
                desiredAngle = self.nn.Get_Value_Of(neuronName) * c.MOTOR_JOINT_RANGE
                self.motors[jointName].Set_Value(self, desiredAngle)
            
                # print("Name=" + neuronName + ", Joint=" + jointName  + ", Angle=" + str(desiredAngle))

    def Act_And_Sound(self, timestep):
        for neuronName in self.nn.Get_Neuron_Names():
            if self.nn.Is_Motor_Neuron(neuronName):
                jointName = self.nn.Get_Motor_Neurons_Joint(neuronName)
                jointName = bytes(jointName, 'UTF-8')
                desiredAngle = self.nn.Get_Value_Of(neuronName) * c.MOTOR_JOINT_RANGE
                self.motors[jointName].Set_Value(self, desiredAngle)
                linkID = pyrosim.Get_Link_ID_From_Joint_Name(jointName)
                contactPoints = p.getContactPoints(self.robotId, linkID)
                if len(contactPoints) > 0 and self.linksInContact[linkID] == False:
                    playsound("sounds/simple_step.mp3", block=False)
                    self.linksInContact[linkID] = True
                elif len(contactPoints) < 0 and self.linksInContact[linkID] == True:
                    self.linksInContact[linkID] = False

    

    def Think(self):
        self.nn.Update()
        # self.nn.Print()