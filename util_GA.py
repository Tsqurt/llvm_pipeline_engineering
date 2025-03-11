#!/usr/bin/python3

import llvm
import conf
from GA import Individual, Population, atom_tree

def GA_mutate_on_file(ll_str, input_str = "", output_str = ""):
    population_size = 200
    generations = 200

    # if you don't want to compare with O2, modify the following line:
    current_file_O2_ll = llvm.pipeline_opt(ll_str, llvm.compose_atom_tree(atom_tree))

    population = Population(population_size, ll_str, current_file_O2_ll, conf.constraint_Semantic, conf.fitness_debugLoc, input_str, output_str)
    population.initialize()

    for _ in range(generations):
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
    print(GA_mutate_on_file(ll_str, input_str, output_str))