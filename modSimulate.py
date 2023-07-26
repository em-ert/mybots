from historian import HISTORIAN
import pyrosim.pyrosim as pyrosim
from modSimulation import MOD_SIMULATION
import sys

origID = sys.argv[1]
historian = HISTORIAN()
uniqueID = historian.uniqueID
setup = MOD_SIMULATION("DIRECT", origID, uniqueID, "True")
setup.Run()

fitness = setup.Get_Robot_Fitness()
solutionID = setup.Get_Robot_SolutionID()

simulation = MOD_SIMULATION("GUI", origID, uniqueID, "True")
simulation.Replay_Run()

historian.Archive_Run_Info(solutionID=solutionID, bestFitness=fitness)
historian.Run_Analysis(fitness=False, steps=True)