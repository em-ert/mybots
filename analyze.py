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
    def Run_Analysis(path, fitness=True, steps=True, bar=True, waterfall=True):
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
        for i in range(c.SIM_STEPS * len(c.TEMPOS)):
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

            fig, ax = plt.subplots(1, 2, sharey=True, figsize = (10,5))
            plt.legend()
            y = maxFitnesses
            x = np.arange(len(y))
            ax[0].xaxis.set_major_locator(ticker.MultipleLocator(base=10))
            ax[0].plot(x, y)
            ax[0].set_xlim(0, len(y)-1)
            ax[0].set_ylabel("Fitness")
            ax[0].set_xlabel("Generation")
            ax[0].set_title("Evolution over generations")

            # Modified for specific random data
            randAgeFitnessArray = np.load(path + "data/random_age_fitness_values.npy")
            ageFitnessArray = np.load(path + "data/age_fitness_values.npy")
            bestFitness = np.amax(ageFitnessArray[c.NUMBER_OF_GENERATIONS - 1, :, :], axis=0)[0]
            ax[1].barh(bestFitness, label="Best Solution", color = "red", height=0.002, width=2, alpha=1.0)
            randSolutions = randAgeFitnessArray[:, 0]
            ax[1].hist(randSolutions, label="Random Solutions", bins=30, orientation="horizontal", alpha=0.5)
            fig.legend()
            plt.gca().set(title='Frequency Histogram', xlabel='Count')
            ax[1].set_title("Distribution of Random Bots")

            plt.savefig(path + "plots/Fitness.png")

        if steps == True:
            fig, ax1 = plt.subplots(figsize=(15, 4))
            metronome, = ax1.eventplot(metronomeClick, label='Metronome', color='gray', linelengths=4)

            backLeg, = ax1.eventplot(backLegTouch, label='Back Leg', color='red', lineoffsets=2.5, linewidths=2)
            frontLeg, = ax1.eventplot(frontLegTouch, label='Front Leg', color='green', lineoffsets=1.5, linewidths=2)
            leftLeg, = ax1.eventplot(leftLegTouch, label='Left Leg', color='orange', lineoffsets=0.5, linewidths=2)
            rightLeg, = ax1.eventplot(rightLegTouch, label='Right Leg', color='blue', lineoffsets=-0.5, linewidths=2)
            ax1.legend(handles=[metronome, backLeg, frontLeg, leftLeg, rightLeg], bbox_to_anchor=(1.1, 1))
            ax1.set_xlim(-5, (c.SIM_STEPS * len(c.TEMPOS)) + 5)
            ax1.xaxis.set_major_locator(ticker.MultipleLocator(base=100))
            ax1.set_ylim(-1, 3)
            ax1.set_yticks([], [])
            ax1.set_ylabel(None)
            ax1.set_xlabel("Timesteps")
            ax1.set_xmargin(2)
            ax1.set_title("Steps vs Metronome Strikes")

            plt.savefig(path + "plots/Steps.png")

        if bar == True:
            fig, ax1 = plt.subplots(figsize=(7,7))
            
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
                roundedFit = round(np.cos(((2*np.pi)/c.MET_FRAME_RATIO)*i), 3)
                legend_labels.append(str(roundedFit))

            blue = Color("blue")
            colors = list(blue.range_to(Color("yellow"),int(c.MET_FRAME_RATIO/2)))
            colors = [color.rgb for color in colors]
            colorsRev = colors[: : -1]
            colors = np.concatenate((colors, colorsRev), axis=0)

            ax1.bar(bar_labels, bars, label=legend_labels, color=colors)
            fig.legend(title='Valuation', bbox_to_anchor=(1, 1))
            ax1.set_ylabel('Total number of Steps')
            ax1.set_xlabel('Number of sim. steps after or before metronome strike')
            ax1.set_title("Distribution of solution's steps across musical bar")

            plt.savefig(path + "plots/Bar.png")

        if waterfall == True:
            ageFitnessArray = np.load(path + "data/age_fitness_values.npy")
            line_hist = []
            ageFitDict = {}
            # Iterate through all generations
            for gen in range(c.NUMBER_OF_GENERATIONS + 1):
                if gen == c.NUMBER_OF_GENERATIONS:
                    ageFitDict[gen] = {}
                else:
                    # Create a preliminary entry with lowest possible fitness.
                    ageFitDict[gen] = {1: 0}
                
                    # For each individual in the generation, save the fitness info
                    for i in range(c.POPULATION_SIZE):
                        currFitness = ageFitnessArray[gen, i, 0]
                        currAge = int(ageFitnessArray[gen, i, 1])

                        # If an individual of this age is not found in this generation yet or the individual is more 
                        # fit than the stored individual, replace the data with that of the current individual
                        if currAge not in ageFitDict[gen] or currFitness > ageFitDict[gen][currAge]:
                            ageFitDict[gen][currAge] = currFitness  # Fittest individual of its age 

                if gen > 0:
                    # For each parent generation
                    for age in ageFitDict[gen - 1]:
                        # Find extinct lineages - if no individual from that age group moved on, or if we are on the final generation
                        if (age + 1) not in ageFitDict[gen] or gen == c.NUMBER_OF_GENERATIONS:
                            # Start a 'lineage'
                            currLine = []
                            n = 0
                            # Iterate through the age fitness dictionary and add individuals to line
                            while age - n > 0:
                                currLine += [ageFitDict[gen-1-n][age-n]]
                                n += 1
                            # (Age - 1) to adjust for 1 indexed ages    
                            prefill = [None]*(gen - int(age - 1))
                            line_hist.append(prefill + currLine[::-1])


            fig, ax = plt.subplots(1, 1, figsize=(7, 5))

            for line in line_hist:
                ax.plot(range(len(line)), line, linewidth=0.8)
            plt.xlabel("Age in Generations")
            plt.ylabel("Fitness")
            plt.title('Rainbow Waterfall Plot')
            plt.savefig(path + "plots/Waterfall.png") 


"""
list = [213, 214, 220, 221, 222]
for i in range(len(list)):
    ANALYZE.Run_Analysis("bestRuns/40sols_50gens/run" + str(list[i]) + "/", bar=False)
"""
# ANALYZE.Run_Analysis("bestRuns/100sols_70gens/run17/", bar=False)