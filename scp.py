# -*- coding: utf-8 -*-
"""
Created on Mon Jan 20 11:28:31 2020

THE SCP CLASS

AN SCP (SEQUENTIAL COGNITION PROCESS) IS A LINKED LIST OF COMPLEX OPERATIONS. EACH SCP BEGINS WITH AN
INITIAL STATE. NO OTHER SCP EXPLICITLY STORES KNOWLEDGE ABOUT THE KNOWLEDGE BASE OR VARIABLES ON WHICH IS WORKS.

Instead, they rely on calls to their predecessors to be passed that information. The complex actions of an SCP
are only bounded by the creativity of the researcher, and the relevence of their ideas to modelling the problem at hand.
This SCP implementation focuses on the WEAK COMPLETION SEMANTICS.

@author: Axel
"""

#an implementation of 3-valued logic
import basicLogic
#used to deepcopy complex objects
import copy
#used to create complex epistemic actions in the seuqence
import complexOperation
#used to throw exceptions for improper use
import scpError

import epistemicState

class scp (object):
    def __init__ (self, epiState1 = None, epistemicStateType="wcs"):
        #the set of complex operations possible in the scp
        self.M = []

        #the first state in the scp, should always be an instance of complexOperation_init
        self.m1 = complexOperation.complexOperation_init ()
        #the knowledge base of the first state is a pointer to the knowledge base of the scp
        switch = {"wcs": epistemicState.epistemicState_weakCompletion(), "dl": epistemicState.epistemicState_defeaultReasoning()}
        #determines the type of state to init
        if epiState1!=None:
            self.si=epiState1
        else:  
            self.si = switch[epistemicStateType]
        
        self.m1.setEpistemicState(self.si)
        

    #@TODO needs to be implemented
    def checkPrecondition ():
        print ("Checking precondition")

    """
    ADD A SET OF COMPLEX OPERATIONS TO M
    @param M: the set of complex operations to add to the scp
    """
    def addM (self, M):
        #@TODOextendToRemoveDuplicates
        for m in M:
            self.addComplexOperation(m)
            
    def getInitialVariables(self):
        return self.initialV

    """
    ADD A RULE TO THE KNOWLEDGE BASE
    @param knowledge: an basicLogic.operator rule of the form a->b or a<->b
    @return True if succesful, False otherwise
    """
    def addKnowledge (self, knowledge):
        return self.si.addKnowledge(knowledge)
    """
    REMOVE A VARIABLE FROM THE INITIAL KB OF THE SCP
    @param varname: the name of the variable to remove
    @return the list of variables without the specified variable
    """
    def removeVariable_initial (self,varname):
        newVars = []
        for var in self.initialV:
            if var.name!= varname:
                newVars.append(var)
        return newVars
    """
    ADD A VARIABLE TO THE INITIAL VARIABLES OF THE SCP
    @param variable: the atom to add
    @overwite: True if the new variable should overwrite the value of an existing variable with
    the same name in the initial variable list
    @return True if the variable is added, False otherwise
    """
    def addVariable (self, variable, overwrite=False):
        return self.si.addVariable(variable)
    def evaluate(self):
        return self.getLastOperation().evaluate()

    """
    GET A VARIABLE IF IT IS NAMED IN THE INITIAL V
    @param variableName: the string name of the variable to get
    @return the variable in V with that name, or None
    """
    def getVariable (self, variableName):
        for v in self.initialV:
            if v.name==variableName:
                return v
        return None
    """
    DETERMINE IF A VARIABLE ALREADY EXISTS IN THE INITIAL V
    @param variableName: the string name of the variable to get
    @return True if the variable exists, False otherwise  
    """
    def existsVariable (self, variableName):
        return self.getVariable(variableName)==None
    
    def addD (self, d):
        self.si.addD(d)
    def addW(self,w):
        self.si.addW(w)
    def addDList(self, D):
        return self.si.addDList(D)
    def addWList(self,W):
        return self.si.addWList(W)
    def addVList(self, V):
        return self.si.addVList(V)    

#==============================================================================
#=============================LINKED LIST OPERATIONS===========================
#==============================================================================

        
    def checkValidInsert (self, m, pos):
        if not isinstance (m,complexOperation.complexOperation):
            raise scpError.InvalidScpInsertion
        if pos <= 0:
            raise scpError.InvalidScpInsertion_FirstPosition
        if pos > len(self):
            raise scpError.InvalidScpInsertion_InvalidPosition
    """
    INSERT A COMPLEX OPERATION m AT POSITION pos IN THE SCP
    @param m: the copmlex operation to be inserted
    @param pos: the position in the SCP to insert m
    @return returns if successful, throws an InvalidScpInsertion exception otherwise
    """
    def insertAtPos (self, m, pos):
        self.checkValidInsert(m,pos)
        m=copy.deepcopy(m) 

        #cycle to the desired position
        node = self.m1
        prev = None
        for i in range (0, pos-1):
            prev=node
            node = node.next
        #if there is no head, just add m to the prev
        if node == None:
            m.prev=prev
            prev.next=m
            return
        #if the current node is the last node, set the next node to m
        m.prev=node
        if node.next==None:
            node.next = m            
            return
        #otherwise, insert m between the node and node.next positions
        else:
            m.next = node.next
            node.next.prev=m
            node.next=m
            return
    def addNext (self,nxt):
        self.insertAtPos(nxt,len(self))      
    def getLastOperation(self):
        node = self.m1
        if node == None:
            return None
        while node.next!=None:
            node = node.next
        return node        
    
    """
    INSERT THE FIRST STATE IN THE SCP (This should always be an instance of complexOperation_init)
    @param state: the state to be inserted at the first position
    @return nothing if successful, throws InvalidScpInsertion otherwise
    """
    def setState1 (self, state):
        if not isinstance (state, complexOperation.complexOperation_init):
            raise scpError.invalidComplexOperation
        self.insertAtPos(state,0)
        self.m1.kb=self.initialKB
        self.m1.v=self.initialV
        
    """
    FIND THE LENGTH OF THE SCP
    @return returns the number of linked complex operation in the scp
    """        
    def __len__(self):
        if self.m1==None:
            return 0
        i = 0
        node = self.m1
        while True:
            node = node.next
            i=i+1
            if (node==None):
                return i        
    """
    APPENDS A COMPLEX OPERATION TO THE LIST OF COMPLEX OPERATIONS M
    """
    def addComplexOperation (self, m):
        if not isinstance (m, complexOperation.complexOperation):
            raise scpError.invalidComplexOperation
        mcopy = copy.copy(m)
        self.M.append(mcopy)  
    """
    REMOVE THE LAST COMPLEX OPERATION IN THE SCP
    @return True if successful, false otherwise
    """
    def removeLast (self):
        if self.getLastOperation()!=self.m1:
            self.getLastOperation().prev.next=None
            return True
        return False
#==============================================================================
#===============================OUTPUT FUNCTIONS===============================
#==============================================================================

    """
    A STATIC METHOD RETURNS A LIST OF RULES AS A HUMAN-READABLE STRING
    @param kb: the list of rules to display
    @return the list of rules as a human-readable string
    """
    @staticmethod
    def strKnowledge(kb):
        k = u"{"
        for i in range (0, len(kb)):
            k = k + u"{}{}".format(kb[i],(", " if i<len(kb)-1 else "") )
        k=k+u"}"
        return k   
    """
    A STATIC METHOD RETURNS A LIST OF VARIABLES AS A HUMAN-READABLE STRING
    @param v: the list of variables to display
    @return the list of variables as a human-readable string
    """
    @staticmethod    
    def strVariables(v):
        vs = "{"
        for i in range (0, len(v)):
            vs = u"{} {} : {} {}".format(vs, v[i], v[i].evaluate(), (", " if i<len(v)-1 else "") )
        vs=vs+"}"
        return vs
    """
    GET THE LIST OF INITIAL RULES AS A HUMAN-READABLE STRING
    @return the list of initial rules as a human-readable string
    """
    def strInitialKB (self):
        return scp.strKnowledge(copy.deepcopy(self.initialKB))
    """
    GET THE LIST OF INITIAL VARIABLES AS A HUMAN-READABLE STRING
    @return the list of initial variables as a human-readable string
    """
    def strInitialV (self):
        return scp.strVariables(copy.deepcopy(self.initialV))  
    """
    GET THE LIST OF FINAL RULES AS A HUMAN-READABLE STRING
    @return the list of final rules as a human-readable string
    """
    def strFinalV (self):
        return scp.strVariables(self.getLastState().evaluatev())
    """
    GET THE LIST OF FINAL VARIABLES AS A HUMAN-READABLE STRING
    @return the list of final variables as a human-readable string
    """
    def strFinalKB (self):
        return scp.strKnowledge(self.getLastState().evaluatekb())
    """
    REPRESENT THE SCP AS A HUMAN-READABLE STRING
    @return for scp=(m1,m2,m3,m4) returns "m1 >> m2 >> m3 >> m4"
    """
    def __str__(self):
        s=""
        m = self.m1
        while m != None:
            s = s + m.name + (" >> " if m.next!= None else "")
            m = m.next
        return s
    """
    REPRESENT THE SCP IN TERMS OF THE INPUT AND OUTPUT OF EACH COMPLEX OPERATION
    @return the input/output of each complex operation after running
    """
    def strDetailed (self):
        node = self.m1
        s = u''
        while node != None:
            s = s + (u'==={}===\n').format(node.name)
            s=s + u'{}\n'.format(node)
            node = node.next    
        return s

    def __repr__(self):
        return self.__str__()
   



























