#!/usr/bin/python3
import re
import os
import subprocess
from dataclasses import dataclass
from pathlib import Path

import pipexplore.interface as interface
from pipexplore.runner import Runner
from pipexplore.llvm import clang

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

    def compile(self, cxx_path: Path):
        command1 = f"{cxx_path} -c {project_abs_path}/demo_Ok_proj/opt.c -o {project_abs_path}/demo_Ok_proj/build/CMakeFiles/main.dir/opt.c.o"
        command2 = f"cd {project_abs_path}/demo_Ok_proj/build && make"
        subprocess.run(command1, shell=True)
        subprocess.run(command2, shell=True, capture_output=True)

    def run(self) -> OkProfile:
        command1 = f"cd {interface.tmp} && valgrind --tool=callgrind --log-file=my_output.log {project_abs_path}/demo_Ok_proj/build/main"
        subprocess.run(command1, shell=True,capture_output=True)
        with open(f"{interface.tmp}/my_output.log", "r") as f:
            text = f.read()
        number = re.findall(r'Collected : (\d+)', text)
        total_computation = int(number[0])
        return OkProfile(total_computation=total_computation)


class ParallelOkExperiment(interface.IndependentExperiment):

    def compile(self, cxx_path: Path):
        output_file = os.path.join(interface.tmp, interface.generate_random_str() + ".o")
        exec_file = os.path.join(interface.tmp, interface.generate_random_str())
        command1 = f"{cxx_path} -c {project_abs_path}/demo_Ok_proj/opt.c -o {output_file}"
        command2 = f"{clang} -o {exec_file} {output_file} {project_abs_path}/demo_Ok_proj/build/CMakeFiles/main.dir/*.o"
        subprocess.run(command1, shell=True)
        subprocess.run(command2, shell=True, capture_output=True)
        self.exec_file = exec_file
        os.remove(output_file)

    def run(self) -> OkProfile:
        log_file = os.path.join(interface.tmp, interface.generate_random_str() + ".log")
        command1 = f"cd {interface.tmp} && valgrind --tool=callgrind --log-file={log_file} {self.exec_file}"
        subprocess.run(command1, shell=True,capture_output=True)
        with open(os.path.join(interface.tmp, log_file), "r") as f:
            text = f.read()
        number = re.findall(r'Collected : (\d+)', text)
        total_computation = int(number[0])
        os.remove(log_file)
        os.remove(self.exec_file)
        return OkProfile(total_computation=total_computation)


if __name__ == "__main__":
    # experiment = OkExperiment()
    experiment = ParallelOkExperiment()

    runner = Runner(experiment, Path("ga_compiler"))
    runner.run()
