from random import choices, randint
from collections import namedtuple
from functools import partial
import time

genome = []
population = []
WEIGHT_LIMIT = 3000

fitness_limit = 1310 

Thing = namedtuple('Thing', ['name', 'value', 'weight'])

things = [
    Thing('Laptop', 500, 2200),
    Thing('Headphones', 150, 160),
    Thing('Coffee Mug', 60, 350),
    Thing('Notepad', 40, 333),
    Thing('Water Bottle', 30, 192),
]

second_example = [
    Thing('Mints', 5, 25),
    Thing('Socks', 10, 38),
    Thing('Tissues', 15, 80),
    Thing('Phone', 500, 200),
    Thing('Baseball Cap', 100, 70)
]

things += second_example

def generate_genome(length):
    return choices([0, 1], k=length)

def generate_popluation(population_size, genome_length):
    return [generate_genome(genome_length) for i in range(population_size)]

def fitness(genome, things, weight_limit):

    if len(genome) != len(things):
        raise ValueError('Genome & Things Must Be Of Same LENGTH')

    weight = 0
    score = 0

    for i, thing in enumerate(things):

        if genome[i] == 1:
            weight += thing.weight
            score += thing.value

            if weight > weight_limit:
                return 0
            
    return score

def selection(population, things, weight_limit):
    return choices(population=population, weights=[fitness(i, things, weight_limit) for i in population], k=2)

def crossing_over(genome1, genome2):

    if len(genome1) != len(genome2):
        raise ValueError('Genomes must be of equal size')

    if len(genome1) < 2:
        return genome1, genome2
    
    index = randint(0, len(genome1)-1)
    return genome1[0:index]+genome2[index:], genome2[0:index]+genome1[index:]

def mutation(genome, mutations_amt, probability=0.5):

    probability = int(probability*10)

    for _ in range(mutations_amt):

        index = randint(0, len(genome)-1)
        if randint(0, 10) > probability:
            genome[index] = 0 if genome[index] == 1 else 1
            # In the music one we have to randomly select an integer from 1-whenever we stop (as we are reperesenting notes)
             
    return genome


def evolve(generation_limit = 100):

    fit = partial(fitness, things = things, weight_limit = WEIGHT_LIMIT)
    population = generate_popluation(5, len(things))

    for i in range(generation_limit):
        print(f'Generation {i}')
        population.sort(key = fit, reverse = True) # Python's sort and sorted put it from least to greatest so we reverse
        # Also sorted is just sort EXCEPT it stores it in a new list
        
        if fit(population[0]) >= fitness_limit:
            break

        next_generation = population[0:3]

        for i in range(len(population)-2):
            parents = selection(population, things, WEIGHT_LIMIT)
            child1, child2 = crossing_over(parents[0], parents[1])
            child1 = mutation(child1, mutations_amt=randint(0,3))
            child2 = mutation(child2, mutations_amt=randint(0,3))

            next_generation += [child1, child2]

        population = next_generation
    
    return population

def genome_to_items(genome):

    ret_list = []

    for i, thing in enumerate(things):
        if genome[i] == 1:
            ret_list.append(thing.name)
    
    return ret_list

start = time.time()
population = evolve()
print(genome_to_items(population[0]))
end = time.time()
print(f'time {end-start}s')