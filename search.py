from afpo import AFPO
import constants as c
import numpy as np
import pickle
import random
import sys

# Get checkpoint from arguments
checkpoint = sys.argv[1]

# Seed rngs
np.random.seed(c.SEED)
random.seed(c.SEED)

# If checkpoint is 0, proceed normally
if int(checkpoint) == 0:
    afpo = AFPO()
    afpo.Evolve()

# Otherwise, load the afpo pickle in and Evolve from the checkpoint
else:
    pickleFile = "checkpoints/" + checkpoint + "gens.pickle"
    try:
        with open(pickleFile, "rb") as f:
            pickleObject = pickle.load(f)
    except:
        raise Exception("Pickled checkpoint file not found: " + pickleFile)
    else:
        afpo = pickleObject[0]
        if c.NUMBER_OF_GENERATIONS > afpo.genSize:
            print(f"Number of gens increased from {afpo.genSize} to {c.NUMBER_OF_GENERATIONS}")
            afpo.fitnessData = np.append(afpo.fitnessData, np.zeros((c.NUMBER_OF_GENERATIONS - afpo.genSize, np.size(afpo.fitnessData, axis=1),  np.size(afpo.fitnessData, axis=2))), axis=0)
            afpo.genSize = c.NUMBER_OF_GENERATIONS
        elif c.NUMBER_OF_GENERATIONS < afpo.currentGeneration:
            print(f"ERROR: Number of generations was modified in a manner that is not executable.")
        elif c.NUMBER_OF_GENERATIONS < afpo.genSize:
            print(f"Number of gens decreased from {afpo.genSize} to {c.NUMBER_OF_GENERATIONS}")
            afpo.genSize = c.NUMBER_OF_GENERATIONS
        np.random.set_state(pickleObject[1])
        random.setstate(pickleObject[2])
        afpo.Evolve(int(checkpoint))

# python3 simulate.py GUI 1 False