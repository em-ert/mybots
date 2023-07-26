from colour import Color
import constants as c
import datetime
import matplotlib.pyplot as plt
from matplotlib import ticker
from matplotlib import cm
import numpy as np
import os
import time

class ANALYZE:
    def __init__():
        pass

    @staticmethod  
    def Run_Analysis(path, fitness=True, steps=True, bar=True):
        now = datetime.datetime.now()

        while not os.path.exists(path + "data/BackLower_sensor_values.npy"):
            time.sleep(c.SLEEP_TIME)
        backLegSensor = np.load(path + "data/BackLower_sensor_values.npy")
        frontLegSensor = np.load(path + "data/FrontLower_sensor_values.npy")
        leftLegSensor = np.load(path + "data/LeftLower_sensor_values.npy")
        rightLegSensor = np.load(path + "data/RightLower_sensor_values.npy")
        metronomeSensor = np.load(path + "data/metronome_sensor_values.npy")

        backLegTouch = []
        frontLegTouch = []
        rightLegTouch = []
        leftLegTouch = []
        metronomeClick = []
        for i in range(c.SIM_STEPS):
            if backLegSensor[i] == 1 and backLegSensor[i-1] == -1:
                backLegTouch.append(i+1)
            if frontLegSensor[i] == 1 and frontLegSensor[i-1] == -1:
                frontLegTouch.append(i+1)
            if leftLegSensor[i] == 1 and leftLegSensor[i-1] == -1:
                leftLegTouch.append(i+1)
            if rightLegSensor[i] == 1 and rightLegSensor[i-1] == -1:
                rightLegTouch.append(i+1)
            if metronomeSensor[i] == 1:
                metronomeClick.append(i+1)

        np.trim_zeros(backLegTouch)
        np.trim_zeros(frontLegTouch)
        np.trim_zeros(leftLegTouch)
        np.trim_zeros(rightLegTouch)
        np.trim_zeros(metronomeClick)

        if fitness == True:
            ageFitnessArray = np.load(path + "data/age_fitness_values.npy")

            # Create new empty list for best fitnesses
            maxFitnesses = np.zeros(c.NUMBER_OF_GENERATIONS)

            for i in range(c.NUMBER_OF_GENERATIONS):
                gen = ageFitnessArray[i, :, :]
                maxFitnesses[i] = np.amax(gen, axis=0)[0]
                # print(gen)
            # print(maxFitnesses)

            fig, ax2 = plt.subplots()
            y = maxFitnesses
            x = np.arange(len(y))
            ax2.xaxis.set_major_locator(ticker.MultipleLocator(base=10))
            ax2.plot(x, y)
            ax2.set_xlim(0, len(y)-1)
            ax2.set_ylabel("Fitness")
            ax2.set_xlabel("Generation")

            plt.savefig(path + "plots/Fitness.png")

        if steps == True:
            fig, ax1 = plt.subplots(figsize=(10, 4))
            metronome, = ax1.eventplot(metronomeClick, label='Metronome', color='gray', linelengths=4)

            backLeg, = ax1.eventplot(backLegTouch, label='Back Leg', color='red', lineoffsets=2.5, linewidths=2)
            frontLeg, = ax1.eventplot(frontLegTouch, label='Front Leg', color='green', lineoffsets=1.5, linewidths=2)
            leftLeg, = ax1.eventplot(leftLegTouch, label='Left Leg', color='orange', lineoffsets=0.5, linewidths=2)
            rightLeg, = ax1.eventplot(rightLegTouch, label='Right Leg', color='blue', lineoffsets=-0.5, linewidths=2)
            ax1.legend(handles=[metronome, backLeg, frontLeg, leftLeg, rightLeg])
            ax1.set_xlim(-5, c.SIM_STEPS+5)
            ax1.xaxis.set_major_locator(ticker.MultipleLocator(base=50))
            ax1.set_ylim(-1, 3)
            ax1.set_yticks([], [])
            ax1.set_ylabel(None)
            ax1.set_xlabel("Timesteps")
            ax1.set_xmargin(2)

            plt.savefig(path + "plots/Steps")

        if bar == True:
            fig, ax1 = plt.subplots()
            
            bars = np.zeros(int(c.MET_FRAME_RATIO), int)
            for i in range(len(backLegTouch)):
                subDiv = backLegTouch[i] % c.MET_FRAME_RATIO
                bars[subDiv] += 1
            for i in range(len(frontLegTouch)):
                subDiv = frontLegTouch[i] % c.MET_FRAME_RATIO
                bars[subDiv] += 1
            for i in range(len(leftLegTouch)):
                subDiv = leftLegTouch[i] % c.MET_FRAME_RATIO
                bars[subDiv] += 1
            for i in range(len(rightLegTouch)):
                subDiv = rightLegTouch[i] % c.MET_FRAME_RATIO
                bars[subDiv] += 1

            bar_labels = []
            for i in range(c.MET_FRAME_RATIO):
                bar_labels.append(str((c.MET_FRAME_RATIO/2)-i))
            legend_labels = []
            for i in range(c.MET_FRAME_RATIO):
                roundedFit = round(np.cos(((2*np.pi)/c.MET_FRAME_RATIO)*i)+0.5, 3)
                legend_labels.append(str(roundedFit))
            print(bars)
            print(bar_labels)
            print(legend_labels)

            blue = Color("blue")
            colors = list(blue.range_to(Color("yellow"),c.MET_FRAME_RATIO))
            colors = [color.rgb for color in colors]

            ax1.bar(bar_labels, bars, label=legend_labels, color=colors)
            ax1.set_ylabel('Number of Steps')
            ax1.set_xlabel('Simulation steps distance from metronome strike')
            ax1.set_title('Distribution of solution steps across musical bar')
            ax1.legend(title='Valuation')

            plt.savefig(path + "plots/Bar")


ANALYZE.Run_Analysis("bestRuns/30sols_100gens/run1/")