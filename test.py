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
        print("Precondition_pos:")
        for x in self.precondition_pos:
            print(x)
        print("----")
        
        self.precondition_neg = []
        for atom in domprob.domain.operators[operator].precondition_neg:
            for pred in domprob.predicates():
                if atom.predicate[0] == pred.predicate_name:
                    myele = Element(pred, tuple([parameters[x] for x in atom.predicate[1:]]))
                    self.precondition_neg.append(myele)

        print("Precondition_neg:")
        for x in self.precondition_neg:
            print(x)
        print("----")

        self.effect_pos = []
        for atom in domprob.domain.operators[operator].effect_pos:
            for pred in domprob.predicates():
                if atom.predicate[0] == pred.predicate_name:
                    myele = Element(pred, tuple([parameters[x] for x in atom.predicate[1:]]))
                    self.effect_pos.append(myele)

        print("Effect_pos:")
        for x in self.effect_pos:
            print(x)
        print("----")

        self.effect_neg = []
        for atom in domprob.domain.operators[operator].effect_neg:
            for pred in domprob.predicates():
                if atom.predicate[0] == pred.predicate_name:
                    myele = Element(pred, tuple([parameters[x] for x in atom.predicate[1:]]))
                    self.effect_neg.append(myele)

        print("Effect_neg:")
        for x in self.effect_neg:
            print(x)
        print("----")
        

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

##    for x in domprob.initialstate():
##        print(type(x))
##    print(type(domprob.initialstate()))

    NUM = 5

    combList = []
    for predicate in domprob.predicates():
        print(predicate.predicate_name, '----')
        varList = []
        for key, value in predicate.variable_list.items():
            argList = []
            for obj, objType in domprob.worldobjects().items():
                if objType == value:
                    argList.append(obj)
            varList.append(argList)

        for e in itertools.product(*varList):
            element = Element(predicate, e)
            combList.append(element)
            print("\t{}".format(element))
    print("------")
    print("------")

    #creating init list
    ini_list = []
    print("!!!!")
    for atom in domprob.initialstate():
        for pred in domprob.predicates():
            if atom.predicate[0] == pred.predicate_name:
                l = []
                for x in range(1, len(atom.predicate)):
                    l.append(atom.predicate[x])
                myele = Element(pred, tuple(l))
                print(myele)
                ini_list.append(myele)
    print("!!!!")
    for x in ini_list:
        print(x)

    goal_list = []
    for atom in domprob.goals():
        for pred in domprob.predicates():
            if atom.predicate[0] == pred.predicate_name:
                myele = Element(pred, tuple(atom.predicate[1:]))
                goal_list.append(myele)
    print("Goals:-----")
    for a in goal_list:
        print(a)

    print("------")
    for a in combList:
        if a in ini_list:
            print(str(a))
        

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



    print("Generating operators")
    opList = []
    for op in domprob.operators():
        varList = []
        varDict = {}
        for key, value in domprob.domain.operators[op].variable_list.items():
            argList = []
            for obj, objType in domprob.worldobjects().items():
                if objType == value:
                    argList.append(obj)
            varList.append(argList)
            varDict[key] = argList
        print(varDict)
        lalalist = (dict(zip(varDict, values)) for values in itertools.product(*varDict.values()))
        for x in lalalist:

            if len(set(x.values())) == len(x.values()):
                print("Operator:", op)
                print("Parameters:")
                print(x)
                print("------")
                element = Operator(op, x)
                opList.append(element)

    
    for i in range(1, NUM):
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

        for a in combList:
            print(a)
            f = Function(str(a), IntSort(), BoolSort())
            clause = Or(f(i), Not(f(i+1)))
            for op in opList:
                if a in op.effect_pos:
                    print('\t',op)
                    g = Function(str(op), IntSort(), BoolSort())
                    clause = Or(clause, g(i))
            s.add(clause)

        for a in opList:
            for b in opList:
                if a != b:
                    f = Function(str(a), IntSort(), BoolSort())
                    g = Function(str(b), IntSort(), BoolSort())
                    s.add(Or(Not(f(i)), Not(g(i))))

    print(s.model)
    print(s.check())
    print(s.model().sexpr())
    
##        for e in itertools.product(*varList):
##            element = Operator(op, e)
##            combList.append(element)
##            print("\t{}".format(element))

        #for values in product(*varDict.values()):
            
        

          
