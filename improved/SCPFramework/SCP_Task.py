# -*- coding: utf-8 -*-
"""
Created on Sat Jun 13 09:09:55 2020

@author: Axel
"""

import sys
sys.path.append("/SCPFramework") 
import copy
#an implementation of 3-valued logic
#used to deepcopy complex objects
from SCPFramework import scpError
from SCPFramework import StatePointOperations
from SCPFramework import CTM

#used to create complex epistemic actions in the seuqence
#used to throw exceptions for improper use


class SCP_Task (object):
    def __init__(self,si=[],M=[],f=[],gamma=[]):
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
    def deNoveSearch(self, depth = 3, searchType="satisfying"):
        searchTypes={"exhaustive":self.s_exhaustive, "satisfying":self.s_satisfying}
        firstCTM = CTM.CTM()
        firstCTM.si = self.si
        
        ctms = firstCTM
        results = self.dns(ctms, depth)
        
        
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
    def s_exhaustive(self, results):
        return StatePointOperations.CTMtoSCP(results,self.f)   
        
    def s_satisfying(self, results):
        satisfyingResults=[]
        for result in results:
            #print ("result is ",result)
            #print (self.f(result))
            if self.gamma in self.f(result):
                satisfyingResults.append(result)
        return StatePointOperations.CTMtoSCP(satisfyingResults,self.f)    

        
    
    
    
    
    
    
    
    
    
    
    
    
    

        