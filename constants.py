SIM_STEPS = 1000
MAX_FORCE = 40

BPM = 120   # Modify this value to auto-set the rest
QUARTER = 60 / BPM              # 0.5
EIGHTH = QUARTER / 2            # 0.25
SIXTEENTH = EIGHTH / 2          # 0.125
THIRTY_SECOND = SIXTEENTH / 2   # 0.0625

FRAME_RATE_S = SIXTEENTH

METRONOME_RATE_S = QUARTER

MET_FRAME_RATIO = QUARTER / SIXTEENTH   # 4


SLEEP_TIME = 0.000166

NUMBER_OF_GENERATIONS = 4

POPULATION_SIZE = 15

INCLUDE_UPPER_LINKS = False
NUM_SENSOR_NEURONS = 4
NUM_HIDDEN_NEURONS = 0
NUM_MOTOR_NEURONS = 8

MOTOR_JOINT_RANGE = 0.4
