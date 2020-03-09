# -*- coding: utf-8 -*-
"""
Created on Mon Jan 20 14:23:02 2020
HEREIN IS AN IMPLEMENTATION OF THE WASON SELECTION TASK USING SCPs
@author: Axel
"""

import basicLogic
import scp
from scpEvaluator import scp_evaluator
import copy
import complexOperation
import scpError

#CARDS THAT CAN BE OBSERVED
card_d = basicLogic.atom("D", setValue=False)
card_k = basicLogic.atom("K", setValue=False)
card_3 = basicLogic.atom("3", setValue=False)
card_7 = basicLogic.atom("7", setValue=False)



#STARTING RULES, FACTS
# the rule d -> 3 which participants are asked to vericy
knowledge_dimp3 = basicLogic.operator_bitonic_implication(card_d,card_3)
# rules for if each card is seen
knowledge_d = basicLogic.operator_bitonic_implication(basicLogic.TRUE, card_d)
knowledge_3 = basicLogic.operator_bitonic_implication(basicLogic.TRUE, card_3)
knowledge_k = basicLogic.operator_bitonic_implication(basicLogic.TRUE, card_k)
knowledge_7 = basicLogic.operator_bitonic_implication(basicLogic.TRUE, card_7)
# the extra fact that 7->not(3)
#CHANGED pPrime = basicLogic.operator_monotonic_negation(card_3)
pPrime = basicLogic.atom("D'", None)

knowledge_primeRelationp = basicLogic.operator_bitonic_implication(card_7,pPrime, immutable=True)
# the extra fact that K->not(D)
#CHANGED qPrime = basicLogic.operator_monotonic_negation(card_k)
qPrime = basicLogic.atom("3'",None)

knowledge_primeRelationq = basicLogic.operator_bitonic_implication(card_d,qPrime, immutable=True)
notPPrime = basicLogic.operator_monotonic_negation(pPrime, immutable=True)
knowledgeNotPtoP = basicLogic.operator_bitonic_implication(notPPrime,card_d, immutable=True)

#ALL POSSIBLE VARIABLES (USED IN ABDUCTION)
allVariables = (card_3,card_7,card_d,card_k,pPrime, qPrime)

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

comp_modusTolens = complexOperation.complexOperation_modusTolens()

"""
CREATE AN SCP CONTAING THE RULE D->3 AS WELL AS THE CARD OBSERVED
@param variable: variable to be added to the SCP (usually the card observed)
@param knowledge: information about observed card x in the form T->x
@return the SCP that results from this process
"""
def createwst_card (variable, knowledge, epistemicStateType="wcs"):
    wst =  scp.scp(epistemicStateType=epistemicStateType)
    # the d-> 3 rule
    wst.addKnowledge(knowledge_dimp3)
    # the observed card
    if knowledge !=None:
        wst.addKnowledge(knowledge) 
    wst.addVariable(card_d)
    wst.addVariable(card_3)   
    if variable!=None:
        wst.addVariable(variable)         
    wst.addNext(comp_addAB)    
    wst.addNext(comp_weak)
    wst.addNext(comp_semantic)
    wst.addNext(comp_semantic)
    wst.addNext(comp_semantic)

    return copy.deepcopy(wst)  

def createwst_noCard_contra ():
    wst =  scp.scp()
    # the d-> 3 rule
    wst.addKnowledge(knowledge_dimp3)
    wst.addVariable(card_d)
    wst.addVariable(card_3)    
    wst.addVariable(pPrime)
    wst.addVariable(qPrime)
    wst.addVariable(card_7)  
    wst.addVariable(card_k) 
    
    wst.addKnowledge(knowledgeNotPtoP)
    wst.addKnowledge(knowledge_primeRelationp)
    #wst.addKnowledge(knowledge_primeRelationq)
    #wst.addKnowledge(knowledgeNotPtoP)
    
       
    wst.addNext(comp_addAB)    
    wst.addNext(comp_weak)
    wst.addNext(comp_semantic)
    wst.addNext(comp_semantic)
    wst.addNext(comp_semantic)
    wst.addNext(comp_semantic)
    wst.addNext(comp_semantic)
    
    wst.insertAtPos(comp_modusTolens, 1)
    return copy.deepcopy(wst)  

"""
METHODS FOR EACH OF THE OBSERVED CARDS
"""
def createwst_card_d ():
    return createwst_card(card_d, knowledge_d) 
def createwst_card_k ():
    return createwst_card(card_k, knowledge_k) 
def createwst_card_3 ():
    return createwst_card(card_3, knowledge_3) 
def createwst_card_7 ():
    return createwst_card(card_7, knowledge_7) 
def createwst_noCard():
    return createwst_card(variable=None, knowledge=None) 
"""
METHODS FOR CASES WHERE CONTRAPOSITION TAKES PLACE
"""

def createwst_card_d_contraposition ():
    wst = createwst_noCard_contra()
    wst.addKnowledge(knowledge_d)
    wst.addVariable(card_d)

    print (wst.evaluate())
    return wst
def createwst_card_k_contraposition ():
    wst = createwst_noCard_contra()
    wst.addKnowledge(knowledge_k)
    wst.addVariable(card_k)

    print (wst.evaluate())
    return wst
def createwst_card_3_contraposition ():
    wst = createwst_noCard_contra()
    wst.addKnowledge(knowledge_3)
    wst.addVariable(card_3)

    print (wst.evaluate())
    return wst
def createwst_card_7_contraposition ():
    wst = createwst_noCard_contra()
    wst.addKnowledge(knowledge_7)
    wst.addVariable(card_7)

    print (wst.evaluate())
    return wst

"""
PRINT OUT THE SCP IN QUESTION SHOWING THEINPUT AND OUTPUTS OF EACH COMPLEX OPERATION CALL
"""
def describeSCP (scp_toDescribe, label):
    print (">>>>>>" + label + "<<<<<<<<")
    print(u'{}'.format(scp_toDescribe.strDetailed()))
    print ("The final sequence: " + str(scp_toDescribe))

#==============================================================================
#=================================UNIT TESTING=================================
#==============================================================================
def unit_compareAtomListStringList (stringList,atomList):
    if len(atomList)!=len(stringList):
        return False
    
    for i in atomList:
        if not i.name in stringList:
            return False
    return True
def unit_compareLeastModels (correctLeastModel, leastModel):
    trueMatch = unit_compareAtomListStringList(correctLeastModel[0],leastModel[0])
    falseMatch = unit_compareAtomListStringList(correctLeastModel[1],leastModel[1])
    if not trueMatch and falseMatch:
        raise scpError.unitTestFailedError
def unit_turnFunction (initialSCP, observation, allVariables, actualTurn, searchType="credulous"):
    turn = turnFunction(initialSCP, observation, allVariables, searchType="credulous")
    if turn != actualTurn:
        raise scpError.unitTestFailedError
def unit_wst (observation, correctLeastModel, actualTurn):
    allVariables = (card_3,card_7,card_d,card_k)
    scp_noCard = createwst_noCard()
    solutionSCPs = scp_evaluator.getRestrictedLeastModelSCPs(scp_noCard, observation, allVariables)
    leastModel_sets=scp_evaluator.leastModelFormatSCPList(solutionSCPs)
    unit_compareLeastModels(correctLeastModel,leastModel_sets)   
    unit_turnFunction(scp_noCard,observation,allVariables, actualTurn, searchType="credulous")
def unit_wst_d ():
    correctLeastModel=[[card_d.name, card_3.name],['ab1']]
    observation = card_d
    unit_wst(observation,correctLeastModel, actualTurn=True)
def unit_wst_k ():
    correctLeastModel=[[card_k.name],['ab1']]
    observation = card_k
    unit_wst(observation,correctLeastModel, actualTurn=False)  
def unit_wst_3 ():
    correctLeastModel=[[card_d.name,card_3.name],['ab1']]
    observation = card_3
    unit_wst(observation,correctLeastModel, actualTurn=True)      
def unit_wst_7 ():
    correctLeastModel=[[card_7.name],['ab1']]
    observation = card_7
    unit_wst(observation,correctLeastModel, actualTurn=False)  
def unit_TestAll ():   
    unit_wst_d()
    unit_wst_k()
    unit_wst_3()
    unit_wst_7()
    print (">>**All unit tests passed**<<")

#unit test to make sure the expected results are observed    


def printSummary (_scp, message):
    print ("{}".format(">"*35))
    print (message)
    print ("{}".format (_scp))
    print (u"Final Knowledge Base:\n{}".format(complexOperation.complexOperation.strKnowledge(_scp.evaluateKB())))
    print ("Final Variables (before abduction):\n{}".format(complexOperation.complexOperation.strVariables(_scp.evaluateV())))
    leastModel = scp_evaluator.getLeastModel(_scp)
    print ("Least Model: {} ".format(scp_evaluator.strLeastModelFromVariables(leastModel)))
    print ("Turn Card: {}".format(turnFunction(_scp)))
    print ("{}".format("<"*35))

def turnFunction (initialSCP, observation, allVariables, searchType="credulous"):
    #The solution SCPs are guaranteeed to be least models which make the obervation true after execution
    print (">>>>>>>>>>>>")
    print(initialSCP.evaluate())
    solutionSCPs = scp_evaluator.getRestrictedLeastModelSCPs(initialSCP, observation, allVariables)
    print ("Num solution SCPs: {}".format(len(solutionSCPs)))
    print("solution SCPs are {}".format(solutionSCPs[0].evaluate()))
    #only apply the semantic operator once
    
    initialSCP=copy.deepcopy(initialSCP)
    while isinstance(initialSCP.getLastOperation().prev, complexOperation.complexOperation_semanticOperator):
        initialSCP.removeLast()
    
    #print (initialSCP)
    #print ("observation {}".format(observation))
    extendedInitialSCP = scp_evaluator.addRuleToScpFromValue(initialSCP, observation.name, True)
    print ("extended initial scp: {}".format(extendedInitialSCP.si))
    print ("extended initial scp: {}".format(extendedInitialSCP.evaluate()))
    if searchType=="credulous":
        # if no solution scp is identical to the shortened scp, then turn
        match = scp_evaluator.credulousSCPCompare_finalEpis(extendedInitialSCP, solutionSCPs)
        #print ("The states match {}".format(match))
        return not match
    elif searchType=="skeptical":
        # if every solution scp is identical to the shortned scp, then don't turn
        match = scp_evaluator.skepticalSCPCompare_finalEpis(extendedInitialSCP, solutionSCPs)
        #print ("The states match {}".format(match))
        return not match
    return None
#only turn the card when there is not enough information to verify the rule after evaluating the scp
#@TODO needs heavy tweaking
def turnFunctionSimple (initialSCP):
    ruleToEval = [knowledge_dimp3]
    epi = initialSCP.evaluate()
    
    v = epi.getV()
    kb = epi.getKB()
    updatedRule = scp_evaluator.setkbfromv(ruleToEval,v)
    print (initialSCP.strKnowledge(kb))
    print (initialSCP.strVariables(v))
    for i in updatedRule:
        if (i.clause1.evaluate()!=None and i.clause2.evaluate()!=None):
            return True    
    return False
    

def printTurnForObs (observation, allVariables, _scp=None, value=True, searchType="credulous"):
    if _scp == None:
        _scp = createwst_noCard()
    print ("turn card {}: {}".format(observation.name,turnFunction(_scp,observation, allVariables, searchType=searchType)))
"""
print ("NORMAL CASES (WEAKLY COMPLETING)")
observation = card_d
carddturn=printTurnForObs(observation=card_d, allVariables=allVariables, value=True, searchType="skeptical")
observation = card_k
cardkturn=printTurnForObs(observation=card_k, allVariables=allVariables, value=True, searchType="skeptical")
observation = card_3
card3turn=printTurnForObs(observation=card_3, allVariables=allVariables, value=True, searchType="skeptical")
observation = card_7
card7turn=printTurnForObs(observation=card_7, allVariables=allVariables, value=True)
"""

#instantiate each normal card observation
wst_d = createwst_card_d()
wst_k = createwst_card_k()
wst_3 = createwst_card_3()
wst_7 = createwst_card_7()

print ("SIMPLIFIED TURN FUNCITON")
print ("Simplified D: {}".format(turnFunctionSimple(initialSCP=wst_d)))
print ("Simplified K: {}".format(turnFunctionSimple(initialSCP=wst_k)))
print ("Simplified 3: {}".format(turnFunctionSimple(initialSCP=wst_3)))
print ("Simplified 7: {}".format(turnFunctionSimple(initialSCP=wst_7)))



#instantiate each card observation with assumed modus tolens
wst_d_contra = createwst_card_d_contraposition()
wst_k_contra = createwst_card_k_contraposition()
wst_3_contra = createwst_card_3_contraposition()
wst_7_contra = createwst_card_7_contraposition() 


print ("SIMPLIFIED TURN FUNCITON WITH CONTRAPOSITION")
print ("Simplified contra D: {}".format(turnFunctionSimple(initialSCP=wst_d_contra)))
print ("Simplified contra K: {}".format(turnFunctionSimple(initialSCP=wst_k_contra)))
print ("Simplified contra 3: {}".format(turnFunctionSimple(initialSCP=wst_3_contra)))
print ("Simplified contra 7: {}".format(turnFunctionSimple(initialSCP=wst_7_contra)))
#print (wst_7.strDetailed())

"""
_scp = createwst_noCard()
#adding knowledge about the second relation k->7, and so not(7)->not(k) now prevents
#the turn function from identifying meaningful cards
#_scp.addKnowledge(knowledge_primeRelationq)

for card in allVariables:
    _scp.addVariable(card)
_scp.insertAtPos(comp_modusTolens, 1)



print wst_3.strKnowledge(wst_7.evaluateKB())
print wst_3.strVariables(wst_7.evaluateV())

print "CONTRA CASES"
print turnFunctionSimple(initialSCP=wst_d_contra)
print turnFunctionSimple(initialSCP=wst_k_contra)
print turnFunctionSimple(initialSCP=wst_3_contra)
print turnFunctionSimple(initialSCP=wst_7_contra)

rules = wst_d_contra.evaluateKB()
varss=wst_d_contra.evaluateV()
newRules = scp_evaluator.setkbfromv(rules,varss)

for rule in newRules:
    print u"{}".format(rule)
    print rule.evaluate()
"""
"""
v = wst_7_contra.evaluateV()
kb = wst_7_contra.evaluateKB()

print scp.scp.strDetailed(wst_7_contra)
"""

"""
print "CONTRA CASES"
observation = card_d
carddturn=printTurnForObs(observation=card_d, allVariables=allVariables, _scp=_scp, value=True)
observation = card_k
cardkturn=printTurnForObs(observation=card_k, allVariables=allVariables,_scp=_scp, value=True)
observation = card_3
card3turn=printTurnForObs(observation=card_3, allVariables=allVariables,_scp=_scp, value=True)
observation = card_7
card7turn=printTurnForObs(observation=card_7, allVariables=allVariables,_scp=_scp, value=True)

print _scp.strKnowledge(_scp.evaluateKB())
print _scp.strVariables(_scp.evaluateV())
"""

"""
print "D"
print _scp.strKnowledge(_scp.initialKB)
print _scp.strKnowledge(wst_7_contra.evaluateKB())
print _scp.strVariables(wst_7_contra.evaluateV())

print "K"
print _scp.strKnowledge(wst_k_contra.evaluateKB())
print _scp.strVariables(wst_k_contra.evaluateV())

print "3"
print _scp.strKnowledge(wst_3_contra.evaluateKB())
print _scp.strVariables(wst_3_contra.evaluateV())
print "7"
print _scp.strKnowledge(wst_7_contra.evaluateKB())
print _scp.strVariables(wst_7_contra.evaluateV())
"""

"""
observation=card_d
nocardcontra = createwst_noCard_contra()

print turnFunction(nocardcontra,observation,allVariables)


observation=card_k
nocardcontra = createwst_noCard_contra()
print turnFunction(nocardcontra,observation,allVariables)

observation=card_3
nocardcontra = createwst_noCard_contra()
print turnFunction(nocardcontra,observation,allVariables)

observation=card_7
nocardcontra = createwst_noCard_contra()
print turnFunction(nocardcontra,observation,allVariables)

"""
"""
observation=card_7
leastModel = scp_evaluator.getRestrictedLeastModelSCPs(_scp,observation,allVariables)
print len(leastModel)

print scp_evaluator.strLeastModelFormatSCPList(leastModel)
"""
#unit_TestAll()

#idea for conjunction fallacy, split a + b -> c











