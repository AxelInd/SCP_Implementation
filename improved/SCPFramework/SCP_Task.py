# -*- coding: utf-8 -*-
"""
Created on Sat Jun 13 09:09:55 2020

@author: Axel
"""

import copy
folderStructure=True
if folderStructure:
    import sys
    sys.path.append("/SCPFramework") 
    from SCPFramework import scpError
    from SCPFramework import StatePointOperations
    from SCPFramework import CTM
else:  
    import scpError
    import StatePointOperations
    import CTM


"""
The <SCP_Task> defines the problem space for the cognitive task to be modelled
It consists of four (4) parts:
    1) s_i: the initial state point (containing epistemic states)
    2) M: the set of cognitive operations which are considered allowable in this task domain
    3) f: the external evaluation function, is a pointer to a user-defined function
    4) gamma: the goal output of <f> which the SCP will attempt to replicate
From the SCP Task, SCPs that model the task are generated
"""
class SCP_Task (object):
    def __init__(self,si=[],M=[],f=None,gamma=[]):
        self.si=si
        self.M=M
        self.f=f
        self.gamma=gamma


    """
    ------------------------------------------------------------------------------
    --------------------------GETTERS AND SETTERS----------------------------------
    ------------------------------------------------------------------------------
    """
    def setSi(self, new_si):
        self.si=new_si
    def getSi(self):
        return self.si
    def setM(self, new_M):
        self.M=new_M
    def getM(self):
        return self.M
    def addm(self,new_m):
        self.M.append(new_m)
    def addmList(self, m_list):
        for m in m_list:
            self.addm(m)
    def setF(self, new_f):
        self.f=new_f
    def getF(self):
        return self.f
    def setGamma(self, new_gamma):
        self.gamma=new_gamma
    def getGamma(self):
        return self.gamma
    def evaluate(self):
        return self.f(self.M)
    """
    Breadth-first search through SCP Space for SCPs m=(<ctm>,<f>) for which f(ctm)|=gamma
    used to generate SCPs.
    """
    def deNoveSearch(self, depth = 3, searchType="satisfying"):
        searchTypes={"exhaustive":self.s_exhaustive, "satisfying":self.s_satisfying}
        firstCTM = CTM.CTM()
        firstCTM.si = self.si
        
        ctms = firstCTM
        results=[]
        for i in range (0, depth+1):
            results += self.dns(ctms, i)
        results = searchTypes[searchType](results)
        
        return results

    def dns (self, ctm, depth):
        if depth == 0:
            return [ctm]
        new_ctms=[]
        for m in self.M:
            n = copy.deepcopy(ctm)
            n.appendm(m)
            new_ctms.append(n)
        toKeep=[]
        for ctm in new_ctms:
            toKeep= toKeep + self.dns(ctm,depth-1)
        return toKeep
    """
    Every SCP in SCP space is considered a valid SCP
    """
    def s_exhaustive(self, results):
        return StatePointOperations.CTMtoSCP(results,self.f)   
    """
    Only SCPs in the SCP space which meet the goal gamma are considered valid
    """
    def s_satisfying(self, results):
        satisfyingResults=[]
        for result in results:
            #print ("result is ",result)
            #print (self.f(result))
            predModelsGamma=StatePointOperations.predictionsModelsGamma_lenient(self.f(result),self.gamma)
            if predModelsGamma:
                satisfyingResults.append(result)
        return StatePointOperations.CTMtoSCP(satisfyingResults,self.f)    

        
    
    
    
    
    
    
    
    
    
    
    
    
    

        