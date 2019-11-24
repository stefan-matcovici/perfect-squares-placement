import matplotlib.pyplot as plt
import numpy as np
from matplotlib import cm

data = np.random.rand(10, 10) * 20

square_sizes = list(reversed([2, 4, 6, 7, 8, 9, 11, 15, 16, 17, 18, 19, 24, 25, 27, 29, 33, 35, 37, 42, 50]))
# square_sizes = [2, 4, 6, 7, 8, 9, 11, 15, 16, 17, 18, 19, 24, 25, 27, 29, 33, 35, 37, 42, 50]
# square_sizes = [2, 50, 4, 42, 6, 37, 7, 35, 8, 33, 9, 29, 11, 27, 15, 25, 16, 24, 17, 19, 18]
big_square_optimum = 112
grid_size = 165
grid = np.zeros((grid_size, grid_size))


def greedy(grid):
    next_square_index = 0
    for i in range(grid_size):
        for j in range(i + 1):
            grid, next_square_index = place_square(grid, next_square_index, (i - j, j))
            if next_square_index == len(square_sizes):
                return grid
    return grid


def place_square(grid, index, start):
    updated_grid = grid.copy()

    if start[0] + square_sizes[index] >= updated_grid.shape[0] or start[1] + square_sizes[index] >= updated_grid.shape[
        1]:
        return grid, index
    for i in range(start[0], start[0] + square_sizes[index]):
        for j in range(start[1], start[1] + square_sizes[index]):
            if updated_grid[i, j] != 0:
                return grid, index
            updated_grid[i, j] = index + 1
    return updated_grid, index + 1


def optimize_greedy(filled_grid):
    big_square_size = max(np.max(np.nonzero(filled_grid[0, :])), np.max(np.nonzero(filled_grid[:, 0])))

    for size in range(big_square_size - 1, 0, -1):
        filled_grid = np.zeros((size, size))
        next_square_index = 0
        try:
            for i in range(size):
                for j in range(i + 1):
                    filled_grid, next_square_index = place_square(filled_grid, next_square_index, (i - j, j))
                    if next_square_index == len(square_sizes):
                        raise Exception
            for i in range(size):
                for j in range(i, 0, -1):
                    filled_grid, next_square_index = place_square(filled_grid, next_square_index,
                                                                  (size - i + j - 1, size - j))
                    if next_square_index == len(square_sizes):
                        raise Exception
        except Exception:
            plot(filled_grid)
            perfect_placement_size = size
    return filled_grid, perfect_placement_size


def plot(grid_to_plot):
    plt.imshow(grid_to_plot, cmap=cm.inferno)
    plt.xticks([]), plt.yticks([])
    plt.show()


if __name__ == '__main__':
    filled_grid = greedy(grid)
    plot(filled_grid)
    double_filled_grid, perfect_placement_min_size = optimize_greedy(filled_grid)
    print("Min square size: ", perfect_placement_min_size)
