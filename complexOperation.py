# -*- coding: utf-8 -*-
"""
Created on Mon Feb 03 11:58:07 2020

THE INDIVIDUAL COMPONENTS OF THE SCP

Each complex operation is pipeline of information. They all take information about
an epistemic state (rules, and actual variable assignments) and transform it according
to the purpose of the operation. However, the output of a complexOperation is ALWAYS
readable by another complex operation which uses it as input.

Together complex operations are a linear linked pipeline of transformations on
the initial epistemic state.
@author: Axel
"""

import copy
#used to create atoms and rules
import basicLogic
#used to throw exceptions for improper use
import scpError

import epistemicState

import helperFunctions

class complexOperation (object):
    """
    CREATE A COMPLEX OPERATION
    @param name: the new name for the complex operation (does not need to be unique)
    """
    def __init__(self, name=""):
        self.name = name
        #the complex operation that uses the output of this one as its input
        self.next = None
        #the complex operation whose output is the input to this complex operation
        self.prev = None
    def evaluate(self):
        raise scpError.notImplementedError_AbstractClass

    """
    REPRESENT THIS COMPLEX OPERATION'S OUTPUT RULES AS A STRING
    @return the rules as a human-readable string
    """
    def strKnowledge_self(self):
        return complexOperation.strKnowledge(self.evaluatekb())  

    """
    REPRESENT THIS COMPLEX OPERATION'S OUTPUT VARIABLES AS A STRING
    @return the variables as a human-readable string
    """
    def strVariables_self(self):
        return complexOperation.strKnowledge(self.evaluatev())
    #this method requires that the truth value of all variables with name x be identical
    @staticmethod
    def getHeads (kb):
        heads=[]
        for rule in kb:
            if isinstance (rule, basicLogic.operator_bitonic_implication):
                heads.append(rule.clause2)
            elif isinstance (rule, basicLogic.operator_bitonic_bijection):
                heads.append(rule.clause2)
                heads.append(rule.clause1)
        return list(dict.fromkeys(heads)) 
    
    """
    REPRESENT THIS COMPLEX OPERATION AS A STRING IN TERMS OF INPUT AND OUTPUT
    @return The name of operation as well as the (KB,V) values for both input and output
    """
    def __str__(self):
        
        epi_input = (self.prev.evaluate() if self.prev!=None else None)
        epi_output = self.evaluate()
        
        #input
        s = "{}\n{}\n>>>Input: {}\n".format(("-"*10),("-"*5), self.name)
        s = s + u"{}\n".format(epi_input)
        
        #output
        s = s+"{}\n>>>Output: {}\n".format(("-"*5), self.name)
        s = s + u"{}\n".format(epi_output)
        
        s = s + "{}\n".format("-"*10)  
        return s 
    
    @staticmethod
    def createEmptyNextEpi(prevEpi):
        if isinstance (prevEpi, epistemicState.epistemicState_weakCompletion):
            return epistemicState.epistemicState_weakCompletion()
        elif isinstance (prevEpi, epistemicState.epistemicState_defeaultReasoning):
            return epistemicState.epistemicState_defeaultReasoning()
        raise scpError.invalidEpistemicStateError
            
"""
THE INIT COMPLEX OPERATIONS IS ASSUMED TO BE THE FIRST STEP OF EVERY SCP
The complexOperation_init holds pointers to epistemic information from the initial state of the scp.
There should be only one init operation per scp
The init operation is the only complex operation with no prev node
"""
class complexOperation_init (complexOperation):
    """
    CREATE AN INSTANCE OF complexOperation_init
    """
    def __init__ (self):
        complexOperation.__init__(self, "init")
        self.epi_state=[]
    def evaluate(self):
        return self.getEpistemicState()
    def setEpistemicState (self, epi):
        self.epi_state=epi
    def getEpistemicState (self):
        return self.epi_state
"""
DEFAULT OPERATIONS ARE USED TO MODIFY EPISTEMIC STATES USED FOR DEFAULT LOGIC
The actual problem is NP complete for propositional logic, but a simplified
version is provided here
"""    
class complexOperation_default (complexOperation):
    """
    CREATE AN INSTANCE OF complexOperation_default (which is abstract)
    @param name: the name of the complexOperation
    """
    def __init__(self, name="defaultOp"):
        complexOperation.__init__(self,name)
"""
USE DEAULT LOGIC TO EVALUATE AN EPISTEMIC STATE IN TERMS OF FACTS, RULES, AND DEFAULTS
"""
class complexOperation_default_drawConclusions (complexOperation_default):
    """
    CREATE AN INSTANCE OF THE complexOperation_default_drawConclusions CLASS
    """
    def __init__(self):
        complexOperation_default.__init__(self,name="drawConcDefault")
    """
    FIND EPISTEMIC STATES THAT CAN BE DERIVED FROM THE INPUT EPISTEMIC STATE USING
    KNOWN DEFAULT RULES.
    @param hastyDerive: find only the single epistemic state resulting from applying all
    default rules in order until knowledge convergence
    @return @TODO
    """
    #@TODO should return a list of epistemic states corresponding to each possible world
    #@TODO this should run until convergence (in this case only variable assignments change)
    def evaluate(self, hastyDerive=False):
        #the result of the previous complex operatoin
        epi_prev = self.prev.evaluate()
        #the current epi
        epi_next = copy.deepcopy(epi_prev)
        
        #the variables of the previous epi
        prevV = epi_prev.getV()
        #determine all variable assignments from the list of rules W
        epi_next=complexOperation_default_drawConclusions.evaluateW(epi_next)
        #determine the epis that result from applying the default rules
        possibleEpis = complexOperation_default_drawConclusions.evaluateD(epi_next,hastyDerive)
        #the variable assignments after the default rules are applied
        currentV = epi_next.getV()
        #keep running until the variable assignments no longer change
        while not basicLogic.compareVariableLists(prevV,currentV):
            #the variables of the previous epi
            prevV = epi_next.getV()
            #determine all variable assignments from the list of rules W
            epi_next=complexOperation_default_drawConclusions.evaluateW(epi_next)
            #@TODO
            #determine the epis that result from applying the default rules
            possibleEpis = complexOperation_default_drawConclusions.evaluateD(epi_next,hastyDerive) 
            #the variable assignments after the default rules are applied
            currentV = epi_next.getV()
        print ("POSSIBLE EPIS ARE\n",possibleEpis)
        print ("--------------------------------ttt------------")
        return epi_next
    """
    REMOVE DUPLICATES FROM A LIST OF EPISTEMIC STATES
    Duplicates are determined by the variable list of the epistemic state
    @param li: list of epistemic states
    @return li where each epi has a unique variables assignment
    """
    @staticmethod
    def uniquifyEpiListByV(li):
        newLi=[]
        for epi in li:
            if not complexOperation_default_drawConclusions.checkEpiInList_checkV(epi,newLi):
                newLi.append(epi)
        return newLi
    # W introducing no branching factor and so only returns one epistemic state
    """
    DETERMINE ALL VARIABLE EVALUATIONS THAT RESULT FROM THE LIST W OF RULES
    As always, this process is only implemented for (body -> head) rules.
    @param epi_next: the epistemic state whose V and W values will be used
    @return a copy of epi_next after all variables have been derived
    """
    @staticmethod
    def evaluateW(epi_next):
        epi_next=copy.deepcopy(epi_next)
        prev  = []
        epi_w = epi_next.getW()
        #find (rule,value) pairs that can derived from W
        current = complexOperation_default_drawConclusions.oneStepDeriveFromW(epi_w)
        #create all variables that can be made from the derived values (at present, only atom and negated atom heads work)
        newVariables = complexOperation_default_drawConclusions.getVariablesFromThW(current)
        #while the current variables are not the same as the new variables, keep adding newly derived variables to the list and repeat
        while not complexOperation_default_drawConclusions.compareCurrentToPrev(current,prev):
            prev = copy.deepcopy(current)
            current=complexOperation_default_drawConclusions.oneStepDeriveFromW(epi_w)
            newVariables = complexOperation_default_drawConclusions.getVariablesFromThW(current)
            #set the variables in the concrete rules to the newly derived values
            for v in newVariables:
                for c in current:
                    c[0].deepSet(v.getName(), v.getValue())
        #print ("derived rules are",derivedRules)
        epi_next.addVList(newVariables)
        return epi_next
    """
    APPLY THE DEFAULT RULES TO THE EPISTEMIC STATE
    Finds either all possible final states, or just the one from applying D in sequence
    @param epi_next: the epistemic state containing V and D
    @hastyDerive: False to find all possible resulting states, True to find just one
    """
    @staticmethod
    def evaluateD(epi_next, hastyDerive=True):
        if hastyDerive:
            epis = [complexOperation_default_drawConclusions.evaluateD_hasty(epi_next)]
            return epis
        else:
            epis = complexOperation_default_drawConclusions.evaluateD_full(epi_next)
            #remove duplicate epis (same V)
            epis = complexOperation_default_drawConclusions.uniquifyEpiListByV(epis)
            return epis
    """
    DETERMINE IF AN EPISTEMIC STATE WITH THE SAME VARIABLE ASSIGNMENTS IS ALREADY IN THE LIST
    @param epi: the epistemic state to be checked
    @param li: the list of epistemic states to be checked
    @return True if there is already an epi with that v in the list, false otherwise
    """
    @staticmethod
    def checkEpiInList_checkV (epi,li):
        for e in li:
            if basicLogic.compareVariableLists(epi.getV(),e.getV()):
                return True
        return False
    """
    DETERMINE EVERY POSSIBLE EPISTEMIC STATE THAT CAN BE REACHED BY APPLYING THE THE DEFAULT
    RULES IN W WITH THE KNOWN VARIABLES VALUES IN ANY ORDER
    @param epi_next: the epistemic state that provides the W and V to be used
    @return every possible conclusion that can be drawn (consistently)
    """
    @staticmethod
    def evaluateD_full(epi_next):        
        #generate every possible sequence of default rules
        values = epi_next.getD()
        #find every possible order of the defeault rules
        allPermutations = helperFunctions.permutation(values)
        uniqueEpis=[]
        #for each possible ordering of the rules find the conclusions that can be drawn
        for D in allPermutations:
            #make a new copy of the epi for each rule ordering
            epi = copy.deepcopy(epi_next)
            #remove the existing (original order) D
            epi.emptyD()
            #add the new epistemic rules
            epi.addDList(D)
            #evaluate the epi in terms of the now limitted rules
            complexOperation_default_drawConclusions.evaluateD_hasty(epi)
            if not complexOperation_default_drawConclusions.checkEpiInList_checkV(epi, uniqueEpis):
                uniqueEpis.append(epi)
        return uniqueEpis
    """
    FIND THE EPISTEMIC STATE THAT RESULTS FROM APPLYING THE KNOWN DEFEAULT RULES IN ORDER
    @param epi_next: the epistemic state that provides the W and V to be used
    @return the single epistemic state that results from applying D in order
    """
    @staticmethod
    def evaluateD_hasty(epi_next):
        d=epi_next.getD()
        v=epi_next.getV()
        derivs = []
        for defaultRule in d:
            #determine if the default rule holds
            ruleEval = defaultRule.evaluate(v)
            #if the ule doesn't hold, do nothing
            if ruleEval==False:
                #nothing happens as this rule has been falsified
                #maybe it should be rmoved from the list of default rules?
                pass
            else:
                #the conclusion of the default rule is made true
                derivs.append((defaultRule.clause3,True))
        #transform the derived rules into variable assignments
        newVariables = complexOperation_default_drawConclusions.getVariablesFromThW(derivs)
        #add the vairables to the epistemic state
        epi_next.addVList(newVariables, overwrite=True)
        return epi_next  
    
    """
    FIND ALL CLAUSES THAT IMMEDIATELY EVALUATE TO A NON-NONE VALUE
    Currently implemented for (->, <->)
    @param w: the set of rules
    @return (clause, value) where the clause can be an atom or normal clause 
    """
    #@TODO this method is really simple and must be expanded for non-monotonic conclusions
    # that is, for cases where there are multiple possible resulting variable assignments
    @staticmethod
    def oneStepDeriveFromW(w):
        v=[]
        for rule in w:
            if isinstance(rule, basicLogic.operator_bitonic_implication):
                ce1 = rule.clause1.evaluate()
                ce2 = rule.clause2.evaluate()
                #print ("Clause 1 :{} = {}  --- Clause 2 :{} = {}".format(rule.clause1,ce1,rule.clause2,ce2))
                if ce1!=None:
                    v.append((rule.clause2,ce1))
            if isinstance(rule, basicLogic.operator_bitonic_bijection):
                ce1 = rule.clause1.evaluate()
                ce2 = rule.clause2.evaluate()
                if ce1!=None:
                    v.append((rule.clause2, ce1))
                if ce2!=None:
                    v.append((rule.clause1, ce2))
        return v
    """
    TURN THE VARIABLE ASSIGNMENTS IN thW IN A LIST OF VARIABLES
    Currently works for Atom and not(Atom) clauses
    @param thW: a list of (clause, value) tuples
    @return a list of variables where all valid tuples are represented as variables
    """
    @staticmethod
    def getVariablesFromThW(thW):
        v=[]
        for x in thW:
            if isinstance(x[0],basicLogic.atom):
                v.append(copy.deepcopy(x[0]))
                v[-1].setValue(x[1])
            elif isinstance(x[0],basicLogic.operator_monotonic_negation):
                v.append(copy.deepcopy(x[0].clause))
                doubleNeg = basicLogic.operator_monotonic_negation(basicLogic.atom('',x[1]))
                v[-1].setValue(doubleNeg.evaluate())
        return v
    """
    SET ALL RULES TO VALUES DESCRIBED BY A LIST OF ATOMS
    @param v: a list of atoms
    @param rules: a set of operator objects
    """
    @staticmethod
    def deepSetVInRules (v, rules):
        basicLogic.setkbfromv(rules,v)
    #@TODO does not compare rules, only atoms
    """
    DETERMINE IF TWO LISTS OF LOGIC ATOMS ARE IDENTICAL
    @PARAM cur: the first list of logic atoms
    @param prev: the second list of logic atoms
    @return True if the list are the same, False otherwise
    """
    @staticmethod
    def compareCurrentToPrev (cur, prev):
        for c in cur:
            cFound=False
            if isinstance (c[0], basicLogic.atom):
                for p in prev:
                    if isinstance(p[0],basicLogic.atom):
                        if c[0]==p[0]:
                            cFound=True
            else:
                cFound = True
            if not cFound:
                return False
        return True

    
    
    
    
    
 
    
    
"""
A COMPLEX OPERATION WHICH ADDS ABNORMALITY VARIABLES TO THE EPISTEMIC STATE
The process her may differ according to the indiivdual needs of the researcher.
In this case, a simple rule is followed:
    "for every a -> b, if there exists no c -> b where c = (True, False, Unknown)
    then create a new abnormality ab_i and replace a -> b with a + ab_i -> b.
    Next, for every other rule a' with a' -> b, introduce not(a') -> ab_i"
"""
class complexOperation_addAB (complexOperation):
    """
    CREATE AN INSTANCE OF A complexOperation_addAB OBJECT
    """
    def __init__ (self):
        complexOperation.__init__(self, "addAB")
    """
    GET THE LIST OF ALL CLAUSES (clause->head) FOR A GIVEN HEAD
    @param head: the head of the rule
    @param kb: the list of all rules
    @return all clauses that affect that head as a list
    """    
    def getRulesThatAffectHead (self, head, kb):
        rulesThatAffectHead=[]
        for rule in kb:
            if isinstance (rule, basicLogic.operator_bitonic_implication):
                if rule.clause2.getName() == head.getName():
                    rulesThatAffectHead.append(rule.clause1)
            elif isinstance (rule, basicLogic.operator_bitonic_bijection):
                if rule.clause2.getName() == head.getName():
                    rulesThatAffectHead.append(rule.clause1)
                if rule.clause1.getName() == head.getName():
                    rulesThatAffectHead.append(rule.clause2)
        return rulesThatAffectHead
    """
    CREATE A RULE WITH A NEW ABNORMALITY abx
    @param head: the head of the rule that needs a new abnormality
    @param body: the body of the rule that needs a new abnormality
    @param li_abs: the list of already-existing abnormality
    @return the new rule (with the abnormality), the new abnormality, the list of abnormalities
    """
    def createBodyFromRulesThatAffectHead (self, head, body, li_abs):
        #if basicLogic.isGroundAtom(body):
        if basicLogic.isGroundAtom(body) or basicLogic.isGroundAtom(head):
            return basicLogic.operator_bitonic_implication(body, head), None, li_abs
        newAbnormality = basicLogic.atom('ab{}'.format(len(li_abs)+1))
        negAbnormality = basicLogic.operator_monotonic_negation(newAbnormality)
        li_abs.append(newAbnormality)    
        newBody = basicLogic.operator_bitonic_and(body, negAbnormality)
        newRule = basicLogic.operator_bitonic_implication(newBody, head)
        return newRule, newAbnormality, li_abs
    """
    REMOVE A RULE FROM A LIST OF RULES
    Rule checking is very very complex and so this function is not very well implemented
    (currently just uses string repr)
    @param rule: the rule to removed
    @param li)rule: the list of rules
    @return the list without rule in it
    """
    def removeRuleFromList (self, rule, li_rule):
        otherRules = []
        for r in li_rule:
            if r!=rule:
                otherRules.append(r)
        return otherRules
    """
    REMOVE ALL GROUND RULES FROM THE LIST OF RULES
    A ground rule is T/F/U <- head
    @param rules: the list of rules
    @return the list of rules without any ground atoms
    """
    #@TODO I do not think this works
    def removeGroundFromRules (self,rules):
        newRules = []
        for rule in rules:
            if not basicLogic.isGroundAtom(rule):
                newRules.append(rule)
        return newRules
    """
    CREATE A BODY CLAUSE TO BE USED WITH THE NEW ABNORMALITY AS A HEAD (BODY->abx).
    Non-ground rules that affect the same head are treated as possible abnormalities.
    @param otherRulesThatAffectHead: a list of clause which all affect the same head in epistemic state
    @return a new clause to be the body of the abnoramlity 
    """
    def createNewAbnormalityInstant (self, otherRulesThatAffectHead):
        # case: KB={D->3, T->3} without this (T -> ab) is created
        otherRulesThatAffectHead=self.removeGroundFromRules(otherRulesThatAffectHead)
        #if nothing else affects the head, assume the abnormality is false by default
        if otherRulesThatAffectHead==[]:
            rule = basicLogic.FALSE
            return rule    
        rule = otherRulesThatAffectHead[0] 
        #added a negated disjunction of all the rules
        for other in range (1,len(otherRulesThatAffectHead)):
            neg = basicLogic.operator_monotonic_negation(rule)
            rule = basicLogic.operator_bitonic_or(rule, neg)
        return rule
    """
    RETURN THE HEADS OF A RULE (0,1 - implication , or 2 - bijection)
    @param rule: the rule to be checked
    @return: a list of all heads in the rule
    """
    def getHeads (self, rule):
        if isinstance(rule, basicLogic.operator_bitonic_bijection):
            return [rule.clause1, rule.clause2]
        if isinstance (rule, basicLogic.operator_bitonic_implication):
            return [rule.clause2]
        return []
    """
    RETURN THE BODIES OF A RULE (0,1 - implication , or 2 - bijection)
    @param rule: the rule to be checked
    @return: a list of all bodies in the rule
    """
    def getBodies (self, rule):
        if isinstance(rule, basicLogic.operator_bitonic_bijection):
            return [rule.clause1, rule.clause2]
        if isinstance (rule, basicLogic.operator_bitonic_implication):
            return [rule.clause1]
        return []
    """
    USE THE PREVIOUS EPISTEMIC STATE AND ADD ALL RELEVENT ABNORMALITIES TO ITS RULES
    Also adds the abnormalities to the variable lists, and gives them a rule with them 
    as the head in the kb.
    "for every a -> b, if there exists no c -> b where c = (True, False, Unknown)
    then create a new abnormality ab_i and replace a -> b with a + ab_i -> b.
    Next, for every other rule a' with a' -> b, introduce not(a') -> ab_i"
    @return an epistemic state with the abnormalities added
    """        
    def evaluate(self):
        #get the previous epistemic state
        epi_prev = self.prev.evaluate()
        #generate an empy epistemic state of the same type as the previous one
        epi_next = complexOperation.createEmptyNextEpi(epi_prev)
        
        #all variables in prevkb will be present in the next one (plus abnormalities)
        prev_v = epi_prev.getV()
        epi_next.addVariableList(prev_v)
        
        #the list of created abnormalities
        ABs = []
        prev_kb = epi_prev.getKB()

        for rule in prev_kb:
            #we do this because there can be 1 or 2 heads/bodies depending on -> or <->
            body = self.getBodies(rule)
            head = self.getHeads(rule)
            if rule.immutable:
                epi_next.addKnowledge(rule)
            else:
                for h in head:
                    for b in body:
                        #truth values don't need abnormalities
                        if basicLogic.isGroundAtom(b):
                            newRule = basicLogic.operator_bitonic_implication(b,h)
                            epi_next.addKnowledge(newRule)
                        else:
                            #find every clause x, with (x->head)
                            rulesThatAffectHead = self.getRulesThatAffectHead(h, prev_kb)
                            #remove this body from the list of rules that affect head
                            otherRulesThatAffectHead = self.removeRuleFromList(b, rulesThatAffectHead)
                            #create the new abnormality
                            newAb = basicLogic.atom("ab{}".format(len(ABs)+1))
                            ABs.append(newAb)
                            negAb = basicLogic.operator_monotonic_negation(newAb)
                            newBody = basicLogic.operator_bitonic_and(b,negAb)
                            newRule = basicLogic.operator_bitonic_implication(newBody,h)
                            epi_next.addKnowledge(newRule)
                            
                            #create a valuation for the new abnormality
                            abInstHead = newAb
                            abInstBody = self.createNewAbnormalityInstant(otherRulesThatAffectHead)
                            abInstBodyIsGroundValue = basicLogic.isGroundAtom(abInstBody)
                            newAbInstBody =  abInstBody if abInstBodyIsGroundValue else basicLogic.operator_monotonic_negation(abInstBody)
                            abInstRule = basicLogic.operator_bitonic_implication(newAbInstBody, abInstHead)
                            epi_next.addKnowledge(abInstRule)
                            
                            #add the new abnormality to the variable list
                            epi_next.addVariable(newAb) 
        return epi_next
        
"""
A COMPLEX OPERATION WHICH PERFORMS WEAK COMPLETION AS DEFINED BY @TODOref
1) replace a_1->x, ..., a_n->x with a_1 + ... + a_n ->x
2) replace all -> with <->
"""        
class complexOperation_weaklyComplete (complexOperation):
    """
    CREATE AN INSTANCE OF THE complexOperation_weaklyComplete CLASS
    """
    def __init__ (self):
        complexOperation.__init__(self, "weaklyComplete")

    """
    USE THE PREVIOUS EPISTEMIC STATE AS BASIS FOR WEAKLY COMPLETING ITS KNOWLEDGE BASE.
    @return an epistemic state with a weakly completed kb
    """
    def evaluate(self):
        #the epistemic state given as input
        prev_epi = self.prev.evaluate()
        #an epistemic state of the same type as prev_epi
        epi_next=complexOperation.createEmptyNextEpi(prev_epi)
        tempKB = []
        
        old_v = prev_epi.getV()
        old_kb = prev_epi.getKB()
        #the set of head atoms in rules
        uniqueHeads = complexOperation.getHeads(old_kb)
        #create a disjunction of all bodies that afffect the same head
        #create a rule (disjunction -> head)
        for head in uniqueHeads:
            other = self.getRulesThatAffectHead(head, old_kb)
            disjunction = basicLogic.createOrFromAtomList(other)
            newRule = basicLogic.operator_bitonic_implication(disjunction,head)
            tempKB.append(newRule)
        #turn implications to bijections, slightly slower but much more readable
        #than combining them in the same loop
        for rule in tempKB:
            if isinstance (rule, basicLogic.operator_bitonic_bijection):
                epi_next.addKnowledge(rule)
            if isinstance (rule, basicLogic.operator_bitonic_implication):
                body = rule.clause1
                head = rule.clause2
                newRule = basicLogic.operator_bitonic_bijection(body,head)
                epi_next.addKnowledge(newRule)
        #copy the old variables across the new epistemic state
        epi_next.addVariableList(old_v)
        return epi_next
    """
    GET ALL RULES WITH GROUND VALUES AS BODY
    @param kb: the knowledge base
    @return a list of all rules with ground atoms as their body
    """        
    def getGroundRules (self, kb):
        ground = []
        for rule in kb:
            if isinstance(rule,basicLogic.operator_bitonic_implication):
                if basicLogic.isGroundAtom(rule.clause1):
                    ground.append(rule)
            if isinstance(rule, basicLogic.operator_bitonic_bijection):
                if basicLogic.isGroundAtom(rule.clause1):
                    ground.append(rule)
                if basicLogic.isGroundAtom(rule.clause2):
                    ground.append(rule)
        return ground
    """
    GET THE LIST OF ALL CLAUSES (clause->head) FOR A GIVEN HEAD
    @param head: the head of the rule
    @param kb: the list of all rules
    @return all clauses that affect that head as a list
    """    
    def getRulesThatAffectHead (self, head, kb):
        rulesThatAffectHead=[]
        for rule in kb:
            if isinstance (rule, basicLogic.operator_bitonic_implication):
                if rule.clause2.getName() == head.getName():
                    rulesThatAffectHead.append(rule.clause1)
            elif isinstance (rule, basicLogic.operator_bitonic_bijection):
                if rule.clause2.getName() == head.getName():
                    rulesThatAffectHead.append(rule.clause1)
                if rule.clause1.getName() == head.getName():
                    rulesThatAffectHead.append(rule.clause2)
        return rulesThatAffectHead

"""
A COMPLEX OPERATION WHICH APPLIES THE SEMANTIC OPERATOR AS DESCRIBED IN @TODOref
T = {A|body->A exists with Interp(Body)=True}
F = {A|body->A exists and Interp(Body) is false in EVERY case}
"""
class complexOperation_semanticOperator (complexOperation):
    def __init__ (self):
        """
        CREATE AN INSTANCE OF THE complexOperation_semanticOperator CLASS
        """
        complexOperation.__init__(self, "semanticOperator")
    """
    USE THE PREVIOUS EPISTEMIC STATE AS A BASIS FOR CALCULATING VARIABLE VALUES
    USING THE SEMANTIC OPERATOR.
    @return the epistemic state after the semantic operator has been applied for one pass
    """
    def evaluate(self):
        prev_epi = self.prev.evaluate()
        return self.semanticOperatorEpi(prev_epi)
    """
    APPLY THE SEMANTIC OPERATOR
    @param prev_epi: the epistemic state to use as a base for application
    @return the epistemic state after the semantic operator has been applied for one pass
    """
    def semanticOperatorEpi (self, prev_epi):
        epi_next=complexOperation.createEmptyNextEpi(prev_epi)
        
        old_kb = prev_epi.getKB()
        old_v = prev_epi.getV()
        tempkb = basicLogic.setkbfromv(old_kb,old_v)
        
        epi_next.addKnowledgeList(tempkb)
        epi_next.addVariableList(old_v)
        epi_next = self.initGroundAtoms(epi_next)
        return epi_next      

    """
    DETERMINE IF THE OPERATOR IN QUESTION IS A BIJECTION
    return True if it is a bijection, False otherwise
    """
    @staticmethod
    def isBijection(rule):
        return isinstance (rule, basicLogic.operator_bitonic_bijection)
    """
    DETERMINE IF THE CLAUSE EVALUATES TO True/False/None.
    Note: does not use the values stored in V, only those of atoms in the rules
    which are usually unknown until set
    @param clause: the logical clause or atom to evaluate
    @return the logical evaluation of the clause
    """
    @staticmethod
    def evalClause (clause):
        if clause.evaluate() == False or isinstance(clause, basicLogic.atom_false):
            return False
        elif clause.evaluate() == True or isinstance(clause, basicLogic.atom_truth):
            return True
        return None
    """
    SET ALL ATOM HEADS WITH I(body)|=value TO value
    @param kb: the knowledge base of the epistemic state (pointer)
    @param v: the variable list of the epistemic state (pointer)
    """    
    @staticmethod
    def setToLogicalValue (kb,v, value):
        for rule in kb:
            head = rule.clause2
            body = rule.clause1
            if complexOperation_semanticOperator.evalClause(body)==value:
                if isinstance(head, basicLogic.atom) and not basicLogic.isGroundAtom(head):
                    for var in v:
                        if var.name == head.name:
                            var.setValue (value)
        for rule in kb:
            head = rule.clause1
            body = rule.clause2
            if complexOperation_semanticOperator.evalClause(body)==value:
                if isinstance(head, basicLogic.atom) and not basicLogic.isGroundAtom(head):
                    for var in v:
                        if var.name == head.name:
                            var.setValue (value)           
    """
    SET ALL ATOM HEADS WITH I(body)|=False TO FALSE
    @param kb: the knowledge base of the epistemic state (pointer)
    @param v: the variable list of the epistemic state (pointer)
    """
    @staticmethod
    def setFalse(kb,v):
        complexOperation_semanticOperator.setToLogicalValue(kb,v,False) 
    """
    SET ALL ATOM HEADS WITH I(body)|=Unknown TO UNKNOWN
    @param kb: the knowledge base of the epistemic state (pointer)
    @param v: the variable list of the epistemic state (pointer)
    """
    def setUnknown(kb,v):
        complexOperation_semanticOperator.setToLogicalValue(kb,v,None) 
    """
    SET ALL ATOM HEADS WITH I(body)|=True TO TRUE
    @param kb: the knowledge base of the epistemic state (pointer)
    @param v: the variable list of the epistemic state (pointer)
    """
    def setTrue(kb,v):
        complexOperation_semanticOperator.setToLogicalValue(kb,v,True)   
        
    """
    DETERMINE THE VALUE OF ATOMS BY FOLLOWING THE PROCEDURE OUTLINE IN THE DESCRIPTION
    OF complexOperation_semanticOperator
    The basic logic followed here is:
        1) set every atom that can be set to false first
        2) then set every atom that can be set to none
        3) then set every atom that can be set to true
    Doing this essentially masks the incorrect assignments from 1) using 2)
    @param kb: the knowledge base under consideration
    @param v: the set of variables being used
    @return the updated set of variables
    """
    @staticmethod
    def initGroundAtoms(epi):
        kb = epi.getKB()
        v = epi.getV()
        #check that every rule is of a valid format
        for rule in kb:
            if not complexOperation_semanticOperator.isBijection(rule):
                raise scpError.NotBijectionError
        complexOperation_semanticOperator.setFalse(kb,v)
        complexOperation_semanticOperator.setUnknown(kb,v)
        complexOperation_semanticOperator.setTrue(kb,v)
        return epi
"""
APPLY THE SEMANTIC OPERATOR UNTIL THE VARIABLE ASSIGNMENTS NO LONGER CHANGE
"""
class complexOperation_semanticOperator_full (complexOperation_semanticOperator):
    """
    CREATE AN INSTANCE OF THE COMPLEX OPERATION VARIABLE
    """
    def __init__ (self):
        complexOperation.__init__(self, "semanticOperatorFull")
    def compareLists (self,li1, li2):
        if len(li1)!=len(li2):
            return False
        for i in li1:
            found = False
            for j in li2:
                
                if i.getName()==j.getName():
                    if i.getValue()==j.getValue():
                        found = True
            if not found:
                return False
        return True
    """
    APPLY THE SEMANTIC OPERATOR UNTIL THE VARIABLE ASSIGNMENTS NO LONGER CHANGE
    @return the epistemic state after the semanticOperator has been completely applied
    """
    def evaluate (self):
        prev_epi=None
        current_epi=self.prev.evaluate()
        while prev_epi==None or not self.compareLists(prev_epi.getV(),current_epi.getV()):
            prev_epi=copy.deepcopy(current_epi)
            current_epi=self.semanticOperatorEpi(current_epi)
        return current_epi
        
        

"""
A COMPLEX OPERATION WHICH DELETES A NAMED VARIABLE FROM ALL SUBSEQUENT COMPLEX OPERATIONS
IN THE SCP
"""
class complexOperation_deleteVariable (complexOperation):
    """
    CREATE AN INSTANCE OF THE COMPLEX OPERATION VARIABLE
    @param variableName: the name of the variable to delete
    """
    def __init__ (self, variableName):
        complexOperation.__init__(self, "deleteVariable" + str(variableName))
        self.toDelete = variableName
    
    """
    IS THE VARIABLE TO DELETE THE HEAD OF THE RULE GIVEN?
    @param rule: implication or bijection rule x >> y
    @return y if y is the atom to delete
    """
    def toDeleteIsHead (self, rule):
        if not isinstance(rule, basicLogic.operator_bitonic):
            raise scpError.notBitonicOperatorError
        
        if rule.clause2.name == self.toDelete:
            return True
        return False
    """
    IS THE VARIABLE TO DELETE THE BODY OF THE GIVEN RULE?
    @param rule: implication or bijection rule x >> y  
    @return x if x is the atom to delete
    """
    def toDeleteIsBody (self, rule):
        if not isinstance(rule, basicLogic.operator_bitonic):
            raise scpError.notBitonicOperatorError
            
        if rule.clause1.name == self.toDelete:
            return True
        return False
    
    """
    IF NEITHER THE HEAD NOR THE BODY OF THE BOJECTION IS THE OPERATOR TO DELETE
    ADD THAT RULE TO THIS LIST OF RULES TO RETURN
    REMOVE THE VARIABLE FROM OUTPUT OF THIS COMPLEX ACTION
    @return an epistemic state with v=v-(self.toDelete), kb=kb-(rules with self.toDelete as head)
    """
    def evaluate(self):
        prev_epi = self.prev.evaluate()
        current_epi = complexOperation.createEmptyNextEpi(prev_epi)
        oldkb =  prev_epi.getKB()
        for old in oldkb:
            if isinstance(old, basicLogic.operator_bitonic_implication):
                if not self.toDeleteIsBody(old) and not self.toDeleteIsHead(old):
                    current_epi.addKnowledge(old)
            elif isinstance(old, basicLogic.operator_bitonic_bijection):
                if not self.toDeleteIsBody(old) and not self.toDeleteIsHead(old):
                    current_epi.addKnowledge(old)
                    
        oldv = prev_epi.getV()
        newv = []
        for old in oldv:
            if not old.name == self.toDelete:
                current_epi.addVariable(old)
        return current_epi        
"""
COMPLEX OPERATION THAT PREVENTS THE VALUE OF A VARIABLE FROM CHANGING IN SBUSEQUENT
COMPLEX OPERATIONS
"""
class complexOperation_fixVariable (complexOperation):
    """
    CREATE AN INSTANCE OF THE complexOperation_fixVariable CLASS
    @param variableName: the name of the variable to fix
    @param value: the value to which variableName must be fixed
    """
    def __init__ (self, variableName, value):

        complexOperation.__init__(self, "fixVariable" + str(variableName))
        self.toFix = variableName
        self.fixValue = value
    def evaluate(self):
        new_epi = copy.deepcopy(self.prev.evaluate())
        new_epi.setVariable(self.toFix, self.fixValue)
        new_epi.fixVariable(self.toFix, fixed=True)
        return new_epi
#==============================================================================
"""
COMPLEX OPERATION THAT ADDS MODUS TOLENS RULES TO THE KNOWLEDGE BASE
Modus Tolens: if a->b then not(b)->not(a)
"""
class complexOperation_modusTolens (complexOperation):
    """
    CREATE AN INSTANCE OF THE complexOperation_modusTolens CLASS
    """
    def __init__ (self):
        complexOperation.__init__(self, "Modus Tolens")
    """
    IS THE GIVEN CLAUSE AN ATOM?
    @param rule: the clause to check
    @return True if it is an atom, false otherwise
    """
    def isAtom(self, rule):
        return isinstance (rule, basicLogic.atom)
    """
    IS THE GIVEN CLAUSE A GROUND ATOM?
    @param rule: the clause to check
    @return True if it is a ground atom, false otherwise
    """
    def isGroundAtom (self, rule):
        return basicLogic.isGroundAtom(rule)
    """
    ADD THE CONTRAPOSITIVE RULE TO EACH NON-GROUND RULE IN THE KB
    @return the updated epistemic state
    """
    def evaluate(self):
        prev_epi = self.prev.evaluate()
        current_epi = complexOperation.createEmptyNextEpi(prev_epi)
        oldkb = prev_epi.getKB()
        oldV = prev_epi.getV()
        
        current_epi.addVariableList(oldV)
        current_epi.addKnowledgeList(oldkb)
        
        for rule in oldkb:
            if not rule.immutable:     
                if isinstance (rule, basicLogic.atom) and not self.isGroundAtom(rule.clause2):
                        negateClause1 = basicLogic.operator_monotonic_negation(rule.clause1)
                        negateClause2 = basicLogic.operator_monotonic_negation(rule.clause2)
                        contraRule = basicLogic.operator_bitonic_implication(negateClause1, negateClause2)
                        current_epi.addKnowledge(contraRule)
        return current_epi
    
    
    
    
    
    
    
 