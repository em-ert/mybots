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
            afpo = pickle.load(f)[0]
            np.random.set_state(pickle.load(f)[1])
            random.set_state(pickle.load(f)[2])
    except:
        raise Exception("Pickled checkpoint file not found: " + pickleFile)
    else:
        afpo.Evolve(int(checkpoint))

# python3 simulate.py GUI 1 False