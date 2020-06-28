# -*- coding: utf-8 -*-
"""
Created on Mon Jan 20 06:41:34 2020

This file includes several examples of implementations of the Wason Selection Task as described in the thesis
All examples make use of the SCP framework.
@author: Axel
"""

folderStructure=True
if folderStructure:
    import sys
    sys.path.append("/SCPFramework") 
    from SCPFramework import SCP_Task
    from SCPFramework import scpNotationParser
    from SCPFramework import CTM
    from SCPFramework import CognitiveOperation
    from SCPFramework import basicLogic
    from SCPFramework import epistemicState
    from SCPFramework import StatePointOperations
else:
    import SCP_Task
    import scpNotationParser
    import CTM
    import CognitiveOperation
    import basicLogic
    import epistemicState
    import StatePointOperations


#INSTANTIATE EACH <cognitiveOperation> object which might be used later
ADDAB = CognitiveOperation.m_addAB()
WC = CognitiveOperation.m_wc()
SEMANTIC = CognitiveOperation.m_semantic()
ABDUCIBLES=CognitiveOperation.m_addAbducibles(maxLength=2)
WCS = CognitiveOperation.m_wcs()

"""
==================================================================================================
==========================================TURN FUNCTION===========================================
"""  
#corresponds to f_WST in the thesis
def f_turnFunction(pi,observations= ['D','K','3','7']):
    decisions={}
    for obs in observations:
        for i in obs:
            decisions[obs]=f_turn(pi,obs)     
    return decisions
#corresponds to f_WST^pref in the thesis
def f_turnFunction_prefDoNoTurn(pi,observations= ['D','K','3','7']):
    #prefer to turn the card if any realised SCP would cause the card to be turned
    prefDontTurn = {'D':'Do Not Turn','K':'Do Not Turn','3':'Do Not Turn','7':'Do Not Turn'}  
    return pref_f(f_turnFunction(pi,observations= ['D','K','3','7']),prefDontTurn)    
        
#Determine if pi explains a specific observation      
def f_turn(pi,observation):

    finalStructures=pi.evaluate()
    finalStates=StatePointOperations.flattenStatePoint(finalStructures)
    
    if not isinstance(finalStates,list):
        finalStates=[finalStates]

    conditional = scpNotationParser.stringListToBasicLogic(["( ( 3 | D ) or ( D' | 7 ) )"])
    # we are willing to turn the card if either the (3 | D) or the contrapositive case ( D' | 7 ) holds
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
        #print ("epi is ", epi)
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
        #print ("mini is : ", mini)
        for cond in conditional:
            #print (cond, "Evaluates to ", cond.evaluate())
            if cond.evaluate()==None:
                
                #print ("evaluation was ", cond.evaluate())
                allCondApplicable = False   
        #print ("cond is ",cond)
                
        if allCondApplicable:
            turns.append('Turn Card')
            #print ("1")
        else:
            turns.append('Do Not Turn')
            #print("2")
                    
    return turns
#a preference function which will returned the prefered response if it is one of the response
#and all the other responses otherwise
def pref_f(responses,pref):
    preferedResonses={}
    for card in pref:
        if pref[card] in responses[card]:
            preferedResonses[card]=pref[card]
        else:
            preferedResonses[card]=responses[card]
    return preferedResonses

#turn an scp list into a list of strings
def strSCPLi(mu):    
    f_aliases={f_turnFunction:"f_WST",f_turnFunction_prefDoNoTurn:"f_pref"}
    scps=[]
    for s in mu:
        for al in f_aliases:
            if s[1]==al:
                scps.append((s[0].__repr__(), f_aliases[al]))
    return scps
            
"""
==================================================================================================
=============================================CREATE Si============================================
"""  
#creates the initial state point with only the conditional (3|D)
def create_si_noContra():
    #define the initial atomic name in the WCS: one for each observed card
    #these atoms have value None
    D    = basicLogic.atom('D')
    K     = basicLogic.atom('K')
    three = basicLogic.atom('3')
    seven = basicLogic.atom('7')
    #this is the atom which means NOT (D)
    Dprime = basicLogic.atom("D'")    

    #create an epistemic state containing the known facts and conditionals
    basePointNoContra=epistemicState.epistemicState('WST')
    #the set of conditionals without the contraposition rule
    delta_nocontra=["( 3 | D )"]
    #the set of conditionals as a set of <basicLogic> clauses
    deltaAsLogic = scpNotationParser.stringListToBasicLogic(delta_nocontra)
    #the set of facts known
    S_nocontra = [""]
    #the set of known facts as <basicLogic>
    SAsLogic = scpNotationParser.stringListToBasicLogic(S_nocontra)
    #the set of abducibles, any subset of which might be an explanation
    abducibs = ['( D <- T )', '( D <- F )', '( K <- T )', '( K <- F )', 
                '( 3 <- T )', '( 3 <- F )', '( 7 <- T )', '( 7 <- F )']
    abducibs = ['( D <- T )',  '( K <- T )', '( 3 <- T )', '( 7 <- T )']
    #transform the set of abducibles to a set of <basicLogic> clauses
    logAbducibs =  scpNotationParser.stringListToBasicLogic(abducibs)

    #set the structural variables of the only epistemic state in the intial state point
    basePointNoContra['S']=SAsLogic
    basePointNoContra['Delta']=deltaAsLogic
    basePointNoContra['V']=[D, K, three, seven, Dprime]
    basePointNoContra['R']={'abducibles':logAbducibs}   
    return [basePointNoContra]

#creates the initial state point wit the conditional (3|D) AND (D'|7)
def create_si_contra():
    #define the initial atomic name in the WCS: one for each observed card
    #these atoms have value None
    D    = basicLogic.atom('D')
    K     = basicLogic.atom('K')
    three = basicLogic.atom('3')
    seven = basicLogic.atom('7')
    #this is the atom which means NOT (D)
    Dprime = basicLogic.atom("D'")    

    #create an epistemic state containing the known facts and conditionals
    basePointContra=epistemicState.epistemicState('WST')
    #the set of conditionals with the contraposition rule
    delta_contra=["( 3 | D )"," ( D' | 7 ) "]
    #the set of conditionals as a set of <basicLogic> clauses
    deltaAsLogic = scpNotationParser.stringListToBasicLogic(delta_contra)
    #the set of facts known, this prevents negative heads in rules
    S_contra = ["( ( D ) <- ( !  D'  ) )"]
    #the set of known facts as <basicLogic>
    SAsLogic = scpNotationParser.stringListToBasicLogic(S_contra)
    #the set of abducibles, any subset of which might be an explanation
    abducibs = ['( D <- T )', '( D <- F )', '( K <- T )', '( K <- F )', 
                '( 3 <- T )', '( 3 <- F )', '( 7 <- T )', '( 7 <- F )']
    abducibs = ['( D <- T )',  '( K <- T )', '( 3 <- T )', '( 7 <- T )']
    #transform the set of abducibles to a set of <basicLogic> clauses
    logAbducibs =  scpNotationParser.stringListToBasicLogic(abducibs)

    #set the structural variables of the only epistemic state in the intial state point
    basePointContra['S']=SAsLogic
    basePointContra['Delta']=deltaAsLogic
    basePointContra['V']=[D, K, three, seven, Dprime]
    basePointContra['R']={'abducibles':logAbducibs}   
    return [basePointContra]



"""
==================================================================================================
=============================================SCP SEARCH===========================================
"""    
#The most common case of the WST, where the cards D and 3 are turned
def mu_D3 ():
    print ("")
    print ("Searching through SCP space to find: D, 3...")
    #create initial base point which has only a single epistemic state in it
    s_i=create_si_noContra()
    
    #the set of cognitive operations which we believe might model this case of the WST
    M=[ABDUCIBLES, ADDAB, WCS]
    #The final state dependent external evaluation function
    f=f_turnFunction
    #the turn responses which would we would like to achieve
    gamma_D3={'D':'Turn Card','K':'Do Not Turn','3':'Turn Card','7':'Do Not Turn'}    
    
    #The SCP task which states what is required from a solution SCP or realised SCP
    task_D3 = SCP_Task.SCP_Task(s_i,M,f,gamma_D3)   
    
    searchRes = task_D3.deNoveSearch(depth = 3, searchType="satisfying")
    
    print ("search results are ", strSCPLi(searchRes))
    return (searchRes)
    
    
#The a case of the WST where only D is turned
def mu_D ():
    print ("")
    print ("Searching through SCP space to find: D...")
    #create initial base point which has only a single epistemic state in it
    s_i=create_si_noContra()
    
    #the set of cognitive operations which we believe might model this case of the WST
    M=[ABDUCIBLES, ADDAB, WCS]
    #The final state dependent external evaluation function
    f=f_turnFunction_prefDoNoTurn
    #the turn responses which would we would like to achieve
    gamma_D={'D':'Turn Card','K':'Do Not Turn','3':'Do Not Turn','7':'Do Not Turn'}  

    #The SCP task which states what is required from a solution SCP or realised SCP
    task_D = SCP_Task.SCP_Task(s_i,M,f,gamma_D)   
    
    searchRes = task_D.deNoveSearch(depth = 3, searchType="satisfying")
    print ("search results are ", strSCPLi(searchRes))
    return searchRes

#The classical logic response to the WST, turning the cards D and 7
def mu_D7 ():
    print ("")
    print ("Searching through SCP space to find: D, 7...")
    #create initial base point which has only a single epistemic state in it
    s_i=create_si_contra()
    
    #the set of cognitive operations which we believe might model this case of the WST
    M=[ABDUCIBLES, ADDAB, WCS]
    #The final state dependent external evaluation function
    f=f_turnFunction_prefDoNoTurn

    #the turn responses which would we would like to achieve
    gamma_D7={'D':'Turn Card','K':'Do Not Turn','3':'Do Not Turn','7':'Turn Card'}  

    #The SCP task which states what is required from a solution SCP or realised SCP
    task_D7 = SCP_Task.SCP_Task(s_i,M,f,gamma_D7)   
    
    searchRes = task_D7.deNoveSearch(depth = 3, searchType="satisfying")
    print ("search results are ", strSCPLi(searchRes))
    return searchRes

#The individual case of the WST, where the cards D, 3, and 7 are turned
def mu_D37 ():
    print ("")
    print ("Searching through SCP space to find: D, 3, 7...")
    #create initial base point which has only a single epistemic state in it
    s_i=create_si_contra()
    
    #the set of cognitive operations which we believe might model this case of the WST
    M=[ABDUCIBLES, ADDAB, WCS]
    #The final state dependent external evaluation function
    f=f_turnFunction
    #the turn responses which would we would like to achieve
    gamma_D37={'D':'Turn Card','K':'Do Not Turn','3':'Turn Card','7':'Turn Card'}    
    
    #The SCP task which states what is required from a solution SCP or realised SCP
    task_D37 = SCP_Task.SCP_Task(s_i,M,f,gamma_D37)   
    
    searchRes = task_D37.deNoveSearch(depth = 3, searchType="satisfying")
    print ("search results are ", strSCPLi(searchRes))
    return searchRes
"""
==================================================================================================
===========================================SCP EXAMPLES===========================================
"""  
#The most common case of the WST, where the cards D and 3 are turned
#Shown for mu=(si => addAB => addExp => WC => semantic,f_turn)
def mu_D3_example ():
    print ("\n>>Example for SCP that turns the cards: D, 3...")
    #create initial base point which has only a single epistemic state in it
    s_i=create_si_noContra()
    #The final state dependent external evaluation function
    f=f_turnFunction
    #the turn responses which would we would like to achieve
    gamma_D3={'D':'Turn Card','K':'Do Not Turn','3':'Turn Card','7':'Do Not Turn'}     
    
    c = CTM.CTM()
    c.setSi(s_i)
    c.appendm(ADDAB)
    c.appendm(ABDUCIBLES)
    c.appendm(WC)
    c.appendm(SEMANTIC)

    #the set of possible observations which might need to be explained to see if we should 
    # turn a card
    observations = ['D','K','3','7']
    
    #use the turn function to evaluate the ctm and see if the card should be turned
    predictions=f(c,observations)   
    
    print ("First state point is ", s_i)
    print ("Example SCP is ", c.__repr__())
    #to print all final states uncomment the next line
    #print("Final State point is : ", c.evaluate())

    
    
    #the decisions made by f() for the SCP (c,f())
    print ("Responses: ",predictions)
    #print True if mu|=gamma_D3
    print ("Lenient: mu|=gamma_D3 :", StatePointOperations.predictionsModelsGamma_lenient(predictions,gamma_D3))
    print ("Strict:  mu|=gamma_D3 :", StatePointOperations.predictionsModelsGamma_strict(predictions,gamma_D3))
    
    
#The individual case of the WST, where the cards D, 3, and 7 are turned
#Shown for mu=(si => addAB => addExp => WC => semantic,f_turn)
def mu_D37_example ():
    print ("\n>>Example for SCP that turns the cards: D, 3, 7...")
    #create initial base point which has only a single epistemic state in it
    s_i=create_si_contra()
    #The final state dependent external evaluation function
    f=f_turnFunction
    #the turn responses which would we would like to achieve
    gamma_D37={'D':'Turn Card','K':'Do Not Turn','3':'Turn Card','7':'Turn Card'}    
    
    #This is a test SCP mu=(c,f()) which is known to work
    c = CTM.CTM()
    c.setSi(s_i)
    c.appendm(ADDAB)
    c.appendm(ABDUCIBLES)
    c.appendm(WC)
    c.appendm(SEMANTIC)

    #the set of possible observations which might need to be explained to see if we should 
    # turn a card
    observations = ['D','K','3','7']
    
    #use the turn function to evaluate the ctm and see if the card should be turned
    predictions=f(c,observations)    
    
    print ("First state point is ", s_i)
    print ("Example SCP is ", c.__repr__())
    #to print all final states uncomment the next line
    #print("Final State point is : ", c.evaluate())
    
    
    #the decisions made by f() for the SCP (c,f())
    print ("Responses: ",predictions)

    #print True if mu|=gamma_D37
    print ("Lenient: mu|=gamma_D37 :", StatePointOperations.predictionsModelsGamma_lenient(predictions,gamma_D37))
    print ("Strict:  mu|=gamma_D37 :", StatePointOperations.predictionsModelsGamma_strict(predictions,gamma_D37))
    
#The classical logic response to the WST, turning the cards D and 7
#Shown for mu=(si => addAB => addExp => WC => semantic,f_turn)
def mu_D7_example ():
    print ("\n>>Example for SCP that turns the cards: D, 7...")
    #create initial base point which has only a single epistemic state in it
    s_i=create_si_contra()

    #The final state dependent external evaluation function
    f=f_turnFunction_prefDoNoTurn

    #the turn responses which would we would like to achieve
    gamma_D7={'D':'Turn Card','K':'Do Not Turn','3':'Do Not Turn','7':'Turn Card'}   
    
    #This is a test SCP mu=(c,f()) which is known to work
    c = CTM.CTM()
    c.setSi(s_i)
    c.appendm(ADDAB)
    c.appendm(ABDUCIBLES)
    c.appendm(WC)
    c.appendm(SEMANTIC)

    #the set of possible observations which might need to be explained to see if we should 
    # turn a card
    observations = ['D','K','3','7']
    
    #use the turn function to evaluate the ctm and see if the card should be turned
    # we prefer the 'Do Not Turn' response in this case
    predictions=f(c,observations)
    
    
    print ("First state point is ", s_i)
    print ("Example SCP is ", c.__repr__())
    #to print all final states uncomment the next line
    #print("Final State point is : ", c.evaluate())
    
    #the decisions made by f() for the SCP (c,f())
    print ("Responses: ",predictions)
    #print True if mu|=gamma_D3
    print ("Lenient: mu|=gamma_D7 :", StatePointOperations.predictionsModelsGamma_lenient(predictions,gamma_D7))
    print ("Strict:  mu|=gamma_D7 :", StatePointOperations.predictionsModelsGamma_strict(predictions,gamma_D7))

    
 
#The a case of the WST where only D is turned
#Shown for mu=(si => addAB => addExp => WC => semantic,f_turn)  
def mu_D_example ():
    print ("\n>>Example for SCP that turns the card: D...")
    #create initial base point which has only a single epistemic state in it
    s_i=create_si_noContra()
    #The final state dependent external evaluation function
    f=f_turnFunction_prefDoNoTurn
    #the turn responses which would we would like to achieve
    gamma_D={'D':'Turn Card','K':'Do Not Turn','3':'Do Not Turn','7':'Do Not Turn'}  
    
    #This is a test SCP mu=(c,f()) which is known to work
    c = CTM.CTM()
    c.setSi(s_i)
    c.appendm(ADDAB)
    c.appendm(ABDUCIBLES)
    c.appendm(WC)
    c.appendm(SEMANTIC)

    #the set of possible observations which might need to be explained to see if we should 
    # turn a card
    observations = ['D','K','3','7']
    
    #use the turn function to evaluate the ctm and see if the card should be turned
    # we prefer the 'Do Not Turn' response in this case
    predictions=f(c,observations)

    print ("First state point is ", s_i)
    print ("Example SCP is ", c.__repr__())
    #to print all final states uncomment the next line
    #print("Final State point is : ", c.evaluate())
    
    
    
    #the decisions made by f() for the SCP (c,f())
    print ("Responses: ",predictions)
    #print True if mu|=gamma_D3
    print ("Lenient: mu|=gamma_D :", StatePointOperations.predictionsModelsGamma_lenient(predictions,gamma_D))
    print ("Strict:  mu|=gamma_D :", StatePointOperations.predictionsModelsGamma_strict(predictions,gamma_D))

#active search to find SCPs which model results
#creates plans and runs search on these plans
mu_D3()
mu_D37()
mu_D()
mu_D7()


#examples of an scp for each case of the WST, see code for comments.
#these searches are fairly slow, but very comprehensive.
#the <m_addabducibles> operation can occur multiple times and introduces a vary large branching factor
#if not intentionally limitted
mu_D3_example()
mu_D37_example()
mu_D_example()
mu_D7_example()
































