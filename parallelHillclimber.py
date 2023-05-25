import constants as c
import copy
import os
from solution import SOLUTION


class PARALLEL_HILLCLIMBER:
    def __init__(self):
        os.system("rm brain*.nndf")
        os.system("rm fitness*.txt")
        self.nextAvailableID = 0
        self.parents = {}
        for p in range(0, c.POPULATION_SIZE):
            self.parents[p] = SOLUTION(self.nextAvailableID)
            self.nextAvailableID += 1

    def Evaluate(self, solutions):
        for solution in solutions:
            solutions[solution].Start_Simulation("DIRECT")
        for solution in solutions:
            solutions[solution].Wait_For_Simulation_To_End()

    def Evolve(self):
        self.Evaluate(self.parents)
        for currentGeneration in range(c.NUMBER_OF_GENERATIONS):
            self.Evolve_For_One_Generation()

    def Evolve_For_One_Generation(self):
        self.Spawn()
        self.Mutate()
        self.Evaluate(self.children)
        self.Print()
        self.Select()

    def Spawn(self):
        self.children = {}
        # Note that parent is an int here
        for parent in self.parents:
            self.children[parent] = copy.deepcopy(self.parents[parent])
            self.children[parent].Set_ID(self.nextAvailableID)
            self.nextAvailableID += 1

    def Mutate(self):
        # Note child is an int here
        for child in self.children:
            self.children[child].Mutate()

    def Select(self):
        for parent in self.parents:
            if self.children[parent].fitness < self.parents[parent].fitness:
                self.parents[parent] = self.children[parent]

    def Print(self):
        print()
        for parent in self.parents:
            print("p:" + str(self.parents[parent].fitness) +
                  " ch:" + str(self.children[parent].fitness))
        print()

    def Show_Best(self):
        bestParent = self.parents[0]
        for parent in self.parents:
            if self.parents[parent].fitness < bestParent.fitness:
                bestParent = self.parents[parent]
        bestParent.Start_Simulation("GUI")