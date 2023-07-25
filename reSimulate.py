import pyrosim.pyrosim as pyrosim
from simulation import SIMULATION
import sys

uniqueID = sys.argv[1]
simulation = SIMULATION("GUI", uniqueID, "True")
simulation.Replay_Run()