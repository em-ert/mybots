SIM_STEPS = 800
MAX_FORCE = 40

#REVIEW - For re-sims: edit pop. size and num. gens to match
SEED = 0
NUMBER_OF_GENERATIONS = 100
POPULATION_SIZE = 50
CHECKPOINT_EVERY = 20
BODY = "Capsule Bot"
ADDITIONAL_DETAILS = "Run with cos function shifted down by 0.5: (np.cos(((2*np.pi)/framesPerBeat)*timestep)-0.5) + and maximized auditory neurons"

#REVIEW - Edit fitness function here
OPTIMIZE_AGE = False

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
