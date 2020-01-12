from random import randint

import numpy as np
from deap import creator, base, tools, algorithms
from matplotlib import pyplot as plt, cm
from matplotlib.colors import ListedColormap

import datasets


def initIndividual():
    # how should we set the max value for the random
    # return randint(0, int(optimal_square_size)), randint(0, int(optimal_square_size))
    return 0, 0


def intersectionArea(a, i, b, j, square_sizes: list):
    dx = min(a[0] + square_sizes[i], b[0] + square_sizes[j]) - max(a[0], b[0])
    dy = min(a[1] + square_sizes[i], b[1] + square_sizes[j]) - max(a[1], b[1])

    if (dx >= 0) and (dy >= 0):
        return dx * dy
    return 0


def evaluate(square_sizes: list, individual: list):
    # dimension of enclosing square
    maxX = max([x[0] + square_sizes[i] for i, x in enumerate(individual)])
    maxY = max([x[1] + square_sizes[i] for i, x in enumerate(individual)])
    comp1 = max(maxX, maxY)

    # area of overlapping squares
    comp2 = 0
    for i in range(len(individual) - 1):
        for j in range(i + 1, len(individual)):
            comp2 += intersectionArea(individual[i], i, individual[j], j, square_sizes)

    return comp1, comp2


def crossover(ind1: list, ind2: list):
    assert (len(ind1) == len(ind2))

    cxPoint = randint(0, len(ind1) - 1)
    return creator.Individual(list(ind1[:cxPoint] + ind2[cxPoint:])), creator.Individual(
        list(ind2[:cxPoint] + ind1[cxPoint:]))


def mutation(dataset: datasets.Dataset, ind: list):
    result = ind

    mPoint = randint(0, len(ind) - 1)
    result[mPoint] = (
        randint(0, int(dataset.master_square_size * 1.5)), randint(0, int(dataset.master_square_size * 1.5)))

    return result,


def mutationWithoutOverlap(dataset: datasets.Dataset, ind: list):
    result = ind

    mPoint = randint(0, len(ind) - 1)

    grid = np.zeros((dataset.master_square_size * 3, dataset.master_square_size * 3))

    for square_index in range(len(dataset.square_sizes)):
        for x in range(ind[square_index][0], ind[square_index][0] + dataset.square_sizes[square_index]):
            for y in range(ind[square_index][1], ind[square_index][1] + dataset.square_sizes[square_index]):
                if square_index != mPoint:
                    grid[x, y] = square_index

    maxX = max([x[0] for x in ind])
    maxY = max([x[1] for x in ind])
    comp1 = max(maxX, maxY)

    for i in range(comp1):
        for j in range(comp1):
            try:
                for x in range(ind[mPoint][0], ind[mPoint][0] + dataset.square_sizes[mPoint]):
                    for y in range(ind[mPoint][1], ind[mPoint][1] + dataset.square_sizes[mPoint]):
                        if grid[x, y] != 0:
                            raise Exception
            except Exception:
                pass
            else:
                result[mPoint] = (i, j)
                return result

    result[mPoint] = initIndividual()

    return result


def plot(ind, square_sizes):
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

    plt.imshow(grid, cmap=my_cmap, alpha=0.3)
    plt.xticks([]), plt.yticks([])
    plt.show()


def genetic_algorithm(dataset: datasets.Dataset, population_size: int, crossover_rate: float, mutation_rate: float,
                      no_generations: int, verbose=False):
    creator.create("FitnessMinMin", base.Fitness, weights=(-1.0, -1.0))
    creator.create("Individual", list, fitness=creator.FitnessMinMin)

    toolbox = base.Toolbox()

    toolbox.register("individual", tools.initRepeat, creator.Individual, initIndividual, n=dataset.no_squares)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)

    toolbox.register("evaluate", evaluate, dataset.square_sizes)
    toolbox.register("mate", crossover)
    toolbox.register("mutate", mutation, dataset)
    toolbox.register("select", tools.selNSGA2)
    toolbox.register("selectBest", tools.selBest)

    stats = None
    if verbose:
        stats = tools.Statistics(key=lambda ind: ind.fitness.values)
        stats.register("avg", np.mean, axis=0)
        stats.register("std", np.std, axis=0)
        stats.register("min", np.min, axis=0)
        stats.register("max", np.max, axis=0)

    pop = toolbox.population(n=population_size)

    hof = tools.ParetoFront()

    algorithms.eaSimple(pop, toolbox, crossover_rate, mutation_rate, ngen=no_generations, stats=stats, halloffame=hof,
                        verbose=verbose)
    return hof


if __name__ == "__main__":
    dataset = datasets.datasets[0]

    hof = genetic_algorithm(dataset=dataset, population_size=100, crossover_rate=0.6, mutation_rate=0.2,
                            no_generations=10, verbose=False)
    hof_objective_values = list(map(lambda x: x.values, hof.keys))

    plt.scatter([x[0] for x in hof_objective_values], [x[1] for x in hof_objective_values])
    plt.xlabel("Enclosing square size")
    plt.ylabel("Overalapping area")
    plt.axvline(x=dataset.master_square_size, label='Optimal value for enclosing square size', c='r')
    plt.legend()
    plt.show()
