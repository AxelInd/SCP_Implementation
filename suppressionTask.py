# -*- coding: utf-8 -*-
"""
Created on Sat Jan 18 09:41:08 2020

@author: Axel
"""
import basicLogic
import scp
import complexOperation
import scpError
import epistemicState
print ("=================THE SUPPRESSION TASK=========================")





print (">>> 1) If she has an essay to write she will study late in the library (e->l).")
print (">>> 2) If the library is open she will study late in the library (o->l).")
print (">>> 3) She has an essay to write (True->e).")

#STARTING VARIABLES
# e: she has an essay to write
e = basicLogic.atom('e', setValue=False)
# l: she will study late in the library
l = basicLogic.atom('l', setValue=False)
# o: the library is open
o = basicLogic.atom('o', setValue=False)

#STARTING RULES, FACTS
# if she has an essay to write, she will study late in the library
knowledge1 = basicLogic.operator_bitonic_implication(e,l)
# she has an essay to write
knowledge2 = basicLogic.operator_bitonic_implication(basicLogic.TRUE, e)
# if the library is open, she will study late in the library
knowledge3 = basicLogic.operator_bitonic_implication(o, l)
# the lirary is open
knowledge4 = basicLogic.operator_bitonic_implication(basicLogic.TRUE, o)

#INITIALISE THE SET OF COMPLEX OPERATORS M

# create the complex operation to add abnormalities
comp_addAB = complexOperation.complexOperation_addAB ()
# create the complex operation to delete a named variable
comp_deleteo = complexOperation.complexOperation_deleteVariable('o')
# create the complex operation to fix a named variable to a specified value
comp_fixab1 = complexOperation.complexOperation_fixVariable('ab1', False)
# Create the complex operation to weakly complete the logic program
comp_weak = complexOperation.complexOperation_weaklyComplete()
# create the complex operation to apply the sematic operator
comp_semantic = complexOperation.complexOperation_semanticOperator()

comp_semantic_full = complexOperation.complexOperation_semanticOperator_full()


def createsuppressionTask_standard():
    suppressionTask = scp.scp()
    #ADD THE FACTS TO THE INITIAL EPISTEMIC STATE
    suppressionTask.addKnowledge(knowledge1)
    suppressionTask.addKnowledge(knowledge2)
    suppressionTask.addKnowledge(knowledge3)
    # LEAVE UNCOMMENTED TO TEST CASES THE WHERE WE HAVE KNOWLEDGE OF THE OPENNESS OF THE LIBRARY
    #a.addKnowledge(knowledge4)
    
    #INITIAL VARIABLE ASSIGNMENTS
    # This adds variables with unknown values to the V set of the epistemic state
    suppressionTask.addVariable(e)
    suppressionTask.addVariable(l)
    suppressionTask.addVariable(o)
    
    suppressionTask.addNext(comp_addAB)
    suppressionTask.addNext(comp_weak)
    suppressionTask.addNext(comp_semantic)
    suppressionTask.addNext(comp_semantic)
    suppressionTask.addNext(comp_semantic)
    return suppressionTask

def createsuppressionTask_noSuppression():
    suppressionTask = scp.scp()
    #ADD THE FACTS TO THE INITIAL EPISTEMIC STATE
    suppressionTask.addKnowledge(knowledge1)
    suppressionTask.addKnowledge(knowledge2)
    #suppressionTask.addKnowledge(knowledge3)
    # LEAVE UNCOMMENTED TO TEST CASES THE WHERE WE HAVE KNOWLEDGE OF THE OPENNESS OF THE LIBRARY
    #a.addKnowledge(knowledge4)
    
    #INITIAL VARIABLE ASSIGNMENTS
    # This adds variables with unknown values to the V set of the epistemic state
    suppressionTask.addVariable(e)
    suppressionTask.addVariable(l)
    #suppressionTask.addVariable(o)
    
    suppressionTask.addNext(comp_addAB)
    suppressionTask.addNext(comp_weak)
    suppressionTask.addNext(comp_semantic)
    suppressionTask.addNext(comp_semantic)
    suppressionTask.addNext(comp_semantic)
    return suppressionTask

def createsuppressionTask_fixVariableab1():
    suppressionTask = scp.scp()
    #ADD THE FACTS TO THE INITIAL EPISTEMIC STATE
    suppressionTask.addKnowledge(knowledge1)
    suppressionTask.addKnowledge(knowledge2)
    suppressionTask.addKnowledge(knowledge3)
    # LEAVE UNCOMMENTED TO TEST CASES THE WHERE WE HAVE KNOWLEDGE OF THE OPENNESS OF THE LIBRARY
    #a.addKnowledge(knowledge4)
    
    #INITIAL VARIABLE ASSIGNMENTS
    # This adds variables with unknown values to the V set of the epistemic state
    suppressionTask.addVariable(e)
    suppressionTask.addVariable(l)
    suppressionTask.addVariable(o)
    
    suppressionTask.addNext(comp_addAB)
    suppressionTask.addNext(comp_fixab1)
    suppressionTask.addNext(comp_weak)
    suppressionTask.addNext(comp_semantic)
    suppressionTask.addNext(comp_semantic)
    suppressionTask.addNext(comp_semantic)
    return suppressionTask

def createsuppressionTask_deleteVariableo():
    suppressionTask = scp.scp()
    #ADD THE FACTS TO THE INITIAL EPISTEMIC STATE
    suppressionTask.addKnowledge(knowledge1)
    suppressionTask.addKnowledge(knowledge2)
    suppressionTask.addKnowledge(knowledge3)
    # LEAVE UNCOMMENTED TO TEST CASES THE WHERE WE HAVE KNOWLEDGE OF THE OPENNESS OF THE LIBRARY
    #a.addKnowledge(knowledge4)
    
    #INITIAL VARIABLE ASSIGNMENTS
    # This adds variables with unknown values to the V set of the epistemic state
    suppressionTask.addVariable(e)
    suppressionTask.addVariable(l)
    suppressionTask.addVariable(o)

    suppressionTask.addNext(comp_deleteo)
    suppressionTask.addNext(comp_addAB)
    suppressionTask.addNext(comp_weak)
    suppressionTask.addNext(comp_semantic)
    suppressionTask.addNext(comp_semantic)
    suppressionTask.addNext(comp_semantic)


    return suppressionTask

def createAtoms (names, vals):
    li = []
    for i in range (0,len(names)):
        at = basicLogic.atom(names[i],vals[i])
        li.append(at)
    return li

def unit_compare(_scp,correctKB, correctNames, correctVals):
    epi = _scp.evaluate()
    v = epi.getV()
    kb = epi.getKB()
    
    correctV = createAtoms(correctNames,correctVals)
    if len(v)!=len(correctV):
        raise scpError.unitTestFailedError
    for i in range (0, len(correctV)):
        if v[i].name!=correctV[i].name or v[i].getValue() != correctV[i].getValue():
            raise scpError.unitTestFailedError
    
def unit_sup_standard ():
    _scp = createsuppressionTask_standard()
    correctKB = None
    print (_scp.evaluate())
    correctNames = ['e','l','o','ab1','ab2']
    correctVals = [True,None,None,None,False]
    print (_scp.strDetailed())
    unit_compare(_scp,correctKB,correctNames,correctVals)
def unit_sup_noSuppression ():
    _scp = createsuppressionTask_noSuppression()
    correctKB = None
    correctNames = ['e','l','ab1',]
    correctVals = [True, True, False]
    unit_compare(_scp,correctKB,correctNames,correctVals)    
def unit_sup_fix ():
    _scp = createsuppressionTask_fixVariableab1()
    correctKB = None
    correctNames = ['e','l','o','ab1','ab2']
    correctVals = [True,True,None,False,False]
    unit_compare(_scp,correctKB,correctNames,correctVals)      
def unit_sup_delete ():
    _scp = createsuppressionTask_deleteVariableo()
    correctKB = None
    correctNames = ['e','l','ab1',]
    correctVals = [True, True, False]
    unit_compare(_scp,correctKB,correctNames,correctVals)      
def unit_TestAll ():
    unit_sup_standard()
    unit_sup_noSuppression()
    unit_sup_fix()
    unit_sup_delete()
    print (">>**All unit tests passed**<<")

    
def describeSCP (scp_toDescribe, label):
    print (">>>>>" + label + "<<<<<<<<")
    print(scp_toDescribe.strDetailed())
    print ("The final sequence: " + str(scp_toDescribe))    
    
"""
#CREATE AN SCP FOR EACH VARIATION OF THE TASK
suppressionTask_standard = createsuppressionTask_standard()
suppressionTask_noSuppression = createsuppressionTask_noSuppression()
suppressionTask_fix = createsuppressionTask_fixVariableab1()
suppressionTask_delete = createsuppressionTask_deleteVariableo()


#CHOOSE WHICH SCP TO SEE DETAILED HERE
describeSCP(suppressionTask_delete, "Standard Suppression Task")

#unit test to make sure the expected results are observed

"""
unit_TestAll()
"""

si = epistemicState.epistemicState_weakCompletion()
si.addKnowledge(knowledge1)
si.addKnowledge(knowledge2)
#si.addKnowledge(knowledge3)

si.addVariable(e)
si.addVariable(l)
#si.addVariable(o)

suppressionTask = scp.scp(epiState1=si)

suppressionTask.addNext(comp_addAB)
suppressionTask.addNext(comp_weak)
suppressionTask.addNext(comp_semantic_full)
describeSCP(suppressionTask, "Standard Suppression Task")


#si2 = epistemicState.epistemicState_weakCompletion()
#print (si)




#suppressionTask.addNext(comp_semantic)
#suppressionTask.addNext(comp_semantic)


#print (si)
"""





















