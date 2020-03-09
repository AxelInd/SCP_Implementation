# -*- coding: utf-8 -*-
"""
Created on Mon Feb 03 08:26:26 2020

@author: Axel
"""

import copy
import basicLogic
import scp
import complexOperation
import epistemicState

"""
THE SCP EVALUATOR IS A STATIC CLASS THAT HANDLES CARIOUS FUNCITON ASSOCIATED WITH
WITH ABDUCTION AND GENERATING LEAST MODELS (as seen in @TODOref).
"""
class scp_evaluator (object):
    #a mapping of every possible truth value to an integer
    logicRep = {0:None, 1:True, 2:False}
  
    """
    DETERMINE IF EVERY RULE IN THE KB OF THE SCP EVALUATES TO TRUE
    @param _scp: The SCP under consideration
    @param externalVariables: The variables that should be used to evaluate the SCP
    when None, uses the SCP's own instance variable list
    @return True if every rule in the KB evaluates to True, False otherwise
    """
    @staticmethod
    def ruleMatch (_scp, externalVariables=None):
        epi = _scp.evaluate()
        kb = epi.getKB()
        
        # If returns a copy of the KB with each atom's value set from those in externalVariables
        # or _scp.V by default
        kb = scp_evaluator.setkbfromv(kb,externalVariables)
        # check that every rule in the kb evaluates to true
        for rule in kb:
            tRule = copy.deepcopy(rule)
            if tRule.evaluate()!=True:
                return False
        return True
            
    """
    INSTANTIATES THE VARIABLES IN kb WITH THE VALUES IN v
    @param kb: the knowledge base (list of rules)
    @param v: the variables (list of basicLogic.atom abjects)
    @return the kb with each atom in each rule set to the values in v
    """
    @staticmethod     
    def setkbfromv (kb, v):
        kb=copy.deepcopy(kb)
        for var in v:
            for rule in kb:
                rule.deepSet(var.name, var.getValue())
        return kb
                
    """
    CONVERTS A NUMBER num TO BASE base AND FORCES A LENGTH OF length
    @param number: integer number
    @param base: desired base (should usually be the length of the logic being used)
    @return a list representing num in the desired base format with a total legth of length
    """
    @staticmethod 
    def toBase (num, base, length=-1):
        n = []
        tn = num
        
        while tn >= base:
            n.append(tn%base)
            tn = tn // base
        n.append(tn%base)
        
        if length > 0 and len(n) < length: 
            padding=[0]*(length-len(n))
            n = n + padding
        n.reverse()
        return n
    """
    CONVERTS A BASE n NUMBER IN A LIST INTO A LIST OF GROUND TRUTH VALUES FOR THE LOGIC
    @param n: the list representing the base n number
    @return a list with each number replaced by its logical equivalent in logicRep
    """
    @staticmethod
    def base_n_ToValuedLogic (n):
        
        li = [scp_evaluator.logicRep[i] for i in n]
        return li
    
    """
    FIND EVERY POSSIBLE TRUTH ASSIGNMENT OF THE FREE VARIABLES
    @param values: the variables that need assignments
    @return a list of list, containing every possible logical assignment of the values
    """
    @staticmethod  
    def generateAllPossibleVariableAssigmentsFromV (values):
        #the total number of possible assignments of the variables in values
        length = len(scp_evaluator.logicRep)**len(values)
        poss = []
        for i in range (0, length):
            #find the base n number that corresponds to i
            n = scp_evaluator.toBase(num=i, base=len(scp_evaluator.logicRep), length=len(values))
            #append a conversion of mapping of n to the logicRep truth table
            poss.append(scp_evaluator.base_n_ToValuedLogic(n))
        return poss

    """
    GIVEN AN INITIAL SCP, FIND THE SHORTEST NUMBER OF True/False/Unknown -> x
    RULES THAT MAKE EVERY RULE TRUE IN THE FINAL STATE
    @param initialSCP: the SCP which describes the task
    @return the least model of the final epistemic state
    """
    @staticmethod   
    def getLeastTrueModel (_scp, allVariables=None):
        if allVariables==None:
            allVariables=_scp.getInitialVariables()
        
        allValues = scp_evaluator.generateAllPossibleVariableAssigmentsFromV(allVariables)
        leastModel =[]
        shortest = 999
        for valueSet in allValues:
            _updatedScp = scp_evaluator.addRuleToSCPFromValueList(_scp, valueSet, allVariables)
            v = _updatedScp.evaluateV()
            kb = _updatedScp.evaluateKB()       
            match = scp_evaluator.ruleMatch(_updatedScp, v)
            if match:
                numRulesAdded = scp_evaluator.countNotUnknown(valueSet)
                if numRulesAdded <= shortest:
                    shortest = numRulesAdded
                    leastModel.append(_updatedScp)
        return leastModel
    
    """
    TAKE A LIST OF ATOMS AND TURN INTO A TWO LIST OF TRUE AND FALSE ATOMS
    @param variables: the variables with corresponding assignments in the least model
    @return the least model as a tuple (_true, _false) of the true and false variable lists respectively
    """
    @staticmethod
    def leastModelFormatVariables(variablesSets):
        _true=[]
        _false=[]
        for variables in variablesSets:
            for v in variables:
                if (v.getValue() == True):
                    _true.append(v)
                elif (v.getValue()==False):
                    _false.append(v)
            return (_true, _false)   
    @staticmethod
    def leastModelFormatSCPList (li):
        v = []
        for i in li:
            v.append(i.evaluateV())
        return scp_evaluator.leastModelFormatVariables(v)
    
    """
    TURN A LEAST MODEL IN SET FORMAT INTO A STRING FOR PRINTING
    @param _leastModelAsSets: a tuple (_true, _false) generated by the strLeastModel_single() function
    @return each least model as a string on a new line
    """
    @staticmethod
    def strLeastModelFromSets (_leastModelAsSets):
        least_raw = _leastModelAsSets
        s = u""
        for i in least_raw:        
            s=s+u"{"+scp_evaluator.strLeastModel_single(i)+"}\n"
        return s
    """
    TURN A LEAST MODEL IN VARIABLE FORMAT INTO A STRING FOR PRINTING
    @param leastModelAsSets: a list of atoms generated by the getLeastModel() function
    @return each least model as a string on a new line
    """
    @staticmethod
    def strLeastModelFromVariables (leastModelAsVariables):
        least_raw = scp_evaluator.leastModelAsSets(leastModelAsVariables)
        s = u""
        for i in least_raw:        
            s=s+u"{"+scp_evaluator.strLeastModel_single(i)+"}\n"
        return s    
    
    """
    TURN A SINGLE LEAST MODEL IN SET FORMAT INTO A STRING
    @param least: a single least model in set format
    @return the least model as a string
    """
    @staticmethod
    def strLeastModel_single (least):
        t=""
        f=""
        _true = [str(i) for i in least[0]]
        for i in range (0, len(_true)):
            t="{}{}{}".format(t,_true[i], "," if i<len(_true)-1 else "")            
        _false = [str(i) for i in least[1]]
        for i in range (0, len(_false)):
            f="{}{}{}".format(f,_false[i], "," if i<len(_false)-1 else "") 
        s = u"True=({}), False=({})".format(t,f)
        return s         
    
    
    
    
    
    @staticmethod
    def countNotUnknown (li):
        count = 0
        for i in li:
            if i!=None:
                count=count+1
        return count    
    
    @staticmethod    
    def addRuleToScpFromValue (_scp,  varName, value=True):
        if value!=None:
            head = basicLogic.atom(varName,None)
            body = basicLogic.getGroundAtomFor(value)
            rule = basicLogic.operator_bitonic_implication(body, head)
            _scp.addKnowledge(rule)
            _scp.addVariable(head)    
        return _scp
    @staticmethod
    def addRuleToSCPFromValueList (_scp, valueSet, allVariables):
        _scp = copy.deepcopy(_scp)
        for variablePos in range (0, len(valueSet)):
            scp_evaluator.addRuleToScpFromValue(_scp,allVariables[variablePos].name,valueSet[variablePos])
        return _scp
    
    @staticmethod
    def getVariableFromList(name, li):
        for i in li:
            if i.name == name:
                return i
        return None
    @staticmethod
    def getVariableInList (name, li):
        if scp_evaluator.getVariableFromList(name, li)==None:
            return False
        return True
    """
    DONE BY FINDING THE MINIMAL x->y RULE TO INSERT AT THE START OF THE SCP
    SUCH THAT THE FINAL EPISTEMIC STATE lm_wcP(F) = True
    @TODO there would be merit in ensuring that rule sets are added in order of length
    this would allow us to avoid processing uneccessarily long rules that could not
    possibly be the least model because there is already a shorter rule
    """
    @staticmethod
    def getRestrictedLeastModelSCPs (_scp, observation, allVariables, requiredObsValue=True):
        allValues = scp_evaluator.generateAllPossibleVariableAssigmentsFromV(allVariables)
        leastModel =[]
        shortest = 999
        for valueSet in allValues:
            _updatedScp = scp_evaluator.addRuleToSCPFromValueList(_scp, valueSet, allVariables)
            _updatedScp.addVariable(observation)
            epi = _updatedScp.evaluate()
            v = epi.getV()
            kb = epi.getKB()       
            match = scp_evaluator.ruleMatch(_updatedScp, v)
            if match:
                obsInScp = scp_evaluator.getVariableFromList(observation.name, v)
                if obsInScp.getValue() == requiredObsValue:
                    numRulesAdded = scp_evaluator.countNotUnknown(valueSet)
                    if numRulesAdded <= shortest:
                        shortest = numRulesAdded
                        leastModel.append(_updatedScp)
        return leastModel
             
    @staticmethod
    #@TODO needs extensive improving
    def compareSCP_finalEpis (scp1, scp2):
        epi1 = scp1.evaluate()
        epi2 = scp2.evaluate()
        if epi1 != epi2:
            return False
        return True

    
    @staticmethod
    def credulousSCPCompare_finalEpis (_scp, scpList):
        for s in scpList:
            match = scp_evaluator.compareSCP_finalEpis(_scp,s)
            if match:
                return True
        return False

    @staticmethod
    def skepticalSCPCompare_finalEpis (_scp,scpList): 
        for s in scpList:
            match = scp_evaluator.compareSCP_finalEpis(_scp,s)
            if not match:
                return False
        return True                
                 
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
