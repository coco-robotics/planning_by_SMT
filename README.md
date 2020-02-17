# AI Planning by SMT

## Task Description
### Target
Solving PDDL planning problems with a SMT solver. Reference: http://planning.cs.uiuc.edu/booka4.pdf, Section 2.4 Using 
Logic to Formulate Discrete Planning.

### Set up environment
- Assume you have a Ubuntu environment (I use Ubuntu 18.04)
- Clone the repo to your local machine
- Create a new branch named with your name
- Create [virtual env](https://virtualenv.pypa.io/en/latest/) for your project
- Under the virtual env, install a pddl parser [pddl-lib](https://github.com/hfoffani/pddl-lib), [antlr4-python3-runtime](https://pypi.org/project/antlr4-python3-runtime/). 
Note here you may need to uninstall defaultly installed antlr4-python3-runtime with pddlpy and install it manually.
- Install SMT solver [z3](https://github.com/Z3Prover/z3)
- Run example.py to see the basic usage of pddlpy

### What do you need to implement
- A python class which can convert the PDDL problem (description files provided in pddl_files) to a [SAT](https://en.wikipedia.org/wiki/Boolean_satisfiability_problem) problem (one file)
- A python script to Call z3 to solve the SAT problem (one file)

### Commit and push your code
- Upload your code to the repo under the branch name you just created

