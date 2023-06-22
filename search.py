from afpo import AFPO
import constants as c

afpo = AFPO(c.NUMBER_OF_GENERATIONS, c.POPULATION_SIZE)
afpo.Evolve()

# python3 simulate.py GUI 1 False