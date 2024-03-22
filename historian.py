"""
The historian class manages bookkeeping for the study. It automatically:
    * Assigns each run a unique ID from which it can be identified
    * Generates graphs for each run
    * 
    * stores key aspects of each run needed for it to be repeated
    * 
"""
from analyze import ANALYZE
import constants as c
from datetime import datetime
import os

# TODO: Update the report to accurately represent constants

class HISTORIAN:
    def __init__(self):
        # Get a unique ID to associate with the run
        self.uniqueID = self.Get_And_Set_Unique_Run_ID()

        # Create folders to store run data
        path = "bestRuns/{}sols_{}gens/run{}".format(c.POPULATION_SIZE, c.NUMBER_OF_GENERATIONS, self.uniqueID)
        os.makedirs(path, exist_ok=False)

        # Add additional slash to path for use in full paths
        self.path = path + "/"
        os.makedirs(self.path + "data", exist_ok=False)
        os.makedirs(self.path + "pickles", exist_ok=False)
        os.makedirs(self.path + "plots", exist_ok=False)
    
    # This method collects all of the necessary information related to the run and stores it in a folder
    def Archive_Run_Info(self, solutionID, bestFitness):
        # Create the info file and write in the study details
        with open(self.path + "/info.txt", "w") as f:
            # Record time of run
            now = datetime.now()
            f.write(now.strftime("Time of run: %H:%M %p on %m/%d/%Y\n"))
            f.write(f"Random Seed: {c.SEED}\n")
            f.write(f"Additional Details: {c.ADDITIONAL_DETAILS}\n")
            f.write("\n")

            f.write("-----REVIEW COMMAND-----\n")
            f.write(f"python3 reSimulate.py GUI {self.uniqueID} True 2&>1\n")
            f.write("\n")

            f.write("-----OPTIMIZATION DETAILS-----\n")
            f.write(f"Fit. Function Type: {c.FIT_FUNCTION}\n")
            f.write(f"Optimize Age?: {c.OPTIMIZE_AGE}\n")
            f.write(f"2nd Objective: {c.SECOND_OBJ}\n")
            f.write(f"Travel Per Click Goal: {c.SECOND_OBJ}\n")
            f.write(f"Double Step Punishment: {c.DOUBLE_STEP_PUNISHMENT}\n")
            f.write(f"Num. Mutations: {c.NUM_MUTATIONS}\n")
            f.write(f"Num. Rand. Children: {c.NUM_RANDOM_CHILDREN}\n")
            f.write("\n")

            f.write("-----GENERAL DETAILS-----\n")
            f.write(f"Morphology: {c.BODY}\n")
            f.write(f"Pop. Size: {c.POPULATION_SIZE}\n")
            f.write(f"Num. Gens: {c.NUMBER_OF_GENERATIONS}\n")
            f.write(f"Num. Parallel Run Groups: {c.NUM_PARALLEL_RUN_GROUPS}\n")
            f.write(f"Sim Frequency: {c.SIM_FREQUENCY}\n")
            f.write(f"Num. Random Solutions Graphed: {c.NUM_RANDOM_SIMS_FOR_GRAPHING}\n")
            f.write("\n")

            f.write("-----RHYTHMIC DETAILS-----\n")
            f.write(f"Tempos: {c.TEMPOS}\n")
            f.write(f"Frame Rate: {c.FRAME_RATE}\n")
            f.write(f"Frames Per Beat: {c.FRAME_RATE}\n")
            f.write(f"Clicks Per Tempo: {c.CLICKS_PER_TEMPO}\n")
            f.write(f"Frames Per Tempo: {c.FRAMES_PER_TEMPO}\n")
            f.write("\n")

            f.write("-----NETWORK DETAILS-----\n")
            f.write(f"Sensor: {c.NUM_SENSOR_NEURONS}\n")
            f.write(f"Auditory: {c.NUM_AUDITORY_NEURONS}\n")
            f.write(f"Hidden: {c.NUM_HIDDEN_NEURONS}\n")
            f.write(f"Motor: {c.NUM_MOTOR_NEURONS}\n")
            f.write("\n")

            f.write("-----BEST SOLUTION-----\n")
            f.write(f"Soln. ID: {solutionID}\n")
            f.write(f"Fitness: {bestFitness}\n")
            f.write("\n")

    
    # Reads in the previous run ID from the last experiment, increments it, then writes it back to the file for the next run
    def Get_And_Set_Unique_Run_ID(self):
        idFile = "unique.txt"
        if os.path.exists(idFile):
            uniqueID = None
            with open(idFile,"r+") as f:
                # Get the previous unique ID
                prevID = int(f.readline())
                # Return the cursor to the beginning of the file and clear it
                f.seek(0)
                f.truncate()
                # Store current ID and save it to the file
                uniqueID = prevID + 1
                f.write(str(uniqueID))
            return uniqueID
        else:
            raise Exception("Unique ID file not found")
        
        
    @staticmethod
    def Get_Unique_Run_ID():
        idFile = "unique.txt"
        uniqueID = None
        if os.path.exists(idFile):
            with open(idFile,"r+") as f:
                # Get the next available unique ID
                uniqueID = int(f.readline())
            return uniqueID
        else:
            raise Exception("Unique ID file not found")
        
    
    # Generates graphs for the run and any additional analysis
    def Run_Analysis(self, fitness=True, steps=True, bar=False, waterfall=True, subFunctionFitness=True):
        ANALYZE.Run_Analysis(self.path, fitness, steps, bar, waterfall, subFunctionFitness)
