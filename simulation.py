import constants as c
import pybullet as p
import pybullet_data
import pyrosim.pyrosim as pyrosim
from robot import ROBOT
import time
from world import WORLD

class SIMULATION:
    def __init__(self):
        self.physicsClient = p.connect(p.GUI)
        p.setAdditionalSearchPath(pybullet_data.getDataPath())
        p.setGravity(0, 0, -9.8)
        self.world = WORLD()
        self.robot = ROBOT()

    def __del__(self):
        p.disconnect()

    def Run(self):
        for t in range(c.simSteps):
            p.stepSimulation()
            self.robot.Sense(t)
            self.robot.Act(t)
            time.sleep(0.00166)
            print(t)

    def Save_Values(self):
        for sensor in self.robot.sensors:
            numpy.save("data/" + self.robot.sensors[sensor].name + "_sensor_values.npy", self.robot.sensors[sensor].values)
            print("Data saved to /data/" + self.robot.sensors[sensor].name + "_sensor_values.npy")