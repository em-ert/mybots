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


class HISTORIAN:
    def __init__(self):
        # Get a unique ID to associate with the run
        self.uniqueID = self.Get_Unique_Run_ID()

        # Create folders to store run data
        path = "bestRuns/{}sols_{}gens/run{}".format(c.POPULATION_SIZE, c.NUMBER_OF_GENERATIONS, self.uniqueID)
        os.makedirs(path, exist_ok=False)

        # Add additional slash to path for use in full paths
        self.path = path + "/"
        os.makedirs(self.path + "data", exist_ok=False)
        os.makedirs(self.path + "pickles", exist_ok=False)
        os.makedirs(self.path + "plots", exist_ok=False)
    
    # This method collects all of the necessary information related to the run and stores it in a folder
    def Archive_Run_Info(self, solutionID, robot):
        # Create the info file and write in the study details
        with open(self.path + "/info.txt", "w") as f:
            # Record time of run
            now = datetime.now()
            f.write(now.strftime("Time of run: %H:%M %p on %m/%d/%Y"))
            f.write("Random Seed: {}".format(c.SEED))
            f.write("Additional Details: {}".format(c.ADDITIONAL_DETAILS))
            f.write()

            f.write("-----REVIEW COMMAND-----")
            f.write("python3 reSimulate.py GUI " + str(self.uniqueID) + " True 2&>1")
            f.write()

            f.write("-----GENERAL DETAILS-----")
            f.write("Morphology: {}".format(c.BODY))
            f.write("Pop. Size: {}".format(c.POPULATION_SIZE))
            f.write("Num. Gens: {}".format(c.NUMBER_OF_GENERATIONS))
            f.write("Steps per sim.: {}".format(c.SIM_STEPS))
            f.write()

            f.write("-----RHYTHMIC DETAILS-----")
            f.write("BPM: {}".format(c.BPM))
            f.write("Frame Rate: {}".format(c.FRAME_RATE))
            f.write("Metronome-frame ratio: {}".format(c.MET_FRAME_RATIO))
            f.write()

            f.write("-----NETWORK DETAILS-----")
            f.write("Sensor: {}".format(c.NUM_SENSOR_NEURONS))
            f.write("Auditory: {}".format(c.NUM_AUDITORY_NEURONS))
            f.write("Hidden: {}".format(c.NUM_HIDDEN_NEURONS))
            f.write("Motor: {}".format(c.NUM_MOTOR_NEURONS))
            f.write()

            f.write("-----BEST SOLUTION-----")
            f.write("Soln. ID: {}".format(solutionID))
            f.write("Fitness: {}".format(robot.fitness))
            f.write()

    
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
    def Run_Analysis(self):
        ANALYZE.Run_Analysis(self.path)
