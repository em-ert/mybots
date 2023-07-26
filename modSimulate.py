import constants as c
from historian import HISTORIAN
import os
import pyrosim.pyrosim as pyrosim
from modSimulation import MOD_SIMULATION
import time
from solution import SOLUTION
import sys

origID = sys.argv[1]
historian = HISTORIAN()
uniqueID = historian.uniqueID
setup = MOD_SIMULATION("DIRECT", origID, uniqueID, "True")
setup.Run()

fitness = setup.Get_Robot_Fitness()
solutionID = setup.Get_Robot_SolutionID()

brainLoc = "bestRuns/{}sols_{}gens/run{}".format(c.POPULATION_SIZE, c.NUMBER_OF_GENERATIONS, origID) + "/brain" + solutionID + ".nndf"

newLoc = "bestRuns/{}sols_{}gens/run{}".format(c.POPULATION_SIZE, c.NUMBER_OF_GENERATIONS, uniqueID) + "/brain" + solutionID + ".nndf"

os.system("cp " + brainLoc + " " + newLoc)

while not os.path.exists(newLoc):
    time.sleep(c.SLEEP_TIME)

historian.Archive_Run_Info(solutionID=solutionID, bestFitness=fitness)
historian.Run_Analysis(fitness=False, steps=True)

simulation = MOD_SIMULATION("GUI", origID, uniqueID, "True")
simulation.Replay_Run()