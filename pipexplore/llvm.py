import os
import subprocess
import re
import sys

from pipexplore.interface import tmp, generate_random_str


# init this module: find clang and opt
# Try to find clang from command line args first
clang = None
for arg in sys.argv:
    if arg.startswith("clang="):
        clang = arg.split("=")[1]
        break

# If not found in args, try finding clang in PATH
if not clang:
    try:
        clang = subprocess.check_output(['which', 'clang']).decode().strip()
    except subprocess.CalledProcessError:
        clang = os.path.join("/usr/bin", "clang")

# Try to execute clang to verify it exists
try:
    subprocess.run([clang, "--version"], capture_output=True)
except (FileNotFoundError, subprocess.SubprocessError):
    print("Error: Could not find working clang installation")
    print("Please specify clang location with clang=/path/to/clang")
    sys.exit(1)

# Get LLVM directory from clang path
llvm_dir = os.path.dirname(clang)
# If LLVM binaries are not in the same directory as clang, try to find it using llvm-config
if not os.path.exists(os.path.join(llvm_dir, "opt")):
    try:
        llvm_dir = subprocess.check_output(['llvm-config', '--bindir']).decode().strip()
    except subprocess.CalledProcessError:
        print("Error: Could not find working opt installation in LLVM directory")
        print("Please verify your LLVM installation includes opt")
        sys.exit(1)

# Find opt in same directory as clang
opt = os.path.join(llvm_dir, "opt")

# Verify opt exists and works
try:
    subprocess.run([opt, "--version"], capture_output=True)
except (FileNotFoundError, subprocess.SubprocessError):
    print("Error: Could not find working opt installation in LLVM directory")
    print("Please verify your LLVM installation includes opt")
    sys.exit(1)

# strip the debug information and other metadata
# argument: ll file path
# return: stripped ll string
def strip_f(input_ll):
    command = [opt, input_ll, "-strip-debug", "-passes=strip", "-S"]
    stdout = subprocess.run(command, capture_output=True).stdout
    lines = stdout.decode().split('\n')

    lines = [line for line in lines if not line.startswith(";")]
    lines = [line.split(";")[0] for line in lines]

    # dropping the metadata:
    # source_filename = "00001.c"
    # target datalayout = "e-m:e-p270:32:32-p271:32:32-p272:64:64-i64:64-i128:128-f80:128-n8:16:32:64-S128"
    # target triple = "x86_64-unknown-linux-gnu"
    lines = [line for line in lines if not line.startswith("source_filename") and not line.startswith("target datalayout") and not line.startswith("target triple")]

    # dropping the attributes line:
    # attributes #0 = {
    lines = [line for line in lines if not line.startswith("attributes #")]

    # dropping the attributes:
    # attributes #0 = {
    lines = [' '.join([word for word in line.split() if not word.startswith("#")]) for line in lines]

    # dropping the debug information:
    # !0 = !{i32 (...)*}
    lines = [line for line in lines if not line.startswith("!")]

    # dropping the inline information:
    # , !"
    lines = [line.split(", !")[0] for line in lines]

    # dropping the debug information related intrinsics:
    # llvm.dbg.declare
    # llvm.lifetime.start
    lines = [line for line in lines if "llvm.dbg." not in line and "llvm.lifetime." not in line]

    # dropping the empty lines:
    lines = [line for line in lines if line.strip()]

    return '\n'.join(lines)

# pipeline the ll file
# argument: ll file path, passes string
# return: optimized ll string
def pipeline_opt_f(input_ll, passes_str):

    command = [opt, input_ll, "-passes=" + passes_str, "-S"]
    # run the command using subprocess
    result = subprocess.run(command, capture_output=True)

    err = result.stderr.decode("utf-8")
    if err != "":
        print(err)
    return result.stdout.decode("utf-8")

# read the preprocessed c file
# argument: c file path
# return: preprocessed c string
def llvm_cfile_read(file):
    command = [clang, "-E", file]
    try:
        result = subprocess.run(command, capture_output=True).stdout.decode("utf-8")
    except Exception as e:
        return ""
    # dropping the precompiled lines:
    result = [line for line in result.split('\n') if not line.startswith("#")]
    # dropping the empty lines:
    result = [line for line in result if line.strip()]
    return '\n'.join(result)

# parse the passes string as a tree
# argument: passes string
# return: tree [subtree, ...]
# subtree:= (name, [subtree, ...]) | name
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

# atomize the tree
# argument: tree
# return: atomized tree [atom1, atom2, ...]
# atom:= pass_name
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

# get the pipeline string
# argument: opt level
# return: pipeline string
def get_pipeline_str(opt_level="O2"):
    cmd = [opt, "-" + opt_level, "--print-pipeline-passes"]
    stdin = ""
    try:
        result = subprocess.run(cmd, input=stdin, capture_output=True, text=True)
        return result.stdout
    except Exception as e:
        return ""

# compose the atomized tree
# argument: atomized tree
# return: pipeline string
def compose_atom_tree(tree):
    return ','.join(atomize_tree(tree))

# read the c string
# argument: c source string
# return: c source string
def llvm_cstr_read(src_str):
    ret = ""
    tmpfile = os.path.join(tmp, f"{generate_random_str()}.c")
    with open(tmpfile, "w") as f:
        f.write(src_str)
    try:
        ret = llvm_cfile_read(tmpfile)
    except Exception as e:
        ret = ""
    try:
        os.remove(tmpfile)
    except Exception as e:
        pass
    return ret

# compile the c string
# argument: c source string
# return: True if compile success, False otherwise
def try_compile_llvm(src_str):
    ret = False
    try:
        input_file = os.path.join(tmp, f"{generate_random_str()}.c")
        with open(input_file, "w") as f:
            f.write(src_str)

        output_file = os.path.join(tmp, f"{generate_random_str()}.ll")

        cmd = [clang, '-S', '-emit-llvm', input_file, '-o', output_file]

        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)

        if result.returncode == 0:
            if os.path.getsize(output_file) > 0:
                ret = True
    except Exception as e:
        print(e)

    try:
        os.remove(input_file)
        os.remove(output_file)
    except Exception:
        pass
    return ret

# compile the c string
# argument: c source string
# return: compiled ll string before optimization
def compile_llvm_noopt(src_str):
    try:
        input_file = os.path.join(tmp, f"{generate_random_str()}.c")
        with open(input_file, "w") as f:
            f.write(src_str)

        output_file = os.path.join(tmp, f"{generate_random_str()}.ll")

        # this is the command to compile the c string to ll string before the optimization stage, i.e. without any optimization
        cmd = [clang, '-g', '-O3', '-mllvm', '-disable-llvm-optzns', '-S', '-emit-llvm', input_file, '-o', output_file]

        subprocess.run(cmd, capture_output=True, text=True, timeout=10)
    except Exception:
        pass

    compiled_str = ""
    try:
        os.remove(input_file)
        with open(output_file, "r") as f:
            compiled_str = f.read()
        os.remove(output_file)
    except Exception:
        pass
    return compiled_str

# pipeline the ll string
# argument: ll string, passes string
# return: optimized ll string
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

# strip the debug information and other metadata
# argument: ll string
# return: stripped ll string
def strip(input_ll_str):
    tmpfile = os.path.join(tmp, f"{generate_random_str()}.ll")
    with open(tmpfile, "w") as f:
        f.write(input_ll_str)
    ret = strip_f(tmpfile)
    try:
        os.remove(tmpfile)
    except Exception:
        pass
    return ret

# whether the two pipelines are equivalent modulo the input
# argument: input ll string, pass string 1, pass string 2
# return: True if equivalent, False otherwise
def pipeline_equivalent_modulo_input(input_ll_str, pass_str_1, pass_str_2):
    out1 = pipeline_opt(input_ll_str, pass_str_1)
    out2 = pipeline_opt(input_ll_str, pass_str_2)
    return out1 == out2

# whether the two ll strings are equivalent modulo matadata
# argument: ll string 1, ll string 2
# return: True if equivalent, False otherwise
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

# minimize the pipeline
# argument: ll string, passes string
# return: minimized pipeline string
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

# a generator that yields a compiler from a pipeline string
def from_pipeline_make_a_compiler_to_path(pipeline_str, compiler_full_path):
    text = f"""#!/usr/bin/python3
clang = "{clang}"
opt = "{opt}"
tmp = "{tmp}"
pipeline_str = "{pipeline_str}"
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
"""
    with open(compiler_full_path, "w") as f:
        f.write(text)

    # add execute permission
    os.chmod(compiler_full_path, 0o755)

    return True

def from_pipeline_make_a_compiler(pipeline_str):
    compiler_full_path = os.path.join(tmp, f"{generate_random_str()}")
    from_pipeline_make_a_compiler_to_path(pipeline_str, compiler_full_path)
    return compiler_full_path
