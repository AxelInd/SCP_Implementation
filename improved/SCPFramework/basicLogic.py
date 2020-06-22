# -*- coding: utf-8 -*-
"""
Created on Sat Jan 18 11:07:55 2020

@author: Axel
"""
import sys
sys.path.append("/SCPFramework") 
from SCPFramework.truthTables import truthTable
"""
ATOMS ARE THE BASIC UNIT OF LOGIC.
Every atom consists of a name and truth value.
"""
class atom (object):
    """
    CREATE AN INSTANCE OF THE ATOM CLASS
    """
    def __init__(self, name, value = None, setValue = True):
        self.name = name
        self.fixed=False
        if setValue:      
            self._value = value
        else:
            self._value=None
            
        #print("I made an atom called " + self.name)
    """
    RETURN THE LOGICAL VALUE OF THE ATOM (usually True, False, None, but others
    are possible)
    @return the value of the atom
    """
    def evaluate(self):
        return self.getValue()
    """
    SET THE VALUE OF THE VARIABLE IF ITS NAME IS RIGHT. THIS METHOD NAME IS SHARED
    WITH THE OPERATOR CLASS AND USED INTERCHANGABLY BETWEEN THEM.
    @param var: the name of the variable
    @param val: the value to set
    @return True if successful, False otherwise
    """
    def deepSet(self, var, val):
        if (self.name == var):
            self.setValue(val)
            return True
        return False
            #print ("Variable " + str(self.name) + " set to " + str(self.value))
    """
    A STRING REPRESENTATION OF THE ATOM
    @return a string representation of the atom
    """
    def __str__ (self):
        return u"{}".format(self.name)
    """
    SET THE VALUE OF THE VARIABLE IF ITS NAME IS RIGHT.
    @param var: the name of the variable
    @param val: the value to set
    @return True if successful, False otherwise   
    """
    def setValue (self, val, setVal = True):
        if not self.fixed and setVal==True:
            self._value = val
    def getValue (self):
        return self._value
    def getName (self):
        return self.name
    def __repr__(self):
        return "({}:{})".format(self.name, self.getValue())
    
    def __hash__(self):
        return hash(self.__repr__())
    def __eq__(self, other):
        if isinstance(other, atom):
            sameName=(self.getName() == other.getName())
            sameVal = (self.getValue() == other.getValue())
            return (sameName and sameVal)
        else:
            return False
    def getAtoms(self):
        return [self]
    """
    def monotonicDelete(self, toDel):
        return self
    def contains_operator(self, op):
        return False
    """
    
class atom_truth (atom):
    def __init__ (self, setValue=True):
        atom.__init__(self, u"\u22A4", value = True, setValue=setValue)
class atom_false (atom):
    def __init__ (self, setValue=True):
        atom.__init__(self, u"\u22A5", value = False, setValue=setValue)

class atom_unknown (atom):
    def __init__ (self, setValue=True):
        atom.__init__(self, "UNKNOWN", value = None, setValue=setValue)
        
 
        
class operator (object):
    """
    Create an instanc of the operator class
    @param immutable: This rule is assumed to be true without abnormalitites
    in practice, this means that no abnormalities will be added by the scp to this operator.
    """
    def __init__(self, immutable=False, logicType = "L"):
        self.name= ""
        self.immutable=immutable
        self.logicType= logicType
        switch = {"L":truthTable.getTruthTables_L(),"P":truthTable.getTruthTables_P()}
        self.tbl_and, self.tbl_or, self.tbl_implication, self.tbl_bijective, self.tbl_not, self.tbl_conditional = switch[logicType]
    def evaluate(self):
        return "I am evaluating"
    def deepSet (self, var, val):
        print (" I am deepsetting")
    def __repr__(self):
        return self.__str__()
    def getName (self):
        return self.name
    def contains_operator(self,target=None):
        print ("NOT IMPLEMENTED FOR ABSTRACT CLASS")
    def monotonicDelete(self,typ):
        print("not implemented for abstract class operator")
    def getAtoms(self):
        print("not implemented for abstract class operator")
#ATOMS FOR BASE TRUTH VALUES      
TRUE = atom_truth (setValue=True)      
FALSE = atom_false (setValue=True)      
UNKNOWN = atom_unknown (setValue=True)
      

def getGroundAtomFor(val):
    if val==None:
        return UNKNOWN
    if val==True:
        return TRUE
    if val==False:
        return FALSE

class operator_monotonic(operator):
    def __init__(self, clause = None, immutable = False, logicType = "L"):
        operator.__init__(self,immutable = immutable, logicType=logicType)    
        self.clause=clause
        
        
    def deepSet (self, var, val):
        self.clause.deepSet(var, val)
        
    def __str__ (self): 
        return u"({} {})".format(self.name,self.clause)   
    #returns True if an operator of type target exists in this clause
    def contains_operator(self,target=None):
        if isinstance(self,target):
            return True
        if isinstance(self.clause,atom) or self.clause == None:    
            return False
        return self.clause.contains_operator(target)
    #delete all mononotonic operators of type typ
    #implemented for monotonic and bitonic operators
    def monotonicDelete(self,typ):
        if isinstance(self.clause,typ):
            self.clause=self.clause.clause
        if self.clause!=None and not isinstance(self.clause,atom):
            self.clause1.monotonicDelete(typ)
    def getAtoms (self):
        return self.clause.getAtoms()
class operator_monotonic_negation (operator_monotonic):
    def __init__(self, clause = None, immutable = False,  logicType = "L"):
        operator_monotonic.__init__(self, clause, immutable = immutable, logicType=logicType)     
        self.name = u"\u00AC"
    def getValue (self):
        return self.evaluate()
        
    def evaluate(self):        
        #@TODO is it valid to return unknown for all evaluation that cannot be handled by the truth table?
        try:    
            return self.tbl_not[str(self.clause.evaluate())]
        except:
            return None  
        
"""
THESE OPERATIONS APPLY TO QUANTIFIED LOGIC
"""
class operator_monotonic_holds (operator_monotonic):
    def __init__(self, clause = None, immutable = False,  logicType = "L"):
        operator_monotonic.__init__(self, clause, immutable = immutable, logicType=logicType)     
        self.name = u"H-"
    def getValue (self):
        return self.evaluate()
        
    def evaluate(self):        
        #@TODO is it right to treat hold as trivial truth?
        print("opmonholds should not be evaluating!!!")
        return True
    
class operator_monotonic_mostly (operator_monotonic):
    def __init__(self, clause = None, immutable = False,  logicType = "L"):
        operator_monotonic.__init__(self, clause, immutable = immutable, logicType=logicType)     
        self.name = u"M-"
    def getValue (self):
        return self.evaluate()
        
    def evaluate(self):        
        #@TODO is it right to treat hold as trivial truth?
        print("opmonmostly should not be evaluating!!!")
        return True
class operator_monotonic_rarely (operator_monotonic):
    def __init__(self, clause = None, immutable = False,  logicType = "L"):
        operator_monotonic.__init__(self, clause, immutable = immutable, logicType=logicType)     
        self.name = u"R-"
    def getValue (self):
        return self.evaluate()
        
    def evaluate(self):        
        #@TODO is it right to treat hold as trivial truth?
        print("opmonrarely should not be evaluating!!!")
        return True

#--------------------------------------------
class operator_bitonic (operator):
    def __init__(self, clause1=None, clause2=None, immutable = False,  logicType = "L"):
        operator.__init__(self, immutable = immutable, logicType=logicType) 
        self.clause1 = clause1
        self.clause2 = clause2
    def deepSet(self, var, val):
        self.clause1.deepSet(var, val)
        self.clause2.deepSet(var, val)
    def __eq__(self, o):
        #simplest cases
        if isinstance(o, type(self)):
            if self.clause1==o.clause1:
                if self.clause2==o.clause2:
                    return True
        #otherwise not equal
        return False
    def __str__(self):
        return u"({} {} {})".format(self.clause1, self.name, self.clause2)

    def contains_operator(self,target=None):
        if isinstance(self, target):
            return True
        c1 = False
        c2 = False
        if not(isinstance(self.clause1,atom) or self.clause1 == None):    
            c1=self.clause1.contains_operator(target)
        if not (isinstance (self.clause2, atom) or self.clause2 == None ):
            c2=self.clause2.contains_operator(target)
        return c1 or c2
    def monotonicDelete(self,typ):
        if isinstance(self.clause1,typ):
            self.clause1=self.clause1.clause
        if isinstance(self.clause2,typ):
            self.clause2=self.clause2.clause
        if self.clause1!=None and not isinstance(self.clause1, atom):
            self.clause1.monotonicDelete(typ)
        if self.clause2!=None and not isinstance(self.clause2, atom):
            self.clause2.monotonicDelete(typ)            
    def getAtoms (self):
        clause1Atoms = self.clause1.getAtoms()
        clause2Atoms = self.clause2.getAtoms()
        return clause1Atoms+clause2Atoms     
        

class operator_bitonic_and (operator_bitonic):      
    def __init__(self, clause1, clause2, immutable = False,  logicType = "L"):
        operator_bitonic.__init__(self,clause1,clause2, immutable = immutable, logicType=logicType) 
        self.name=u"\u2227"
    def evaluate(self):
        clauseVal1 = self.clause1.evaluate()
        clauseVal2 = self.clause2.evaluate()
        #@TODO is it valid to return unknown for all evaluation that cannot be handled by the truth table?
        try:           
            return self.tbl_and[str(clauseVal1)][str(clauseVal2)]
        except:
            return None        
class operator_bitonic_or (operator_bitonic):      
    def __init__(self, clause1, clause2, immutable = False,  logicType = "L"):
        operator_bitonic.__init__(self,clause1,clause2,immutable=immutable, logicType=logicType) 
        self.name=u"\u2228"
    def evaluate(self):
        clauseVal1 = self.clause1.evaluate()
        clauseVal2 = self.clause2.evaluate()
        #@TODO is it valid to return unknown for all evaluation that cannot be handled by the truth table?
        try:        
            return self.tbl_or[str(clauseVal1)][str(clauseVal2)]    
        except:
            return None
class operator_bitonic_implication (operator_bitonic):      
    def __init__(self, clause1, clause2, immutable = False,  logicType = "L"):
        operator_bitonic.__init__(self,clause1,clause2, immutable = immutable, logicType=logicType) 
        self.name=u"\u2190"
    def evaluate(self):
        clauseVal1 = self.clause1.evaluate()
        clauseVal2 = self.clause2.evaluate()
        
        #@TODO is it valid to return unknown for all evaluation that cannot be handled by the truth table?
        try:
            return self.tbl_implication[str(clauseVal1)][str(clauseVal2)] 
        except:
            return None
            
class operator_bitonic_conditional (operator_bitonic):      
    def __init__(self, clause1, clause2, immutable = False,  logicType = "L"):
        operator_bitonic.__init__(self,clause1,clause2, immutable = immutable, logicType=logicType) 
        self.name=u"|"
    def evaluate(self):
        clauseVal1 = self.clause1.evaluate()
        clauseVal2 = self.clause2.evaluate()
        
        #@TODO is it valid to return unknown for all evaluation that cannot be handled by the truth table?
        try:
            return self.tbl_conditional[str(clauseVal1)][str(clauseVal2)] 
        except:
            return None
        
class operator_bitonic_bijection (operator_bitonic):      
    def __init__(self, clause1, clause2,immutable=False,  logicType = "L"):
        operator_bitonic.__init__(self,clause1,clause2, immutable=immutable, logicType=logicType) 
        self.name=u"\u2194"
    def evaluate(self):
        clauseVal1 = self.clause1.evaluate()
        clauseVal2 = self.clause2.evaluate()
        #@TODO is it valid to return unknown for all evaluation that cannot be handled by the truth table?
        try:
            return self.tbl_bijective[str(clauseVal1)][str(clauseVal2)]
        except:
            return None   

    





class operator_tritonic (operator):
    def __init__(self, clause1=None, clause2=None, clause3=None, immutable=False, truthTable = "L"):
        operator.__init__(self, immutable = immutable)
        self.clause1 = clause1
        self.clause2 = clause2
        self.clause3 = clause3

    def __str__(self):
        return u"({}:{}|{})".format(self.clause1, self.clause2, self.clause3)        
class operator_tritonic_defaultRule(operator_tritonic):
    def __init__(self, clause1, clause2, clause3, immutable = False, truthTable = "L"):
        operator_tritonic.__init__(self,clause1,clause2, clause3, immutable = immutable)
        self.name=u"DR"
    
    def evaluate(self, derived):
        clauseVal1 = self.clause1.evaluate()
        #attempt to derive the negation of the consistency condition
        consistencyConditions = self.clause2
        
        if consistencyConditions==[]:
            return True
        negatedConsistencyConditions = negateRuleList(consistencyConditions)
        #evaluateRuleList_relaxed(negatedConsistencyConditions, expected=True)
        negationDerivable = testDerivableList(negatedConsistencyConditions,derived)
        if negationDerivable:
            return False
        
        # alpha must be derived before rule is applied
        if clauseVal1 == None:
            return None
        # the negation of beta must not be derivable
        return self.clause3
    
    def deepSet(self, var, val):
        self.clause1.deepSet(var, val)
        self.clause2.deepSet(var, val)
    def getAtoms(self):
        c2 = self.clause2 
        c=[]
        if isinstance(c2,list):
            for cl in c2:
                c=c+cl.getAtoms()
        return self.clause1.getAtoms()+ c + self.clause3.getAtoms()
    def isApplicableToW (self,W):
        #assume W is deductively closed
        #precondition is true
        precondition = self.clause1
        if precondition in W:
            #check no justification is falsified
            negJusts = negateRuleList(self.clause2)
            for neg in negJusts:
                if colapseNeg(neg) in W:
                    return False
            return True
        else:
            return False
        #conclusion does not lead to a contradition
        return False

#@TODO needs a lot of work
def testDerivableList(rules,der):
    for rule in rules:
        #some negation is derivable
        if testDerivable(rule, der):
            return True
    #no negation was derivable
    return False
def testDerivable (rule, der):
    if rule.evaluate()==True:
        return True
    if rule.evaluate()==False:
        return False
    for r in der:
        if str(r) == str(rule):
            return True
    return False

def negateRuleList (li):
    newli = []
    for rule in li:
        neg = operator_monotonic_negation(rule)
        newli.append(neg)
    return newli


def evaluateRuleList_strict(li, expected=True):
    for rule in li:
        if rule.evaluate()!=expected:
            return False
    return True
def evaluateRuleList_relaxed(li, expected=True):
    for rule in li:
        if rule.evaluate()==expected:
            return True
    return False


def createOrFromAtomList (li):
    bigOr = li[0]
    for i in range(1,len(li)):
        bigOr = operator_bitonic_or(bigOr,li[i])
    return bigOr


"""
INSTANTIATES THE VARIABLES IN kb WITH THE VALUES IN v
@param kb: the knowledge base (list of rules)
@param v: the variables (list of basicLogic.atom abjects)
@return the kb with each atom in each rule set to the values in v
"""
def setkbfromv (kb, v):
    for var in v:
        for rule in kb:
            rule.deepSet(var.name, var.getValue())
    return kb
"""
REPRESENT A SET OF VARIABLES AS A UNICODE STRING
@param v: the variables to represent
@return the variables as a human-readable string
"""  
def strVariables(v):
    vs = "{"
    if v == None:
        return "{}"
    for i in range (0, len(v)):
        vs = vs + u"{} : {}{}".format(v[i],v[i].evaluate(),(", " if i<len(v)-1 else "") )
    vs=vs+"}"
    return vs

"""
REPRESENT A SET OF RULES AS A UNICODE STRING
@param kb: the knowledge to represent
@return the rules as a human-readable string
"""     
def strKnowledge(kb):
        k = "{"
        if kb == None:
            return "{}"
        for i in range (0, len(kb)):
            k = u'{} {} {}'.format(k, kb[i], (", " if i<len(kb)-1 else "") )
        k=k+"}"
        return k        
        
def isGroundAtom (clause):
    if isinstance(clause, atom_truth):
        return True
    if isinstance (clause, atom_false):
        return True
    if isinstance (clause, atom_unknown):
        return True
    return False       


def compareVariableLists(li1,li2):
    if len(li1)!=len(li2):
        return False
    for v in li1:
        found = False
        for v2 in li2:
            if v.getName()==v2.getName():
                found=True
                if v.getValue() != v2.getValue():
                    return False
                if not found:
                    return False
    return True
def colapseNeg(neg):
    clause=neg.clause
    if isinstance (clause, operator_monotonic_negation):
        return clause.clause
    if isinstance(clause,operator_bitonic_implication):
        if clause.clause2 == TRUE:
            newNeg = operator_bitonic_implication(clause.clause1,FALSE)
            return newNeg
        if clause.clause2 == FALSE:
            newNeg = operator_bitonic_implication(clause.clause1,TRUE)
            return newNeg            

















