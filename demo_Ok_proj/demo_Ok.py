import sys
import os
import subprocess
import re

_proj_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 添加父目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pipexplore.interface import *

@dataclass
class OkProfile(Profile):
    """
    Performance profile of a single experiment.
    """
    total_computation: int
    def fitness(self) -> float:
        return self.total_computation

class OkExperiment(Experiment):
    def __init__(self):
        super().__init__()

    def compile(self, cxx_path: Path):
        command1 = f"{cxx_path} {_proj_path}/demo_Ok_proj/opt.c -o {_proj_path}/demo_Ok_proj/build/CMakeFiles/main.dir/opt.c.o"
        command2 = f"cd {_proj_path}/demo_Ok_proj/build && make"
        subprocess.run(command1, shell=True)
        subprocess.run(command2, shell=True)
    
    def run(self) -> OkProfile:
        command1 = f"cd /tmp/ && valgrind --tool=callgrind --log-file=my_output.log {_proj_path}/demo_Ok_proj/build/main"
        subprocess.run(command1, shell=True, capture_output=True)
        with open("/tmp/my_output.log", "r") as f:
            text = f.read()
        number = re.findall(r'Collected : (\d+)', text)
        total_computation = int(number[0])
        return OkProfile(total_computation=total_computation)

if __name__ == "__main__":
    experiment = OkExperiment()
    profile = experiment.run()
    print(profile)