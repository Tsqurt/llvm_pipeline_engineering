# This file is just a demo to show how to pass this demo

main.o: main.c
	clang -c main.c

opt.o: opt.c
	clang -c -O2 opt.c

no_opt.o: no_opt.c
	clang -c no_opt.c

hidden_numbers.o: hidden_numbers.c
	clang -c hidden_numbers.c

main: main.o opt.o no_opt.o hidden_numbers.o
	clang main.o opt.o no_opt.o hidden_numbers.o -o main

clean:
	rm -f main.o opt.o no_opt.o hidden_numbers.o main