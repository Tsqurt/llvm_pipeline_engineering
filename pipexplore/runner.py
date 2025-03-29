from pathlib import Path

from pipexplore.interface import Experiment, IndependentExperiment
import pipexplore.llvm as llvm
from pipexplore.xGA import Population


class Runner:
    def __init__(self,
                 experiment: Experiment | IndependentExperiment,
                 output_binary_path: Path,
                 population_size: int = 100,
                 generations: int = 100):
        self.experiment = experiment
        self.output_binary_path = output_binary_path
        self.population_size = population_size
        self.generations = generations

    def run(self):
        # Calculate and compare fitness between O2 and GA optimized version
        population = Population(self.population_size, self.experiment)
        population.initialize()

        best_ind_before = population.get_best_individual()
        best_fitness_before = best_ind_before.profile.fitness()

        for _ in range(self.generations):
            # Print progress bar
            progress = int((_ + 1) / self.generations * 50)  # 50 character progress bar
            print(f"\rGeneration {_ + 1}/{self.generations} [{'=' * progress}{' ' * (50-progress)}] {(_+1)/self.generations*100:.1f}%", end='')
            # Get the best individual and print its fitness
            best_ind = population.get_best_individual()
            best_fitness = best_ind.profile.fitness()
            print(f" Best fitness: {best_fitness}", end='')
            population.evolve()

        best_ind_after = population.get_best_individual()
        best_fitness_after = best_ind_after.profile.fitness()
        if best_fitness_after > best_fitness_before:
            print(f"GA optimized pipeline is better than O2, fitness {best_fitness_before} -> {best_fitness_after}")
            ga_pipeline = best_ind_after.to_string()
        else:
            print(f"failed to find a better pipeline")
            ga_pipeline = best_ind_before.to_string()

        print(f"GA optimized pipeline is saved in {self.output_binary_path.as_posix()}")
        llvm.from_pipeline_make_a_compiler_to_path(ga_pipeline,  self.output_binary_path)
