import os

from pipexplore.interface import Experiment, Profile


class MyProfile(Profile):
    def fitness(self) -> float:
        return 0.0


class MyExperiment(Experiment):
    def compile(self, cxx_path):
        os.system("CXX={cxx_path} make")
