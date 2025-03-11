from concurrent.futures import ThreadPoolExecutor
import os

# batch map
# argument: atom list, batch size, atom function, but in parallel
# return: [atom_func(atom) for atom in atom_list] 
def batch_map(atom_list, batch_size, atom_func):
    blist = []
    for i in range(0, len(atom_list), batch_size):
        blist.append(atom_list[i:i+batch_size])

    def process_batch(batch):
        return [atom_func(atom) for atom in batch]

    with ThreadPoolExecutor(max_workers=os.cpu_count()) as executor:
        batch_result = executor.map(process_batch, blist)
    return [item for sublist in batch_result for item in sublist]
