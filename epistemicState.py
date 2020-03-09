# -*- coding: utf-8 -*-
"""
Created on Tue Feb 11 09:47:35 2020

@author: Axel
"""
import basicLogic
import copy
class epistemicState (object):
    def __init__(self):
        print ("epistemic State Created")
    def __str__(self):
        return "ABSTRACT"
    def __repr__(self):
        return self.__str__()
    def __hash__(self):
        return hash(self.__repr__())
    def __eq__(self, other):
        if isinstance(other, epistemicState):
            return self.__str__() == other.__str__()
        else:
            return False
        
class epistemicState_weakCompletion (epistemicState):
    def __init__(self):
        self.v=[]
        self.kb=[]
        
    def addKnowledge (self, knowledge):
        #still needs checks for duplicate knowledge
        newKnowledge=copy.deepcopy(knowledge)
        self.kb.append(newKnowledge)
        
        #remove duplicates
        self.kb=list(dict.fromkeys(self.kb))
    def addVariable (self, variable, overwrite=False):
        newVariable = copy.copy(variable)
        if not overwrite:
            for v in self.v:
                #prevents adding duplicate variables (at the start at least)
                if v.name == newVariable.name:
                    return False
        else:
            self.removeVariable(variable.name)
        self.v.append(newVariable)
        return True
    def addKnowledgeList (self, li):
        for rule in li:
            self.addKnowledge(rule)
    def addVariableList (self, li):
        for v in li:
            self.addVariable(v)
    def getKB (self):
        return self.kb
    def getV (self):
        return self.v
    def addVList(self,V, overwrite=False):
        for _v in V:
            self.addV(_v, overwrite=overwrite)
    
    def removeVariable(self,varName):
        self.v = [var for var in self.v if var.getName()!=varName]
        return True
    def setVariable (self, varName, varVal):
        for var in self.v:
            if var.getName()==varName and not var.fixed:
                var.setValue(varVal)
    def fixVariable (self, varName, fixed=True):
        for var in self.v:
            if var.getName()==varName:
                var.fixed=fixed 
    def __str__(self):
        sv = basicLogic.strVariables(self.v)
        skb = basicLogic.strKnowledge(self.kb)
        return "KB = {}\nV = {}".format(skb, sv)
    
class epistemicState_defeaultReasoning (epistemicState_weakCompletion):
    def __init__(self):
        #D: set of default rules
        self.d=[]
        epistemicState_weakCompletion.__init__(self)
    def deriveRules (self):
        return True
    def emptyD(self):
        self.d=[] 
    def getD (self):
        return self.d
    def getW (self):
        return self.kb
    def addD(self, d):
        self.d.append(d)
    def addW(self,w):
        self.kb.append(w)
        
    def addV(self,v, overwrite=False):
        for var in self.v:
            if var.name==v.name:
                if overwrite:
                    var.setValue(v.getValue())
                    """
                    if var.getValue()==None:
                        var.setValue(v.getValue())
                        return True
                    else:
                        #overwrite won't destroy an existing variable assignment
                        self.v.append(v)
                        return True
                    """
                return False
        self.v.append(v)
        return True
                
        if (v in self.v) or overwrite:
            self.v.append(v)

    def addWList(self,W):
        for _w in W:
            self.addW(_w)
    def addDList(self,D):
        for _d in D:
            self.addD(_d)
    def getV(self):
        return self.v
    def __str__(self):
        sw = self.getW()
        sd = self.getD()
        sv = self.getV()
        return "=========\nW = {} \nD = {}\nV={}\n=========".format(sw, sd, sv)
    


        
        




















