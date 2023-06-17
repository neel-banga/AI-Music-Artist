# Create function with logisitic regression now! - start by importing then do it custom! or start custom?!

from sklearn.linear_model import LinearRegression
import csv
from ast import literal_eval
from typing import List
import music

import warnings
from sklearn.exceptions import ConvergenceWarning

warnings.filterwarnings("ignore", category=ConvergenceWarning)

def extract_data_csv(filename):
    data = []
    labels = []

    with open(filename, 'r') as file:
        csv_reader = csv.reader(file)

        for row in csv_reader:
            for i, value in enumerate(row):
                data.append(value) if i%2 == 0 else labels.append(value)

    return data, labels

def create_logistic_regression(data, labels):
    model = LinearRegression()
    model.fit(data, labels)
    return model

def evaluate_input(model, input: List[int]):
    return model.predict([input])[0]

def handle_string_data(data):
    return [literal_eval(element) for element in data] 

def handle_string_labels(labels):
    return [int(i) for i in labels]

def manual_fitness(genome: List[int]):
    music.play_music(genome)
    score = int(input('Rate This Song On A Scale Of 1-10: '))
    append_CSV([[genome, score]], 'midi_fitness_data.csv')
    return score

def deep_fitness(genome: List[int]):
    music.create_music(genome)
    data, labels = extract_data_csv('fitness_data.csv')
    data = handle_string_data(data)
    labels = handle_string_labels(labels)
    model = create_logistic_regression(data, labels)
    return evaluate_input(model, genome)

def append_CSV(vals: List[List[str]], csv_path: str) -> None:
    with open(csv_path, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(vals)