import sys
sys.path.append("/SCPFramework") 
import copy


from SCPFramework import SCP_Task
from SCPFramework import scpNotationParser
from SCPFramework import CTM
from SCPFramework import CognitiveOperation
from SCPFramework import basicLogic
from SCPFramework import epistemicState
from SCPFramework import StatePointOperations



# Minimal subsets which verify/falsify the conditional and explain the observation o
# Are vallid iff and only 

def f_turnFunction(pi,observations):
    decisions={}
    for obs in observations:
        print ("observation is ", obs)
        for i in obs:
            decisions[obs]=f_turn(pi,obs)
            
            
    return decisions
        
        
        
def f_turn(pi,observation):

    finalStructures=pi.evaluate()
    finalStates=StatePointOperations.flattenStatePoint(finalStructures)
    
    if not isinstance(finalStates,list):
        finalStates=[finalStates]
    #print("Final states")
    #print(finalStates)
    
    #severe problem using interpetation of conditionals with de-finnetti truth table
    # @TODO how do we resolve????
    # maybe determine if the conditional CAN be falsified?
    #@TODO parser struggles with ( ( a | b) or ( c | d ) )
    conditional = scpNotationParser.stringListToBasicLogic(["( ( 3 | D ) or ( D' | 7 ) )"])
    # we are willing to turn the card if either the (3 | D) or the contrapositive case ( D' | 7 ) holds
    print ("CONDITIONAL")
    print (conditional)
    obs = scpNotationParser.stringListToBasicLogic(['( {} <- T )'.format(observation)])
    
    responses=[]
    for epi in finalStates:
        #print ("\n")
        #print (epi)
        
        basicLogic.setkbfromv(obs,epi['V'])
        
        #the conditional must be verified or falsified
        #the observation must be True
        allObsTrue=True
        for o in obs: 
            if o.evaluate()!=True:
                allObsTrue=False
        #allCondApplicable = True

        if allObsTrue:
            responses.append('observations hold')
        else:
            responses.append('observations do not')

              
        
        
            
    #now we need to find the minimal set of abducibles to turn the cards
    turnResponses=[]
    #WE PREFER MINIMAL EXPLANATIONS
    for i in range (0,len(responses)):
        if responses[i]=='observations hold':
            turnResponses.append(finalStates[i])
    minimalSubset = []
     
    for epi in turnResponses:
        print ("epi is ", epi)
        #print ("we made it here")
        #print (epi['R']['abducibles'])
        #print ("and then here")
        x = [StatePointOperations.properSubset(ot['R']['abducibles'],epi['R']['abducibles'])  for ot in turnResponses]
        #another least model is a subset of this one
        if True in x:
            pass
        else:
            minimalSubsetAsVariables=epi['V']
            minimalSubsetAsList=StatePointOperations.VtoTupleList(minimalSubsetAsVariables,ignoreNone=True)
            if minimalSubsetAsList not in minimalSubset:
                minimalSubset.append(minimalSubsetAsVariables)

    turns=[]
    for mini in minimalSubset:
        allCondApplicable=True
        #this is done later
        basicLogic.setkbfromv(conditional,mini)
        print ("mini is : ", mini)
        for cond in conditional:
            print (cond, "Evaluates to ", cond.evaluate())
            if cond.evaluate()==None:
                
                #print ("evaluation was ", cond.evaluate())
                allCondApplicable = False   
        #print ("cond is ",cond)
                
        if allCondApplicable:
            turns.append('Turn Card')
            #print ("1")
        else:
            turns.append('Do Not Turn Card')
            #print("2")
                    
    return turns

    
D = basicLogic.atom('D')
K = basicLogic.atom('K')
three = basicLogic.atom('3')
seven=basicLogic.atom('7')


Dprime = basicLogic.atom("D'")

basePointNoAbd=epistemicState.epistemicState('')
#The possible starting states for the SCP
delta_contra=["( 3 | D )"," ( D' | 7 ) "]
#delta_nocontra=["( 3 | D )"]
#delta1=["( l | e )", "( l | o )"]
#S_nocontra = [""]
S_contra = ["( ( D ) <- ( !  D'  ) )"]



#set to 8 to run all abducibles
abducibs = ['( D <- T )', '( D <- F )', '( K <- T )', '( K <- F )', '( 3 <- T )', '( 3 <- F )', '( 7 <- T )', '( 7 <- F )']
#abducibs = ['( K <- T )']
#abducibs = [ '( 7 <- T )', '( 7 <- F )']
logAbducibs =  scpNotationParser.stringListToBasicLogic(abducibs)


delta1AsLogic = scpNotationParser.stringListToBasicLogic(delta_contra)
S1AsLogic = scpNotationParser.stringListToBasicLogic(S_contra)

print (S1AsLogic)


basePointNoAbd['S']=S1AsLogic
basePointNoAbd['Delta']=delta1AsLogic
basePointNoAbd['V']=[D, K, three, seven, Dprime]
basePointNoAbd['R']={'abducibles':logAbducibs}


#Create the first state point
# K case
basePointD= copy.deepcopy(basePointNoAbd)
basePointD.setName('abducible:D')
basePointD['S'] = basePointD['S'] + (scpNotationParser.stringListToBasicLogic(['( D <- T )']))

basePointK= copy.deepcopy(basePointNoAbd)
basePointK.setName('abducible:K')
basePointK['S'] = basePointD['S'] + (scpNotationParser.stringListToBasicLogic(['( K <- T )']))

basePoint3= copy.deepcopy(basePointNoAbd)
basePoint3.setName('abducible:3')
basePoint3['S'] = basePointD['S'] + (scpNotationParser.stringListToBasicLogic(['( 3 <- T )']))


basePoint7= copy.deepcopy(basePointNoAbd)
basePoint7.setName('abducible:7')
basePoint7['S'] = basePointD['S'] + (scpNotationParser.stringListToBasicLogic(['( 7 <- T )']))


#statePoints=[basePointD,basePointK,basePoint3,basePoint7]
statePoints=[basePointNoAbd]
s_i=statePoints

#The set of possible states
M=[]
#The external evaluation function
f=f_turn
#The desired output of the external evaluation function
gamma={'D':'Turn Card','K':'Do Not Turn Card','3':'Turn Card','7':'Do Not Turn Card'}

#The SCP task which states what is required from a solution SCP or realised SCP
task = SCP_Task.SCP_Task(s_i,M,f,gamma)    


ADDAB = CognitiveOperation.m_addAB()
WC = CognitiveOperation.m_wc()
SEMANTIC = CognitiveOperation.m_semantic()
ABDUCIBLES=CognitiveOperation.m_addAbducibles(maxLength=4)

#test ctm
c = CTM.CTM()
c.setSi(s_i)
c.appendm(ADDAB)
c.appendm(ABDUCIBLES)
c.appendm(WC)
c.appendm(SEMANTIC)
#print(c)
#print(c.evaluate())



observations = ['D','K','3','7']
predictions=f_turnFunction(c,observations)
print (predictions)




print (StatePointOperations.predictionsModelsGamma_lenient(predictions,gamma))
print (StatePointOperations.predictionsModelsGamma_strict(predictions,gamma))




#test = [ "( ( A ) or ( ( X ) & ( Y ) ) )"]
#test = ["( ( 3 | D ) or ( D' | 7 ) )"]
#res = scpNotationParser.stringListToBasicLogic(test)

#print (res)






































