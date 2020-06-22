# -*- coding: utf-8 -*-
"""
Created on Sat Jun 13 09:29:03 2020

@author: Axel
"""
import sys
sys.path.append("/SCPFramework") 
import copy

from SCPFramework import epistemicState
from SCPFramework import StatePointOperations
from SCPFramework import scpError

class CTM (object):
    def __init__(self):
        self.si=None
        self.last=[]
        #partial transition model (no intial state)
        self.pCTM=[]
    #this method is not perfect and cannot handle validity when different epis in si do not have the same structure!
    def getSiStructure(self):
        structure=[]
        flattenedSi = StatePointOperations.flattenStatePoint(self.si)
        if not isinstance(flattenedSi,list):
            flattenedSi=[flattenedSi]
        #print ("FLATTENED si IS ", flattenedSi)
        for epi in flattenedSi:
            structure=structure+epi.getStructuralVariables()
        return list(dict.fromkeys(structure))
        
    def setSi(self,si):
        self.si=si
    def insertm (self, pos, m):
        self.pCTM.insert(pos,m)
    def appendm (self, m):
        self.insertm(len(self.pCTM),m)
        
    def evaluate(self, validity=["hybrid"]):
        validityTypes={"trivial":self.validity_trivial,"hybrid":self.validity_hybrid}
        currentStatePoint=self.si
        for i in range(0,len(self.pCTM)):
            valid = True
            for val in validity:
                if validityTypes[val](self.pCTM[0:i], self.pCTM[i])!=True:
                    print ("OH NOOOOOO invalid!!!!")
                    valid = False
                if not valid:
                    raise scpError.invalidCTMError()
            currentStatePoint=self.J(currentStatePoint,self.pCTM[i])
        return currentStatePoint
    @staticmethod
    def J(p,m):
        
        #if it is a base point
        if isinstance (p,epistemicState.epistemicState):
            return [CTM.J_epi(p,m)]
        #if it is only a state point
        pPrime=[]
        for sub in p:
            pPrime.append(CTM.J(sub,m))
        return pPrime
    def __getitem__(self, pos):
        if pos==0:
            return self.si
        return self.pCTM[pos-1]
    @staticmethod
    def J_epi(epi,m):
        #copy the epi so that it won't be overwritten if accessed elsewhere
        epi=copy.deepcopy(epi)
        return m.evaluateEpistemicState(epi)
        
    def __str__(self):
        s = str(self.si)
        pCTM = ""
        for i in self.pCTM:
            pCTM = pCTM + " => "+str(i)
        #return "si"+pCTM 
        return s + pCTM

    def __repr__(self):
        s = "si"
        pCTM = ""
        for i in self.pCTM:
            pCTM = pCTM + " => "+str(i)
        return s + pCTM     
    def __len__(self):
        return len(self.pCTM)+1
    
    def validity_trivial(self,m_prev, m_current):
        return True
    def validity_hybrid (self,M_prev, m_current):
        
        previousOutputStructure = self.getSiStructure()
        for m in M_prev:
            previousOutputStructure=previousOutputStructure+m.outputStructure
        #previousOutputStructure=list(dict.fromkeys(previousOutputStructure))
        #print ("Only accepting output structure of : ", previousOutputStructure)
        if set(m_current.outputStructure).issubset(set(previousOutputStructure)):
            #print (set(m_current.outputStructure), " is a subset of ", set(previousOutputStructure))
            return True
        #print (set(m_current.outputStructure), " is NOT a subset of ", set(previousOutputStructure))
        return False
    
        
    def reversepCTM(self):
        return self.pCTM[::-1]
    def NMTransformation(self):
        rev= self.reversepCTM()
        self.si=rev[0]
        self.pCTM=None
        self.pCTM=rev[1:len(rev)]
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        