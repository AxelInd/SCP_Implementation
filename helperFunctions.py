"""
CONVERTS A NUMBER num TO BASE base AND FORCES A LENGTH OF length
@param number: integer number
@param base: desired base (should usually be the length of the logic being used)
@return a list representing num in the desired base format with a total legth of length
"""
def toBase (num, base, length=-1):
    n = []
    tn = num
    
    while tn >= base:
        n.append(tn%base)
        tn = tn // base
    n.append(tn%base)
    
    if length > 0 and len(n) < length: 
        padding=[0]*(length-len(n))
        n = n + padding
    n.reverse()
    return n
"""
CONVERTS A BASE n NUMBER IN A LIST INTO A LIST OF GROUND TRUTH VALUES FOR THE LOGIC
@param n: the list representing the base n number
@return a list with each number replaced by its logical equivalent in logicRep
"""
def base_n_ToValuedLogic (n, logicRep):
    
    li = [logicRep[i] for i in n]
    return li

"""
FIND EVERY POSSIBLE TRUTH ASSIGNMENT OF THE FREE VARIABLES
@param values: the variables that need assignments
@return a list of list, containing every possible logical assignment of the values
"""
def generateAllPossibleVariableAssigmentsFromV (values, logicRep=[True,False,None]):
    #the total number of possible assignments of the variables in values
    length = len(logicRep)**len(values)
    poss = []
    for i in range (0, length):
        #find the base n number that corresponds to i
        n = toBase(num=i, base=len(logicRep), length=len(values))
        #append a conversion of mapping of n to the logicRep truth table
        poss.append(base_n_ToValuedLogic(n,logicRep))
    return poss

#https://www.geeksforgeeks.org/generate-all-the-permutation-of-a-list-in-python/
# Python function to print permutations of a given list 
def permutation(lst): 
    # If lst is empty then there are no permutations 
    if len(lst) == 0: 
        return [] 
    # If there is only one element in lst then, only 
    # one permuatation is possible 
    if len(lst) == 1: 
        return [lst] 
    # Find the permutations for lst if there are 
    # more than 1 characters 
    l = [] # empty list that will store current permutation 
    # Iterate the input(lst) and calculate the permutation 
    for i in range(len(lst)): 
       m = lst[i] 
       # Extract lst[i] or m from the list.  remLst is 
       # remaining list 
       remLst = lst[:i] + lst[i+1:] 
       # Generating all permutations where m is first 
       # element 
       for p in permutation(remLst): 
           l.append([m] + p) 
    return l 



















