import random

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
        c[i] = random.uniform(-10,10)
    return c

#Caluclate fitness for each chromosome





def get_rand() -> float:
    random_num = random()
    return random_num

# selection 
def rank_selection(n:int , cummulative_rank:list) -> list:
    selected = []
    for i in range(n):
        num = get_rand()
        for i in range(len(cummulative_rank)):
            if num <= cummulative_rank[i] :
                selected.append(i)
                break
    return selected

# crossover
def crossover_swaper(n_point:int , chromosome1:list , chromosome2:list) -> list[list]:
    new_chromosome1 = chromosome1[0:n_point] + chromosome2[n_point:]
    new_chromosome2 = chromosome2[0:n_point] + chromosome1[n_point:]
    return [new_chromosome1 , new_chromosome2]

def crossover(selected:list , chromosomes:list[list] , Pc:float) -> list[list]:
    offsprings = []
    i = 0
    while(i < len(selected)):
        chrome1 = chromosomes[selected[i]]
        chrome2 = chromosomes[selected[i+1]]
        rand = get_rand()
        if rand <= Pc:
            offsprings.extend(crossover_swaper(randint(1 , len(chrome1)-1) , chrome1 , chrome2))
        else:
            offsprings.append(chrome1)
            offsprings.append(chrome2)
        i+=2
    return offsprings
        
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



