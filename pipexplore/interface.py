import random

from dataclasses import dataclass
from pathlib import Path


tmp = "/tmp"


def generate_random_str():
    keys = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    return ''.join(random.choices(keys, k=32))


class CannotCompileError(Exception):
    '''
    Raised by the user when a compilation fails.
    '''
    pass


class MiscompilationError(Exception):
    '''
    Raised by the user when a miscompilation is detected at runtime.
    '''
    pass


@dataclass
class Profile:
    """
    Performance profile of a single experiment.
    """
    def fitness(self) -> float:
        raise NotImplementedError("This should be implemented by the user.")

    """
    Optional: if some cases are not valid but potentially beneficial for evolution, return False.
    """
    def constraint(self) -> bool:
        return True

class Experiment:
    """
    In our usage of experiment, every instance will call 'compile()' only once and then 'run()' only once.
    And once 'compile()' of an object is called, we would never copy this object later.
    So feel free if you want to save some information in this object. (^_^)
    """
    def compile(self, cxx_path: Path):
        '''
        Compile with the given compiler.
        '''
        raise NotImplementedError("This should be implemented by the user.")

    def run(self) -> Profile:
        '''
        Run the executable and obtain profiling data.
        '''
        raise NotImplementedError("This should be implemented by the user.")

class IndependentExperiment(Experiment):
    """
    Optional:Independent experiment class.
    When implementing this class, ensure that compile and run methods are thread-safe,
    and do not share resources that could lead to race conditions.
    """
    def compile(self, cxx_path: Path):
        '''
        Compile with the given compiler.
        This method must be thread-safe and can be executed concurrently.
        '''
        raise NotImplementedError("This should be implemented by the user.")

    def run(self) -> Profile:
        '''
        Run the executable and obtain profiling data.
        This method must be thread-safe and can be executed concurrently.
        '''
        raise NotImplementedError("This should be implemented by the user.")