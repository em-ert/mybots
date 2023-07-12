import constants as c
import copy
import numpy as np
import os
from playsound import playsound
from solution import SOLUTION

class AFPO:
    def __init__(self, genSize, popSize):
        # Clear brain and fitness files
        os.system("rm brain*.nndf")
        os.system("rm fitness*.txt")

        # Create the world and body files for the simulation
        SOLUTION.Create_World()
        SOLUTION.Create_Body(0, 0, 1.2)

        # Set initial values for AFPO
        self.genSize = genSize
        self.popSize = popSize
        self.nextAvailableID = 0
        self.currentGeneration = 0
        self.population = {}
        self.paretoFront = []

        # Create initial population
        for i in range(self.popSize):
            self.population[i] = SOLUTION(self.nextAvailableID)
            self.nextAvailableID += 1

    def Evolve(self):
        for currentGeneration in range(self.genSize):
            if currentGeneration == 0:
                genCount = self.genSize
                print("Start: " + str(genCount))
                # Run simulation for first generation
                self.Run_Simulations(self.population)
                genCount -= 1
                print("Remaining: " + str(genCount))
                    
                
            else:
                # Evolve for one generation
                self.Evolve_For_One_Generation()
                genCount -= 1
                print("Remaining: " + str(genCount))
                if genCount == 0:
                    playsound("sounds/toaster_ding.mp3", block=False)
            # Could save results at n-1 generation or at end?
        
        # self.Save_All_Pareto_Front_Brains()
        # self.Show_All_Pareto_Front_Brains()
        best = self.Get_Best_Brain()
        self.Save_Best_Brain(best)
        self.Show_Best_Brain(best)
        
            

    def Evolve_For_One_Generation(self):
        # Age individuals in the population
        self.Age_Generation()

        # Spawn children for next generation
        children = self.Spawn_Children_From_Parents()
        children = self.Spawn_Random_Child(children)

        # Run Simulations on children to get their respective fitnesses
        self.Run_Simulations(children)
        print(len(self.population))

        # Update the population dictionary to include the children
        self.population.update(children)
        print(len(self.population))

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
    Competes two randomly-chosen individuals against eachother and removes the non-dominant individual until target population size is reached (unless the pareto front is larger than the size of the target population--see more about this below)
    """
    def Select(self):
        self.Update_Pareto_Front()
        # Validate pareto front size to prevent infinite loop
        if len(self.paretoFront) > self.popSize:
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
        # If indivuduals have same stats, return newer one (i1 dom. if newer)
        if self.population[i1].age == self.population[i2].age and self.population[i1].fitness == self.population[i2].fitness:
            return self.population[i1].myID > self.population[i2].myID
        
        # If i1 dominates (has lower age AND higher fitness) return true, return false otherwise
        elif self.population[i1].age <= self.population[i2].age and self.population[i1].fitness >= self.population[i2].fitness:
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

    """
    def Print(self):
        print()
        for parent in self.parents:
            print("p:" + str(self.parents[parent].fitness) +
                  " ch:" + str(self.children[parent].fitness))
        print()
    """
    def Save_All_Pareto_Front_Brains(self):
        for individual in self.paretoFront: 
            best = self.population[individual]
            best.Create_Brain()          
            os.system("mv brain" + str(best.myID) + ".nndf best/brain" + str(best.myID) + ".nndf")

    def Show_All_Pareto_Front_Brains(self):
        for individual in self.paretoFront:
            self.population[individual].Start_Simulation("GUI", True)

    def Get_Best_Brain(self):
        best = self.population[self.paretoFront[0]]
        for individual in self.paretoFront:
            if self.population[individual].fitness > best.fitness:
                best = self.population[individual]

        return best
    
    def Save_Best_Brain(self, bestSolution):
        bestSolution.Create_Brain()          
        os.system("mv brain" + str(bestSolution.myID) + ".nndf best/brain" + str(bestSolution.myID) + ".nndf")

    def Show_Best_Brain(self, bestSolution):
        bestSolution.Start_Simulation("DIRECT", True)
        bestSolution.Start_Simulation("GUI", True)
