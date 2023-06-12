import constants as c
from playsound import playsound
import pybullet as p
import pybullet_data
import pyrosim.pyrosim as pyrosim
from robot import ROBOT
import time
from world import WORLD

x = 0
y = 1
height = 2

class SIMULATION:
    def __init__(self, directOrGUI, solutionID):
        # Setup display mode
        self.directOrGUI = directOrGUI
        if self.directOrGUI=="GUI":
            self.physicsClient = p.connect(p.GUI)
        else:
            self.physicsClient = p.connect(p.DIRECT)

        # Set up the rest of the sim's features
        p.setAdditionalSearchPath(pybullet_data.getDataPath())
        p.setGravity(0, 0, -9.8)
        self.world = WORLD()
        self.robot = ROBOT(solutionID)

    def __del__(self):
        """
        for sensor in self.robot.sensors:
            self.robot.sensors[sensor].Save_Values()
        for motor in self.robot.motors:
            self.robot.motors[motor].Save_Values()
        """
        p.disconnect()

    def Get_Fitness(self, solutionID):
        self.robot.Get_Fitness(solutionID)

    def Run(self):
        for t in range(c.SIM_STEPS):
            p.stepSimulation()
            self.robot.Sense(t, self.directOrGUI)
            self.robot.Think()
            self.robot.Act(t)
            if self.directOrGUI == "GUI":
                if t % 20 == 0:
                    playsound("sounds/metronome.mp3", block=False)
                time.sleep(c.SLEEP_TIME)

            """
            for object in range(self.world.numObjects):
                position = self.world.Get_Link_Position(object)
                print(position)
                xPosition = position[x]
                yPosition = position[y]
                height = position[height]
            """
            # print(t)