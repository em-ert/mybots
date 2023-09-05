import constants as c
from historian import HISTORIAN
from metronome import METRONOME
import os
import pickle
import pybullet as p
import pybullet_data
from pyglet.resource import media
import pyrosim.pyrosim as pyrosim
from robot import ROBOT
from savedRobot import SAVED_ROBOT
import time
from world import WORLD

x = 0
y = 1
height = 2

class SIMULATION:
    def __init__(self, directOrGUI, solutionID, showBest):
        # Setup display mode
        self.directOrGUI = directOrGUI
        self.showBest = showBest
        if self.directOrGUI=="GUI":
            # If GUI, number fed into solution ID is the uniqueID
            uniqueID = solutionID
            self.physicsClient = p.connect(p.GUI)
            self.robot = SAVED_ROBOT(uniqueID)
            self.metronome = METRONOME(sonify=True)
        else:
            self.physicsClient = p.connect(p.DIRECT)
            self.robot = ROBOT(solutionID)
            self.metronome = METRONOME(sonify=False)

        p.configureDebugVisualizer(p.COV_ENABLE_GUI,0)
        # Set up the rest of the sim's features
        p.setAdditionalSearchPath(pybullet_data.getDataPath())
        p.setGravity(0, 0, -9.8)
        p.setTimeStep(c.FRAME_RATE)
        self.world = WORLD()


    def __del__(self):
        p.disconnect()
        


    def Run(self, solutionID):
        if self.showBest == "False":
            self.Standard(solutionID)
        elif self.directOrGUI == "DIRECT":
            self.Save()
        else:
            self.Load()


    def Standard(self, solutionID):
        p.stepSimulation()
        for i in range(len(c.TEMPOS)):
            self.metronome.Reset(tempo=c.TEMPOS[i])
            for t in range(c.SIM_STEPS):
                clickInfo = self.metronome.StepFunction()
                self.robot.Sense(t + (c.SIM_STEPS * i), clickInfo[1])
                self.robot.Sense_Rhythm(t + (c.SIM_STEPS * i), clickInfo[0])
                self.robot.Think(clickInfo[0])
                self.robot.Act()
                time.sleep(c.SLEEP_TIME)
                p.stepSimulation()
            self.robot.Get_Fitness(solutionID)


    def Save(self):
        p.stepSimulation()
        for i in range(len(c.TEMPOS)):
            self.metronome.Reset(tempo=c.TEMPOS[i])
            for t in range(c.SIM_STEPS):
                clickInfo = self.metronome.StepFunction()
                self.robot.Sense(t + (c.SIM_STEPS * i), clickInfo[1])       # Steps to click
                self.robot.Sense_Rhythm(t + (c.SIM_STEPS * i), clickInfo[0])   # Click (1 or 0)
                self.robot.Think(clickInfo[0])
                self.robot.Act_And_Save(t + (c.SIM_STEPS * i))
                time.sleep(c.SLEEP_TIME)
                p.stepSimulation()

        # Get the unique ID from the historian and set in robot
        uniqueID = HISTORIAN.Get_Unique_Run_ID()
        self.robot.Set_Unique_ID_And_Path(uniqueID)
        # Save sensor and motor values for the future
        self.robot.Save_Motor_Values()
        self.robot.Save_Sensor_Values()
        self.robot.Save_Metronome_Sensor_Values()


    def Load(self):
        os.system("rm fitness*.txt")
        p.stepSimulation()
        for i in range(len(c.TEMPOS)):
            self.metronome.Reset(tempo=c.TEMPOS[i])
            for t in range(c.SIM_STEPS):
                stepEnd = time.time() + (c.FRAME_RATE)
                self.metronome.StepFunction()
                self.robot.Act(t + (c.SIM_STEPS * i))
                remaining = stepEnd - time.time()
                if remaining > 0:
                    time.sleep(remaining)
                elif remaining > c.REPLAY_DELAY_TOLERANCE:
                    pass
                # REVIEW: Temporarily changed this
                """else:
                    raise Exception("Time error, ended with " + str(remaining) + " seconds")"""
                p.stepSimulation()       

                   
    """
    if self.directOrGUI == "GUI":
        if t % 20 == 0:
            playsound("sounds/metronome.mp3", block=False)
    # time.sleep(c.SLEEP_TIME)
    """

"""
for object in range(self.world.numObjects):
    position = self.world.Get_Link_Position(object)
    print(position)
    xPosition = position[x]
    yPosition = position[y]
    height = position[height]
"""