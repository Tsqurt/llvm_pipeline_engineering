import os
import llvm
import random
import copy
import re
from typing import List, Tuple
import pipexplore.interface as interface
from batch_map import batch_map

raw_available_passes = llvm.get_pipeline_str()
raw_tree = llvm.parse_string_as_tree(raw_available_passes)
atom_tree = llvm.atomize_tree(raw_tree)
available_passes = atom_tree
max_batch_size = os.cpu_count()

class Individual:
    def __init__(self, passes: List[str]):
        self.passes = passes 
        self.profile = None

    def __len__(self):
        return len(self.passes)
    
    def to_string(self):
        return ",".join(self.passes)
    
    def mutate_replace(self) -> None:
        if len(self.passes) > 0:
            pos = random.randint(0, len(self.passes) - 1)
            self.passes[pos] = random.choice(available_passes)
    
    def mutate_delete(self) -> None:
        if len(self.passes) > 1:  
            pos = random.randint(0, len(self.passes) - 1)
            self.passes.pop(pos)
    
    def mutate_insert(self) -> None:
        pos = random.randint(0, len(self.passes))
        self.passes.insert(pos, random.choice(available_passes))
    
    def mutate_swap(self) -> None:
        if len(self.passes) >= 2:
            pos1, pos2 = random.sample(range(len(self.passes)), 2)
            self.passes[pos1], self.passes[pos2] = self.passes[pos2], self.passes[pos1]
    
    def mutate_duplicate(self) -> None:
        if len(self.passes) >= 2:
            start = random.randint(0, len(self.passes) - 1)
            end = random.randint(start + 1, len(self.passes))
            segment = self.passes[start:end]
            insert_pos = random.randint(0, len(self.passes))
            self.passes[insert_pos:insert_pos] = segment
    
    def mutate_reverse(self) -> None:
        if len(self.passes) >= 2:
            start = random.randint(0, len(self.passes) - 2)
            end = random.randint(start + 1, len(self.passes))
            self.passes[start:end] = reversed(self.passes[start:end])

    @staticmethod
    def crossover(parent1: 'Individual', parent2: 'Individual') -> Tuple['Individual', 'Individual']:
        if len(parent1.passes) < 2 or len(parent2.passes) < 2:
            return parent1, parent2

        point1 = random.randint(0, min(len(parent1.passes), len(parent2.passes)) - 1)
        point2 = random.randint(point1 + 1, min(len(parent1.passes), len(parent2.passes)))

        child1_passes = (
            parent1.passes[:point1] +
            parent2.passes[point1:point2] +
            parent1.passes[point2:]
        )
        child2_passes = (
            parent2.passes[:point1] +
            parent1.passes[point1:point2] +
            parent2.passes[point2:]
        )
        
        return Individual(child1_passes), Individual(child2_passes)
    
    def run_profile(self, experiment: interface.Experiment):
        # 1. create a compiler 
        compiler_full_path = llvm.from_pipeline_make_a_compiler(self.to_string())
        # 2. copy experiment and compile
        experiment_copy = copy.deepcopy(experiment)
        try:
            experiment_copy.compile(compiler_full_path)
        except interface.CannotCompileError:
            return False

        # 3. remove the compiler
        os.remove(compiler_full_path)

        # 4. run
        try:
            self.profile = experiment_copy.run()
        except interface.MiscompilationError:
            return False
        return True 

class Population:
    # define the population
    # size: the size of the population
    def __init__(self, size: int, experiment: interface.Experiment):
        self.individuals: List[Individual] = []
        self.size = size
        self.generation = 0
        self.experiment = experiment

    def profile_individual(self):
        # 0. profile
        # Check if experiment is an instance of IndependentExperiment
        if isinstance(self.experiment, interface.IndependentExperiment):
            # Use batch_map for parallel processing if it's an IndependentExperiment

            profile_individual = lambda individual: (individual, individual.run_profile(self.experiment))
            
            results = batch_map(self.individuals, max_batch_size, profile_individual)
            # Filter out individuals that failed profiling
            self.individuals = [ind for ind, success in results if success]
        else:
            # Sequential processing for regular Experiment
            self.individuals = [ind for ind in self.individuals if ind.run_profile(self.experiment)]

    def initialize(self) -> None:
        self.individuals = []
        for _ in range(self.size):
            self.individuals.append(Individual(available_passes))
        self.profile_individual()

    def evolve(self, mutation_rate: float = 0.2) -> None:
        new_population = []

        # Retention strategy:
        # 1. Individuals with fitness less than O2 will be removed
        # 2. Keep 20% of elite individuals from equivalent code
        # 3. Keep 5% of elite individuals overall
        # 4. Randomly retain up to 25%
        elite_size = max(1, int(self.size * 0.25))  # Keep 25% elite individuals
        equ_size = max(1, int(self.size * 0.2))   # Keep 20% equivalent elite individuals  
        eli_size = max(1, int(self.size * 0.05))  # Keep 5% elite individuals
        
        equivalence_individuals = [ind for ind in self.individuals if ind.profile.constraint()]

        sorted_individuals = sorted(equivalence_individuals, 
                                     key=lambda x: x.profile.fitness(),
                                     reverse=True)

        new_population.extend(sorted_individuals[:equ_size])
        
        sorted_individuals = sorted(self.individuals, 
                                     key=lambda x: x.profile.fitness(),
                                     reverse=True)

        new_population.extend(sorted_individuals[:eli_size])
        
        while len(new_population) < elite_size:
            new_population.append(random.choice(self.individuals))

        while len(new_population) < self.size:
            parent1 = random.choice(self.individuals)
            parent2 = random.choice(self.individuals)
            
            child1, child2 = Individual.crossover(parent1, parent2)
            
            for child in [child1, child2]:
                if random.random() < mutation_rate:
                    mutation = random.choice([
                        lambda: child.mutate_replace(),
                        lambda: child.mutate_delete(),
                        lambda: child.mutate_insert(),
                        lambda: child.mutate_swap(),
                        lambda: child.mutate_duplicate(),
                        lambda: child.mutate_reverse()
                    ])
                    mutation()
            
            new_population.extend([child1, child2])
            
            if len(new_population) > self.size:
                new_population = new_population[:self.size]
        
        self.individuals = new_population
        self.generation += 1
        self.profile_individual()
    
    # return the number of individuals that satisfy the constraint
    def get_best_individual_cnt(self):
        count = 0
        for ind in self.individuals:
            if ind.profile.constraint():
                count += 1
        return count 
    
    # return the best individual that satisfies the constraint and has the highest fitness
    def get_best_individual(self):
        equivalence_individuals = [ind for ind in self.individuals if ind.profile.constraint()]
        return sorted(equivalence_individuals, key=lambda x: x.profile.fitness(), reverse=True)[0]
