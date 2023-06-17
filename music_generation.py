from random import choices, randrange, randint
import music
from typing import List
from fitness import *

def generate_genome(length):
    return [randrange(music.END_NOTE_NUM) for _ in range(length)]

def generate_population(population_size, genome_length):
    return [generate_genome(genome_length) for _ in range(population_size)]

def selection(population: List[List[int]], fitness_scores: List[int]):
    return choices(population=population, weights=fitness_scores, k=2)

def crossing_over(genome1: List[int], genome2: List[int]):

    if len(genome1) != len(genome2):
        raise ValueError('Genomes must be of equal size')

    if len(genome1) < 2:
        return genome1, genome2
    
    index = randint(0, len(genome1)-1)
    return genome1[0:index]+genome2[index:], genome2[0:index]+genome1[index:]

def mutation(genome: List[int], mutations_amt: int, probability=0.4) -> List[int]:

    probability = 10 - (int(probability*10))

    # So 0.4 turns into 6, so there is only 4 values that can beat it leading to a 40% chance

    for _ in range(mutations_amt):

        index = randint(0, len(genome)-1)
        if randint(0, 10) > probability:
            genome[index] = randrange(music.END_NOTE_NUM)
             
    return genome

def evolve(fitness_limit=15, generation_limit = 100):

    population = generate_population(6, 20)

    for i in range(generation_limit):
        print(f'Generation {i}')

        fitness_scores = [deep_fitness(genome) for genome in population]

        sorted_population = sorted(population, key=lambda x: fitness_scores[population.index(x)], reverse=True) 
        
        best_index = population.index(sorted_population[0])

        if fitness_scores[best_index] >= fitness_limit:
            break

        next_generation = sorted_population[0:2]

        for i in range(2):
            parents = selection(population, fitness_scores) # This function takes fitness
            child1, child2 = crossing_over(parents[0], parents[1])

            next_generation += [child1, child2]

        next_generation = [mutation(genome, mutations_amt=randint(0, 5)) for genome in next_generation]

        population = next_generation

    return population

if __name__ == '__main__':
    a = evolve()
    print(a)
    music.create_music(a[0])
    music.play_midi_file()