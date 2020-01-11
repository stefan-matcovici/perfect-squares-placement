import random

import numpy as np
from deap import creator, base, tools
from deap.tools import cxOrdered, mutShuffleIndexes

from datasets import Dataset, datasets
from priorityHeuristic import phspprg
from visualize import visualize


def evaluate(dataset: Dataset, individual: list):
    height, _ = phspprg(dataset.master_square_size,
                        [(dataset.square_sizes[i], dataset.square_sizes[i]) for i in individual])
    return height,


def genetic_algorithm(dataset: Dataset, verbose=False):
    creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
    creator.create("Individual", list, fitness=creator.FitnessMin)

    toolbox = base.Toolbox()

    toolbox.register("indices", random.sample, range(len(dataset.square_sizes)), len(dataset.square_sizes))
    toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.indices)

    toolbox.register("population", tools.initRepeat, list, toolbox.individual)

    toolbox.register("evaluate", evaluate, dataset)
    toolbox.register("mate", cxOrdered)
    toolbox.register("mutate", mutShuffleIndexes)
    toolbox.register("select", tools.selRoulette)
    toolbox.register("selectBest", tools.selBest)

    stats = tools.Statistics(key=lambda ind: ind.fitness.values)
    stats.register("avg", np.mean, axis=0)
    stats.register("std", np.std, axis=0)
    stats.register("min", np.min, axis=0)
    stats.register("max", np.max, axis=0)

    pop = toolbox.population(n=10)
    CXPB, MUTPB, NGEN = 0.6, 0.1, 50

    # Evaluate the entire population
    fitnesses = map(toolbox.evaluate, pop)
    for ind, fit in zip(pop, fitnesses):
        ind.fitness.values = fit

    for g in range(NGEN):
        # Logging current population fitnesses
        record = stats.compile(pop)
        if verbose:
            print(record)

        # Select the next generation individuals
        offspring = toolbox.select(pop, 100)
        # Clone the selected individuals
        offspring = list(map(toolbox.clone, offspring))

        # Apply crossover and mutation on the offspring
        for child1, child2 in zip(offspring[::2], offspring[1::2]):
            if random.random() < CXPB:
                child1, child2 = toolbox.mate(child1, child2)
                del child1.fitness.values
                del child2.fitness.values

        for mutant in offspring:
            if random.random() < MUTPB:
                toolbox.mutate(mutant, 0.7)
                del mutant.fitness.values

        # Evaluate the individuals with an invalid fitness
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = map(toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit

        # The population is entirely replaced by the offspring
        pop[:] = offspring

        best = toolbox.selectBest(pop, 1)

        height, rectangles = phspprg(dataset.master_square_size,
                                     [(dataset.square_sizes[i], dataset.square_sizes[i]) for i in best[0]])
        if verbose:
            visualize(dataset.master_square_size, height, rectangles)

    return best[0]


if __name__ == '__main__':
    best = genetic_algorithm(dataset=datasets[0])
    print(best.fitness)
