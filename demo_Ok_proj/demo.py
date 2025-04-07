#!/usr/bin/python3
import re
import os
import argparse
import shutil
import tempfile
import subprocess
from dataclasses import dataclass
from pathlib import Path
import csv

import pipexplore.interface as interface
from pipexplore.runner import Runner


@dataclass
class OkProfile(interface.Profile):
    """
    Performance profile of a single experiment.
    """
    cycles: int
    instructions: int
    task_clock: float

    def fitness(self) -> float:
        return -self.cycles

    def constraint(self) -> bool:
        return True


class ParallelOkExperiment(interface.IndependentExperiment):

    def __init__(self, project_dir: Path):
        super().__init__()
        self.project_dir = project_dir
        self.project_target_executable = None

    def __del__(self):
        if self.project_target_executable is not None:
            to_be_deleted = Path(self.project_target_executable)
            if to_be_deleted.exists() and to_be_deleted.parent == Path(tempfile.gettempdir()):
                os.remove(to_be_deleted)

    def compile(self, cxx_path: str):
        # build in temporary directory
        with tempfile.TemporaryDirectory() as build_dir:
            subprocess.run(
                f"cmake {self.project_dir.absolute().as_posix()} -DTRANSFORMER_PATH={cxx_path} && cmake --build .",
                cwd=build_dir,
                shell=True,
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL)
            # Generate a unique path for the executable
            unique_id = next(tempfile._get_candidate_names())
            self.project_target_executable = f"{tempfile.gettempdir()}/{unique_id}"
            shutil.move(Path(build_dir) / "main", self.project_target_executable)

    def run(self, round=10) -> OkProfile:
        assert self.project_target_executable is not None and Path(
            self.project_target_executable).exists(), "Executable file not found"
        with tempfile.NamedTemporaryFile() as log_file:
            subprocess.run([
                "perf", "stat", "-r",
                str(round), "-x,", "-e", "cycles,instructions,task-clock", "-o", log_file.name,
                self.project_target_executable
            ],
                           check=True,
                           stdout=subprocess.DEVNULL,
                           stderr=subprocess.DEVNULL)

            # Extract col 1 and col 3 from the CSV output as values and keys, create the OkProfile object
            reader = csv.reader(open(log_file.name))
            metrics = dict()

            # Skip the first 2 rows (header and empty line)
            next(reader)  # Skip first row
            next(reader)  # Skip second row

            for row in reader:
                key, value = row[2], row[0]
                if key in ('cycles:u', 'instructions:u'):
                    metrics[key[:-2]] = int(value)
                elif key == 'task-clock:u':
                    metrics['task_clock'] = float(value)
        return OkProfile(**metrics)


parser = argparse.ArgumentParser()
parser.add_argument("--project-dir", type=Path, required=True)  # CMake project directory
parser.add_argument("--output", type=Path, required=True)  # path to the final optimized compiler executable
args = parser.parse_args()

if __name__ == "__main__":
    experiment = ParallelOkExperiment(args.project_dir)
    Runner(experiment, args.output).run()
