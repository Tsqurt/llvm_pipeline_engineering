import re, os, subprocess, time
import llvm

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

def constraint_Semantic(pipeline, raw_ll, opt_ll, input_str, output_str):
    pipeline = llvm.compose_atom_tree(available_passes)
    our_opt_ll = llvm.pipeline_opt(raw_ll, pipeline)
    return llvm.strip(our_opt_ll) == llvm.strip(opt_ll)

# TODO: write your own constraint function
def constraint_correctness(pipeline, raw_ll, opt_ll, input_str, output_str):
    # Compile and run the optimized code
    # Save optimized LLVM IR to temp file
    tmp_ll = os.path.join(llvm.tmp, f"{llvm.generate_random_str()}.ll")
    with open(tmp_ll, "w") as f:
        f.write(raw_ll)

    # Compile to executable
    tmp_exe = os.path.join(llvm.tmp, f"{llvm.generate_random_str()}")
    compile_cmd = [llvm.clang, tmp_ll, "-o", tmp_exe]
    try:
        subprocess.run(compile_cmd, capture_output=True, check=True)
    except subprocess.CalledProcessError:
        # Compilation failed
        try:
            os.remove(tmp_ll)
        except OSError:
            pass
        return False

    # Run executable with input
    try:
        result = subprocess.run([tmp_exe], input=input_str.encode(), 
                              capture_output=True, timeout=5)
        actual_output = result.stdout.decode()
        
        # Clean up temp files
        try:
            os.remove(tmp_ll)
        except OSError:
            pass
        try:
            os.remove(tmp_exe)
        except OSError:
            pass
        
        # Compare outputs
        return actual_output.strip() == output_str.strip()
        
    except (subprocess.TimeoutExpired, subprocess.SubprocessError):
        # Execution failed or timed out
        try:
            os.remove(tmp_ll)
        except OSError:
            pass
        try:
            os.remove(tmp_exe)
        except OSError:
            pass
        return False

# TODO: write your own fitness function
def fitness_efficiency(pipeline, raw_ll, opt_ll, input_str, output_str):
    # Maximum execution time in microseconds (10 seconds)
    MAX_TIME = 10 * 1000000

    # Save optimized LLVM IR to temp file
    tmp_ll = os.path.join(llvm.tmp, f"{llvm.generate_random_str()}.ll")
    with open(tmp_ll, "w") as f:
        f.write(raw_ll)

    # Compile to executable
    tmp_exe = os.path.join(llvm.tmp, f"{llvm.generate_random_str()}")
    compile_cmd = [llvm.clang, tmp_ll, "-o", tmp_exe]
    try:
        subprocess.run(compile_cmd, capture_output=True, check=True)
    except subprocess.CalledProcessError:
        # Compilation failed
        try:
            os.remove(tmp_ll)
        except OSError:
            pass
        return MAX_TIME

    # Run executable with input and measure time
    try:
        start_time = time.time()
        result = subprocess.run([tmp_exe], input=input_str.encode(),
                              capture_output=True, timeout=10)
        end_time = time.time()
        execution_time = int((end_time - start_time) * 1000000) # Convert to microseconds
        
        # Clean up temp files
        try:
            os.remove(tmp_ll)
        except OSError:
            pass
        try:
            os.remove(tmp_exe)
        except OSError:
            pass
            
        return min(execution_time, MAX_TIME)
        
    except (subprocess.TimeoutExpired, subprocess.SubprocessError):
        # Execution failed or timed out
        try:
            os.remove(tmp_ll)
        except OSError:
            pass
        try:
            os.remove(tmp_exe)
        except OSError:
            pass
        return MAX_TIME