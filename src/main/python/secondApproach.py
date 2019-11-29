import random

import numpy as np
from deap import creator, base, tools
from deap.tools import cxOrdered, mutShuffleIndexes

from greedy import greedy
from ph import phspprg
from visualize import visualize

square_sizes = [2, 4, 6, 7, 8, 9, 11, 15, 16, 17, 18, 19, 24, 25, 27, 29, 33, 35, 37, 42, 50]
optimal_square_size = 112


def evaluate(individual):
    height, _ = phspprg(optimal_square_size, [(square_sizes[i], square_sizes[i]) for i in individual])
    return height,

# def evaluate(individual):
#     height = greedy([square_sizes[i] for i in individual])
#     return height,


if __name__ == '__main__':
    creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
    creator.create("Individual", list, fitness=creator.FitnessMin)

    toolbox = base.Toolbox()

    toolbox.register("indices", random.sample, range(len(square_sizes)), len(square_sizes))
    toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.indices)

    toolbox.register("population", tools.initRepeat, list, toolbox.individual)

    toolbox.register("evaluate", evaluate)
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

    with open("bi-objective-stats.csv", "w") as f:
        for g in range(NGEN):
            # Logging current population fitnesses
            record = stats.compile(pop)
            f.write(f"{record['min'][0]},{record['avg'][0]},{record['max'][0]}\n")

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
            height, rectangles = phspprg(optimal_square_size, [(square_sizes[i], square_sizes[i]) for i in best[0]])
            visualize(optimal_square_size, height, rectangles)
