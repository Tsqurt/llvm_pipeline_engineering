#!/usr/bin/python3
clang = "clang"
opt = "opt"
tmp = "/tmp"
pipeline_str = "sroa,simplifycfg,licm,adce"
import sys
import os
import subprocess
import random

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

# if -O<level> specified ... remove
args = [arg for arg in args if not arg.startswith('-O')]

def generate_random_str():
    keys = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    return ''.join(random.choices(keys, k=32))

# step 1. precompile with old and new flags
step1_result_file = os.path.join(tmp, generate_random_str() + ".bc")
cmd = [clang, '-O3', '-mllvm', '-disable-llvm-optzns', '-emit-llvm', '-o', step1_result_file] + args
subprocess.run(cmd, check=True)

# step 2. optimize with pipeline
step2_result_file = os.path.join(tmp, generate_random_str() + ".bc")
cmd = [opt, step1_result_file, '-passes=' + pipeline_str, '-o', step2_result_file]
subprocess.run(cmd, check=True)

# step 3. compile to object file
cmd = [clang, '-c', step2_result_file, '-o', output_file]
subprocess.run(cmd, check=True)

# step 4. remove temporary files, allowing failure
try:
    os.remove(step1_result_file)
    os.remove(step2_result_file)
except Exception as e:
    pass
