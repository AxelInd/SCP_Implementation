# -*- coding: utf-8 -*-
"""
Created on Sat Jun 13 11:43:35 2020

@author: Axel
"""
import copy
folderStructure=True
if folderStructure:
    import sys
    sys.path.append("/SCPFramework") 
    from SCPFramework import basicLogic
    from SCPFramework import CTM
    from SCPFramework import StatePointOperations
else:  
    import basicLogic
    import CTM
    import StatePointOperations

"""
A <CognitiveOperation> is a pipe in the <CTM> pipeline. Cognitive operations are immutable once
defined, and their usefulness come from their well-founded definitions of specific aspects of human
cognition. Each cognitive process takes a state point as input and produces a state point as output.
"""
class CognitiveOperation(object):
    """
    @param name: the unique name of the SCP, shown in output, not used for comparissons
    """
    def __init__(self,name):
        self.name=name
        self.inputStructuralRequirements=[]
        self.outputStructure=[]
    """
    The core funtionality of a <cognitiveOperation> takes an epistemic state as input and produces
    an epistemic state as output after performing some transformations on the set of structural
    variables.
    @param epi: a single <epistemicState> passed as input
    @return p: an epistemic state point, each base point in p has the same structural variables
    """
    def evaluateEpistemicState(self, epi):
        pass
    def __str__(self):
        return self.name
    def __repr__(self):
        return str(self)
    

    """
    @param head: head of the clause
    @param S: the propositional knowledge base to be searched
    @return [body1 + ... + bodyn | head <- bodyi in clauses]
    """
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
"""
Adds interprets conditionals in p[Delta] as licenses for implication.
Creates abnormalities as definied in <addAB> in the thesis.
"""
class m_addAB (CognitiveOperation):
    def __init__(self):
        CognitiveOperation.__init__(self,name="addAB")
        self.inputStructuralRequirements=['Delta']
        self.outputStructure=['S','Delta']
    """
    @param epi: a single <epistemicState>
    @return k the lowest number for which ab_k does not yet exist
    """
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
    """
    @param consequence: a consequence of a conditional
    @return all the preconditions in p[delta] which share a consequence
    """
    @staticmethod
    def findAllConditionalDependencyPreconditions(consequence, delta):
        bodies = []
        for d in delta:
            if d.clause1 == consequence:
                bodies.append(d.clause2)
        return bodies
    """
    @param epi: a single <epistemicState>
    @return p: a single epistemic state with conditionals interpreted as licenses for implication
    """
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
                
"""
weakly completes S of the epistemic state
"""
class m_wc (CognitiveOperation):
    def __init__(self):
        CognitiveOperation.__init__(self,name="wc")
        self.inputStructuralRequirements=['S']
        self.outputStructure=['S']        
    """
    @return a single disjunction of the contents of every clause in clauses
    """
    @staticmethod
    def disjunctionOfClauses(clauses):
        disjunction=[]
        
        for clause in clauses:
            if disjunction==[]:
                disjunction=clause
            else:
                disjunction = basicLogic.operator_bitonic_or(disjunction, clause)
        return disjunction
    """
    @param epi: the spistemic state input
    @return the weak completion of epi
    """
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
"""
an aggregate <cognitiveOperation> which combines the functionality of the <wc> and <semantic>
cognitive operations.
"""
class m_wcs (CognitiveOperation):
    def __init__(self):
        CognitiveOperation.__init__(self,name="wcs")
        self.inputStructuralRequirements=['S','V']
        self.outputStructure=['S','V']
    """
    @param epi: the <epistemicState> input
    @return p: the weak completion of epi[S], and the result of the svl stored in p[V]
    """
    def evaluateEpistemicState(self,epi):
        tempCTM=CTM.CTM()
        tempCTM.si=[epi]
        tempCTM.appendm(m_wc())
        tempCTM.appendm(m_semantic())
        p = tempCTM.evaluate()
        return p

"""
Applies the semantic operator
"""        
class m_semantic (CognitiveOperation):
    def __init__(self):
        CognitiveOperation.__init__(self,name="semantic")
        self.inputStructuralRequirements=['S','V']
        self.outputStructure=['S','V']
    """
    set the value of the atom called atomName in V, to value
    """
    @staticmethod    
    def changeAssignmentInV(atomName, Value, V):
        for atom in V:
            if atom.getName()==atomName:
                atom.setValue(Value)
    """
    T = [A | there exists a clause A <- Body in epi[S] with I(Body)=T]
    @return epi with epi[V][v] = T if v in T 
    """
    @staticmethod
    def setTruth(epi):
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
                    
    """
    F = [A | there exists a clause A <- Body in epi[S], and for all A <- Body in epi[S]
    we find I(Body)=F]
    @return epi with epi[V][v] = F if v in F 
    """
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
                    
    """
    @param epi: an input <epistemicState>
    @return p: epi with epi[V] representing the least model
    """
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
"""
Add some combination of any length of the set of abducibles
and add it to the input <epistemicState>
"""
class m_addAbducibles(CognitiveOperation):
    """
    @param maxLength: the maximum size of the explanation to be added
    NOTE: large sizes make search EXTREMELY inneficient because multiple <m_addAbducibles>
    operations can occur in a single <CTM> (the number of resulting state points can be huge)
    """
    def __init__(self, maxLength=9999):
        CognitiveOperation.__init__(self,name="addExp")
        self.maxLength=maxLength
        self.inputStructuralRequirements=['S','R']
        self.outputStructure=['S','R']
    """
    @param epi: the <epistemicState> input
    @return p: epi, with epi[R][]
    """
    def evaluateEpistemicState(self,epi):
        nextEpis=[]
        #find only as many abducibles as the max length allows
        abducibles=epi['R']['abducibles']
        for i in range(0, min(len(abducibles)+1,self.maxLength)):  
            perm = combinations(abducibles,i)

            for j in list(perm): 
                newEpi = copy.deepcopy(epi)
                newEpi['R']['explanation']=list(j)
                newEpi['S']=newEpi['S']+list(j)   
                nextEpis.append(newEpi)
        return nextEpis    
"""
Delete all variables mentioned in epi[delete] from epi[S], epi[delta], and epi[V]
"""    
class m_deleteo(CognitiveOperation):
    def __init__(self, maxLength=3):
        CognitiveOperation.__init__(self,name="delete")
        self.maxLength=maxLength
        self.inputStructuralRequirements=['S','R']
        self.outputStructure=['S','R']
    """
    completely remove a variable varname from the epi
    """
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
    """
    @param epi: the input <epistemicState>
    @return p: epi, with variables in ['R']['delete'] deleted
    """
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
"""
Placeholder <cognitiveOperation> only used when comparing <CTM> objects using the scoring NW
scoring algorithm for SCPs and the extended NW algorith for SCPs. (see thesis chapter: 8)
"""
class m_insertionOperation(CognitiveOperation):
    def __init__(self):
        CognitiveOperation.__init__(self,name="INSERT")

"""
This operation represents an arbitrary operation for scoring with <CTM>. For example, if the
operation <m_applySystemP> is assumed to exist in an SCP, then we can score that scp
without explicitly defining <m_applySystemP>.
"""
class m_dummyOperation(CognitiveOperation):
    def __init__(self,name="dummy"):
        CognitiveOperation.__init__(self,name=name)
"""
A very simplified version of the deductive closure of a program. Any element in p[S]
is in the deductive close of epi[S], but only some elements of the deductive close are in p[S]
"""
class m_th_simplified(CognitiveOperation):
    def __init__(self,name="th", target='S'):
        CognitiveOperation.__init__(self,name=name)
        self.target=target
        self.inputStructuralRequirements=[self.target,'V']
        self.outputStructure=[self.target,'V']
    
    """
    @return the value of every variable called name in li set to val
    """
    @staticmethod
    def addVarAssignmentToV(li, name, val):
        li=copy.deepcopy(li)
        for variable in li:
            if variable.getName()==name:
                variable.setValue(val)
        return li
    """
    @param epi: the input <epistemicState>
    @return p: the simplified deductive closure of epi[S] stored in p[S]
    """
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

"""
Determine the results of applying each extension possible of the default theory (epi[D],epi[W])
Makes use of <m_th>, meaning that it cannot produce the true deductive closure of epi[W], or
in the In sets, but it is good enough for our purposes.
"""
from itertools import permutations
"""
@param maxLength: the maximum length of the generated default processes
"""
class m_default(CognitiveOperation):
    def __init__(self,name="th", maxLength=3):
        CognitiveOperation.__init__(self,name=name)
        self.inputStructuralRequirements=['W','D','V']
        self.outputStructure=['W','D','V']
        self.maxLength=maxLength
    """
    Do not consider extensions of length 0
    """
    @staticmethod
    def isValidDefaultSubProcess (dp, W):
        if len (dp)==0:
            return True
    """
    add the conlusion of the default process d to epi[W]
    """
    @staticmethod
    def addConclusionToEpi (d, epi):
        epi['W'].append(d.clause3)
        return epi
    
    #assumed to hold
    """
    Determine in the inset and outset of epi[S] when using default process dp
    @return inset, outset
    """
    @staticmethod
    def INOUT (dp, epi):
        IN_epi=copy.deepcopy(epi)
        if len(dp)==0:
            return epi['W'], []
        #GET OUT SET
        OUT = []
        for proc in dp:
            OUT+=basicLogic.negateRuleList(proc.clause2)
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
    """
    @return True if dp is valid default process on epi. Shares redundant code with INOUT(), but
    increases readability of the code.
    """
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
    
    """
    determine the simplified deductive closure of epi[W]
    """
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
        #@TODO incomplete and being rewritten
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
        for dp in validProcesses:
            IN, OUT = m_default.INOUT(dp,epi)
        successfulProcesses=[]
        for dp in validProcesses:
            #intersection in, out should be the empty set
            IN, OUT = m_default.INOUT(dp,epi)
            failed=False
            for IN_rule in IN:
                if IN_rule in OUT:
                    failed=True
            if not failed:
                successfulProcesses.append(dp)
        for dp in successfulProcesses:
            IN, OUT = m_default.INOUT(dp,epi)
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
        return epi
        for dp in closedSuccessfulProcesses:
            print ("DP is ", dp)
            IN, OUT = m_default.INOUT(dp,epi)
            print ("In is ", IN)
            print ("Out is ", OUT)        
        
    
        
        #check each previous subprocess [0:D_n-1] was successful
        # 3) repeat 1), 2)
        return epi
























     
       