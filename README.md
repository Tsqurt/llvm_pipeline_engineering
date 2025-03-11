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

```bash
touch input.in
touch output.out
clang -g -O3 -mllvm -disable-llvm-optzns -S -emit-llvm your_file.c -o your_file.ll
python3 util_GA.py your_file.ll input.in output.out
```

## About the project

This infrastructure serves as a foundation for research in compiler optimization techniques and program analysis within the SPAR research group.
For more information about the SPAR research group and our other projects, please visit our website at:
https://ics.nju.edu.cn/spar/index.html

## Contact

For any questions or feedback, please contact:

Senqi Tan
Email: 652024330022@smail.nju.edu.cn
