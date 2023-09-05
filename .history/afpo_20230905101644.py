import constants as c
import copy
import datetime
from historian import HISTORIAN
import numpy as np
import matplotlib.pyplot as plt
import os
import operator
import pickle
from pyglet.resource import media
import random
from solution import SOLUTION

class AFPO:
    def __init__(self, nextAvailableID=0, currentGeneration=0, population={}, paretoFront = [], fitnessData=None):
        # Clear brain and fitness files
        os.system("rm brain*.nndf")
        os.system("rm fitness*.txt")


        # Create the world and body files for the simulation
        SOLUTION.Create_World()
        SOLUTION.Create_Body(0, 0, 1.2)

        # Set initial values for AFPO
        self.genSize = c.NUMBER_OF_GENERATIONS
        self.popSize = c.POPULATION_SIZE
        self.checkpointEvery = c.CHECKPOINT_EVERY

        self.optimizeAge = c.OPTIMIZE_AGE

        self.nextAvailableID = nextAvailableID
        self.currentGeneration = currentGeneration
        self.population = population
        self.paretoFront = paretoFront
        if fitnessData == None:
            self.fitnessData = np.zeros(shape=(self.genSize, self.popSize, 2))

        # Create initial population
        for i in range(self.popSize):
            self.population[i] = SOLUTION(self.nextAvailableID)
            self.nextAvailableID += 1
        
        self.historian = HISTORIAN()


    def Evolve(self, fromCheckpoint=0):
        remainingGens = c.NUMBER_OF_GENERATIONS - fromCheckpoint
        # XXX: Eventually remove this after testing
        if (fromCheckpoint != self.currentGeneration):
            raise Exception("Mismatched genCount")
        
        for currentGeneration in range(remainingGens):
            if currentGeneration == 0:
                # Run simulation for first generation
                self.Run_Simulations(self.population)
                self.Save_Stats()
                self.currentGeneration += 1
                print("Remaining: " + str(self.genSize - self.currentGeneration))
                
            else:
                # Evolve for one generation
                self.Evolve_For_One_Generation()
                self.Save_Stats()
                
                # Check for checkpoint
                if self.currentGeneration % self.checkpointEvery == 0:
                    self.Save_Checkpoint()

                # Ding if necessary
                if self.genSize - self.currentGeneration == 1:
                    toaster = media("sounds/toaster_ding.mp3", streaming=False)
                    toaster.play()
                
                self.currentGeneration += 1
                print("Remaining: " + str(self.genSize - self.currentGeneration))
                            
        # self.Save_All_Pareto_Front_Brains()
        # self.Show_All_Pareto_Front_Brains()
        best = self.Get_Best_Brain()
        self.Save_Best_Brain(best, self.historian.path)
        self.Prep_Best_Brain(best)
        self.Save_Fitness_Data_For_Analysis(self.historian.path)
        bestFitness = (np.amax(self.fitnessData[self.genSize-1, :, :], axis=0)[0])
        self.Preserve_Record(best.myID, bestFitness)
        self.Show_Best_Brain()
    
    def Save_Stats(self):
        for index, solID in enumerate(self.population):
            self.fitnessData[self.currentGeneration, index, 0] = self.population[solID].fitness
            if self.optimizeAge == True:
                self.fitnessData[self.currentGeneration, index, 1] = self.population[solID].age
            else:
                self.fitnessData[self.currentGeneration, index, 1] = self.population[solID].fitness2

        # XXX: Eventually remove this after testing
        print("\n")
        print(np.amax(self.fitnessData[self.currentGeneration, :, :], axis=0)[0])

    def Save_Checkpoint(self):
        filename = "checkpoints/{}gens.pickle".format(self.currentGeneration)

        np_rng_state = np.random.get_state()
        rng_state = random.getstate()

        print("Checkpoint reached at gen " + str(self.currentGeneration) + "! Saving population in file: ", filename)
        with open(filename, 'wb') as f:
            pickle.dump([self, np_rng_state, rng_state], f, pickle.HIGHEST_PROTOCOL)


    def Evolve_For_One_Generation(self):
        # Age individuals in the population
        self.Age_Generation()

        # Spawn children for next generation
        children = self.Spawn_Children_From_Parents()
        self.Mutate(children)
        children = self.Spawn_Random_Child(children)

        # Run Simulations on children to get their respective fitnesses
        self.Run_Simulations(children)

        # Update the population dictionary to include the children
        self.population.update(children)

        self.Select()


    """
    Increases the ages of all individuals in the population by 1 to prep for addition of the next generation
    """
    def Age_Generation(self):
        for individual in self.population:
            self.population[individual].age += 1
        

    """
    Spawns[pop. size] children from parents selected by tournament
    """
    def Spawn_Children_From_Parents(self):
        children = {}

        for i in range(self.popSize):
            parent = self.Tournament_Selection()

            # Make a deep copy of parent, mutate it, add it to "children"
            child = copy.deepcopy(self.population[parent])
            child.Set_ID(self.nextAvailableID)
            self.nextAvailableID += 1
            child.Reset_Simulation_State()

            # Add child to children with key of child's ID
            children[child.myID] = child
        
        return children
    

    def Mutate(self, children):
        # Note child is an int here
        for child in children:
            for i in range(c.NUM_MUTATIONS):
                children[child].Mutate()
    

    """
    Spawns a single random child 
    """
    def Spawn_Random_Child(self, children):
        randomChild = SOLUTION(self.nextAvailableID)
        self.nextAvailableID += 1

        # Add random child to children and return children
        children[randomChild.myID] = randomChild
        return children


    """
    Picks two random ints (IDs) in range of pop.size, chooses the individual with the highest fitness to reproduce (asexually)
    """
    def Tournament_Selection(self):
        p1 = np.random.choice(list(self.population))
        p2 = np.random.choice(list(self.population))
        while p1 == p2:
            p2 = np.random.choice(list(self.population))
        # Return individual with highest fitness to spawn mutated child
        if self.population[p1].fitness > self.population[p2].fitness:
            return p1
        else:
            return p2


    """
    Competes two randomly-chosen individuals against each other and removes the non-dominant individual until target population size is reached (unless the pareto front is larger than the size of the target population--see more about this below)
    """
    def Select(self):
        self.Update_Pareto_Front()
        # Validate pareto front size to prevent infinite loop
        if len(self.paretoFront) > self.popSize:
            newLayer = np.zeros((self.genSize, len(self.paretoFront)-self.popSize , 2), float)
            self.fitnessData = np.append(self.fitnessData, newLayer, axis=1)
            self.popSize = len(self.paretoFront)


        while len(self.population) > self.popSize:
            # Pick two random ints in range of pop.size
            i1 = np.random.choice(list(self.population))
            i2 = np.random.choice(list(self.population))
            while i1 == i2:
                i2 = np.random.choice(list(self.population))

            # If i1 dominates, remove i2 from the population
            if self.Dominates(i1, i2):
                self.population.pop(i2)
            # If i2 dominates, remove i1 from the population
            elif self.Dominates(i2, i1):
                self.population.pop(i1)
            # If neither are dominant, continue the loop and pick 2 new individuals


    """
    Check size of pareto front (number of non-dominated individuals) to ensure it is smaller than the population size. If not, increase population size to be equal to that of the pareto front to avoid an infinite loop.
    """
    def Update_Pareto_Front(self):
        self.paretoFront = []
        for i in self.population:
            iNonDominated = True
            for j in self.population:
                if i == j:
                    continue
                elif self.Dominates(j, i):
                    iNonDominated = False
                    break
            if iNonDominated:
                self.paretoFront.append(i)
            

    """
    Checks to see if an individual is dominant over the younger -- meaning it has the same stats but is newer or is BOTH younger AND more fit
    """
    def Dominates(self, i1, i2):
        if self.optimizeAge == True:
            # If individuals have same stats, return newer one (i1 dom. if newer)
            if self.population[i1].age == self.population[i2].age and self.population[i1].fitness == self.population[i2].fitness:
                return self.population[i1].myID > self.population[i2].myID
            
            # If i1 dominates (has lower age AND higher fitness) return true, return false otherwise
            elif self.population[i1].age <= self.population[i2].age and self.population[i1].fitness >= self.population[i2].fitness:
                return True
            else:
                return False
        else:
            # If indivuduals have same stats, return newer one (i1 dom. if newer)
            if self.population[i1].fitness2 == self.population[i2].fitness2 and self.population[i1].fitness == self.population[i2].fitness:
                return self.population[i1].myID > self.population[i2].myID
            
            # If i1 dominates (has higher fitness AND higher fitness2) return true, return false otherwise
            elif self.population[i1].fitness2 >= self.population[i2].fitness2 and self.population[i1].fitness >= self.population[i2].fitness:
                return True
            else:
                return False    

    """
    Runs simulations for any solutions that have not been simulated
    """
    def Run_Simulations(self, solutions):
        for solution in solutions:
            if not solutions[solution].wasSimulated:
                solutions[solution].Start_Simulation("DIRECT", False)
        for solution in solutions:
            if not solutions[solution].wasSimulated:
                solutions[solution].Wait_For_Simulation_To_End()


    def Get_Best_Brain(self):
        popList = list(self.population.values())
        return sorted(popList, key=operator.attrgetter('fitness'), reverse=True)[0]
    

    def Save_Best_Brain(self, bestSolution, path):
        bestSolution.Create_Brain()
        fullPath =  path + "brain" + str(bestSolution.myID) + ".nndf"
        os.system("mv brain" + str(bestSolution.myID) + ".nndf " + fullPath)
        print("Data saved to " + fullPath)


    def Prep_Best_Brain(self, bestSolution):
        bestSolution.Start_Simulation("DIRECT", True)


    """
    def Show_All_Pareto_Front_Brains(self):
        for individual in self.paretoFront:
            self.population[individual].Start_Simulation("GUI", True)

    """
        
    
    def Save_All_Pareto_Front_Brains(self, path):
        for individual in self.paretoFront: 
            best = self.population[individual]
            best.Create_Brain()       
            fullPath =  path + "brain" + str(best.myID) + ".nndf"
            os.system("mv brain" + str(best.myID) + ".nndf " + fullPath)
            print("Data saved to " + fullPath)


    def Save_Fitness_Data_For_Analysis(self, path):
        fullPath = path + "data/age_fitness_values.npy"
        np.save(fullPath, self.fitnessData)
        print("Data saved to " + fullPath)

    
    def Preserve_Record(self, bestID, bestFitness):
        self.historian.Archive_Run_Info(bestID, bestFitness)
        self.historian.Run_Analysis(fitness=True, steps=True)

    
    def Show_Best_Brain(self):
        os.system("python3 simulate.py GUI " + str(self.historian.uniqueID) + " True 2&>1")