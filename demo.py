#!/usr/bin/python3
import re
import os
import subprocess
from dataclasses import dataclass
from pathlib import Path

import pipexplore.llvm as llvm
from pipexplore.xGA import Population
import pipexplore.interface as interface

project_abs_path = os.path.abspath(os.path.dirname(__file__))

@dataclass
class OkProfile(interface.Profile):
    """
    Performance profile of a single experiment.
    """
    total_computation: int

    def fitness(self) -> float:
        return - self.total_computation

    def constraint(self) -> bool:
        return True

class OkExperiment(interface.Experiment):
    def __init__(self):
        super().__init__()

    def compile(self, cxx_path: Path):
        command1 = f"{cxx_path} -c {project_abs_path}/demo_Ok_proj/opt.c -o {project_abs_path}/demo_Ok_proj/build/CMakeFiles/main.dir/opt.c.o"
        command2 = f"cd {project_abs_path}/demo_Ok_proj/build && make"
        subprocess.run(command1, shell=True)
        subprocess.run(command2, shell=True, capture_output=True)

    def run(self) -> OkProfile:
        command1 = f"cd {llvm.tmp} && valgrind --tool=callgrind --log-file=my_output.log {project_abs_path}/demo_Ok_proj/build/main"
        subprocess.run(command1, shell=True,capture_output=True)
        with open(f"{llvm.tmp}/my_output.log", "r") as f:
            text = f.read()
        number = re.findall(r'Collected : (\d+)', text)
        total_computation = int(number[0])
        return OkProfile(total_computation=total_computation)


class ParallelOkExperiment(interface.IndependentExperiment):
    def __init__(self):
        super().__init__()

    def compile(self, cxx_path: Path):
        output_file = os.path.join(llvm.tmp, llvm.generate_random_str() + ".o")
        exec_file = os.path.join(llvm.tmp, llvm.generate_random_str())
        command1 = f"{cxx_path} -c {project_abs_path}/demo_Ok_proj/opt.c -o {output_file}"
        command2 = f"{llvm.clang} -o {exec_file} {output_file} {project_abs_path}/demo_Ok_proj/build/CMakeFiles/main.dir/*.o"
        subprocess.run(command1, shell=True)
        subprocess.run(command2, shell=True, capture_output=True)
        self.exec_file = exec_file
        os.remove(output_file)

    def run(self) -> OkProfile:
        log_file = os.path.join(llvm.tmp, llvm.generate_random_str() + ".log")
        command1 = f"cd {llvm.tmp} && valgrind --tool=callgrind --log-file={log_file} {self.exec_file}"
        subprocess.run(command1, shell=True,capture_output=True)
        with open(os.path.join(llvm.tmp, log_file), "r") as f:
            text = f.read()
        number = re.findall(r'Collected : (\d+)', text)
        total_computation = int(number[0])
        os.remove(log_file)
        os.remove(self.exec_file)
        return OkProfile(total_computation=total_computation)


def GA_mutate_on_experiment(experiment: interface.Experiment):
    population_size = 100
    generations = 100

    population = Population(population_size, experiment)
    population.initialize()

    best_ind_before = population.get_best_individual()
    best_fitness_before = best_ind_before.profile.fitness()

    for _ in range(generations):
        # Print progress bar
        progress = int((_ + 1) / generations * 50)  # 50 character progress bar
        print(f"\rGeneration {_ + 1}/{generations} [{'=' * progress}{' ' * (50-progress)}] {(_+1)/generations*100:.1f}%", end='')
        # Get the best individual and print its fitness
        best_ind = population.get_best_individual()
        best_fitness = best_ind.profile.fitness()
        print(f" Best fitness: {best_fitness}", end='')
        population.evolve()

    best_ind_after = population.get_best_individual()
    best_fitness_after = best_ind_after.profile.fitness()
    if best_fitness_after > best_fitness_before:
        print(f"GA optimized pipeline is better than O2, fitness {best_fitness_before} -> {best_fitness_after}")
        return best_ind_after.to_string()
    else:
        print(f"failed to find a better pipeline")
        return best_ind_before.to_string()

if __name__ == "__main__":
    # experiment = OkExperiment()
    experiment = ParallelOkExperiment()

    # Calculate and compare fitness between O2 and GA optimized version
    ga_pipeline = GA_mutate_on_experiment(experiment)

    print(f"GA optimized pipeline is saved in ga_compiler")
    llvm.from_pipeline_make_a_compiler_to_path(ga_pipeline,  "ga_compiler")
