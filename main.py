from random import uniform , randint , random

#we are given N ,D and for each N we get the x, y
#for example N=4 D=2 (1,5), (2,8), (3,13), (4,20)
#we generate chromosomes its length of bits = D+1, that contain random float number form -10 to 10
#calculate each fitness with the mean square error 
#for ex: C1 = [1.95, 8.16. -2.0] we calcultae the fitness for each (x,y)
# c1_fitness1 =  [(1.95 + 8.16 * 1 + (-2) * (1^2)->"the index of the point (x,y) in 1-indexed" ) - 5]^2 = 9.67
# c1_fitness2 =  [(1.95 + 8.16 * 2 + (-2) * (2^2)->"the index of the point (x,y) in 1-indexed" ) - 8]^2 = 5.15
# c1_fitness3 =  [(1.95 + 8.16 * 3 + (-2) * (3^2)->"the index of the point (x,y) in 1-indexed" ) - 13]^2 = 20.88
# c1_fitness4 =  [(1.95 + 8.16 * 4 + (-2) * (4^2)->"the index of the point (x,y) in 1-indexed" ) - 20]^2 = 303.1
# C1_fitness = (9.67 + 5.15 + 20.88 + 303.1)/4 = 84.7 we want to minimize the = 1/84.7
# then make selection and crossover as we learn then we make a "non_uniform mutation"  


#intialization
def initialize_chromosome(n : int) -> list:
    c = [0] * n
    for i in range(n):
        #for generate random float num between -10 and 10 
        c[i] = uniform(-10,10)
    return c


def fitness(chromosome: list , xPoints: list , yPoints: list) -> float:
    fitness = 0
    yPredicted = []
    for x in xPoints:
        y = 0
        for i in range(len(chromosome)):
            y += (x**i) * (chromosome[i])
        yPredicted.append(y)

    for i in range(len(yPredicted)):
        fitness += ((yPoints[i] - yPredicted[i])**2)

    return fitness / len(yPoints)

def tournamentSelectionHelper(firstChromosome: list , secondChromosome: list , xPoints: list , yPoints: list) -> list :
    return firstChromosome if fitness(firstChromosome , xPoints , yPoints) < fitness(secondChromosome , xPoints , yPoints) else secondChromosome

def tournamentSelection(chromosomes: list[list] , k: int , xPoints: list , yPoints: list) -> list[list]:
    matingPool = []
    toBeRemoved = []
    for i in range(0 , len(chromosomes) , 2):
        chosenChromosome = tournamentSelectionHelper(chromosomes[i] , chromosomes[i+1] , xPoints , yPoints)
        matingPool.append(chosenChromosome)
        toBeRemoved.append(chosenChromosome)
    
    for i in range(len(toBeRemoved)):
        chromosomes.remove(toBeRemoved[i])
    return matingPool

# crossover
def crossover_swaper(n_point:int , m_point:int , chromosome1:list , chromosome2:list) -> list[list]:
    firstPoint = min(n_point , m_point)
    secondPoint = max(n_point , m_point)
    c1 = chromosome1[0:firstPoint+1] + chromosome2[firstPoint+1 : secondPoint+1] + chromosome1[secondPoint+1 :]
    c2 = chromosome2[0:firstPoint+1] + chromosome1[firstPoint+1 : secondPoint+1] + chromosome2[secondPoint+1 :]
    return [c1 , c2]

def crossover(matingPool:list[list] , chromsomes:list[list] , PC:float) -> list[list]:
    offsprings = []
    for i in range( 0, len(matingPool) , 2):
        randomNumber = random()
        if randomNumber <= PC:
            offsprings.extend(crossover_swaper(randint(1 , len(chromsomes[i])-2) , randint(1 , len(chromsomes[i])-2) , matingPool[i] , matingPool[i+1]))
    return offsprings

def applyNonUniformMutation(chromosome:list , PM:float , generation:int , maxGeneration:int) -> list:
    for i in range(len(chromosome)):
        randomNumber = random()
        if randomNumber <= PM:
            factor = (generation / maxGeneration) ** 2
            mutation_change = uniform(-0.5, 0.5) * factor
            chromosome[i] += mutation_change
            chromosome[i] = max(min(chromosome[i], 10), -10)  # problem constraint
    return chromosome

def nonUniformMutation(offsprings:list[list] , PM:float , generation:int , maxGeneration:int ) -> list[list]:
    for i in range(len(offsprings)):
        offsprings[i] = applyNonUniformMutation(offsprings[i] , PM , generation , maxGeneration)
    return offsprings

def elitistReplacement(offsprings:list[list] , matingPool:list[list] ,xPoints:list , yPoints:list , k:int ) -> list[list]: # don't forget to combine the mating pool with offsprings
    potentialGeneration = offsprings + matingPool
    potentialGeneration = sorted(potentialGeneration , key = lambda x: fitness(x , xPoints , yPoints))
    return potentialGeneration[:k] # extend it on the generation in the main

def parser(filePath:str):
    numberOfData = 0
    numberOfPoints = []
    polyDegree = []
    xPointsList = []
    yPointsList = []

    with open(filePath, 'r') as file:
        lines = file.readlines()
    
    numberOfData = int(lines[0])

    i = 1
    while(i<len(lines)):
        line = lines[i].split(' ')
        numberOfPoints.append(int(line[0]))
        polyDegree.append(int(line[1]))
        i+=1

        xPoints = []
        yPoints = []
        for point in range(numberOfPoints[-1]):
            line = lines[i].split(' ')
            xPoints.append(float(line[0]))
            yPoints.append(float(line[1]))
            i+=1
        
        xPointsList.append(xPoints)
        yPointsList.append(yPoints)

    return numberOfData , polyDegree , xPointsList , yPointsList



def main():
    iterations = 1000
    popSize = 8 
    k = 4
    PC = 0.7
    PM = 0.02

    numberOfData , polyDegrees , xPointsList , yPointsList = parser('curve_fitting_input.txt')

    for testCase in range(numberOfData):
        polyDegree = polyDegrees[testCase]
        xPoints = xPointsList[testCase]
        yPoints = yPointsList[testCase]

        generation = [initialize_chromosome(polyDegree+1)] * popSize
        for i in range(iterations):
            matingPool = tournamentSelection(generation , k , xPoints , yPoints)
            offsprings = crossover(matingPool , generation , PC)
            offsprings = nonUniformMutation(offsprings , PM , i , 1000)
            generation.extend(elitistReplacement(offsprings , matingPool , xPoints , yPoints , k))
        



        
main()
#make the non_unoiform mutation        
# You should iterate over each bit in each offspring chromosome, but we’ll just show you 
# the mutation on the first bit (i=0) of O1:
# Generate a random number (rm) between 0 and 1.
# if rm <= Pm:
#  ∆Lxi = 1.95 – (-10) = 11.95
#  ∆Uxi = 10 – 1.95 = 8.05
#  Generate r1 ∈ [0,1]: if r1 <= 0.5, y = ∆Lxi, else r1 > 0.5, y = ∆Uxi
# (Assume r1 = 0.19, therefore y = 11.95)
#  ∆(t,y) = y * (1 – r ^ ((1 - t\T) ^ b))
# =
#  ∆(1,11.95) = 11.95 * (1 – 0.67 ^ ((1 - 1\100) ^ 1))
# =
# 3.9
#  Since y = ∆Lxi, therefore Xinew = 1.95 – 3.9 = -1.95



