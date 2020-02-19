import os.path as osp

import pddlpy


class PDDLtoSAT():

    def __init__(self):

    def convert(self):
        # Propositionalize the actions

        # Define initial state

        # Propositionalize the goals

        # Add successor-state axioms

        # Add precondition axioms

        # Add action exclusion axiom

if __name__ == '__main__':
    root_path = osp.dirname(osp.abspath(__file__))

    pddl_domain_file = osp.join(root_path, 'pddl_files', 'feeding_domain.pddl')
    pddl_problem_file = osp.join(root_path, 'pddl_files', 'feeding_problem.pddl')

    # Use pddlpy to parse pddl problem definitions
    domprob = pddlpy.DomainProblem(pddl_domain_file, pddl_problem_file)

    # Print goal state of the pddl problem
    print("Goal states: ", domprob.goals())

    # Print world objects of the pddl problem
    print("Objects: ", domprob.worldobjects())

    # Print predicates of the domain
    for predicate in domprob.predicates():
        print('Predicate: name: {} variable list: {}'.format(predicate.predicate_name,
                                                             predicate.variable_list))

    # Print initial states of the pddl problem
    print("Initial states: ", domprob.initialstate())

    # Print list of operators
    for operator in domprob.operators():
        # Print operator's name
        print("Operator name: {}".format(operator))
        # Print variable list
        print("  Variable list: ", domprob.domain.operators[operator].variable_list)
        # Print positive preconditions
        print(" Positive preconditions: ", domprob.domain.operators[operator].precondition_pos)
        # Print negative preconditions
        print(" Negative preconditions: ", domprob.domain.operators[operator].precondition_neg)
        # Print positive effects
        print(" Positive effects: ", domprob.domain.operators[operator].effect_pos)
        # Print negative effects
        print(" Negative effects: ", domprob.domain.operators[operator].effect_neg)