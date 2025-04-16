#!/usr/bin/python3
clang = "clang"
opt = "opt"
llc = "llc"
tmp = "/tmp"
pipeline_str = "sroa,simplifycfg,adce"
minimized_pipeline_file = "a.p"
import re
import sys
import os
import subprocess
import random
import sys
import os
import subprocess
import random

def parse_string_as_tree(s):
    """parse a string as a tree"""
    """return a tree"""
    """ 1. remove all spaces"""
    s = s.replace(" ", "")
    """ 2. remove all newlines"""
    s = s.replace("\n", "")
    """ 3. remove all tabs"""
    s = s.replace("\t", "")
    """ 4. remove all carriage returns"""
    s = s.replace("\r", "")

    """ 1. case 1, the string is empty"""
    if s == "":
        return []

    total_length = len(s)

    stack = [] # stack to store the parsing state
    current_dir = []
    current_str = ""

    for i in range(total_length):
        """what we care about are ", ( ) "  """
        if s[i] == "(":
            stack.append((current_dir, current_str))
            current_dir = []
            current_str = ""
        elif s[i] == ")":
            current_dir.append(current_str) if current_str != "" else None
            current_str = ""
            temp_list, temp_name = stack.pop()
            temp_list.append((temp_name, current_dir))
            current_dir = temp_list
        elif s[i] == ",":
            current_dir.append(current_str) if current_str != "" else None
            current_str = ""
        else:
            current_str += s[i]
    current_dir.append(current_str) if current_str != "" else None
    return current_dir

def atomize_tree(tree):
    autom_list = []
    for i in range(len(tree)):
        if isinstance(tree[i], tuple):
            t1, t2 = tree[i]
            t2 = atomize_tree(t2)
            for atom in t2:
                autom_list.append(t1 + "(" + atom + ")")
        else:
            autom_list.append(tree[i])
    # dropping the BitcodeWriterPass
    if autom_list and autom_list[-1] == "BitcodeWriterPass":
        autom_list = autom_list[:-1]
    # dropping the verify pass
    autom_list = [atom for atom in autom_list if "verify" != atom]
    return autom_list

def pipeline_opt_f(input_ll, passes_str):

    command = [opt, input_ll, "-passes=" + passes_str, "-S"]
    # run the command using subprocess
    result = subprocess.run(command, capture_output=True)

    err = result.stderr.decode("utf-8")
    if err != "":
        print(err)
    return result.stdout.decode("utf-8")

def pipeline_opt(input_ll_str, passes_str):
    tmpfile = os.path.join(tmp, f"{generate_random_str()}.ll")
    with open(tmpfile, "w") as f:
        f.write(input_ll_str)
    ret = pipeline_opt_f(tmpfile, passes_str)
    try:
        os.remove(tmpfile)
    except Exception:
        pass
    return ret

def text_ll_equivalent(ll_str_1, ll_str_2):
    # remove the following metadata:
    # ; ModuleID = 'build/tmp/kDSjFe2Sj4xWUHPkm5VL5AJVdlAH0BCv.c'
    # source_filename = "build/tmp/kDSjFe2Sj4xWUHPkm5VL5AJVdlAH0BCv.c"
    # !1 = !DIFile("build/tmp/kDSjFe2Sj4xWUHPkm5VL5AJVdlAH0BCv.c",

    lines1 = ll_str_1.split("\n")
    lines2 = ll_str_2.split("\n")

    filtered_lines1 = []
    filtered_lines2 = []

    for line in lines1:
        if not (line.startswith("; ModuleID = ") or
                line.startswith("source_filename = ") or
                re.match(r"!\d+ = !DIFile\(", line)):
            filtered_lines1.append(line)

    for line in lines2:
        if not (line.startswith("; ModuleID = ") or
                line.startswith("source_filename = ") or
                re.match(r"!\d+ = !DIFile\(", line)):
            filtered_lines2.append(line)

    return "\n".join(filtered_lines1) == "\n".join(filtered_lines2)

def compose_atom_tree(tree):
    return ','.join(atomize_tree(tree))

def pipeline_minimize(input_ll_str, passes_str):
    
    pass_tree = parse_string_as_tree(passes_str)
    pass_atom_tree = atomize_tree(pass_tree)
    # check if each pass can be removed
    # consider the order of the passes
    current_input = input_ll_str
    minimized_pass_tree = []
    removed = 0
    for i in range(len(pass_atom_tree)):
        next_input = pipeline_opt(current_input, pass_atom_tree[i])
        if text_ll_equivalent(next_input, current_input):
            current_input = next_input
            removed += 1
        else:
            current_input = next_input
            minimized_pass_tree.append(pass_atom_tree[i])
    return compose_atom_tree(minimized_pass_tree)

args = sys.argv[1:]

# processing flags
# if -o specified ... record and remove
output_file = None
if '-o' in args:
    output_file = args[args.index('-o') + 1]
    args.remove('-o')
    args.remove(output_file)
else:
    print("Error: -o not specified. File name deduction from input file name is unsupported.")
    exit(1)

# if -c not specified ... stop
if '-c' not in args:
    print("Error: -c not specified. This compiler supports compiling only.")
    exit(1)

# if -O<level> specified ... record and remove
if '-O' in args:
    opt_level = args[args.index('-O') + 1]
    args.remove('-O')
    args.remove(opt_level)
else:
    opt_level = "3"

def generate_random_str():
    keys = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    return ''.join(random.choices(keys, k=32))

# step 1. precompile with old and new flags
step1_result_file = os.path.join(tmp, generate_random_str() + ".ll")
cmd = [clang, '-O3', '-mllvm', '-disable-llvm-optzns', '-emit-llvm','-S', '-o', step1_result_file] + args
subprocess.run(cmd, check=True)

# step 2. optimize with pipeline
step2_result_file = os.path.join(tmp, generate_random_str() + ".ll")
cmd = [opt, step1_result_file, '-passes=' + pipeline_str, '-S', '-o', step2_result_file]
subprocess.run(cmd, check=True)

if minimized_pipeline_file != "":
    with open(step2_result_file, "r") as f:
        input_ll_str = f.read()
    minimized_pipeline = pipeline_minimize(input_ll_str, pipeline_str)
    with open(minimized_pipeline_file, "w") as f:
        f.write(minimized_pipeline)

# step 3. compile to object file with specified optimization level
cmd = [clang, step2_result_file, '-c', '-o', output_file, '-O' + opt_level]
subprocess.run(cmd, check=True)

# step 4. remove temporary files, allowing failure
try:
    os.remove(step1_result_file)
    os.remove(step2_result_file)
except Exception as e:
    pass