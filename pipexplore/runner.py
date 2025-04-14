from pathlib import Path

from pipexplore.interface import Experiment, IndependentExperiment
import pipexplore.llvm as llvm
from pipexplore.xGA import Population


class Runner:
    def __init__(self,
                 experiment: Experiment | IndependentExperiment,
                 output_binary_path: Path,
                 population_size: int = 100,
                 generations: int = 100,
                 log_path: Path = None):
        self.experiment = experiment
        self.output_binary_path = output_binary_path
        self.population_size = population_size
        self.generations = generations
        self.log_path = log_path
    
    def run(self):
        # Calculate and compare fitness between O2 and GA optimized version
        population = Population(self.population_size, self.experiment)
        population.initialize()

        if population.get_best_individual_cnt() == 0:
            with open(self.log_path, 'w') as f:
                f.write("No valid pipelines found, exiting")
            return

        best_ind_before = population.get_best_individual()
        best_fitness_before = best_ind_before.profile.fitness()

        if self.log_path:
            with open(self.log_path, 'w') as f:
                f.write(f"Generation {0} fitness: {best_fitness_before}\n")

        for _ in range(self.generations):
            # Print progress bar
            progress = int((_ + 1) / self.generations * 50)  # 50 character progress bar
            print(f"\rGeneration {_ + 1}/{self.generations} [{'=' * progress}{' ' * (50-progress)}] {(_+1)/self.generations*100:.1f}%", end='')
            # Get the best individual and print its fitness
            best_ind = population.get_best_individual()
            best_fitness = best_ind.profile.fitness()
            print(f" Best fitness: {best_fitness}", end='')
            population.evolve()

            if self.log_path:
                with open(self.log_path, 'a') as f:
                    f.write(f"Generation {_ + 1} best fitness: {best_fitness}\n")
                    for ind in population.individuals:
                        f.write(f"\t(fitness: {ind.profile.fitness()}) passes: {ind.to_string()}\n")

        best_ind_after = population.get_best_individual()
        best_fitness_after = best_ind_after.profile.fitness()
        if best_fitness_after > best_fitness_before:
            print(f"GA optimized pipeline is better than baseline*, fitness {best_fitness_before} -> {best_fitness_after}")
            ga_pipeline = best_ind_after.to_string()
        else:
            print(f"failed to find a better pipeline")
            ga_pipeline = best_ind_before.to_string()

        print(f"GA optimized pipeline is saved in {self.output_binary_path.as_posix()}")
        llvm.from_pipeline_make_a_compiler_to_path(ga_pipeline,  self.output_binary_path)
