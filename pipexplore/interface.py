from dataclasses import dataclass
from pathlib import Path


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


class Experiment:

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
