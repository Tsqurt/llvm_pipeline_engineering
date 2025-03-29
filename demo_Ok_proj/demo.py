#!/usr/bin/python3
import re
import os
import argparse
import shutil
import tempfile
import subprocess
from dataclasses import dataclass
from pathlib import Path

import pipexplore.interface as interface
from pipexplore.runner import Runner


@dataclass
class OkProfile(interface.Profile):
    """
    Performance profile of a single experiment.
    """
    total_computation: int

    def fitness(self) -> float:
        return -self.total_computation

    def constraint(self) -> bool:
        return True


class ParallelOkExperiment(interface.IndependentExperiment):

    def __init__(self, project_dir: Path):
        super().__init__()
        self.project_dir = project_dir
        self.project_target_executable = None

    def __del__(self):
        if self.project_target_executable:
            os.remove(self.project_target_executable.name)

    def compile(self, cxx_path: Path):
        # build in temporary directory
        with tempfile.TemporaryDirectory() as build_dir:
            subprocess.run(
                f"cmake {self.project_dir.absolute().as_posix()} -DTRANSFORMER_PATH={cxx_path} && cmake --build .",
                cwd=build_dir,
                shell=True,
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL)

            self.project_target_executable = tempfile.NamedTemporaryFile(delete=False)
            shutil.move(Path(build_dir) / "main", self.project_target_executable.name)

    def run(self) -> OkProfile:
        assert self.project_target_executable is not None and Path(
            self.project_target_executable.name).exists(), "Executable file not found"
        with tempfile.NamedTemporaryFile() as log_file:
            subprocess.run(
                ["valgrind", "--tool=callgrind", f"--log-file={log_file.name}", self.project_target_executable.name],
                cwd=tempfile.gettempdir(),
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL)
            number = re.findall(r'Collected : (\d+)', Path(log_file.name).read_text())
        total_computation = int(number[0])
        return OkProfile(total_computation=total_computation)


parser = argparse.ArgumentParser()
parser.add_argument("--project-dir", type=Path, required=True)  # CMake project directory
parser.add_argument("--output", type=Path, required=True)  # path to the final optimized compiler executable
args = parser.parse_args()

if __name__ == "__main__":
    experiment = ParallelOkExperiment(args.project_dir)
    Runner(experiment, args.output).run()
