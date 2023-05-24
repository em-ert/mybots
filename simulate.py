import pyrosim.pyrosim as pyrosim
from simulation import SIMULATION
import sys

directOrGUI = sys.argv[1]
simulation = SIMULATION(directOrGUI)
simulation.Run()
simulation.Get_Fitness()

"""
# numpy.save("data/sinusoidalValues", targetAngles)
# exit()
numpy.save("data/backLegSensorValues", backLegSensorValues)
numpy.save("data/frontLegSensorValues", frontLegSensorValues)
numpy.save("data/sinusoidalValues", c.targetAngles)
"""