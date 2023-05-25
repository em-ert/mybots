import pyrosim.pyrosim as pyrosim
from simulation import SIMULATION
import sys

directOrGUI = sys.argv[1]
solutionID = sys.argv[2]
simulation = SIMULATION(directOrGUI, solutionID)
simulation.Run()
simulation.Get_Fitness(solutionID)

"""
# numpy.save("data/sinusoidalValues", targetAngles)
# exit()
numpy.save("data/backLegSensorValues", backLegSensorValues)
numpy.save("data/frontLegSensorValues", frontLegSensorValues)
numpy.save("data/sinusoidalValues", c.targetAngles)
"""