from random import choices, randrange, randint
import music
import csv
from typing import List, Tuple

def generate_genome(length):
    return [randrange(music.END_NOTE_NUM) for _ in range(length)]

def generate_population(population_size, genome_length):
    return [generate_genome(genome_length) for _ in range(population_size)]

# Eventually score fitness with neural network for now manually rate it

# Add a method that takes in the genome and rating and then puts it in like a CSV file or something
# Then make a method that uses that CSV file to create training data lists and makes a Logistic Regression Model
# And Then make a function called deep_fitness or something and have it use the regression model
# Also connect on github and publish this even if it's a bit small - maybe make a website for more LOC? User puts in instrament so 1-whatever it ends 
# and we just play the music.wav 
# The only issue with this opposed to a neural net is it has to "train" everytime
# Put this in it's own file? Write Logistic Regression from scratch

def fitness(genome: List[int]):
    
    music.create_music(genome)
    #music.play_music()

    score = int(input('Rate This Song On A Scale Of 1-10: '))

    append_CSV([[genome, score]], 'fitness_data.csv')

    return score

def append_CSV(vals: List[List[str]], csv_path: str) -> None:

    with open(csv_path, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(vals)

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

def evolve(fitness_limit=10, generation_limit = 100):

    population = generate_population(6, 20)

    for i in range(generation_limit):
        print(f'Generation {i}')

        fitness_scores = [fitness(genome) for genome in population]

        print(fitness_scores)

        sorted_population = sorted(population, key=lambda x: fitness_scores[population.index(x)], reverse=True) 
        
        best_index = population.index(sorted_population[0])

        if fitness_scores[best_index] >= fitness_limit:
            break

        print('making next gn')
        next_generation = sorted_population[0:2]
        print(next_generation)

        for i in range(2):
            parents = selection(population, fitness_scores) # This function takes fitness
            child1, child2 = crossing_over(parents[0], parents[1])

            next_generation += [child1, child2]

        next_generation = [mutation(genome, mutations_amt=randint(0, 5)) for genome in next_generation]

        print(len(next_generation))


        population = next_generation

    return population

evolve()