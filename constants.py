import math

SIM_STEPS = 400
MAX_FORCE = 40

#REVIEW - For re-sims: edit pop. size and num. gens to match
SEED = 0
NUMBER_OF_GENERATIONS = 30
POPULATION_SIZE = 40
CHECKPOINT_EVERY = 10
NUM_PARALLEL_RUN_GROUPS = 2
BODY = "Capsule Bot"
BODY_SIZE = 1
TRAVEL_PER_CLICK_GOAL = BODY_SIZE / 25
DOUBLE_STEP_PUNISHMENT = 0.05

#REVIEW - [3] Edit fitness function here
ADDITIONAL_DETAILS = "if (rhythm * balance) >= 0.95: scaffoldedFitness = (rhythm * balance) + distance)"
# Can be COS, EXP, EXP_PUNISH, or BIN
FIT_FUNCTION = "COS"

# General COS:
    # if stepValue > 0: self.fitness += (framesPerBeat * np.cos(((2*np.pi)/framesPerBeat)*timestep))
# General EXP:
    # if stepsToClick >= 0 and stepValue > 0: self.fitness += (((2-stepsToClick)**2)+0.5)    
# General EXP_PUNISH:
    # if stepsToClick >= 0 and stepValue > 0: self.fitness += (((2-stepsToClick)**2)+0.5); else: self.fitness -= stepValue * 0.5


#REVIEW - [3.5] Edit fitness function here
OPTIMIZE_AGE = True
# Below can be AGE, DISTANCE, DUAL, or SYMMETRY
SECOND_OBJ = "Age"
NUM_MUTATIONS = 1
NUM_RANDOM_CHILDREN = 4

# Can accommodate 60, 75, 80, 100, 120, 150, and 160 BPM
TEMPOS = [120, 80, 100]
FRAME_RATE = 0.0250
FRAMES_PER_BEAT = [math.ceil((60/tempo)/FRAME_RATE) for tempo in TEMPOS]
CLICKS_PER_TEMPO = math.ceil(SIM_STEPS/min(FRAMES_PER_BEAT))
FRAMES_PER_TEMPO = [numFrames * CLICKS_PER_TEMPO for numFrames in FRAMES_PER_BEAT]

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
