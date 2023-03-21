import matplotlib.pyplot as ax
import numpy as numpy

backLegSensorValues = numpy.load("data/backLegSensorValues.npy")
frontLegSensorValues = numpy.load("data/frontLegSensorValues.npy")

backLeg, = ax.plot(backLegSensorValues, label='Back Leg', linewidth="3")
frontLeg, = ax.plot(frontLegSensorValues, label='Front Leg')
ax.legend(handles=[backLeg, frontLeg])
ax.show()