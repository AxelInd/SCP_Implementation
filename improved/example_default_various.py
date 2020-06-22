# -*- coding: utf-8 -*-
"""
Created on Mon Jun 22 10:14:11 2020

@author: Axel
"""
import sys
sys.path.append("/SCPFramework") 

from SCPFramework import basicLogic
from SCPFramework import scpNotationParser as no
from SCPFramework import epistemicState
from SCPFramework import CTM
from SCPFramework import CognitiveOperation as cop


DEFAULT = cop.m_default()

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


example_birds()
example_suppression()
example_nixon()



















