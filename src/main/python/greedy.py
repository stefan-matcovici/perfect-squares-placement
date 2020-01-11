import numpy as np

import datasets


def get_enclosing_square_size(grid: np.ndarray):
    return np.max(np.nonzero(grid))


def initial_greedy(grid, sizes, grid_size):
    next_square_index = 0
    for i in range(grid_size):
        for j in range(i + 1):
            grid, next_square_index = place_square(grid, sizes, next_square_index, (i - j, j))
            if next_square_index == len(sizes):
                return grid
    exit(1)


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


def optimize_binary_search_greedy(filled_grid, sizes, big_square_optimum):
    big_square_size = get_enclosing_square_size(filled_grid)

    optimal_filled_grid = filled_grid.copy()
    optimal_square_size = big_square_size

    size_to_attempt = (big_square_size + big_square_optimum) // 2
    last_size_to_attempt = -1
    found_solution = False

    while not found_solution:
        try:
            grid = fill_both_ways(size_to_attempt, sizes)
        except Exception:
            if size_to_attempt == last_size_to_attempt:
                last_size_to_attempt = big_square_size
                break

            last_size_to_attempt = size_to_attempt
            size_to_attempt = (size_to_attempt + big_square_size + 1) // 2
        else:
            optimal_filled_grid = grid
            optimal_square_size = size_to_attempt
            break

    for size in range(size_to_attempt - 1, last_size_to_attempt, -1):
        try:
            grid = fill_both_ways(size, sizes)
        except Exception:
            pass
        else:
            optimal_filled_grid = grid
            optimal_square_size = size

    return optimal_filled_grid, optimal_square_size


def optimize_greedy(filled_grid, sizes, big_square_optimum):
    big_square_size = get_enclosing_square_size(filled_grid)

    optimal_filled_grid = filled_grid.copy()
    optimal_square_size = big_square_size

    for size in range(big_square_size - 1, big_square_optimum, -1):
        try:
            grid = fill_both_ways(size, sizes)
        except Exception:
            pass
        else:
            optimal_filled_grid = grid
            optimal_square_size = size

    return optimal_filled_grid, optimal_square_size


def fill_both_ways(size_attempt, square_sizes):
    current_filled_grid = np.zeros((size_attempt, size_attempt))
    next_square_index = 0
    for i in range(size_attempt):
        for j in range(i + 1):
            current_filled_grid, next_square_index = place_square(current_filled_grid, square_sizes, next_square_index,
                                                                  (i - j, j))
            if next_square_index == len(square_sizes):
                return current_filled_grid
    for i in range(size_attempt):
        for j in range(i, 0, -1):
            current_filled_grid, next_square_index = place_square(current_filled_grid, square_sizes, next_square_index,
                                                                  (size_attempt - i + j - 1, size_attempt - j))
            if next_square_index == len(square_sizes):
                return current_filled_grid
    raise Exception


def greedy(dataset: datasets.Dataset):
    starting_grid_size = int(dataset.master_square_size * 1.4)

    grid = np.zeros((starting_grid_size, starting_grid_size))
    filled_grid = initial_greedy(grid, dataset.square_sizes, starting_grid_size)
    double_filled_grid, perfect_placement_min_size = optimize_binary_search_greedy(filled_grid, dataset.square_sizes,
                                                                                   dataset.master_square_size)

    return perfect_placement_min_size


if __name__ == '__main__':
    dataset = datasets.datasets[6]
    print(greedy(dataset))
