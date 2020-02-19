import os.path as osp

import pddlpy

from z3 import *

import itertools

class Element(object):
    def __init__(self, predicate, variables=None):
        self.predicate = predicate
        self.variables = variables

    def __repr__(self):
        return "{} {}".format(self.predicate, "".join(self.variables))

    def __str__(self):
        return "{} {}".format(self.predicate.predicate_name, ",".join(self.variables))

    def __eq__(self, other):
        return isinstance(other, Element) and other.predicate == self.predicate and other.variables == self.variables


class Operator(object):
    def __init__(self, operator, parameters):
        self.operator = operator
        self.parameters = parameters

        self.precondition_pos = []
        for atom in domprob.domain.operators[operator].precondition_pos:
            for pred in domprob.predicates():
                if atom.predicate[0] == pred.predicate_name:
                    myele = Element(pred, tuple([parameters[x] for x in atom.predicate[1:]]))
                    self.precondition_pos.append(myele)
        
        self.precondition_neg = []
        for atom in domprob.domain.operators[operator].precondition_neg:
            for pred in domprob.predicates():
                if atom.predicate[0] == pred.predicate_name:
                    myele = Element(pred, tuple([parameters[x] for x in atom.predicate[1:]]))
                    self.precondition_neg.append(myele)

        self.effect_pos = []
        for atom in domprob.domain.operators[operator].effect_pos:
            for pred in domprob.predicates():
                if atom.predicate[0] == pred.predicate_name:
                    myele = Element(pred, tuple([parameters[x] for x in atom.predicate[1:]]))
                    self.effect_pos.append(myele)

        self.effect_neg = []
        for atom in domprob.domain.operators[operator].effect_neg:
            for pred in domprob.predicates():
                if atom.predicate[0] == pred.predicate_name:
                    myele = Element(pred, tuple([parameters[x] for x in atom.predicate[1:]]))
                    self.effect_neg.append(myele)

        

    def __repr__(self):
        return "{} {}".format(self.operator, "".join(self.parameters))

    def __str__(self):
        return "{} {}".format(self.operator, ",".join(self.parameters.values()))

    def __eq__(self, other):
        return isinstance(other, Operator) and other.operator == self.operator and other.parameters == self.parameters

if __name__ == '__main__':
    root_path = osp.dirname(osp.abspath(__file__))

    pddl_domain_file = osp.join(root_path, 'pddl_files', 'feeding_domain.pddl')
    pddl_problem_file = osp.join(root_path, 'pddl_files', 'feeding_problem.pddl')

    domprob = pddlpy.DomainProblem(pddl_domain_file, pddl_problem_file)

    #the num of steps
    NUM = 5

    #Generating all possible combinations of predicates
    combList = []
    for predicate in domprob.predicates():
        varList = []    #Temporary list to generate cartesian product
        for key, value in predicate.variable_list.items():
            #Find all suitable arguments
            argList = [obj for obj, objType in domprob.worldobjects().items() if objType == value]
            varList.append(argList)
            
        for e in itertools.product(*varList):
            element = Element(predicate, e)
            combList.append(element)

    #creating init list
    ini_list = []
    for atom in domprob.initialstate():
        for pred in domprob.predicates():
            if atom.predicate[0] == pred.predicate_name:
                l = []
                for x in range(1, len(atom.predicate)):
                    l.append(atom.predicate[x])
                myele = Element(pred, tuple(l))
                ini_list.append(myele)
                
    goal_list = []
    for atom in domprob.goals():
        for pred in domprob.predicates():
            if atom.predicate[0] == pred.predicate_name:
                myele = Element(pred, tuple(atom.predicate[1:]))
                goal_list.append(myele)


    s = Solver()
    #Adding initial state
    for a in combList:
        f = Function(str(a), IntSort(), BoolSort())
        if a in ini_list:
            s.add(f(1))
        else:
            s.add(Not(f(1)))

    #Adding goal state
    for a in combList:
        f = Function(str(a), IntSort(), BoolSort())
        if a in goal_list:
            s.add(f(NUM))


    #Generating all possible ops
    opList = []
    for op in domprob.operators():
        varList = []
        varDict = {}    #params mapping
        for key, value in domprob.domain.operators[op].variable_list.items():
            argList = []
            for obj, objType in domprob.worldobjects().items():
                if objType == value:
                    argList.append(obj)
            varList.append(argList)
            varDict[key] = argList
        for x in (dict(zip(varDict, values)) for values in itertools.product(*varDict.values())):
            if len(set(x.values())) == len(x.values()):
                element = Operator(op, x)
                opList.append(element)

    
    for i in range(1, NUM):
        #Assertion: op happens <==> all preconditions and effects are met
        for a in opList:
            f = Function(str(a), IntSort(), BoolSort())
            for pre in a.precondition_pos:
                g = Function(str(pre), IntSort(), BoolSort())
                s.add(Or(Not(f(i)), g(i)))
            for pre in a.precondition_neg:
                g = Function(str(pre), IntSort(), BoolSort())
                s.add(Or(Not(f(i)), Not(g(i))))
            for eff in a.effect_pos:
                g = Function(str(eff), IntSort(), BoolSort())
                s.add(Or(Not(f(i)), g(i + 1)))
                
            for eff in a.effect_neg:
                g = Function(str(eff), IntSort(), BoolSort())
                s.add(Or(Not(f(i)), Not(g(i + 1))))

        #Assertion: Literal changes <==> an op that causes it must occur
        for a in combList:
            f = Function(str(a), IntSort(), BoolSort())
            clause = Or(f(i), Not(f(i+1)))
            for op in opList:
                if a in op.effect_pos:
                    g = Function(str(op), IntSort(), BoolSort())
                    clause = Or(clause, g(i))
            s.add(clause)

        #Assertion: Only one op per step
        for a in opList:
            for b in opList:
                if a != b:
                    f = Function(str(a), IntSort(), BoolSort())
                    g = Function(str(b), IntSort(), BoolSort())
                    s.add(Or(Not(f(i)), Not(g(i))))

    if s.check() == sat:
        print(s.model().sexpr())
    else:
        print("No solution")

        

          
