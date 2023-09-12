import constants as c
import numpy as np
import pybullet as p
# from pyglet.resource import media
import pyglet.media as pyglet
import pyrosim.pyrosim as pyrosim

class MOTOR:
    def __init__(self, jointName, hollow):
        self.jointName = jointName
        self.storedValues = np.zeros(c.SIM_STEPS * len(c.TEMPOS))
        self.sensorValues = np.zeros(c.SIM_STEPS * len(c.TEMPOS))
        if hollow:
            self.player = pyglet.Player()
            self.stepSound = pyglet.StaticSource(pyglet.load("sounds/step.mp3"))
            self.player.queue(self.stepSound)


    def Load_Value_Array(self, storedValues):
        self.storedValues = storedValues


    def Load_Sensor_Array(self, sensorValues):
        self.sensorValues = sensorValues


    # For standard direct run
    def Set_Value(self, robot, desiredAngle):
        pyrosim.Set_Motor_For_Joint(
            bodyIndex=robot.robotId,
            jointName=self.jointName,
            controlMode=p.POSITION_CONTROL,
            targetPosition=desiredAngle,
            maxForce=c.MAX_FORCE)
        
    
    # For hollow run setup
    def Set_And_Save_Value(self, robot, desiredAngle, timestep):
        pyrosim.Set_Motor_For_Joint(
            bodyIndex=robot.robotId,
            jointName=self.jointName,
            controlMode=p.POSITION_CONTROL,
            targetPosition=desiredAngle,
            maxForce=c.MAX_FORCE)
        self.storedValues[timestep] = desiredAngle
    

    # For hollow run
    def Set_Stored_Value(self, robot, timestep):
        desiredAngle = self.storedValues[timestep]
        pyrosim.Set_Motor_For_Joint(
            bodyIndex=robot.robotId,
            jointName=self.jointName,
            controlMode=p.POSITION_CONTROL,
            targetPosition=desiredAngle,
            maxForce=c.MAX_FORCE)
        if self.sensorValues[timestep] > self.sensorValues[timestep - 1]:
           self.player.play()
           self.player.queue(self.stepSound)

    """
    def Save_Values(self):
        np.save("data/" + str(self.jointName, 'UTF-8') + "_motor_values.npy", self.motorValues)
        print("Data saved to /data/" + str(self.jointName, 'UTF-8') + "_motor_values.npy")
    """