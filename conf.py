import re
import llvm

# TODO: write your own fitness function
def fitness_debugLoc(pipeline, raw_ll, input_str, output_str):
    """Fitness function: Calculate the fitness of optimized code"""
    ll_str = llvm.pipeline_opt(raw_ll, pipeline)
    cnt = 0
    counted = set()
    lines = ll_str.split("\n")
    for line in lines:
        for match in re.finditer(r'!dbg !(\d+)', line):
            if match.group(1) not in counted:
                cnt += 1
                counted.add(match.group(1))
    return cnt

raw_available_passes = llvm.get_pipeline_str()
raw_tree = llvm.parse_string_as_tree(raw_available_passes)
atom_tree = llvm.atomize_tree(raw_tree)
available_passes = atom_tree

# TODO: write your own constraint function
def constraint_Semantic(pipeline, raw_ll, opt_ll, input_str, output_str):
    pipeline = llvm.compose_atom_tree(available_passes)
    our_opt_ll = llvm.pipeline_opt(raw_ll, pipeline)
    return llvm.strip(our_opt_ll) == llvm.strip(opt_ll)