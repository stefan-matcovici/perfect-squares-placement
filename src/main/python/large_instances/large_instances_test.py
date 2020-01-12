from multiprocessing import Manager

from datasets import Dataset, datasets
from greedy import greedy
from large_instances.timing import timing


@timing(timeout=100)
def call_greedy(dataset: Dataset, r):
    r.value = greedy(dataset)


if __name__ == '__main__':
    print("instance_no,optim,square_no,result,time")
    manager = Manager()

    for i in range(100):
        dataset = datasets[i]
        result, t = call_greedy(dataset)
        print(f"{i},{dataset.master_square_size},{dataset.no_squares},{result},{t:.2f}")
