import os.path as osp

import pddlpy

import itertools

from z3 import *

class PDDLtoSAT():

    def __init__(self):
        pass

    def convert(self):
        # Propositionalize the actions

        # Define initial state

        # Propositionalize the goals

        # Add successor-state axioms

        # Add precondition axioms

        # Add action exclusion axiom
        pass

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

    objDict = {}
    for obj, objType in domprob.worldobjects().items():
        if objType not in objDict:
            objDict[objType] = [obj]
        else:
            objDict[objType].append(obj)

    print(objDict)


    # Print predicates of the domain
    for predicate in domprob.predicates():
        print('Predicate: name: {}, variable list: {}'.format(predicate.predicate_name,
                                                             predicate.variable_list))
        for obj, objType in predicate.variable_list.items():
            print('ObjType is', objType, 'possible objs:', objDict[objType])

    all_predicates = []
    for predicate in domprob.predicates():
        p_name = predicate.predicate_name
        possibleVar = []
        for obj, objType in predicate.variable_list.items():
            # Storing all variables of that object type
            # e.g. if objType is location, we store 'start_loc', 'bowl1', etc.
            possibleVar.append(objDict[objType])

        possible_comb = itertools.product(*possibleVar)
        print('possible comb', *possible_comb)
        all_predicates.append({p_name: possible_comb})

    print(all_predicates)

    # Print initial states of the pddl problem
    initial_states = []
    print("Initial states: ", domprob.initialstate())
    for initial_state in domprob.initialstate():
        action_name = initial_state.predicate[0]
        tup = {action_name: initial_state.predicate[1:]}
        print(tup)
        initial_states.append({action_name: initial_state.predicate[1:]})

    goal_states = []
    for goal_state in domprob.goals():
        action_name = goal_state.predicate[0]
        goal_states.append({action_name: goal_state.predicate[1:]})


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

    # Z3 Setup
    Z = IntSort()
    B = BoolSort()

