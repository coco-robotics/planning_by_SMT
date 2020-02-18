# AI Planning by SMT

## Updated Feb 18 2020: blackbox executable
There is an executable blackbox in current directory. As developed and described by https://www.cs.rochester.edu/u/kautz/satplan/blackbox/: "Blackbox is a planning system that works by converting problems specified in STRIPS notation into Boolean satisfiability problems, and then solving the problems with a variety of state-of-the-art satisfiability engines".
This executable works for test cases(domain and problem) in strips_test directory, but not for the pddl_files directory. 

### To Run blackbox
1. Clone this repo 
2. $> ./blackbox -o strips_test/domain.pddl -f strips_test/problem.pddl

### Problems
I am not sure why the blackbox does not work for the pddl files in pddl_files directory, can you explain that? Thanks!
