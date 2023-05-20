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
            self.amplitude = c.FrontLeg_Amplitude
            self.frequency = c.FrontLeg_Frequency
            self.offset = c.FrontLeg_PhaseOffset
        if (self.jointName == b"Torso_BackLeg"):
            self.amplitude = c.BackLeg_Amplitude
            self.frequency = c.BackLeg_Frequency
            self.offset = c.BackLeg_PhaseOffset
        self.motorValues = numpy.sin(numpy.linspace(0, 2 * numpy.pi, c.simSteps) * self.frequency + self.offset) * self.amplitude

    def SetValue(self, robot, timestep):
        pyrosim.Set_Motor_For_Joint(
            bodyIndex=robot.robotId,
            jointName=self.jointName,
            controlMode=p.POSITION_CONTROL,
            targetPosition=self.motorValues[timestep],
            maxForce=c.maxForce)