import logging

import numpy as np
from ConfigSpace.hyperparameters import UniformFloatHyperparameter, UniformIntegerHyperparameter
from smac.configspace import ConfigurationSpace
from smac.facade.smac_bo_facade import SMAC4BO
from smac.scenario.scenario import Scenario

from datasets import datasets
from firstApproach import genetic_algorithm

logging.basicConfig(level=logging.INFO)


def genetic(conf):
    hof = genetic_algorithm(dataset, conf['pop_size'], conf['crossover_rate'], conf['mutation_rate'],
                            conf['no_generations'],
                            False)
    hof_objective_values = list(map(lambda x: x.values, hof.keys))
    return np.mean([x[1] for x in hof_objective_values])


if __name__ == "__main__":
    dataset = datasets[0]

    configuration_space = ConfigurationSpace()
    pop_size_hyperparam = UniformIntegerHyperparameter("pop_size", 10, 200, default_value=100)
    crossover_hyperparam = UniformFloatHyperparameter("crossover_rate", 0.7, 0.99, default_value=0.9)
    mutation_hyperparam = UniformFloatHyperparameter("mutation_rate", 0.01, 0.3, default_value=0.1)
    no_generation_hyperparam = UniformIntegerHyperparameter("no_generations", 50, 120, default_value=70)

    configuration_space.add_hyperparameters(
        [pop_size_hyperparam, crossover_hyperparam, mutation_hyperparam, no_generation_hyperparam])

    scenario = Scenario({"run_obj": "quality",
                         "runcount-limit": 30,
                         "cs": configuration_space,
                         "deterministic": "true"
                         })

    smac = SMAC4BO(scenario=scenario, rng=np.random.RandomState(42), tae_runner=genetic, )
    smac.optimize()
