from random import randint, random

import numpy as np
from deap import creator, base, tools
from matplotlib import pyplot as plt, cm
from matplotlib.colors import ListedColormap

square_sizes = [2, 4, 6, 7, 8, 9, 11, 15, 16, 17, 18, 19, 24, 25, 27, 29, 33, 35, 37, 42, 50]
optimal_square_size = 112


def initIndividual():
    # how should we set the max value for the random
    # return randint(0, int(optimal_square_size)), randint(0, int(optimal_square_size))
    return (0, 0)


def intersectionArea(a, i, b, j):
    dx = min(a[0] + square_sizes[i], b[0] + square_sizes[j]) - max(a[0], b[0])
    dy = min(a[1] + square_sizes[i], b[1] + square_sizes[j]) - max(a[1], b[1])

    if (dx >= 0) and (dy >= 0):
        return dx * dy
    return 0


def evaluate(individual: list):
    # dimension of enclosing square
    maxX = max([x[0] + square_sizes[i] for i, x in enumerate(individual)])
    maxY = max([x[1] + square_sizes[i] for i, x in enumerate(individual)])
    comp1 = max(maxX, maxY)

    # area of overlapping squares
    comp2 = 0
    for i in range(len(individual) - 1):
        for j in range(i, len(individual)):
            comp2 += intersectionArea(individual[i], i, individual[j], j)

    return comp2,


def crossover(ind1: list, ind2: list):
    assert (len(ind1) == len(ind2))

    cxPoint = randint(0, len(ind1) - 1)
    return creator.Individual(list(ind1[:cxPoint] + ind2[cxPoint:])), creator.Individual(list(ind2[:cxPoint] + ind1[cxPoint:]))


def mutation(ind: list):
    result = ind

    mPoint = randint(0, len(ind) - 1)
    result[mPoint] = (randint(0, int(optimal_square_size)), randint(0, int(optimal_square_size)))

    return result


def mutationWithoutOverlap(ind: list):
    result = ind

    mPoint = randint(0, len(ind) - 1)

    grid = np.zeros((optimal_square_size * 3, optimal_square_size * 3))

    for square_index in range(len(square_sizes)):
        for x in range(ind[square_index][0], ind[square_index][0] + square_sizes[square_index]):
            for y in range(ind[square_index][1], ind[square_index][1] + square_sizes[square_index]):
                if square_index != mPoint:
                    grid[x, y] = square_index

    maxX = max([x[0] for x in ind])
    maxY = max([x[1] for x in ind])
    comp1 = max(maxX, maxY)

    for i in range(comp1):
        for j in range(comp1):
            try:
                for x in range(ind[mPoint][0], ind[mPoint][0] + square_sizes[mPoint]):
                    for y in range(ind[mPoint][1], ind[mPoint][1] + square_sizes[mPoint]):
                        if grid[x, y] != 0:
                            raise Exception
            except Exception:
                pass
            else:
                result[mPoint] = (i, j)
                return result

    result[mPoint] = initIndividual()

    return result


def plot(ind):
    maxX = max([x[0] + square_sizes[i] for i, x in enumerate(ind)])
    maxY = max([x[1] + square_sizes[i] for i, x in enumerate(ind)])

    grid = np.zeros((maxX, maxY))

    for square_index in range(len(square_sizes)):
        for x in range(ind[square_index][0], ind[square_index][0] + square_sizes[square_index]):
            for y in range(ind[square_index][1], ind[square_index][1] + square_sizes[square_index]):
                grid[x, y] = square_index

    my_cmap = cm.inferno(np.arange(cm.inferno.N))
    my_cmap[:, -1] = np.linspace(0, 1, cm.inferno.N)
    my_cmap = ListedColormap(my_cmap)

    plt.imshow(grid, cmap=my_cmap)
    plt.xticks([]), plt.yticks([])
    plt.show()


if __name__ == "__main__":
    creator.create("FitnessMinMin", base.Fitness, weights=(-1.0,))
    creator.create("Individual", list, fitness=creator.FitnessMinMin)

    toolbox = base.Toolbox()

    toolbox.register("individual", tools.initRepeat, creator.Individual, initIndividual, n=len(square_sizes))
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)

    toolbox.register("evaluate", evaluate)
    toolbox.register("mate", crossover)
    toolbox.register("mutate", mutation)
    toolbox.register("select", tools.selTournament)
    toolbox.register("selectBest", tools.selBest)

    stats = tools.Statistics(key=lambda ind: ind.fitness.values)
    stats.register("avg", np.mean, axis=0)
    stats.register("std", np.std, axis=0)
    stats.register("min", np.min, axis=0)
    stats.register("max", np.max, axis=0)

    pop = toolbox.population(n=100)
    CXPB, MUTPB, NGEN = 0.6, 0.2, 100

    # Evaluate the entire population
    fitnesses = map(toolbox.evaluate, pop)
    for ind, fit in zip(pop, fitnesses):
        ind.fitness.values = fit

    for g in range(NGEN):
        # Logging current population fitnesses
        record = stats.compile(pop)
        # print(record)

        # Select the next generation individuals
        offspring = toolbox.select(pop, 50, tournsize=100)
        # Clone the selected individuals
        offspring = list(map(toolbox.clone, offspring))

        # Apply crossover and mutation on the offspring
        for child1, child2 in zip(offspring[::2], offspring[1::2]):
            if random() < CXPB:
                child1, child2 = toolbox.mate(child1, child2)
                del child1.fitness.values
                del child2.fitness.values

        for mutant in offspring:
            if random() < MUTPB:
                toolbox.mutate(mutant)
                del mutant.fitness.values

        # Evaluate the individuals with an invalid fitness
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = map(toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit

        # The population is entirely replaced by the offspring
        pop[:] = offspring

        best = toolbox.selectBest(pop, 1)
        plot(best[0])
