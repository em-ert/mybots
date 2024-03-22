from bots.capsuleBot import CAPSULE_BOT
import constants as c
import os
import pickle
import math
import string
import pybullet as p
from pyrosim.neuralNetwork import NEURAL_NETWORK
import pyrosim.pyrosim as pyrosim
from sensor import SENSOR
import sys
from metronomeSensor import METRONOME_SENSOR
from motor import MOTOR
import numpy as np


class ROBOT:
    def __init__(self, solutionID):
        self.robotId = p.loadURDF("body.urdf")
        self.motors = {}
        self.sensors = {}

        bot = CAPSULE_BOT()
        self.joints = bot.joints

        self.nn = NEURAL_NETWORK("brain" + str(solutionID) + ".nndf")

        self.previousLocation = [0, 0]
        self.totalDistance = 0
        self.fitness = 0
        self.fitness2 = 0
        self.numClicks = 0
        self.maxFitness = 0

        # TODO: Modify and incorporate this into fitness function calculation
        self.storedSteps = np.zeros(sum(c.FRAMES_PER_TEMPO))
        self.storedDistances = np.zeros(sum(c.FRAMES_PER_TEMPO))

        pyrosim.Prepare_To_Simulate(self.robotId)
        self.Prepare_To_Act()
        self.Prepare_To_Sense()
        self.Prepare_To_Sense_Audio()

        os.system("rm brain" + str(solutionID) + ".nndf")

    # REVIEW: [1.5] Edit fitness function here
    def Get_Fitness(self, solutionID):
        if c.OPTIMIZE_AGE == False and c.SECOND_OBJ == "DISTANCE":
            stateOfLinkZero = p.getLinkState(self.robotId, 0)
            positionOfLinkZero = stateOfLinkZero[0]
            xCoordinateOfLinkZero = positionOfLinkZero[0]
            yCoordinateOfLinkZero = positionOfLinkZero[1]
            self.fitness2 = math.sqrt((xCoordinateOfLinkZero**2) + (yCoordinateOfLinkZero**2))

        if c.OPTIMIZE_AGE == False and c.SECOND_OBJ == "SYMMETRY":
            for sensor in self.sensors:
                for sensorB in self.sensors:
                    if self.sensors[sensor].name < self.sensors[sensorB].name:
                        self.fitness2 += -1 * abs(self.sensors[sensor].numSteps - self.sensors[sensorB].numSteps)

        if c.OPTIMIZE_AGE == False and c.SECOND_OBJ == "DUAL":  
            #  !--- CALCULATE BALANCE ---!
            balanceScore = 0
            numActiveSensors = 0
            for sensor in self.sensors:
                if sensor != self.sensors["RightLower"] and sensor.endswith("Lower"):
                   numActiveSensors += 1
                   balanceScore += abs(self.sensors["RightLower"].numSteps - self.sensors[sensor].numSteps)
                   
            # Take average and add 1
            balanceScore = (balanceScore / numActiveSensors) + 1
            # Scale so 1 is the max
            balanceScore = 1 / balanceScore

            # !--- CALCULATE DISTANCE ---!
            # Calculate how closely the robot was to the distance goal
            # Post-process steps to find fitnesses
            distanceScore = 0
            frameStartIndex = 0
            # Perform for each tempo...
            for i in range(len(c.TEMPOS)):
                # Get number of frames per beat for the tempo
                framesPerBeat = c.FRAMES_PER_BEAT[i]
                # Isolate region of data relevant to the current tempo - the current 'condition'
                conditionDistData = self.storedDistances[frameStartIndex : frameStartIndex + c.FRAMES_PER_TEMPO[i]]
                conditionDistData = np.reshape(conditionDistData, (c.CLICKS_PER_TEMPO, framesPerBeat))
                distancePerClick = np.sum(conditionDistData, axis = 1)
                # Add 1 point for each spot distance is goal amount
                metGoalDistance = distancePerClick[distancePerClick >= c.TRAVEL_PER_CLICK_GOAL]
                distanceScore += len(metGoalDistance)
                # Otherwise add sqrt(real/goal)
                belowGoalDistance = distancePerClick[distancePerClick < c.TRAVEL_PER_CLICK_GOAL]
                belowGoalDistance = belowGoalDistance / c.TRAVEL_PER_CLICK_GOAL
                distanceScore += sum(np.sqrt(belowGoalDistance))
                self.numClicks += len(distancePerClick)
            # Find average
            distanceScore = distanceScore / self.numClicks   
            
            # !--- CALCULATE POINTS ---!
            # Post-process steps to find fitnesses
            frameStartIndex = 0
            # Perform for each tempo...
            for i in range(len(c.TEMPOS)):
                # Get number of frames per beat for the tempo
                framesPerBeat = c.FRAMES_PER_BEAT[i]
                # Isolate region of full data relevant to the current tempo - the current 'condition'
                conditionData = self.storedSteps[frameStartIndex : frameStartIndex + c.FRAMES_PER_TEMPO[i]]
                conditionData = np.reshape(conditionData, (c.CLICKS_PER_TEMPO, framesPerBeat))
                # Create an array containing a single period worth of cosine values
                period = framesPerBeat
                amplitude = framesPerBeat / 2
                offset = framesPerBeat / 2
                cosPointsArray = np.linspace(0, period, period + 1)
                cosPointsArray = cosPointsArray[0: period] 
                cosPointsArray = amplitude * np.cos(((2*np.pi)/period) * cosPointsArray) + offset
                # Multiply each row in conditionData by cosPointsArray 
                conditionData = np.multiply(conditionData, cosPointsArray)
                # Flatten it back into one row
                conditionData = conditionData.flatten()
            
                # Iterate through the arrays to find points values
                remaining = c.FRAMES_PER_TEMPO[i]
                startIndex = 0
                tempFitness = np.max(conditionData[startIndex : math.ceil(period / 2)])
                # If more steps than one, decrease score by 25%
                if tempFitness < np.sum(conditionData[startIndex : math.ceil(period / 2)]):
                    self.fitness += tempFitness * (1 - c.DOUBLE_STEP_PUNISHMENT)
                else:
                    self.fitness += tempFitness
                startIndex = math.ceil(period / 2)
                remaining -= (startIndex - 1)
                self.maxFitness += (amplitude + offset)
                while remaining > 0:
                    # If not a full amount remain to be processed
                    if remaining < period:
                        # For each extra step, detract amount specified in constants
                        regionOfInterest = conditionData[startIndex : startIndex + remaining]
                        tempFitness = np.max(regionOfInterest)
                        if tempFitness < np.sum(regionOfInterest):
                            numExtraSteps = len(regionOfInterest[regionOfInterest > 0]) - 1
                            self.fitness += tempFitness * (1 - (c.DOUBLE_STEP_PUNISHMENT * (numExtraSteps**2)))
                        else:
                            self.fitness += tempFitness  
                    # If a normal number of steps remain to be processed        
                    else:
                        regionOfInterest = conditionData[startIndex : startIndex + period]
                        tempFitness = np.max(regionOfInterest)
                        self.maxFitness += (amplitude + offset)
                        # If more steps than one, decrease score by double step punishment%
                        if tempFitness < np.sum(regionOfInterest):
                            numExtraSteps = len(regionOfInterest[regionOfInterest > 0]) - 1
                            self.fitness += tempFitness * (1 - (c.DOUBLE_STEP_PUNISHMENT * (numExtraSteps**2)))
                        else:
                            self.fitness += tempFitness
                    startIndex += period
                    remaining -= period 


            scaledRhythmFitness = (self.fitness / self.maxFitness)
            self.fitness = scaledRhythmFitness
            if scaledRhythmFitness > 0.97:
                self.fitness += distanceScore

            self.fitness2 = balanceScore

            print(str(self.fitness) + "," + str(self.fitness2), file=sys.stderr)    
        
        # NOTE: Here is where I print the fitness to stderr    
        if c.OPTIMIZE_AGE == True:
            #  !--- CALCULATE BALANCE ---!
            balanceScore = 0
            numActiveSensors = 0
            for sensor in self.sensors:
                if sensor != self.sensors["RightLower"] and sensor.endswith("Lower"):
                   numActiveSensors += 1
                   balanceScore += (self.sensors["RightLower"].numSteps - self.sensors[sensor].numSteps)**2
                   
            # Take average and add 1
            balanceScore = (balanceScore / numActiveSensors) + 1
            # Scale so 1 is the max
            balanceScore = 1 / math.sqrt(balanceScore)

            # !--- CALCULATE DISTANCE ---!
            # Calculate how closely the robot was to the distance goal
            # Post-process steps to find fitnesses
            distanceScore = 0
            frameStartIndex = 0
            # Perform for each tempo...
            for i in range(len(c.TEMPOS)):
                # Get number of frames per beat for the tempo
                framesPerBeat = c.FRAMES_PER_BEAT[i]
                # Isolate region of data relevant to the current tempo - the current 'condition'
                conditionDistData = self.storedDistances[frameStartIndex : frameStartIndex + c.FRAMES_PER_TEMPO[i]]
                conditionDistData = np.reshape(conditionDistData, (c.CLICKS_PER_TEMPO, framesPerBeat))
                distancePerClick = np.sum(conditionDistData, axis = 1)
                # Add 1 point for each spot distance is goal amount
                metGoalDistance = distancePerClick[distancePerClick >= c.TRAVEL_PER_CLICK_GOAL]
                distanceScore += len(metGoalDistance)
                # Otherwise add sqrt(real/goal)
                belowGoalDistance = distancePerClick[distancePerClick < c.TRAVEL_PER_CLICK_GOAL]
                belowGoalDistance = belowGoalDistance / c.TRAVEL_PER_CLICK_GOAL
                distanceScore += sum(np.sqrt(belowGoalDistance))
                self.numClicks += len(distancePerClick)
            # Find average
            distanceScore = distanceScore / self.numClicks   
            
            # !--- CALCULATE POINTS ---!
            # Post-process steps to find fitnesses
            frameStartIndex = 0
            # Perform for each tempo...
            for i in range(len(c.TEMPOS)):
                # Get number of frames per beat for the tempo
                framesPerBeat = c.FRAMES_PER_BEAT[i]
                # Isolate region of full data relevant to the current tempo - the current 'condition'
                conditionData = self.storedSteps[frameStartIndex : frameStartIndex + c.FRAMES_PER_TEMPO[i]]
                conditionData = np.reshape(conditionData, (c.CLICKS_PER_TEMPO, framesPerBeat))
                # Create an array containing a single period worth of cosine values
                period = framesPerBeat
                amplitude = framesPerBeat / 2
                offset = framesPerBeat / 2
                cosPointsArray = np.linspace(0, period, period + 1)
                cosPointsArray = cosPointsArray[0: period] 
                cosPointsArray = amplitude * np.cos(((2*np.pi)/period) * cosPointsArray) + offset
                # Multiply each row in conditionData by cosPointsArray 
                conditionData = np.multiply(conditionData, cosPointsArray)
                # Flatten it back into one row
                conditionData = conditionData.flatten()
            
                # Iterate through the arrays to find points values
                remaining = c.FRAMES_PER_TEMPO[i]
                startIndex = 0
                regionOfInterest = conditionData[startIndex : math.ceil(period / 2)]
                tempFitness = np.max(regionOfInterest)
                # If more steps than one, decrease score
                if tempFitness < np.sum(regionOfInterest):
                    numExtraSteps = len(regionOfInterest[regionOfInterest > 0]) - 1
                    self.fitness += tempFitness * (1 - (c.DOUBLE_STEP_PUNISHMENT * (numExtraSteps**2)))
                else:
                    self.fitness += tempFitness
                startIndex = math.ceil(period / 2)
                remaining -= (startIndex - 1)
                self.maxFitness += (amplitude + offset)
                while remaining > 0:
                    # If not a full amount remain to be processed
                    if remaining < period:
                        # For each extra step, detract amount specified in constants
                        regionOfInterest = conditionData[startIndex : startIndex + remaining]
                        tempFitness = np.max(regionOfInterest)
                        if tempFitness < np.sum(regionOfInterest):
                            numExtraSteps = len(regionOfInterest[regionOfInterest > 0]) - 1
                            self.fitness += tempFitness * (1 - (c.DOUBLE_STEP_PUNISHMENT * (numExtraSteps**2)))
                        else:
                            self.fitness += tempFitness  
                    # If a normal number of steps remain to be processed        
                    else:
                        regionOfInterest = conditionData[startIndex : startIndex + period]
                        tempFitness = np.max(regionOfInterest)
                        self.maxFitness += (amplitude + offset)
                        # If more steps than one, decrease score by double step punishment%
                        if tempFitness < np.sum(regionOfInterest):
                            numExtraSteps = len(regionOfInterest[regionOfInterest > 0]) - 1
                            self.fitness += tempFitness * (1 - (c.DOUBLE_STEP_PUNISHMENT * (numExtraSteps**2)))
                        else:
                            self.fitness += tempFitness
                    startIndex += period
                    remaining -= period 
            scaledRhythmFitness = (self.fitness / self.maxFitness)

            self.fitness = scaledRhythmFitness * balanceScore * distanceScore

            # calculatedFitness = scaledRhythmFitness * balanceScore * distanceScore
            print(f"{self.fitness}, {scaledRhythmFitness}, {balanceScore}, {distanceScore}", file=sys.stderr)
        else:
            print(str(self.fitness) + "," + str(self.fitness2), file=sys.stderr)


    def Prepare_To_Sense(self):
        self.sensors = {}
        sensor_name = 0
        for linkName in pyrosim.linkNamesToIndices:
            self.sensors[linkName] = SENSOR(linkName, sensor_name)
            sensor_name += 1


    def Prepare_To_Sense_Audio(self):
        self.metronomeSensor = METRONOME_SENSOR(0)


    def Prepare_To_Act(self):
        self.motors = {}
        for jointName in pyrosim.jointNamesToIndices:
            self.motors[jointName] = MOTOR(jointName, hollow=False)


    #REVIEW - [1] Edit fitness function here + stepsToClick v. framesPerBeat
    def Sense(self, timestep, framesPerBeat, metInfo):
        stepValue = 0
        for sensor in self.sensors:
            curr_sensor = self.sensors[sensor]
            curr_sensor.Get_Value(timestep)
            stepValue = curr_sensor.Get_Step(timestep)

            if curr_sensor == self.sensors["RightLower"] and stepValue > 0:
                self.storedSteps[timestep] = stepValue

            """
            if metInfo == framesPerBeat:
                self.numClicks += 1
                self.maxFitness += framesPerBeat

            # Look at movement of only one leg - POINTS
            if curr_sensor == self.sensors["RightLower"] and stepValue > 0:
                # Adjust subdivision for graphing (1 index to 0)
                metInfo -= 1
                # Reward the first step of any leg when the metronome strikes
                if self.storedSteps[self.numClicks] == 0:
                    self.storedSteps[self.numClicks] = stepValue
                    self.fitness += (framesPerBeat * np.cos(((2*np.pi)/framesPerBeat) * metInfo))
            """
            """
            # Reward the first step of any leg when the metronome strikes
            if stepValue > 0 and metInfo == 1 and self.storedSteps[timestep] == 0:
                self.storedSteps[timestep] = stepValue
                self.fitness += (framesPerBeat * np.cos(((2*np.pi)/framesPerBeat) * metInfo))
            elif stepValue > 0 and metInfo == 1 and self.storedSteps[timestep] != 0:
                self.fitness -= stepValue
            elif stepValue > 0 and metInfo % 1 == 0 and self.storedSteps[timestep] == 0:
                self.storedSteps[timestep] = stepValue
                self.fitness += stepValue * 2
            elif stepValue > 0 and metInfo % 1 == 0 and self.storedSteps[timestep] != 0:
                self.fitness -= stepValue   
            elif stepValue > 0 and metInfo % 1 != 0:
                self.fitness -= stepValue * 2   
            """    

        # For distance - Use this to scale 
        stateOfLinkZero = p.getLinkState(self.robotId, 0)
        positionOfLinkZero = stateOfLinkZero[0]
        currentLocation = [positionOfLinkZero[0], positionOfLinkZero[1]]
        self.storedDistances[timestep] = abs(math.dist(currentLocation, self.previousLocation))
        # self.totalDistance += abs(math.dist(currentLocation, self.previousLocation))
        self.previousLocation = currentLocation

        """
        if curr_sensor == self.sensors["RightLower"] and stepValue > 0:
            self.fitness += (framesPerBeat * np.cos(((2*np.pi)/framesPerBeat)*timestep)) 
        """     

        """stepValue = 0
        for sensor in self.sensors:
            curr_sensor = self.sensors[sensor]
            curr_sensor.Get_Value(timestep)
            step = curr_sensor.Get_Step(timestep)
            stepValue += step

        if c.FIT_FUNCTION == "COS":
            if stepValue > 0:
                self.fitness += (framesPerBeat * np.cos(((2*np.pi)/framesPerBeat)*timestep))

        elif c.FIT_FUNCTION == "EXP":
            if metInfo >= 0 and stepValue > 0:    
                self.fitness += (((2-metInfo)**2)+0.5)

        elif c.FIT_FUNCTION == "EXP_PUNISH":
            if metInfo >= 0 and stepValue > 0:    
                self.fitness += (((2-metInfo)**2)+0.5)
            else:
                self.fitness -= stepValue * 0.5

        else:
            raise Exception("Fitness function error") """       
        
            
    def Sense_Rhythm(self, timestep, click):
        self.metronomeSensor.Get_Value(timestep, click)
        
        """
        for link in ["FrontLower", "BackLower", "LeftLower", "RightLower"]:
            linkIndex = pyrosim.linkNamesToIndices[link]
            linkState = p.getLinkState(self.robotId, linkIndex, 1)
            linkVelocities = linkState[6]
            totalChange = 0
            for velocity in linkVelocities:
                totalChange += velocity
            self.fitness += totalChange * click
        """    

    def Act(self):
        for neuronName in self.nn.Get_Neuron_Names():
            if self.nn.Is_Motor_Neuron(neuronName):
                jointName = self.nn.Get_Motor_Neurons_Joint(neuronName)
                jointName = bytes(jointName, 'UTF-8')
                desiredAngle = self.nn.Get_Value_Of(neuronName) * c.MOTOR_JOINT_RANGE
                self.motors[jointName].Set_Value(self, desiredAngle)


    def Act_And_Save(self, timestep):
        for neuronName in self.nn.Get_Neuron_Names():
            if self.nn.Is_Motor_Neuron(neuronName):
                jointName = self.nn.Get_Motor_Neurons_Joint(neuronName)
                jointName = bytes(jointName, 'UTF-8')
                desiredAngle = self.nn.Get_Value_Of(neuronName) * c.MOTOR_JOINT_RANGE
                self.motors[jointName].Set_And_Save_Value(self, desiredAngle, timestep)
            
                # print("Name=" + neuronName + ", Joint=" + jointName  + ", Angle=" + str(desiredAngle))


    def Set_Unique_ID_And_Path(self, uniqueID):
        self.uniqueID = uniqueID
        self.path = "bestRuns/{}sols_{}gens/run{}".format(c.POPULATION_SIZE, c.NUMBER_OF_GENERATIONS, self.uniqueID) + "/"


    def Save_Motor_Values(self):
        motorValues = {}
        for neuronName in self.nn.Get_Neuron_Names():
            if self.nn.Is_Motor_Neuron(neuronName):
                jointName = self.nn.Get_Motor_Neurons_Joint(neuronName)
                jointName = bytes(jointName, 'UTF-8')
                motorValues[jointName] = self.motors[jointName].storedValues
        # Pickled values
        with open(self.path + "pickles/motorValues.pickle", "wb") as f:
            pickle.dump(motorValues, f, pickle.HIGHEST_PROTOCOL)


    def Save_Sensor_Values(self):
        sensorValues = {}
        # Data values
        for neuronName in self.nn.Get_Neuron_Names():
            if len(sensorValues) == c.NUM_SENSOR_NEURONS:
                break
            linkName = None
            if self.nn.Is_Sensor_Neuron(neuronName):
                linkName = self.nn.Get_Sensor_Neurons_Link(neuronName)
                for joint in self.joints:
                    if joint.child == linkName:
                        joint_for_sensor = joint.name
                        sensorValues[joint_for_sensor] = self.sensors[linkName].values
                        self.sensors[linkName].Save_Values(self.path)
                        break
        # Pickle Values
        with open(self.path + "pickles/sensorValues.pickle", "wb") as f:
            pickle.dump(sensorValues, f, pickle.HIGHEST_PROTOCOL)


    # Data values
    def Save_Metronome_Sensor_Values(self):
        self.metronomeSensor.Save_Values(self.path)


    def Think(self, click):
        self.nn.Update(click)
        # self.nn.Print()