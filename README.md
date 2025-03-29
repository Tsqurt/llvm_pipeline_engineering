# LLVM Pipeline Engineering

## Overview

This project, led by Senqi Tan, was initially developed for research purposes within the SPAR group. It provides an infrastructure for constructing and manipulating LLVM optimization pipelines to achieve specific objectives.

## Purpose

The LLVM Pipeline Engineering project enables researchers and developers to:

- Construct customized LLVM optimization pipelines
- Analyze the effects of different optimization passes
- Minimize optimization pipelines while maintaining their effectiveness
- Compare and verify the equivalence of different optimization strategies

## Features

- Pipeline construction and manipulation
- Optimization pass analysis
- Pipeline minimization
- Code equivalence verification

## Usage

The project provides various utilities for working with LLVM IR and optimization pipelines, including:

- Stripping debug information for equivalence checking
- Applying custom optimization pipelines to LLVM IR
- Minimizing pipelines by removing redundant passes
- Analyzing optimization effects on code
...

## Quick Start

First, check your python and clang+llvm installation.

```bash
apt-get install clang llvm python3
```

To check your installation, you can run the following command.

```bash
python3 util_self_test.py
```

This project provide an infrastructure for mutating LLVM pipeline.

For a demo, switch to demo_xGA.py and demo_Ok_proj. To run this demo project, you may install valgrind as a demo performance profiling tool. You may install cmake as our build tool.

```bash
apt install cmake valgrind
```

Let's talk about the demo_Ok_proj directory. It is a CMake project.`opt.c` contain a functional test and a performance test, which pass only after optimizations. `no_opt.c` contain a functional test, which passes only before optimizations. Optimizations are intended to apply to only `opt.c`. No optimization will be applied to any other file. By project configuration, compilation optimizations are disabled for all `.c` files, including `opt.c`.

To build this project, following the instructions below. 

```bash
mkdir build
cd build
cmake ..
make
```

Run the test. Since `opt.c` is not optimized by default, this test will fail.

```bash
./main
```

We prepare a shell script for hacking this compilation process: we replace `opt.c.o` with its optimized version, so the build system will `believe` the file is the latest file, so no need to build once again.

```bash
<!-- demo_hack.sh -->
clang -O2 -c opt.c -o build/CMakeFiles/main.dir/opt.c.o
```

Now re-build the project, and run our test.

```bash
make
./main
```

This time our test will pass.

We prepare a searching script in demo_xGA.py. This will compile `opt.c` sorely with different compilation options, and then linking it with all prebuit models manually. Since `opt.c.o` can only be linked once, so we need to remove it manually.

```bash
<!-- make sure you've run a successful compilation process before -->
rm build/CMakeFiles/main.dir/opt.c.o
```

Then run our script, find the best configurations for compiling `opt.c`:
```bash
cd ..
python3 demo_xGA.py
```

This script will take a few time, and give you a compiler named `ga_compiler`.

Now you can compile your file using this compiler. Note: since this is *just* a compiler, most functionality in modern compiler frontend, like linking an object or preprocessing a file, or analyzing a file, is disabled. Specifying `-c` flag and `-o` flag is required. For example, 

```bash
ga_compiler -c -o opt.o opt.c
```

You may want to make a copy of `demo_xGA.py` to write your own script for your own object, especially the `experiment` object. In our demo, we show a way to make every experiment independent to each other for your reference, and thus our framework will parallel to enhance profiling speed. If you are unsure how to write an independent impementation, you can use no-parallel version: in the `__main__` part of `demo_xGA.py`, enabling the following code:

```python
    experiment = OkExperiment()
    # experiment = ParallelOkExperiment()
```

If you are unsure whether your experiment implementation is independent, feel free to use the `Experiment` as your base class, at the cost of searching speed.

## About the project

This infrastructure serves as a foundation for research in compiler optimization techniques and program analysis within the SPAR research group.
For more information about the SPAR research group and our other projects, please visit our website at:
https://ics.nju.edu.cn/spar/index.html

## Contact

For any questions or feedback, please contact:

Senqi Tan
Email: tsqurt@qq.com
