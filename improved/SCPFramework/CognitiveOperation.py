# -*- coding: utf-8 -*-
"""
Created on Sat Jun 13 11:43:35 2020

@author: Axel
"""
import sys
sys.path.append("/SCPFramework") 
import copy

from SCPFramework import basicLogic
from SCPFramework import CTM
from SCPFramework import StatePointOperations

class CognitiveOperation(object):
    def __init__(self,name):
        self.name=name
        self.inputStructuralRequirements=[]
        self.outputStructure=[]
    def evaluateEpistemicState(self, epi):
        pass
    def precondition(self, epi):
        print ("Checking preconditions")
    def __str__(self):
        return self.name
    def __repr__(self):
        return str(self)
    


    @staticmethod
    def getBodiesWhichShareHead (head, S):
        bodies = []
        for rule in S:
            #for <-
            lrImplication = isinstance (rule,basicLogic.operator_bitonic_implication)
            bijection = isinstance (rule,basicLogic.operator_bitonic_bijection)
            if  (lrImplication or bijection) and rule.clause1 == head:
                bodies.append(rule.clause2)
            if  (bijection) and rule.clause2 == head:
                bodies.append(rule.clause1)
        return bodies
class m_addAB (CognitiveOperation):
    def __init__(self):
        CognitiveOperation.__init__(self,name="addAB")
        self.inputStructuralRequirements=['Delta']
        self.outputStructure=['S','Delta']
    @staticmethod
    def findLowestK(epi):
        #the lowest number for which ab_1 does not exist
        lowest_k = None
        
        k=1
        while lowest_k == None:
            #all atomic names that appear in these structural variables
            ats = epi.getAtomNamesInStructuralVariables(['S','Delta','V'])
            candidateAbnormality = 'ab_'+str(k)
            if candidateAbnormality not in ats:
                lowest_k = k
            k=k+1
        return lowest_k
    @staticmethod
    def findAllConditionalDependencyPreconditions(consequence, delta):
        bodies = []
        for d in delta:
            if d.clause1 == consequence:
                bodies.append(d.clause2)
        return bodies
    def evaluateEpistemicState(self,epi):
        #set of conditional rules
        delta = epi['Delta']
        S = epi['S']
        V = epi['V']
        
        resolvedDependencies=[]
        for conditional in delta:
            consequence = conditional.clause1
            precondition = conditional.clause2
            if consequence not in resolvedDependencies:
                lowestk = m_addAB.findLowestK(epi)
                allDependencies = m_addAB.findAllConditionalDependencyPreconditions(consequence,delta)
                abBody = None
                for dep in allDependencies:
                    negateDep = basicLogic.operator_monotonic_negation(dep)
                    if dep!=precondition:
                        if abBody == None:
                            abBody = negateDep
                        else:
                            abBody = basicLogic.operator_bitonic_or(abBody, negateDep)
                if abBody == None:
                    abBody = basicLogic.FALSE
                abName='ab_'+str(lowestk)
                abAtom = basicLogic.atom(abName,None)
                ab = basicLogic.operator_bitonic_implication(abAtom, abBody)
                
                negABAtom = basicLogic.operator_monotonic_negation(abAtom)
                
                newBody = basicLogic.operator_bitonic_and(precondition, negABAtom)
                newRule = basicLogic.operator_bitonic_implication(consequence, newBody)
                #add the abnormality and its assignment to the list of rules
                S.append(newRule)
                S.append(ab)
                V.append(abAtom)
            resolvedDependencies=resolvedDependencies+allDependencies
        #all conditionals have now been interpreted
        epi['Delta']=[]
        
        return epi
                
                
class m_wc (CognitiveOperation):
    def __init__(self):
        CognitiveOperation.__init__(self,name="wc")
        self.inputStructuralRequirements=['S']
        self.outputStructure=['S']        

    @staticmethod
    def disjunctionOfClauses(clauses):
        disjunction=[]
        
        for clause in clauses:
            if disjunction==[]:
                disjunction=clause
            else:
                disjunction = basicLogic.operator_bitonic_or(disjunction, clause)
        return disjunction
    def evaluateEpistemicState(self,epi):
        S = epi['S']
        # replace all clauses pointing to the same head with their conjunction
        # heads must be atomic so just get the list of all atoms in S
        # replace <- with <->
        # can be done in this one step
        atoms = epi.getAtomsInStructuralVariables(['S'])
        newS=[]
        handledHeads=[]
        for rule in S:
            head = rule.clause1
            if head not in handledHeads or head not in atoms:
                bodieswhichsharehead=CognitiveOperation.getBodiesWhichShareHead(head, S)
                disjunctionOfBodies=m_wc.disjunctionOfClauses(bodieswhichsharehead)
                newRule = basicLogic.operator_bitonic_bijection(head, disjunctionOfBodies)
                newS.append(newRule)
                handledHeads.append(head)
            else:
                pass
        
        epi['S']=newS
        
        #step 1, find all 
        return epi
        

class m_semantic (CognitiveOperation):
    def __init__(self):
        CognitiveOperation.__init__(self,name="semantic")
        self.inputStructuralRequirements=['S','V']
        self.outputStructure=['S','V']
    @staticmethod    
    def changeAssignmentInV(atomName, Value, V):
        for atom in V:
            if atom.getName()==atomName:
                atom.setValue(Value)
    @staticmethod
    def setTruth(epi):
        #I_V(S)
        S = epi['S']
        V = epi['V']
        
        
        ats = epi.getAtomNamesInStructuralVariables(['S'])
        #Assign TRUTH in possible world
        for rule in S:
            #clear the interpretation
            basicLogic.setkbfromv(epi['S'], V)
            
            left = rule.clause1
            right = rule.clause2
            if left.getName() in ats:
                evaluation = right.evaluate()
                if evaluation==True:
                    m_semantic.changeAssignmentInV(left.getName(), evaluation, V)  
            left = rule.clause2
            right = rule.clause1
            if left.getName() in ats:
                evaluation = right.evaluate()
                if evaluation==True:
                    m_semantic.changeAssignmentInV(left.getName(), evaluation, V)  
                    
        return epi
                    
    #There exists A<- body and FOR ALL clauses A <- body we find I_V(body)=False   
    # currently NOT NONMONOTONIC! @TODOfix!
    # will currently only converge to one least model!
    # possible solution, run for each possible reordering of the rules
    @staticmethod
    def setFalse(epi):
        #I_V(S)
        S = epi['S']
        V = epi['V']
        
        
        ats = epi.getAtomNamesInStructuralVariables(['S'])
        #Assign TRUTH in possible world
        for rule in S:
            #clear the interpretation
            epi['S']=basicLogic.setkbfromv(epi['S'], V)
            
            left = rule.clause1
            right = rule.clause2
            if left.getName() in ats:
                evaluation = right.evaluate()
                if evaluation==False:
                    shared = CognitiveOperation.getBodiesWhichShareHead(left, epi['S'])
                    allFalse=True
                    for body in shared:
                        if body.evaluate() != False:
                            allFalse=False
                    if allFalse:
                        m_semantic.changeAssignmentInV(left.getName(), evaluation, V) 
                     
            left = rule.clause2
            right = rule.clause1
            if left.getName() in ats:
                evaluation = right.evaluate()
                if evaluation==False:
                    shared = CognitiveOperation.getBodiesWhichShareHead(left, epi['S'])
                    allFalse=True
                    for body in shared:
                        if body.evaluate() != False:
                            allFalse=False
                    if allFalse:
                        m_semantic.changeAssignmentInV(left.getName(), evaluation, V) 
                    
        return epi
                    
                            
    def evaluateEpistemicState(self,epi):
        originalS = copy.deepcopy(epi['S'])
        originalV = copy.deepcopy(epi['V'])
        
        prevV = None
        currentV = originalV
        while currentV != prevV:
            prevV = copy.deepcopy(currentV)
            
            m_semantic.setTruth(epi)
        
            m_semantic.setFalse(epi)
            currentV=copy.deepcopy(epi['V'])
        epi['S']=originalS
        return epi
    

from itertools import combinations
class m_addAbducibles(CognitiveOperation):
    def __init__(self, maxLength=9999):
        CognitiveOperation.__init__(self,name="addExp")
        self.maxLength=maxLength
        self.inputStructuralRequirements=['S','R']
        self.outputStructure=['S','R']
    def evaluateEpistemicState(self,epi):
        nextEpis=[]
        #find only as many abducibles as the max length allows
        abducibles=epi['R']['abducibles']
        for i in range(0, min(len(abducibles)+1,self.maxLength)):  
            perm = combinations(abducibles,i)

            for j in list(perm): 
                newEpi = copy.deepcopy(epi)
                newEpi['R']={'abducibles':list(j)}
                newEpi['S']=newEpi['S']+list(j)
                        
                nextEpis.append(newEpi)
        return nextEpis    
    
class m_deleteo(CognitiveOperation):
    def __init__(self, maxLength=9999):
        CognitiveOperation.__init__(self,name="delete")
        self.maxLength=maxLength
        self.inputStructuralRequirements=['S','R']
        self.outputStructure=['S','R']
    def delete(self,varname,epi):
        V = epi['V']
        S = epi['S']
        V = [v for v in V if v.getName()!=varname]
        newP=[]
        
        for rule in S:
            head = rule.clause1
            body = rule.clause2
            if isinstance (head, basicLogic.atom):
                if head.getName()==varname:
                    head=None
            if isinstance(body,basicLogic.operator_monotonic):
    
                if body.clause.getName()==varname:
                    body.clause=basicLogic.FALSE
            if isinstance (body, basicLogic.atom):
                body = basicLogic.TRUE
            if isinstance (body, basicLogic.operator_bitonic):
                if body.clause1.getName() == varname:
                    body=body.clause2
                elif body.clause2.getName() == varname:
                    body=body.clause1   
            if head != None:
                newP.append(basicLogic.operator_bitonic_implication(head,body))
            
        epi['V']=V
        epi['S']=newP
        return epi
        
    def evaluateEpistemicState(self,epi):
        nextEpis=[]
        #find only as many abducibles as the max length allows
        for i in range(0, min(len(epi['R']['delete'])+1,self.maxLength)):  
            perm = combinations(epi['R']['delete'],i)

            for j in list(perm): 
                newEpi = copy.deepcopy(epi)
                for i in j:
                    newEpi=self.delete(i,newEpi)
                newEpi['R']['deleted']=j
                nextEpis.append(newEpi)
        return nextEpis    

#only used for the NM algorithm
class m_insertionOperation(CognitiveOperation):
    def __init__(self):
        CognitiveOperation.__init__(self,name="INSERT")

#this operation is used in place of an undefined operation for scoring
class m_dummyOperation(CognitiveOperation):
    def __init__(self,name="dummy"):
        CognitiveOperation.__init__(self,name=name)

  


class m_th_simplified(CognitiveOperation):
    def __init__(self,name="th", target='S'):
        CognitiveOperation.__init__(self,name=name)
        self.target=target
        self.inputStructuralRequirements=[self.target,'V']
        self.outputStructure=[self.target,'V']
        
    @staticmethod
    def addVarAssignmentToV(li, name, val):
        li=copy.deepcopy(li)
        for variable in li:
            if variable.getName()==name:
                variable.setValue(val)
        return li
        
    def evaluateEpistemicState(self,epi):
        kb = epi[self.target]
        v=epi['V']
        basicLogic.setkbfromv(kb, v)
        
        # we are allowed to assume a monotonic logic base for this
        for rule in kb:
            if isinstance (rule, basicLogic.atom):
                v=m_th_simplified.addVarAssignmentToV(v,rule.getName(),True)
            elif isinstance(rule,basicLogic.operator_monotonic_negation):
                if isinstance(rule.clause, basicLogic.atom):
                    v=m_th_simplified.addVarAssignmentToV(v,rule.clause.getName(),False)  
            elif isinstance(rule,basicLogic.operator_bitonic):
                head = rule.clause1
                body = rule.clause2
                bodyVal = body.evaluate()
                if isinstance (rule, basicLogic.operator_bitonic_implication):
                    if isinstance (head, basicLogic.atom):
                        if bodyVal!=None:
                            v=m_th_simplified.addVarAssignmentToV(v,head.getName(),bodyVal)  
                else:
                    print ("unknown bitonic")
            else:
                print ("unknown operation")
                    
                    
                    
        epi['V']=v
        epi[self.target]=kb
        #remove all v assignments from this epi, th is not an evaluation function
        for v in epi['V']:
            for rule in epi[self.target]:
                rule.deepSet(v.getName(), None)
        return epi


from itertools import permutations
class m_default(CognitiveOperation):
    def __init__(self,name="th", maxLength=3):
        CognitiveOperation.__init__(self,name=name)
        self.inputStructuralRequirements=['W','D','V']
        self.outputStructure=['W','D','V']
        self.maxLength=maxLength
    @staticmethod
    def isValidDefaultSubProcess (dp, W):
        if len (dp)==0:
            return True
    @staticmethod
    def addConclusionToEpi (d, epi):
        epi['W'].append(d.clause3)
        return epi
    
    #assumed to hold
    @staticmethod
    def INOUT (dp, epi):
        IN_epi=copy.deepcopy(epi)
        if len(dp)==0:
            return epi['W'], []
        #GET OUT SET
        OUT = []
        for proc in dp:
            OUT+=basicLogic.negateRuleList(proc.clause2)
        #print ("OUT:: ", OUT)
        
        
        #GET IN SET
        for proc in dp:
            #basicLogic.setkbfromv(IN_epi['W'], IN_epi['V'])
            IN_epi=m_default.getTh(IN_epi)
            IN_epi = m_default.getTh(m_default.addConclusionToEpi(proc,IN_epi))
            IN = IN_epi['W']
            #print (">>>>>>>> is ",IN, "    :::   proc : ", proc)
            if not proc.isApplicableToW(IN):
                #@TODOthrowexception
                return False
        return IN, OUT
        
    @staticmethod
    def isValidDefaultProcess (dp, epi):
        #GET OUT SET
        OUT = []
        for proc in dp:
            OUT+=basicLogic.negateRuleList(proc.clause2)
        #print ("OUT:: ", OUT)
        
        IN_epi=copy.deepcopy(epi)
        #GET IN SET
        for proc in dp:
            #basicLogic.setkbfromv(IN_epi['W'], IN_epi['V'])
            IN_epi=m_default.getTh(IN_epi)
            IN_epi = m_default.getTh(m_default.addConclusionToEpi(proc,IN_epi))
            IN = IN_epi['W']
            #print (">>>>>>>> is ",IN, "    :::   proc : ", proc)
            if not proc.isApplicableToW(IN):
                return False
        return True
            
        
        return True
    @staticmethod
    def getTh (epi):
        tempCTM=CTM.CTM()
        tempCTM.si=[epi]
        tempCTM.appendm(m_th_simplified(target='W'))
        #guaranteed to be monotonic
        epi = StatePointOperations.flattenStatePoint(tempCTM.evaluate())[0]
        # 2) generateProcesses
        return epi
    #very very inefficient, but suitable for a proof of concept
    def evaluateEpistemicState(self,epi):
        D = epi['D']
        possibleProcesses=[]
        for i in range(0, min(len(D)+1,self.maxLength)):  
            possibleProcesses+= list(permutations(D,i))

        validProcesses=[]
        for dp in possibleProcesses: 
            #print (dp)
            isValid = m_default.isValidDefaultProcess(dp,epi)
            if isValid:
                validProcesses.append(dp)
            else:
                print(dp, " is invalid")
        print (">>>>>>VALID PROCS<<<<<<<<<<<<<<<<<<")
        for dp in validProcesses:
            print ("DP is ", dp)
            IN, OUT = m_default.INOUT(dp,epi)
            print ("In is ", IN)
            print ("Out is ", OUT)
        successfulProcesses=[]
        for dp in validProcesses:
            #intersection in, out should be the empty set
            IN, OUT = m_default.INOUT(dp,epi)
            failed=False
            for IN_rule in IN:
                if IN_rule in OUT:
                    print ("d = INVALID")
                    failed=True
            if not failed:
                successfulProcesses.append(dp)
        print ("+++++++++SUCCESSFUL PROCS+++++++++++++++")
        for dp in successfulProcesses:
            print ("DP is ", dp)
            IN, OUT = m_default.INOUT(dp,epi)
            print ("In is ", IN)
            print ("Out is ", OUT)
        closedSuccessfulProcesses= []
        for dp in successfulProcesses:
            dpHolds=True
            for d in D:
                IN, OUT = m_default.INOUT(dp,epi)
                if d.isApplicableToW(IN):
                    if not d in dp:
                        dpHolds=False
            if dpHolds:
                closedSuccessfulProcesses.append(dp)
            dpHolds=True
        print ("+++++++++SUCCESSFUL CLOSED PROCS+++++++++++++++")
        for dp in closedSuccessfulProcesses:
            print ("DP is ", dp)
            IN, OUT = m_default.INOUT(dp,epi)
            print ("In is ", IN)
            print ("Out is ", OUT)        
        
    
        
        #check each previous subprocess [0:D_n-1] was successful
        # 3) repeat 1), 2)
        return epi
























     
       