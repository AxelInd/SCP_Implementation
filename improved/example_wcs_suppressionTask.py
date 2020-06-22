# -*- coding: utf-8 -*-
"""
Created on Sat Jan 18 09:41:08 2020

@author: Axel
"""
import sys
sys.path.append("/SCPFramework") 
import copy

from SCPFramework import basicLogic
from SCPFramework import epistemicState
from SCPFramework import SCP_Task
from SCPFramework import scpNotationParser
from SCPFramework import CTM
from SCPFramework import CognitiveOperation
from SCPFramework import StatePointOperations
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
        print ("Epistemic state:")
        print (epi)
        print ("response(p_bar):", responses[-1])
        print ("------------------------------")
    return responses
        
# THE SET OF COGNITIVE OPERATIONS APPROPRIATE TO THE SUPPRESSION TASK
ADDAB = CognitiveOperation.m_addAB()
WC = CognitiveOperation.m_wc()
SEMANTIC = CognitiveOperation.m_semantic()
ABDUCIBLES=CognitiveOperation.m_addAbducibles(maxLength=4)
DELETE=CognitiveOperation.m_deleteo()

        
basePoint1=epistemicState.epistemicState('el')
delta1=["( l | e )"]
S1 = ["( e <- T )"]
delta1AsLogic = scpNotationParser.stringListToBasicLogic(delta1)
S1AsLogic = scpNotationParser.stringListToBasicLogic(S1)
basePoint1['S']=S1AsLogic
basePoint1['Delta']=delta1AsLogic
basePoint1['V']=[e,l]


#The elo case expressed as the addition of information to the el case
basePoint2=copy.deepcopy(basePoint1)
basePoint2.setName('elo')
#The possible starting states for the SCP
extraConditional=["( l | o )"]
extraConditionalAsLogic = scpNotationParser.stringListToBasicLogic(extraConditional)
basePoint2['Delta']=basePoint2['Delta']+extraConditionalAsLogic
basePoint2['V']=basePoint2['V']+[o]
basePoint1['R']={'delete':["o","e"]}
basePoint2['R']={'delete':["o","e"]}
#abducibs= []
#abducibs = [ '( o <- T )']
#abducibs = [ '( l <- T )', '( l <- F )','( o <- T )', '( o <- F )']
#logAbducibs =  scpNotationParser.stringListToBasicLogic(abducibs)
#basePoint1['R']={'abducibles':logAbducibs}
#basePoint2['R']={'abducibles':logAbducibs}

#Create the first state point
statePoints=[basePoint1,basePoint2]
s_i=statePoints

#The set of possible states
M=[ADDAB,SEMANTIC,WC]
#The external evaluation function
f=f_suppression_studyLate
#The desired output of the external evaluation function
gamma={'el':'She will study late in the library','elo':'We are uncertain if she will study late in the library'}

#The SCP task which states what is required from a solution SCP or realised SCP
task = SCP_Task.SCP_Task(s_i,M,f,gamma)    






#test ctm
c = CTM.CTM()
c.setSi(s_i)
c.appendm(ADDAB)
#c.appendm(ABDUCIBLES)
c.appendm(DELETE)
c.appendm(WC)

c.appendm(SEMANTIC)

predictions = f(c)
print ('predictions: ', predictions)


print ("Lenient Interp")
print (StatePointOperations.predictionsModelsGamma_lenient(predictions,gamma))
print("Strict Interp")
print (StatePointOperations.predictionsModelsGamma_strict(predictions,gamma))

#print (c.evaluate())
"""
searchResult = task.deNoveSearch()
print ("\nSEARCH RESULTS:")
print(searchResult)
print("\n")

result1=searchResult[0]

print ("RESULT 1: IS\n",result1)
"""
"""

"""

def standardSuppression():
    print ("===========================================================")
    print ("================STANDARD SUPPRESSION========================")
    print ("===========================================================")
    #The epistemic state for the initial state of a reasoner who only knows
    #conditional ( l | e )
    basePoint1=epistemicState.epistemicState('el')
    delta1=["( l | e )"]
    S1 = ["( e <- T )"]
    delta1AsLogic = scpNotationParser.stringListToBasicLogic(delta1)
    S1AsLogic = scpNotationParser.stringListToBasicLogic(S1)
    basePoint1['S']=S1AsLogic
    basePoint1['Delta']=delta1AsLogic
    basePoint1['V']=[e,l]
    
    #The elo case expressed as the addition of information to the el case
    basePoint2=copy.deepcopy(basePoint1)
    basePoint2.setName('elo')
    #The possible starting states for the SCP
    extraConditional=["( l | o )"]
    extraConditionalAsLogic = scpNotationParser.stringListToBasicLogic(extraConditional)
    basePoint2['Delta']=basePoint2['Delta']+extraConditionalAsLogic
    basePoint2['V']=basePoint2['V']+[o]
    
    #Create the first state point
    statePoints=[basePoint1,basePoint2]
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
    basePoint1=epistemicState.epistemicState('el')
    delta1=["( l | e )"]
    S1 = ["( e <- T )"]
    delta1AsLogic = scpNotationParser.stringListToBasicLogic(delta1)
    S1AsLogic = scpNotationParser.stringListToBasicLogic(S1)
    basePoint1['S']=S1AsLogic
    basePoint1['Delta']=delta1AsLogic
    basePoint1['V']=[e,l]
    
    
    #The elo case expressed as the addition of information to the el case
    basePoint2=copy.deepcopy(basePoint1)
    basePoint2.setName('elo')
    #The possible starting states for the SCP
    extraConditional=["( l | o )"]
    extraConditionalAsLogic = scpNotationParser.stringListToBasicLogic(extraConditional)
    basePoint2['Delta']=basePoint2['Delta']+extraConditionalAsLogic
    basePoint2['V']=basePoint2['V']+[o]
    


    #abducibs = [ '( l <- T )', '( l <- F )','( o <- T )', '( o <- F )']
    abducibs = ['( o <- T )', '( o <- F )']
    logAbducibs =  scpNotationParser.stringListToBasicLogic(abducibs)
    basePoint1['R']={'abducibles':logAbducibs}
    basePoint2['R']={'abducibles':logAbducibs}
    #Create the first state point
    statePoints=[basePoint1,basePoint2]
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
    basePoint1=epistemicState.epistemicState('el')
    delta1=["( l | e )"]
    S1 = ["( e <- T )"]
    delta1AsLogic = scpNotationParser.stringListToBasicLogic(delta1)
    S1AsLogic = scpNotationParser.stringListToBasicLogic(S1)
    basePoint1['S']=S1AsLogic
    basePoint1['Delta']=delta1AsLogic
    basePoint1['V']=[e,l]
    
    
    #The elo case expressed as the addition of information to the el case
    basePoint2=copy.deepcopy(basePoint1)
    basePoint2.setName('elo')
    #The possible starting states for the SCP
    extraConditional=["( l | o )"]
    extraConditionalAsLogic = scpNotationParser.stringListToBasicLogic(extraConditional)
    basePoint2['Delta']=basePoint2['Delta']+extraConditionalAsLogic
    basePoint2['V']=basePoint2['V']+[o]
    basePoint1['R']={'delete':["o","e"]}
    basePoint2['R']={'delete':["o","e"]}
    #abducibs= []
    #abducibs = [ '( o <- T )']
    #abducibs = [ '( l <- T )', '( l <- F )','( o <- T )', '( o <- F )']
    #logAbducibs =  scpNotationParser.stringListToBasicLogic(abducibs)
    #basePoint1['R']={'abducibles':logAbducibs}
    #basePoint2['R']={'abducibles':logAbducibs}
    
    #Create the first state point
    statePoints=[basePoint1,basePoint2]
    s_i=statePoints
    
    #The external evaluation function
    f=f_suppression_studyLate
    #The desired output of the external evaluation function
    gamma={'el':'She will study late in the library','elo':'We are uncertain if she will study late in the library'}

    #test ctm
    c = CTM.CTM()
    c.setSi(s_i)
    c.appendm(ADDAB)
    #c.appendm(ABDUCIBLES)
    c.appendm(DELETE)
    c.appendm(WC)
    c.appendm(SEMANTIC)

    predictions = f(c)
    print ('predictions: ', predictions)
    print ("Lenient Interp")
    print (StatePointOperations.predictionsModelsGamma_lenient(predictions,gamma))
    print("Strict Interp")
    print (StatePointOperations.predictionsModelsGamma_strict(predictions,gamma))
   
    
#print (standardSuppression())
abducibleSuppression()
#print (deletionSuppression())

































