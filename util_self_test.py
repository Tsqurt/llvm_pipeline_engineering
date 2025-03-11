#!/usr/bin/python3
# tests

from batch_map import batch_map
import time 
import random
import sys
import os 
import llvm


list = [i for i in range(1000)]

def func(x):
    return x + 2

TFtable = batch_map(list, 16, func)

RFtable = [func(x) for x in list]

assert TFtable == RFtable

a1_src, a2_src, a3_src, a4_src, a5_src, a6_src = [open(f"test/{f}.c", "r").read() for f in ['a1', 'a2', 'a3', 'a4', 'a5', 'a6']]

assert llvm.try_compile_llvm(a1_src)
assert llvm.try_compile_llvm(a2_src)
assert not llvm.try_compile_llvm(a3_src)
# a4 is GCC's syntax
assert not llvm.try_compile_llvm(a4_src)
# a5 is Clang's syntax
assert llvm.try_compile_llvm(a5_src)

a1_e = llvm.llvm_cstr_read(a1_src)
a2_e = llvm.llvm_cstr_read(a2_src)
a3_e = llvm.llvm_cstr_read(a3_src)
a6_e = llvm.llvm_cstr_read(a6_src)

assert a1_e == llvm.llvm_cfile_read(f"test/a1.c")
assert a2_e == llvm.llvm_cfile_read(f"test/a2.c")
assert a3_e == llvm.llvm_cfile_read(f"test/a3.c")
assert a6_e == llvm.llvm_cfile_read(f"test/a6.c")

assert a1_e == llvm.llvm_cstr_read(a1_src)
assert a2_e == llvm.llvm_cstr_read(a2_src)
assert a3_e == llvm.llvm_cstr_read(a3_src)

assert a1_e == llvm.llvm_cstr_read(a1_e)
assert a2_e == llvm.llvm_cstr_read(a2_e)
assert a3_e == llvm.llvm_cstr_read(a3_e)
assert a6_e == llvm.llvm_cstr_read(a6_e)

assert a6_e != a1_e
a6_ll = llvm.compile_llvm_noopt(a6_src)
a1_ll = llvm.compile_llvm_noopt(a1_src)

assert a6_ll != a1_ll

pipeline = llvm.get_pipeline_str()
tree = llvm.parse_string_as_tree(pipeline)
atom_tree = llvm.atomize_tree(tree)
atom_pipeline = llvm.compose_atom_tree(atom_tree)

a6_ll_opt = llvm.pipeline_opt(a6_ll, atom_pipeline)
a1_ll_opt = llvm.pipeline_opt(a1_ll, atom_pipeline)

assert a6_ll_opt != a1_ll_opt

a6_ll_opt_stripped = llvm.strip(a6_ll_opt)
a1_ll_opt_stripped = llvm.strip(a1_ll_opt)

assert a6_ll_opt_stripped == a1_ll_opt_stripped

mini_pipeline = llvm.pipeline_minimize(a6_ll, atom_pipeline)
assert mini_pipeline and mini_pipeline != atom_pipeline

mini_pipeline = llvm.pipeline_minimize(a1_ll, atom_pipeline)
assert mini_pipeline and mini_pipeline != atom_pipeline

mini_pipeline = llvm.pipeline_minimize(a6_ll_opt, atom_pipeline)
count = len(llvm.parse_string_as_tree(mini_pipeline))
# some passes are infer attrs only, but they change IR's attrs.
assert count < 5 and count > 0

print("all tests passed")