#!/usr/bin/python3

import llvm
import conf
from GA import Individual, Population, atom_tree

def GA_mutate_on_file(ll_str, input_str = "", output_str = ""):
    population_size = 200
    generations = 200

    # if you don't want to compare with O2, modify the following line:
    current_file_O2_ll = llvm.pipeline_opt(ll_str, llvm.compose_atom_tree(atom_tree))

    population = Population(population_size, ll_str, current_file_O2_ll, conf.constraint_correctness, conf.fitness_efficiency, input_str, output_str)
    population.initialize()

    for _ in range(generations):
        # Print progress bar
        progress = int((_ + 1) / generations * 50)  # 50 character progress bar
        print(f"\rGeneration {_ + 1}/{generations} [{'=' * progress}{' ' * (50-progress)}] {(_+1)/generations*100:.1f}%", end='')
        # Get the best individual and print its fitness
        best_ind = population.get_best_individual()
        best_fitness = population.fitness_func(best_ind.to_string(), population.raw_ll, population.opt_ll, population.input_str, population.output_str)
        print(f" Best fitness: {best_fitness}", end='')
        population.evolve()
    
    return  population.get_best_individual().to_string()

import sys
if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python3 util_GA.py <file.ll> <input_file> <output_file>")
        sys.exit(1)
    try:
        ll_str = open(sys.argv[1], "r").read()
        input_str = open(sys.argv[2], "r").read()
        output_str = open(sys.argv[3], "r").read()
    except Exception as e:
        print(e)
        sys.exit(1)
    # Calculate and compare fitness between O2 and GA optimized version
    ga_pipeline = GA_mutate_on_file(ll_str, input_str, output_str)
    o2_pipeline = llvm.compose_atom_tree(atom_tree)
    
    ga_fitness = conf.fitness_efficiency(ga_pipeline, ll_str, None, input_str, output_str)
    o2_fitness = conf.fitness_efficiency(o2_pipeline, ll_str, None, input_str, output_str)
    
    print(f"\nFitness comparison:")
    print(f"GA optimized fitness: {ga_fitness}")
    print(f"O2 optimized fitness: {o2_fitness}")
    print(f"Improvement ratio: {ga_fitness/o2_fitness:.2f}x")