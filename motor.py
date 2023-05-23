import constants as c
import numpy
import pybullet as p
import pyrosim.pyrosim as pyrosim

class MOTOR:
    def __init__(self, jointName):
        self.jointName = jointName

    def SetValue(self, robot, desiredAngle):
        pyrosim.Set_Motor_For_Joint(
            bodyIndex=robot.robotId,
            jointName=self.jointName,
            controlMode=p.POSITION_CONTROL,
            targetPosition=desiredAngle,
            maxForce=c.MAX_FORCE)

    """
    def Save_Values(self):
        numpy.save("data/" + str(self.jointName, 'UTF-8') + "_motor_values.npy", self.motorValues)
        print("Data saved to /data/" + str(self.jointName, 'UTF-8') + "_motor_values.npy")
    """