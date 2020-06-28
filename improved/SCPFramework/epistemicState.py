# -*- coding: utf-8 -*-
"""
Created on Tue Feb 11 09:47:35 2020

@author: Axel
"""

folderStructure=True
if folderStructure:
    import sys
    sys.path.append("/SCPFramework") 
    from SCPFramework import basicLogic
else:
    import basicLogic
"""
The core data structure of the SCP frameworks. Every <cognitiveOperation> takes an epistemic state
as input and produces a set of epistemic states (a state point) as output.
An epistemic state is a collection of structural variables which are lists or task-specific 
properties
"""
class epistemicState (object):
    def __init__(self, name=""):
        self.name=name
        self.structuralVariables={}
    def setName(self,name):
        self.name=name
    """
    @return the names of every structural variable in this <epistemicState>
    """
    def getStructuralVariables (self):
        return list(self.structuralVariables.keys())
    def getName(self):
        return self.name
    def __str__(self):
        structVarsAsString = ''
        for i in self.structuralVariables:
            structVarsAsString=structVarsAsString+str(i)+':: '+str(self.structuralVariables[i])+"\n"
        return "\n===>" + self.name + "<===\n" + structVarsAsString
    def __repr__(self):
        return self.__str__()
    def __hash__(self):
        return hash(self.__repr__())
    def __eq__(self, other):
        if isinstance(other, epistemicState):
            return self.__str__() == other.__str__()
        else:
            return False
    """
    Allows indexing by structuralVariable names
    """
    def __getitem__(self, key):
        if key in self.structuralVariables:
            return self.structuralVariables[key]
        else:
               print ("Invalid key!")
    """
    Allows setting of structuralVariables (including creation) by key
    """
    def __setitem__(self,key, value):
        self.structuralVariables[key]=value
    """
    @return the set of all atoms occuring in all structural variables
    """
    def getAtomsInStructuralVariables(self,li):
        ats = []
        for l in li:
            for r in self[l]:
                ats=ats+r.getAtoms()
        atsWithGroundTruths = list(dict.fromkeys(ats))
        return [atm for atm in atsWithGroundTruths if not basicLogic.isGroundAtom(atm)]
    """
    @return the name string names of each atom in the SCP
    """
    def getAtomNamesInStructuralVariables(self,li):
        return [atm.getName() for atm in self.getAtomsInStructuralVariables(li)] 












