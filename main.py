import random
import math
import time

class DNA:
    # Constructor
    def __init__(self, n):
        self.size = n
        self.genes = []
        self.createGenes()

    # Create random genes
    def createGenes(self):
        for i in range(self.size):
            self.genes.append(random.randrange(0, self.size))


class Individual:
    def __init__(self, n):
        self.DNA = DNA(n)

    # check how many queens that not clash with other return percentage
    def check_fit(self):
        nonColisionIndex = []

        genSize = len(self.DNA.genes)

        # check horizontally
        for i in range(genSize):
            for j in range(genSize):
                if i != j and self.DNA.genes[i] == self.DNA.genes[j]:
                    break
                elif j == genSize-1:
                    nonColisionIndex.append(i)

        # check diagonally
        eliminatedIndex = []
        for i in nonColisionIndex:
            for j in range(genSize):
                if i != j:
                    dx = abs(i - j)
                    dy = abs(self.DNA.genes[i] - self.DNA.genes[j])

                    if dx == dy:
                        eliminatedIndex.append(i)
                        break

        for i in eliminatedIndex:
            nonColisionIndex.remove(i)

        totalNonColision = len(nonColisionIndex)
        percentage = totalNonColision / genSize * 100

        return percentage


class population:
    # Constructor
    def __init__(self, nDNA, nPopulation = 200):
        self.elements = []
        self.nDNA = nDNA
        self.nPopulation = nPopulation

        # initializing first generation by creating n population with random genes of dna
        for i in range(nPopulation):
            self.elements.append(Individual(nDNA))

        self.nGeneration = 1

    # mixing 2 DNA from 2 individual
    def crossover(self, parent1, parent2):
        midpoint = random.randrange(self.nDNA)
        left = parent1.DNA.genes[0:midpoint]
        right = parent2.DNA.genes[midpoint:]

        newDna = left + right
        child = Individual(self.nDNA)
        child.DNA.genes = newDna

        return child

    # Generating new population to next generation
    def generateNewPopulation(self, mutation_rate=0.1):
        # creating mating pool based on the fitness
        matingpool = []
        for individual in self.elements:
            fitness = individual.check_fit()

            for i in range(math.ceil(fitness)):
                matingpool.append(individual)

        # crossovering / mixing 2 parents
        self.elements.clear()
        for i in range(self.nPopulation):
            # picking 2 parents randomly from mating pool
            random1 = random.randrange(len(matingpool))
            random2 = random.randrange(len(matingpool))

            parent1 = matingpool[random1]
            parent2 = matingpool[random2]

            child = self.crossover(parent1, parent2)

            # mutation
            if random.uniform(0, 1) <= mutation_rate:
                size = len(child.DNA.genes)
                genIndex = random.randrange(size)
                newGen = child.DNA.genes[genIndex]
                while newGen == child.DNA.genes[genIndex]:
                    newGen = random.randrange(size)

                child.DNA.genes[genIndex] = newGen

            self.elements.append(child)

        self.nGeneration += 1

        return self.elements


if __name__ == '__main__':

    print("N-Queen Problem Solving with Genetic Algorithm")
    nQueen = int(input("N-Queen? "))
    nPopulation = int(input("N-Population in a Generation? "))
    print("Finding solution ...")

    t_start = time.process_time()
    populations = population(nQueen, nPopulation)

    finish = False

    while not finish:
        for individual in populations.elements:
            print(str(individual.DNA.genes) + " = " + str(individual.check_fit()))
            if individual.check_fit() == 100:
                t_stop = time.process_time()
                finish = True
                solution = individual
                break

        populations.generateNewPopulation()

    print(" ")
    print(" ")
    print(str(nQueen)+"-Queen solution:")
    print(solution.DNA.genes)
    print("Solution is found in " + str(populations.nGeneration) + " Generation")
    print("Process time: " + str(t_stop - t_start) + "s")
    print(" ")
    input("Enter to close this program ")


