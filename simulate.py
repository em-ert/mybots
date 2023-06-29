import pyrosim.pyrosim as pyrosim
from simulation import SIMULATION
import sys

directOrGUI = sys.argv[1]
solutionID = sys.argv[2]
showBest = sys.argv[3]
simulation = SIMULATION(directOrGUI, solutionID, showBest)
simulation.Run(solutionID)


"""
parser = argparse.ArgumentParser()

parser.add_argument("directOrGUI", help="Display mode: 'GUI' or 'DIRECT'", choices=['GUI', 'DIRECT'], default="DIRECT")

parser.add_argument("id", help="ID of the solution to be simulated", type=int)

parser.add_argument("show_best", help="Whether or not the simulation is showing a best solution - relevant while running", type=bool, default=False)

args = parser.parse_args()

# numpy.save("data/sinusoidalValues", targetAngles)
# exit()
numpy.save("data/backLegSensorValues", backLegSensorValues)
numpy.save("data/frontLegSensorValues", frontLegSensorValues)
numpy.save("data/sinusoidalValues", c.targetAngles)
"""