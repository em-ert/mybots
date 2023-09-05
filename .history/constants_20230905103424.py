SIM_STEPS = 800
MAX_FORCE = 40

#REVIEW - For re-sims: edit pop. size and num. gens to match
SEED = 0
NUMBER_OF_GENERATIONS = 50
POPULATION_SIZE = 50
CHECKPOINT_EVERY = 20
BODY = "Capsule Bot"

#REVIEW - [3] Edit fitness function here
ADDITIONAL_DETAILS = "FIXED MUTATIONS! 1 mutation, FPB scaled cos function, distance traveled: (framesPerBeat * np.cos(((2*np.pi)/framesPerBeat)*timestep)) and maximized auditory neurons"

#REVIEW - [3.5] Edit fitness function here
OPTIMIZE_AGE = False
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
