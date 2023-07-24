SIM_STEPS = 800
MAX_FORCE = 40

SEED = 0
NUMBER_OF_GENERATIONS = 50
POPULATION_SIZE = 30
CHECKPOINT_EVERY = 10

INCLUDE_UPPER_LINKS = False
NUM_SENSOR_NEURONS = 4
NUM_AUDITORY_NEURONS = 1
NUM_HIDDEN_NEURONS = 3
NUM_MOTOR_NEURONS = 8

BPM = 120  # Modify this value to auto-set the rest
QUARTER = 60 / BPM              # 0.5
EIGHTH = QUARTER / 2            # 0.25
SIXTEENTH = EIGHTH / 2          # 0.125
THIRTY_SECOND = SIXTEENTH / 2   # 0.0625
SIXTY_FOURTH = THIRTY_SECOND / 2    # 0.03125
ONE_TWENTY_EIGHTH = SIXTY_FOURTH / 2

FRAME_RATE = SIXTY_FOURTH
METRONOME_RATE = QUARTER
MET_FRAME_RATIO = QUARTER / FRAME_RATE

MOTOR_JOINT_RANGE = 0.4

SLEEP_TIME = 0.000166
