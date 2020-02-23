import os.path as osp

import pddlpy

import itertools

from z3 import *

class PDDL_to_SAT():

    def __init__(self, pddl_domain_path, pddl_problem_path):
        

    def convert_initial(self):


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

    goal_states = []
    for goal_state in domprob.goals():
        p_name = goal_state.predicate[0]
        goal_states.append({'p_name': p_name, 'params': tuple(goal_state.predicate[1:])})

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
        # for obj, objType in predicate.variable_list.items():
            # print('ObjType is', objType, 'possible objs:', objDict[objType])

    all_predicates = []
    all_predicates_dict = {}
    all_predicates_comb = []
    for predicate in domprob.predicates():
        p_name = predicate.predicate_name
        possibleVar = []
        for obj, objType in predicate.variable_list.items():
            # Storing all variables of that object type
            # e.g. if objType is location, we store 'start_loc', 'bowl1', etc.
            possibleVar.append(objDict[objType])

        possible_combs = tuple(itertools.product(*possibleVar))
        print('possible comb', *possible_combs)
        all_predicates.append({'p_name': p_name, 'params': possible_combs})
        all_predicates_dict[p_name] = possible_combs
        for comb in possible_combs:
            all_predicates_comb.append({'p_name': p_name, 'params': comb})

    print('all predicates: ', all_predicates)

    # Print initial states of the pddl problem
    initial_states = []
    print("Initial states: ", domprob.initialstate())
    for initial_state in domprob.initialstate():
        p_name = initial_state.predicate[0]
        tup = {'p_name': p_name, 'params': tuple(initial_state.predicate[1:])}
        print(tup)
        initial_states.append({'p_name': p_name, 'params': tuple(initial_state.predicate[1:])})

    print('New initial states', initial_states)

    # Print list of operators
    if False:
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
    s = Solver()
    t = 3 # Steps we hypothesize to reach goal

    '''
    SAT Problem: 

    Init ^ Goal ^ Successor State ^ Precondition ^ Action Exclusion
    '''
    # Converting initial states to SMT
    for predicate in all_predicates_comb:
        str_p = str(predicate)
        print('str_p is ', str_p)
        clause = Function(str(predicate), Z, B)
        if predicate in initial_states:
            # Passing 0 as initial time step
            s.add(clause(0))
        else:
            # Implicitly 
            s.add(Not(clause(0)))

    # Converting goal states to SMT
    for goal in goal_states:
        print('goal string', str(goal))
        clause = Function(str(goal), Z, B)
        s.add(clause(t))

    eff_to_action = []
    # Operator encodings
    for i in range(1, t):
        actions_list = []
        all_possible_combs = []
        for operator in domprob.operators():
            print('*****')
            print('Operator: ', operator)
            possible_var = []
            variable_list = []

            for var, var_type in domprob.domain.operators[operator].variable_list.items():
                possible_var.append(objDict[var_type])
                variable_list.append(var)

            possible_combs = tuple(itertools.product(*possible_var))
            all_possible_combs.append(possible_combs)                

            print('var list type is ', type(variable_list))
            
            for comb in possible_combs:
                var_to_obj = {}
                for x in range(len(comb)):
                    var = variable_list[x]
                    var_to_obj[var] = comb[x]

                for var, obj in var_to_obj.items():
                    print('var: ', var, ' obj: ', obj)

                action_pred = {'p_name': operator, "params": comb}
                print("op_str: ", action_pred)
                action = Function(str(action_pred), Z, B)
                actions_list.append(action)

                # Converting successor states to SMT
                effect_pos_list = domprob.domain.operators[operator].effect_pos
                for effect_pos in effect_pos_list:
                    p_name = effect_pos.predicate[0]
                    obj_list = [var_to_obj[var] for var in effect_pos.predicate[1:]]
                    eff_pred = {'p_name': p_name, 'params': tuple(obj_list)}
                    print('p_str is ', eff_pred)
                    eff_pos_clause = Function(str(eff_pred), Z, B)
                    s.add(Implies(action(i), eff_pos_clause(i + 1)))

                    if i == 1:
                        eff_to_action.append((eff_pred, action_pred))

                effect_neg_list = domprob.domain.operators[operator].effect_neg
                for effect_neg in effect_neg_list:
                    p_name = effect_neg.predicate[0]
                    obj_list = [var_to_obj[var] for var in effect_neg.predicate[1:]]
                    eff_pred = {'p_name': p_name, 'params': tuple(obj_list)}
                    print('p_str is ', eff_pred)
                    eff_neg_clause = Function(str(eff_pred), Z, B)
                    s.add(Implies(action(i), Not(eff_neg_clause(i + 1))))

                    if i == 1:
                        eff_to_action.append((eff_pred, action_pred))


                # Converting precondition states to SMT
                pre_pos_list = domprob.domain.operators[operator].precondition_pos
                for pre_pos in pre_pos_list:
                    p_name = pre_pos.predicate[0]
                    obj_list = [var_to_obj[var] for var in pre_pos.predicate[1:]]
                    pred = {'p_name': p_name, 'params': tuple(obj_list)}
                    print('p_str is ', pred)
                    pre_pos_clause = Function(str(pred), Z, B)
                    s.add(Implies(action(i), pre_pos_clause(i)))

                pre_neg_list = domprob.domain.operators[operator].precondition_neg
                for pre_neg in pre_neg_list:
                    p_name = pre_neg.predicate[0]
                    obj_list = [var_to_obj[var] for var in pre_neg.predicate[1:]]
                    pred = {'p_name': p_name, 'params': tuple(obj_list)}
                    print('p_str is ', pred)
                    pre_neg_clause = Function(str(pred), Z, B)
                    s.add(Implies(action(i), Not(pre_neg_clause(i))))


        # Frame axiom
        for predicate in all_predicates_comb:
            l = Function(str(predicate), Z, B)
            clause = Or(l(i), Not(l(i + 1)))

            # Find op that causes literal change

            # TODO: Figure out a way for faster lookup
            for eff_pred, action_pred in eff_to_action:
                # print('predicate is', predicate)
                # print('eff_pred is ', eff_pred)
                if predicate == eff_pred:
                    print('frame axiom inside!')
                    print(action_pred)
                    o = Function(str(action_pred), Z, B)
                    clause = Or(o(i), clause)

            s.add(clause)

        # Complete exclusion axiom
        for x in range(len(actions_list)):
            for y in range(x, len(actions_list)):
                action_x = actions_list[x]
                action_y = actions_list[y]

                s.add(Or(Not(action_x(i)), Not(action_y(i))))

    print(s.check())
    if s.check() == sat:
        print(s.model())