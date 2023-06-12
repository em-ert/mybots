from afpo import AFPO
import constants as c

afpo = AFPO(c.NUMBER_OF_GENERATIONS, c.POPULATION_SIZE)
afpo.Evolve()