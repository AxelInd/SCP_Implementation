# -*- coding: utf-8 -*-
"""
Created on Mon Feb 17 08:59:41 2020

@author: Axel
"""
import scp
import basicLogic
import epistemicState
import complexOperation

comp_def_eval = complexOperation.complexOperation_default_drawConclusions()
def unit_tweetyAndChilly ():
    #create the two birds as individual scps
    tweety = scp.scp(epistemicStateType="dl")
    chilly = scp.scp(epistemicStateType="dl")
    
    #variables
    flies = basicLogic.atom('flies')
    bird = basicLogic.atom('bird')  
    
    notflies = basicLogic.operator_monotonic_negation(flies)
    #the only inference rule
    rule1 = basicLogic.operator_tritonic_defaultRule(bird,[flies],flies)
    
    fact_bird = basicLogic.operator_bitonic_implication(basicLogic.TRUE, bird)
    factNotFlies = basicLogic.operator_bitonic_implication(basicLogic.TRUE, notflies)
    #the set of concrete rules
    W_tweety=[fact_bird]
    W_chilly=[fact_bird,factNotFlies]
    #in this case both tweety and chilly share the same inference rules
    D = [rule1]
    V = [flies,bird]
    #create wteety
    tweety.addDList(D)
    tweety.addVList(V)
    tweety.addWList(W_tweety)
    #create chilly
    chilly.addDList(D)
    chilly.addVList(V)
    chilly.addWList(W_chilly)
    #add the complex operator for evaluating default rules
    tweety.addNext(comp_def_eval)
    chilly.addNext(comp_def_eval)
    print ("<<<<<<<<TWEETY>>>>>>>>>>")
    print (tweety.evaluate())
    
    
    print (chilly.evaluate())

def unit_quakersRepublicans():
    dick = scp.scp(epistemicStateType="dl")
    
    republican = basicLogic.atom('republican')
    quaker = basicLogic.atom('quaker')
    pacifist = basicLogic.atom('pacifist')
    
    factRepublican = basicLogic.operator_bitonic_implication(basicLogic.TRUE, republican)
    factQuaker = basicLogic.operator_bitonic_implication(basicLogic.TRUE, quaker)
    
    notPacifist = basicLogic.operator_monotonic_negation(pacifist)
    #republicans are usually not pacifists
    rule1 = basicLogic.operator_tritonic_defaultRule(republican,[notPacifist],notPacifist)
    #quakers are usually pacifists
    rule2 = basicLogic.operator_tritonic_defaultRule(quaker,[pacifist],pacifist)
    
    D = [rule1,rule2]
    W = [factRepublican,factQuaker]
    V = [republican,quaker,pacifist]
    
    dick.addDList(D)
    dick.addWList(W)
    dick.addVList(V)
    
    dick.addNext(comp_def_eval)
    
    print ("<<<<<<<<DICK>>>>>>>>>>")
    print (dick.evaluate())

def unit_yuvalOnions():
    yuval = scp.scp(epistemicStateType="dl")
    eatonionSoup = basicLogic.atom("eatOnionSoup")
    loveEating= basicLogic.atom("loveEating")
    eatOnions=basicLogic.atom("eatOnions")
    brushTeeth=basicLogic.atom("brushTeeth")
    careForHygiene=basicLogic.atom("careForHygiene")
    
    dontEatOnions=basicLogic.operator_monotonic_negation(eatOnions)
    
    rule1=basicLogic.operator_tritonic_defaultRule(eatonionSoup,[eatOnions],eatOnions)
    rule2=basicLogic.operator_tritonic_defaultRule(eatonionSoup,[loveEating],loveEating)
    rule3=basicLogic.operator_tritonic_defaultRule(loveEating,[brushTeeth],brushTeeth)
    rule4=basicLogic.operator_tritonic_defaultRule(brushTeeth,[careForHygiene],careForHygiene)
    rule5=basicLogic.operator_tritonic_defaultRule(careForHygiene,[dontEatOnions],dontEatOnions)
    
    factEatsOnionSoup = basicLogic.operator_bitonic_implication(basicLogic.TRUE,eatonionSoup)
    
    D = [rule1,rule2,rule3,rule4,rule5]
    W = [factEatsOnionSoup]
    V =  [eatonionSoup, loveEating, eatOnions, brushTeeth, careForHygiene]
    
    yuval.addDList(D)
    yuval.addVList(V)
    yuval.addWList(W)
    
    yuval.addNext(comp_def_eval)
    
    print ("<<<<<<<<YUVAL>>>>>>>>>>")
    
    print (yuval.evaluate())    
unit_tweetyAndChilly()
unit_quakersRepublicans()
unit_yuvalOnions()



























