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
import math
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
        timestep = 0
        for i in range(len(c.TEMPOS)):
            self.metronome.Reset(tempo=c.TEMPOS[i])
            # Find number of metronome clicks for the first tempo and use that to scale the rest
            # That way, robots trained on same number of clicks per tempo
            for t in range(c.FRAMES_PER_TEMPO[i]):
                clickInfo = self.metronome.StepFunction()
                self.robot.Sense(timestep, clickInfo[1], clickInfo[2])
                self.robot.Sense_Rhythm(timestep, clickInfo[0])
                self.robot.Think(clickInfo[0])
                self.robot.Act()
                time.sleep(c.SLEEP_TIME)
                p.stepSimulation()
                timestep += 1
        # NOTE: Fitness only obtained once in simulation (one fitness for all tempos). If fitness for each individual tempo is desired, this could be moved to the and of the loop above       
        self.robot.Get_Fitness(solutionID)


    def Save(self):
        p.stepSimulation()
        timestep = 0
        for i in range(len(c.TEMPOS)):
            self.metronome.Reset(tempo=c.TEMPOS[i])
            for t in range(c.FRAMES_PER_TEMPO[i]):
                clickInfo = self.metronome.StepFunction()
                self.robot.Sense(timestep, clickInfo[1], clickInfo[2])       # Steps to click
                self.robot.Sense_Rhythm(timestep, clickInfo[0])   # Click (1 or 0)
                self.robot.Think(clickInfo[0])
                self.robot.Act_And_Save(timestep)
                time.sleep(c.SLEEP_TIME)
                p.stepSimulation()
                timestep += 1

        # Get the unique ID from the historian and set in robot
        uniqueID = HISTORIAN.Get_Unique_Run_ID()
        self.robot.Set_Unique_ID_And_Path(uniqueID)
        # Save sensor and motor values for the future
        self.robot.Save_Motor_Values()
        self.robot.Save_Sensor_Values()
        self.robot.Save_Metronome_Sensor_Values()


    def Load(self):
        p.stepSimulation()
        timestep = 0
        for i in range(len(c.TEMPOS)):
            self.metronome.Reset(tempo=c.TEMPOS[i])
            for t in range(c.FRAMES_PER_TEMPO[i]):
                stepEnd = time.time() + (c.FRAME_RATE)
                self.metronome.StepFunction()
                self.robot.Act(timestep)
                remaining = stepEnd - time.time()
                if remaining > 0:
                    time.sleep(remaining)
                elif remaining > c.REPLAY_DELAY_TOLERANCE:
                    pass
                # REVIEW: Temporarily changed this
                """else:
                    raise Exception("Time error, ended with " + str(remaining) + " seconds")"""
                p.stepSimulation()
                timestep += 1     

                   
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