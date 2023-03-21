import numpy
import pybullet as p
import pybullet_data
import pyrosim.pyrosim as pyrosim
import time

simSteps = 100
physicsClient = p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())

p.setGravity(0, 0, -9.8)
planeId = p.loadURDF("plane.urdf")
robotId = p.loadURDF("body.urdf")

p.loadSDF("world.sdf")
pyrosim.Prepare_To_Simulate(robotId)

backLegSensorValues = numpy.zeros(simSteps)
frontLegSensorValues = numpy.zeros(simSteps)
for i in range(simSteps):
    p.stepSimulation()
    backLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("BackLeg")
    frontLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("FrontLeg")
    time.sleep(0.00166)
    print(i)
numpy.save("data/backLegSensorValues", backLegSensorValues)
numpy.save("data/frontLegSensorValues", frontLegSensorValues)

p.disconnect()
