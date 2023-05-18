import math
import numpy
import pybullet as p
import pybullet_data
import pyrosim.pyrosim as pyrosim
import random
import time

simSteps = 1000

BackLeg_Amplitude = (numpy.pi / 4)
BackLeg_Frequency = 6
BackLeg_PhaseOffset =  (numpy.pi / 4)
BackLeg_TargetAngles = numpy.linspace(0, 2 * numpy.pi, simSteps)
BackLeg_TargetAngles = BackLeg_Amplitude * numpy.sin(BackLeg_Frequency * BackLeg_TargetAngles + BackLeg_PhaseOffset)

FrontLeg_Amplitude = (numpy.pi / 4)
FrontLeg_Frequency = 10
FrontLeg_PhaseOffset = 0
FrontLeg_TargetAngles = numpy.linspace(0, 2 * numpy.pi, simSteps)
FrontLeg_TargetAngles = FrontLeg_Amplitude * numpy.sin(FrontLeg_Frequency * FrontLeg_TargetAngles + FrontLeg_PhaseOffset)

physicsClient = p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())

p.setGravity(0, 0, -9.8)
planeId = p.loadURDF("plane.urdf")
robotId = p.loadURDF("body.urdf")

p.loadSDF("world.sdf")
pyrosim.Prepare_To_Simulate(robotId)

backLegSensorValues = numpy.zeros(simSteps)
frontLegSensorValues = numpy.zeros(simSteps)

# numpy.save("data/sinusoidalValues", targetAngles)
# exit()
for i in range(simSteps):
    p.stepSimulation()
    backLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("BackLeg")
    frontLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("FrontLeg")
    pyrosim.Set_Motor_For_Joint(
        bodyIndex=robotId,
        jointName=b'Torso_BackLeg',
        controlMode=p.POSITION_CONTROL,
        targetPosition=BackLeg_TargetAngles[i],
        maxForce=8)
    pyrosim.Set_Motor_For_Joint(
        bodyIndex=robotId,
        jointName=b'Torso_FrontLeg',
        controlMode=p.POSITION_CONTROL,
        targetPosition=FrontLeg_TargetAngles[i],
        maxForce=8)
    time.sleep(0.00166)
    print(i)
numpy.save("data/backLegSensorValues", backLegSensorValues)
numpy.save("data/frontLegSensorValues", frontLegSensorValues)
numpy.save("data/sinusoidalValues", targetAngles)

p.disconnect()
