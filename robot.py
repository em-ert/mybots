from playsound import playsound
import pybullet as p
from pyrosim.neuralNetwork import NEURAL_NETWORK
import pyrosim.pyrosim as pyrosim
from sensor import SENSOR
from motor import MOTOR


class ROBOT:
    def __init__(self):
        self.robotId = p.loadURDF("body.urdf")
        self.motors = {}
        self.sensors = {}

        self.nn = NEURAL_NETWORK("brain.nndf")

        pyrosim.Prepare_To_Simulate(self.robotId)
        self.Prepare_To_Act()
        self.Prepare_To_Sense()
        self.old_values = [1,1,1]

    def Get_Fitness(self):
        stateOfLinkZero = p.getLinkState(self.robotId, 0)
        positionOfLinkZero = stateOfLinkZero[0]
        xCoordinateOfLinkZero = positionOfLinkZero[0]
        fitnessFile = open("fitness.txt", "w")
        fitnessFile.write(str(xCoordinateOfLinkZero))
        fitnessFile.close()


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

    def Sense(self, timestep):
        for sensor in self.sensors:
            curr_sensor = self.sensors[sensor]
            curr_sensor.Get_Value(timestep)
            # self.Step_Audio(timestep, curr_sensor)

    def Step_Audio(self, timestep, curr_sensor):
        old_value = curr_sensor.values[timestep - 1]
        new_value = curr_sensor.values[timestep]
        if (new_value == 1 and curr_sensor.linkName != "Torso" and new_value != old_value):
            print("playing sound")
            print(curr_sensor.name)
            print(old_value)
            print(new_value)
            playsound('sounds/light_step.mp3', False)

    def Act(self, timestep):
        for neuronName in self.nn.Get_Neuron_Names():
            if self.nn.Is_Motor_Neuron(neuronName):
                jointName = self.nn.Get_Motor_Neurons_Joint(neuronName)
                desiredAngle = self.nn.Get_Value_Of(neuronName)
                self.motors[bytes(jointName, 'UTF-8')].Set_Value(self, desiredAngle)
                # print("Name=" + neuronName + ", Joint=" + jointName  + ", Angle=" + str(desiredAngle))

    def Think(self):
        self.nn.Update()
        # self.nn.Print()