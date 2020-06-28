# -*- coding: utf-8 -*-
"""
Created on Sat Jun 22 09:45:08 2020

This file includes several examples of implementations of Reiter's Default as described in the thesis
All examples make use of the SCP framework.

The <m_default> cognitive function adds shows the results of adding each possible extension
@author: Axel
"""

folderStructure=True
if folderStructure:
    import sys
    sys.path.append("/SCPFramework") 
    
    from SCPFramework import basicLogic
    from SCPFramework import scpNotationParser as no
    from SCPFramework import epistemicState
    from SCPFramework import CTM
    from SCPFramework import CognitiveOperation as cop
else:
    import basicLogic
    import scpNotationParser as no
    import epistemicState
    import CTM
    import CognitiveOperation as cop

#the operaton on a default theory <W,D> to find extensions
DEFAULT = cop.m_default()
"""
A classical example for Reiter's default logic about whether a given bird flies, presented
propositionally
"""
def example_birds():
    W = no.stringListToBasicLogic(['( bird <- T )'])
    
    V =  no.stringListToBasicLogic(['bird', 'flies', 'penguin'])
    dParts = no.stringListToBasicLogic(['( bird <- T )', '( flies <- T ) ', '( flies <- T )'])
    default1 = basicLogic.operator_tritonic_defaultRule(dParts[0],[dParts[1]],dParts[2])
    
    dParts2 = no.stringListToBasicLogic(['( cold <- T )', '( flies <- F ) ', '( flies <- F )'])
    default2 = basicLogic.operator_tritonic_defaultRule(dParts2[0],[dParts2[1]],dParts2[2])
    D=[default1,default2]
    
    basePoint = epistemicState.epistemicState('Bird Example')
    basePoint['D']=D
    basePoint['W']=W
    basePoint['V']=V
    
    
    ctm_flight = CTM.CTM()
    ctm_flight.si=[basePoint]
    #ctm_flight.appendm(TH)
    ctm_flight.appendm(DEFAULT)
    
    
    print (ctm_flight)
    print (ctm_flight.evaluate())


#SUPPRESSION TASK
"""
The suppression task modelled with Reiter's Defult Logic as it appears in the thesis, no
suppression is observed
"""
def example_suppression():
    W = no.stringListToBasicLogic(['( e <- T )'])
    #W = no.stringListToBasicLogic([' bird ', ' penguin '])
    
    V =  no.stringListToBasicLogic(['e', 'l', 'o'])
    #dParts = no.stringListToBasicLogic(['( bird <- T )', '( penguin <- F ) ', '( flies <- T )'])
    dParts1 = no.stringListToBasicLogic(['( e <- T )', '( ab1 <- F ) ', '( l <- T )'])
    default1 = basicLogic.operator_tritonic_defaultRule(dParts1[0],[dParts1[1]],dParts1[2])
    
    dParts2 = no.stringListToBasicLogic(['( o <- T )', '( ab2 <- F ) ', '( l <- T )'])
    default2 = basicLogic.operator_tritonic_defaultRule(dParts2[0],[dParts2[1]],dParts2[2])
    
    dParts3 = no.stringListToBasicLogic(['( o <- F )', '( ab1 <- T ) ', '( ab1 <- T )'])
    default3 = basicLogic.operator_tritonic_defaultRule(dParts3[0],[dParts3[1]],dParts3[2])
    
    dParts4 = no.stringListToBasicLogic(['( e <- F )', '( ab2 <- T ) ', '( ab2 <- T )'])
    default4 = basicLogic.operator_tritonic_defaultRule(dParts4[0],[dParts4[1]],dParts4[2])
    
    D=[default1,default2,default3,default4]
    
    basePoint = epistemicState.epistemicState('Bird Example')
    basePoint['D']=D
    basePoint['W']=W
    basePoint['V']=V
    
    
    ctm_flight = CTM.CTM()
    ctm_flight.si=[basePoint]
    #ctm_flight.appendm(TH)
    ctm_flight.appendm(DEFAULT)
    
    
    print (ctm_flight)
    print (ctm_flight.evaluate())

"""
The nixon diamond, a classical example of non-monotonicity in the default logic framework. Allows
2 extensions
"""
def example_nixon():
    DEFAULT = cop.m_default()
    W = no.stringListToBasicLogic(['( quaker <- T )', ' ( republican <- T ) '])
    #W = no.stringListToBasicLogic([' bird ', ' penguin '])
    
    V =  no.stringListToBasicLogic(['quaker', 'republican', 'pacifist'])
    #dParts = no.stringListToBasicLogic(['( bird <- T )', '( penguin <- F ) ', '( flies <- T )'])
    dParts = no.stringListToBasicLogic(['( quaker <- T )', '( pacifist <- T ) ', '( pacifist <- T )'])
    default1 = basicLogic.operator_tritonic_defaultRule(dParts[0],[dParts[1]],dParts[2])
    
    dParts2 = no.stringListToBasicLogic(['( republican <- T )', '( pacifist <- F ) ', '( pacifist <- F )'])
    default2 = basicLogic.operator_tritonic_defaultRule(dParts2[0],[dParts2[1]],dParts2[2])
    D=[default1,default2]
    
    basePoint = epistemicState.epistemicState('Bird Example')
    basePoint['D']=D
    basePoint['W']=W
    basePoint['V']=V
    
    
    ctm_flight = CTM.CTM()
    ctm_flight.si=[basePoint]
    ctm_flight.appendm(DEFAULT)
    
    
    print (ctm_flight)
    print (ctm_flight.evaluate())


#Run these examples to test the <m_default> cognitive operation
example_birds()
example_suppression()
example_nixon()



















