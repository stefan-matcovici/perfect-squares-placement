import numpy as np

import datasets


def initial_greedy(grid, sizes, grid_size):
    next_square_index = 0
    for i in range(grid_size):
        for j in range(i + 1):
            grid, next_square_index = place_square(grid, sizes, next_square_index, (i - j, j))
            if next_square_index == len(sizes):
                return grid
    return grid


def place_square(grid, sizes, index, start):
    updated_grid = grid.copy()

    if start[0] + sizes[index] >= updated_grid.shape[0] or start[1] + sizes[index] >= updated_grid.shape[1]:
        return grid, index
    for i in range(start[0], start[0] + sizes[index]):
        for j in range(start[1], start[1] + sizes[index]):
            if updated_grid[i, j] != 0:
                return grid, index
            updated_grid[i, j] = index + 1
    return updated_grid, index + 1


def optimize_greedy(filled_grid, sizes, big_square_optimum):
    big_square_size = max(np.max(np.nonzero(filled_grid[0, :])), np.max(np.nonzero(filled_grid[:, 0])))

    perfect_size = np.inf

    for size in range(big_square_size - 1, big_square_optimum, -1):
        filled_grid = np.zeros((size, size))
        next_square_index = 0
        try:
            for i in range(size):
                for j in range(i + 1):
                    filled_grid, next_square_index = place_square(filled_grid, sizes, next_square_index, (i - j, j))
                    if next_square_index == len(sizes):
                        raise Exception
            for i in range(size):
                for j in range(i, 0, -1):
                    filled_grid, next_square_index = place_square(filled_grid, sizes, next_square_index,
                                                                  (size - i + j - 1, size - j))
                    if next_square_index == len(sizes):
                        raise Exception
        except Exception:
            perfect_size = size
    return filled_grid, perfect_size


def greedy(dataset: datasets.Dataset):
    starting_grid_size = int(dataset.master_square_size * 1.5)

    grid = np.zeros((starting_grid_size, starting_grid_size))
    filled_grid = initial_greedy(grid, dataset.square_sizes, starting_grid_size)
    double_filled_grid, perfect_placement_min_size = optimize_greedy(filled_grid, dataset.square_sizes,
                                                                     dataset.master_square_size)

    return perfect_placement_min_size


if __name__ == '__main__':
    dataset = datasets.datasets[6]
    print(greedy(dataset))
