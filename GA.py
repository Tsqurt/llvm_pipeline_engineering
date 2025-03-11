
import llvm
import random
import re
from typing import List, Tuple
import conf
raw_available_passes = llvm.get_pipeline_str()
raw_tree = llvm.parse_string_as_tree(raw_available_passes)
atom_tree = llvm.atomize_tree(raw_tree)
available_passes = atom_tree

class Individual:
    def __init__(self, passes: List[str]):
        self.passes = passes 
    
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
    
class Population:
    # define the population
    # size: the size of the population
    # raw_ll: the raw LLVM IR code
    # opt_ll: the optimized LLVM IR code
    # constraint_func: the constraint function
    # fitness_func: the fitness function
    # input_str: the input string
    # output_str: the output string
    def __init__(self, size: int,
                 raw_ll: str,
                 opt_ll: str,
                 constraint_func,
                 fitness_func,
                 input_str,
                 output_str):
        self.individuals: List[Individual] = []
        self.size = size
        self.generation = 0
        self.raw_ll = raw_ll
        self.opt_ll = opt_ll
        self.input_str = input_str
        self.output_str = output_str
        self.constraint_func = constraint_func
        self.fitness_func = fitness_func

    def initialize(self) -> None:
        self.individuals = []
        for _ in range(self.size):
            self.individuals.append(Individual(available_passes))
    
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
        
        equivalence_individuals = [ind for ind in self.individuals if ind.constraint(self.raw_ll, self.opt_ll)]

        sorted_individuals = sorted(equivalence_individuals, 
                                     key=lambda x: self.fitness_func(x.to_string(), self.raw_ll, self.input_str, self.output_str),
                                     reverse=True)

        new_population.extend(sorted_individuals[:equ_size])
        
        sorted_individuals = sorted(self.individuals, 
                                     key=lambda x: self.fitness_func(x.to_string(), self.raw_ll, self.input_str, self.output_str),
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
    
    # return the number of individuals that satisfy the constraint
    def get_best_individual_cnt(self):
        count = 0
        for ind in self.individuals:
            if self.constraint_func(ind.to_string(), self.raw_ll, self.opt_ll, self.input_str, self.output_str):
                count += 1
        return count 
    
    # return the best individual that satisfies the constraint and has the highest fitness
    def get_best_individual(self):
        equivalence_individuals = [ind for ind in self.individuals if self.constraint_func(ind.to_string(), self.raw_ll, self.opt_ll, self.input_str, self.output_str)]
        return sorted(equivalence_individuals, key=lambda x: self.fitness_func(x.to_string(), self.raw_ll, self.input_str, self.output_str), reverse=True)[0]
