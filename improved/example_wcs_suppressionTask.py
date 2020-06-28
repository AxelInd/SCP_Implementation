# -*- coding: utf-8 -*-
"""
Created on Sat Jan 18 09:41:08 2020

This file includes several examples of implementations of the Suppression Task as described in the thesis
All examples make use of the SCP framework.
@author: Axel
"""

import copy
folderStructure=True
if folderStructure:
    import sys
    sys.path.append("/SCPFramework") 
    from SCPFramework import basicLogic
    from SCPFramework import epistemicState
    from SCPFramework import SCP_Task
    from SCPFramework import scpNotationParser
    from SCPFramework import CTM
    from SCPFramework import CognitiveOperation
    from SCPFramework import StatePointOperations
else:
    import basicLogic
    import epistemicState
    import SCP_Task
    import scpNotationParser
    import CTM
    import CognitiveOperation
    import StatePointOperations

print ("=================THE SUPPRESSION TASK=========================")
print (">>> 1) If she has an essay to write she will study late in the library (l|e).")
print (">>> 2) If the library is open she will study late in the library (l|o).")
print (">>> 3) She has an essay to write (e <- T).")
  

#STARTING VARIABLES
# e: she has an essay to write
e = basicLogic.atom('e', setValue=False)
# l: she will study late in the library
l = basicLogic.atom('l', setValue=False)
# o: the library is open
o = basicLogic.atom('o', setValue=False)

# THE SET OF COGNITIVE OPERATIONS APPROPRIATE TO THE SUPPRESSION TASK
ADDAB = CognitiveOperation.m_addAB()
WC = CognitiveOperation.m_wc()
SEMANTIC = CognitiveOperation.m_semantic()
ABDUCIBLES=CognitiveOperation.m_addAbducibles(maxLength=4)
DELETE=CognitiveOperation.m_deleteo()

"""
==================================================================================================
================================EXTERNAL EVALUATION FUNCTIONS=====================================
"""
# Compares the subSCPs 'el' and 'elo' and if there is a response in 'el' that is
# not in 'elo', then we have supressed an inference.
def f_suppression_studyLate(pi):
    finalStructures=pi.evaluate()
    finalStates=StatePointOperations.flattenStatePoint(finalStructures)
    #print (finalStates)
    #get all realised epis with 'el' name 
    statesForCaseEL = StatePointOperations.extractBasePointsFromFlattenedStatePoint(finalStates,name="el")
    #get all realised epis with 'elo' name 
    statesForCaseELO = StatePointOperations.extractBasePointsFromFlattenedStatePoint(finalStates,name="elo")
    
    # find the set of responses that that the realised SCPs of 'el' could reach
    responsesEL = f_studyLateSingle(statesForCaseEL)
    # find the set of responses that that the realised SCPs of 'elo' could reach
    responsesELO = f_studyLateSingle(statesForCaseELO)
    
    #suppression has occured if there is a response in responsesEL which is NOT
    # in responsesELO
    """
    for r1 in responsesEL:
        if r1 not in responsesELO:
            print ("The response '{}' occurs for 'el', but not for 'elo'".format(r1))
            return "Suppression observed"
    return "Suppression not observed"
    """
    return {'el':responsesEL,'elo':responsesELO}

# suppression is observed when el leads to the inference (l:True) and elo does not
# evaluates a single epistmeic state to model the conclusion
def f_studyLateSingle(finalEpis):
    if not isinstance(finalEpis,list):
        finalEpis=[finalEpis]
    #print("Final states:")
    #print(finalEpis)
    goal2 = [('l',True)]
    responses=[]
    for epi in finalEpis:
        #print ("\n")
        #print (epi)
        V = epi['V']
        
        for var in V:
            for goal in goal2:
                if var.getName()==goal[0] :
                    if var.getValue()==goal[1]:
                        responses.append("She will study late in the library")
                    if var.getValue()!=None and var.getValue()!=goal[1]:
                        responses.append("She will not study late in the library")
                    if var.getValue()==None:
                        responses.append("We are uncertain if she will study late in the library")
        #print ("Epistemic state:")
        #print (epi)
        #print ("response(p_bar):", responses[-1])
        #print ("------------------------------")
    return responses
        


"""
==================================================================================================
======================================CREATE BASE POINTS==========================================
"""
def createBasePoint_el (): 
    basePoint_el=epistemicState.epistemicState('el')
    delta1=["( l | e )"]
    S1 = ["( e <- T )"]
    delta1AsLogic = scpNotationParser.stringListToBasicLogic(delta1)
    S1AsLogic = scpNotationParser.stringListToBasicLogic(S1)
    basePoint_el['S']=S1AsLogic
    basePoint_el['Delta']=delta1AsLogic
    basePoint_el['V']=[e,l]
    return basePoint_el

def createBasePoint_elo():
    #The elo case expressed as the addition of information to the el case
    basePoint_el=copy.deepcopy(createBasePoint_el())
    basePoint_elo=copy.deepcopy(basePoint_el)
    basePoint_elo.setName('elo')
    #The possible starting states for the SCP
    extraConditional=["( l | o )"]
    extraConditionalAsLogic = scpNotationParser.stringListToBasicLogic(extraConditional)
    basePoint_elo['Delta']=basePoint_elo['Delta']+extraConditionalAsLogic
    basePoint_elo['V']=basePoint_elo['V']+[o]
    basePoint_elo['R']={'delete':["o","e"]}
    basePoint_elo['R']={'delete':["o","e"]}
    return basePoint_elo
"""
==================================================================================================
====================================SUPPRESSION EXAMPLES==========================================
"""
def standardSuppression():
    print ("===========================================================")
    print ("================STANDARD SUPPRESSION========================")
    print ("===========================================================")
    basePoint_el = createBasePoint_el()
    basePoint_elo = createBasePoint_elo()
    statePoints=[basePoint_el,basePoint_elo]
    s_i=statePoints
    
    f=f_suppression_studyLate
    #The desired output of the external evaluation function
    gamma={'el':'She will study late in the library',
           'elo':'We are uncertain if she will study late in the library'}
    
    #test ctm
    c = CTM.CTM()
    c.setSi(s_i)
    c.appendm(ADDAB)
    c.appendm(WC)
    c.appendm(SEMANTIC)

    predictions = f(c)
    print ('predictions: ', predictions)
    print ("Lenient Interp")
    print (StatePointOperations.predictionsModelsGamma_lenient(predictions,gamma))
    print("Strict Interp")
    print (StatePointOperations.predictionsModelsGamma_strict(predictions,gamma))
    print ("f(pi) models gamma_Sup? : ", 
           (StatePointOperations.predictionsModelsGamma_lenient(predictions,gamma)))  


def abducibleSuppression():
    print ("===========================================================")
    print ("=================ABDUCIBLE SUPPRESSION=====================")
    print ("===========================================================")
    basePoint_el = createBasePoint_el()
    basePoint_elo = createBasePoint_elo()
    statePoints=[basePoint_el,basePoint_elo]

    #abducibs = [ '( l <- T )', '( l <- F )','( o <- T )', '( o <- F )']
    abducibs = ['( o <- T )', '( o <- F )']
    logAbducibs =  scpNotationParser.stringListToBasicLogic(abducibs)
    basePoint_el['R']={'abducibles':logAbducibs}
    basePoint_elo['R']={'abducibles':logAbducibs}
    #Create the first state point
    statePoints=[basePoint_el,basePoint_elo]
    s_i=statePoints
    
    f=f_suppression_studyLate
    #The desired output of the external evaluation function
    gamma={'el':'She will study late in the library','elo':'We are uncertain if she will study late in the library'}

    #test ctm
    c = CTM.CTM()
    c.setSi(s_i)
    c.appendm(ADDAB)
    c.appendm(ABDUCIBLES)
    c.appendm(WC)
    c.appendm(SEMANTIC)    
    predictions = f(c)
    print ('predictions: ', predictions)

    print ("Lenient Interp")
    print (StatePointOperations.predictionsModelsGamma_lenient(predictions,gamma))
    print("Strict Interp")
    print (StatePointOperations.predictionsModelsGamma_strict(predictions,gamma))
    print ("f(pi) models gamma_noSup? : ", (StatePointOperations.predictionsModelsGamma_lenient(predictions,gamma)))


def deletionSuppression():
    print ("===========================================================")
    print ("================DELETION SUPPRESSION=======================")
    print ("===========================================================")        
    print ("===========================================================")
    basePoint_el = createBasePoint_el()
    basePoint_elo = createBasePoint_elo()
    statePoints=[basePoint_el,basePoint_elo]
    basePoint_el['R']={'delete':["o","e"]}
    basePoint_elo['R']={'delete':["o","e"]}
    
    #Create the first state point
    statePoints=[basePoint_el,basePoint_elo]
    s_i=statePoints
    
    #The external evaluation function
    f=f_suppression_studyLate
    #The desired output of the external evaluation function
    gamma={'el':'She will study late in the library','elo':'We are uncertain if she will study late in the library'}

    #test ctm
    c = CTM.CTM()
    c.setSi(s_i)
    c.appendm(ADDAB)
    c.appendm(DELETE)
    c.appendm(WC)
    c.appendm(SEMANTIC)

    predictions = f(c)
    print ('predictions: ', predictions)
    print ("Lenient Interp")
    print (StatePointOperations.predictionsModelsGamma_lenient(predictions,gamma))
    print("Strict Interp")
    print (StatePointOperations.predictionsModelsGamma_strict(predictions,gamma))

"""
==================================================================================================
============================================SEARCH================================================
"""
def scpSearch():
    print ("=======================BEGINNING SEARCH===============================")
    basePoint_el = createBasePoint_el()
    basePoint_elo = createBasePoint_elo()
    
    #abducibs = [ '( l <- T )', '( l <- F )','( o <- T )', '( o <- F )']
    abducibs = ['( o <- T )', '( o <- F )']
    logAbducibs =  scpNotationParser.stringListToBasicLogic(abducibs)
    
        
    basePoint_el['R']={'delete':["o","e"]}
    basePoint_elo['R']={'delete':["o","e"]}
    basePoint_el['R']['abducibles']=logAbducibs
    basePoint_elo['R']['abducibles']=logAbducibs
    
    #Create the first state point
    statePoints=[basePoint_el,basePoint_elo]
    s_i=statePoints    
    #The set of possible states
    M=[ADDAB,SEMANTIC,WC]
    #The external evaluation function
    f=f_suppression_studyLate
    #The desired output of the external evaluation function
    gamma={'el':'She will study late in the library','elo':'We are uncertain if she will study late in the library'}
    
    #The SCP task which states what is required from a solution SCP or realised SCP
    task = SCP_Task.SCP_Task(s_i,M,f,gamma)  
    
    searchResult = task.deNoveSearch()
    print ("\nSEARCH RESULTS:")
    print(strSCPLi(searchResult))

#turn an scp list into a list of strings
def strSCPLi(mu):    
    f_aliases={f_suppression_studyLate:"f_sup"}
    scps=[]
    for s in mu:
        for al in f_aliases:
            if s[1]==al:
                scps.append((s[0].__repr__(), f_aliases[al]))
    return scps 

"""
==================================================================================================
===========================================TESTING================================================
"""
#show that suppression can be modelled in the SCP framework 
standardSuppression()
    
#show that suppression no longer occurs when <m_addAbducibles> adds explanations about the var o
abducibleSuppression()

#show that suppression no longer occurs when the <m_delete> cognitive operation it used
deletionSuppression()

#find SCPs of Pi which demonstrate suppression
scpSearch()


























