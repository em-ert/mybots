from afpo import AFPO
import os
import pickle
import sys

# Get checkpoint from arguments
checkpoint = sys.argv[1]

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
    except:
        raise Exception("Pickled checkpoint file not found: " + pickleFile)
    else:
        afpo.Evolve(int(checkpoint))

# python3 simulate.py GUI 1 False