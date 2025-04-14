# batch map with CPU core binding, avoiding CPU0
# argument: atom list, batch size, atom function, but in parallel with CPU affinity
# return: [atom_func(atom) for atom in atom_list]
# 处理一个批次并绑定到特定核心
import os
import psutil
import multiprocessing
from concurrent.futures import ThreadPoolExecutor

def batch_map(atom_list, batch_size, atom_func):

    # 获取物理核心数(C数)，而非逻辑处理器数(T数)
    physical_cores = psutil.cpu_count(logical=False)

    with ThreadPoolExecutor(max_workers=physical_cores) as executor:
        # ThreadPoolExecutor.map自动将任务分配给可用线程
        results = list(executor.map(atom_func, atom_list, chunksize=batch_size))
    
    return results