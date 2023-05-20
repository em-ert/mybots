import constants as c
import math
import numpy
import pybullet as p
import pybullet_data
import pyrosim.pyrosim as pyrosim
import random
from simulation import SIMULATION
import time

simulation = SIMULATION()
simulation.Run()

"""
# numpy.save("data/sinusoidalValues", targetAngles)
# exit()
numpy.save("data/backLegSensorValues", backLegSensorValues)
numpy.save("data/frontLegSensorValues", frontLegSensorValues)
numpy.save("data/sinusoidalValues", c.targetAngles)
"""