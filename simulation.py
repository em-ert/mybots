import constants as c
from historian import HISTORIAN
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
        else:
            self.physicsClient = p.connect(p.DIRECT)
            self.robot = ROBOT(solutionID)
            
        p.configureDebugVisualizer(p.COV_ENABLE_GUI,0)
        # Set up the rest of the sim's features
        p.setAdditionalSearchPath(pybullet_data.getDataPath())
        p.setGravity(0, 0, -9.8)
        self.world = WORLD()


    def __del__(self):
        p.disconnect()

    def Run(self, solutionID):
        # For standard runs
        if self.directOrGUI != "GUI" and self.showBest == "False":
            stepEnd = time.time() + (c.FRAME_RATE)
            p.stepSimulation()
            self.robot.Sense(0)
            for t in range(c.SIM_STEPS):
                if t % c.MET_FRAME_RATIO == 0:
                    click = 1                    
                else: 
                    click = -1
                self.robot.Think(click)
                self.robot.Act()
                self.robot.Sense_Rhythm(t, click)
                if t != c.SIM_STEPS - 1:
                    self.robot.Sense(t+1)
                    
                remaining = stepEnd - time.time()
                if remaining < 0:
                    raise Exception("Time error, ended with " + str(remaining) + " seconds")
                else: time.sleep(remaining)
                stepEnd = time.time() + c.FRAME_RATE
                p.stepSimulation()
            self.robot.Get_Fitness(solutionID)


        # Runs that save data in preparation for hollow runs
        # These runs additionally prep for data storage
        elif self.directOrGUI != "GUI" and self.showBest == "True":
            stepEnd = time.time() + c.FRAME_RATE
            p.stepSimulation()
            self.robot.Sense(0)
            for t in range(c.SIM_STEPS):
                if t % c.MET_FRAME_RATIO == 0:
                    click = 1
                else: 
                    click = -1
                self.robot.Think(click)
                self.robot.Act_And_Save(t)
                self.robot.Sense_Rhythm(t, click)
                if t != c.SIM_STEPS - 1:
                    self.robot.Sense(t+1)
                    
                remaining = stepEnd - time.time()
                if remaining < 0:
                    raise Exception("Time error, ended with " + str(remaining) + " seconds")
                else: time.sleep(remaining)
                stepEnd = time.time() + c.FRAME_RATE
                p.stepSimulation()

            # Get the unique ID from the historian and set in robot
            uniqueID = HISTORIAN.Get_Unique_Run_ID()
            self.robot.Set_Unique_ID_And_Path(uniqueID)
            # Save sensor and motor values for the future
            self.robot.Save_Motor_Values()
            self.robot.Save_Sensor_Values()
            self.robot.Save_Metronome_Sensor_Values()

        else:
            self.Replay_Run()

    
    def Replay_Run(self):
        metronome = media("sounds/metronome.mp3", streaming=False)
        stepEnd = time.time() + c.FRAME_RATE
        p.stepSimulation()
        for t in range(c.SIM_STEPS):
            if t % c.MET_FRAME_RATIO == 0:
                click = 1
                metronome.play()
            else: 
                click = -1
            self.robot.Act(t)
            remaining = stepEnd - time.time()
            if remaining < 0:
                raise Exception("Time error, ended with " + str(remaining) + " seconds")
            else: time.sleep(remaining)
            stepEnd = time.time() + c.FRAME_RATE
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
# print(t)