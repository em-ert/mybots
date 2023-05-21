import constants as c
import numpy
import pybullet as p
import pyrosim.pyrosim as pyrosim

class MOTOR:
    def __init__(self, jointName):
        self.jointName = jointName
        self.Prepare_To_Act()

    def Prepare_To_Act(self):
        print(self.jointName)
        if (self.jointName == b"Torso_FrontLeg"):
            self.amplitude = c.FRONT_AMPLITUDE
            self.frequency = c.FRONT_FREQUENCY
            self.offset = c.FRONT_OFFSET
        if (self.jointName == b"Torso_BackLeg"):
            self.amplitude = c.BACK_AMPLITUDE
            self.frequency = c.BACK_FREQUENCY
            self.offset = c.BACK_OFFSET
        self.motorValues = numpy.sin(numpy.linspace(0, 2 * numpy.pi, c.SIM_STEPS) * self.frequency + self.offset) * self.amplitude

    def SetValue(self, robot, timestep):
        pyrosim.Set_Motor_For_Joint(
            bodyIndex=robot.robotId,
            jointName=self.jointName,
            controlMode=p.POSITION_CONTROL,
            targetPosition=self.motorValues[timestep],
            maxForce=c.MAX_FORCE)

    def Save_Values(self):
        numpy.save("data/" + str(self.jointName, 'UTF-8') + "_motor_values.npy", self.motorValues)
        print("Data saved to /data/" + str(self.jointName, 'UTF-8') + "_motor_values.npy")