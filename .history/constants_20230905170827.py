SIM_STEPS = 800
MAX_FORCE = 40

#REVIEW - For re-sims: edit pop. size and num. gens to match
SEED = 0
NUMBER_OF_GENERATIONS = 50
POPULATION_SIZE = 50
CHECKPOINT_EVERY = 20
BODY = "Capsule Bot"

#REVIEW - [3] Edit fitness function here
ADDITIONAL_DETAILS = "1 mutation, FPB scaled exp function, EXP + AGE: if stepsToClick >= 0 and stepValue > 0: self.fitness += (((2-stepsToClick)**2)+0.5); else: self.fitness -= stepValue * 0.5"
# Can be COS, EXP, or EXP_PUNISH
FIT_FUNCTION = "EXP"

# General COS:
    # if stepValue > 0: self.fitness += (framesPerBeat * np.cos(((2*np.pi)/framesPerBeat)*timestep))
# General EXP:
    # if stepsToClick >= 0 and stepValue > 0: self.fitness += (((2-stepsToClick)**2)+0.5)    
# General EXP_PUNISH:
    # if stepsToClick >= 0 and stepValue > 0: self.fitness += (((2-stepsToClick)**2)+0.5); else: self.fitness -= stepValue * 0.5


#REVIEW - [3.5] Edit fitness function here
OPTIMIZE_AGE = True
# Below can be AGE, DISTANCE, or SYMMETRY
SECOND_OBJ = "DISTANCE"
NUM_MUTATIONS = 1

# Can accommodate 60, 75, 80, 100, 120, 150, and 160 BPM
TEMPOS = [120, 80, 100]
FRAME_RATE = 0.0250

INCLUDE_UPPER_LINKS = False
NUM_SENSOR_NEURONS = 4
NUM_AUDITORY_NEURONS = 1
NUM_HIDDEN_NEURONS = 3
NUM_MOTOR_NEURONS = 8

HERTZ = 1000
S_TO_MS = 1000
SIM_FREQUENCY = HERTZ / (FRAME_RATE * S_TO_MS)

MOTOR_JOINT_RANGE = 0.4
SLEEP_TIME = 0.000166
REPLAY_DELAY_TOLERANCE = -0.05
