from random import randint,random
from numpy import array,argmax,argmin

#Fitness Function
def fitness(chromosome,items,target):
	nutrition = [0,0,0]

	for index,amount in enumerate(chromosome):
		for i in range(3):
			nutrition[i] += amount * items[index][i]

	fitness_value = 0
	for i in range(len(items[0])):
		fitness_value += (nutrition[i] - target[i]) ** 2

	return -fitness_value

def get_fittest(fitness_values):
	tempFitness = array(fitness_values)
	return (min(tempFitness),argmin(tempFitness))

#Selection
def select(population,fitness_values):
	parent1,parent2 = -1,-1
	first_value,second_value = float('inf'),float("inf")

	for index,value in enumerate(fitness_values):
		if(value < first_value):
			second_value = first_value
			first_value = value
			parent2 = parent1
			parent1 = index
		elif(value < second_value):
			second_value = value
			parent2 = index

	parents = (population[parent1],population[parent2])
	return parents

#Crossover the parents
def crossover(parents):
	crossover_point = randint(1,len(parents[0]) - 2)
	first_offspring = parents[0][:crossover_point] + parents[1][crossover_point:]
	second_offspring = parents[1][:crossover_point] + parents[0][crossover_point:]
	return (first_offspring,second_offspring)


#mutate
def mutate(off_spring):
	mutation_point = randint(0,len(off_spring) - 2)
	if(random() < 0.5):
		change = -0.5
	else:
		change = 0.5

	amounts = list(off_spring)
	amounts[mutation_point] += change
	if(amounts[mutation_point] <= 0):
		amounts[mutation_point] = 0.5
	return tuple(amounts)

#Genetic Algorithm
def genetic(target,items):

	population = []
	fitness_values = []

	for i in range(5):
		chromosome = []
		for j in range(len(items)):
			chromosome.append(int(random() * 3) + 0.5)
		chromosome = tuple(chromosome)
		population.append(chromosome)
		fitness_values.append(fitness(chromosome,items,target))

	fittest = get_fittest(fitness_values)
	fittest_index = fittest[1]
	fittest = fittest[0]

	maxAttempts = 10
	count = 0
	iteration = 0
	threshold = -5
	#Generations
	while(True):
		parents = select(population,fitness_values)
		off_springs = crossover(parents)
		
		mutation_chance = random()
		if(mutation_chance > 0.5):
			off_springs = (mutate(off_springs[0]),off_springs[1])

		mutation_chance = random()
		if(mutation_chance > 0.5):
			off_springs = (off_springs[0],mutate(off_springs[1]))

		temp_fitness = array(fitness_values)
		lowest_fitness = argmin(temp_fitness)
		if(fitness(off_springs[0],items,target) > fitness(off_springs[1],items,target)):
			population[lowest_fitness] = off_springs[0]
			fitness_values[lowest_fitness] = fitness(off_springs[0],items,target)
		else:
			population[lowest_fitness] = off_springs[1]
			fitness_values[lowest_fitness] = fitness(off_springs[1],items,target)

		prev_fittest = fittest
		fittest = get_fittest(fitness_values)
		fittest_index = fittest[1]
		fittest = fittest[0]
		iteration += 1
		#print("Generation {}: {}, {}".format(iteration,population[fittest_index],fittest))

		if(prev_fittest == fittest):
			count += 1

		if(count == maxAttempts):
			count = 0
			threshold -= 0.5

		if(fittest > threshold):
			return population[fittest_index]
			break

