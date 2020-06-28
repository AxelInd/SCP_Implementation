

import copy
#take a state point and return every base point in the state point
def flatten_list(nested_list):
    """Flatten an arbitrarily nested list, without recursion (to avoid
    stack overflows). Returns a new list, the original list is unchanged.
    >> list(flatten_list([1, 2, 3, [4], [], [[[[[[[[[5]]]]]]]]]]))
    [1, 2, 3, 4, 5]
    >> list(flatten_list([[1, 2], 3]))
    [1, 2, 3]
    """
    if not isinstance(nested_list,list):
        nested_list=[nested_list]
    nested_list = copy.deepcopy(nested_list)

   
    
    while nested_list:
        sublist = nested_list.pop(0)

        if isinstance(sublist, list):
            nested_list = sublist + nested_list
        else:
            yield sublist

def flattenStatePoint(statePoint):
    if not isinstance (statePoint,list):
        statePoint=[statePoint]
    return list(flatten_list(statePoint))

#find all epis with a specific name in a list flattened with flattenEpiList()
def extractBasePointsFromFlattenedStatePoint(epiList, name):
    li=[]
    for epi in epiList:
        if epi.getName()==name:
            li.append(epi)
    return li

def properSubset(li1,li2):
    if li1 == li2:
        return False
    for v1 in li1:
        #if there is some v in the first list that is not in the second list, they can't be subsets
        match=False
        for v2 in li2:
            #print (v1.clause1)
            #print (v1.clause2)
            if v1.clause1 == v2.clause1:
                if v1.clause2 == v2.clause2:
                    match=True
        if not match:
            return False
    return True

def VtoTupleList(v_1, ignoreNone=True):
    v_1AsSet = set([(v.getName(),v.getValue())  for v in v_1 if (v.getValue()!=None or ignoreNone==False)])
    return v_1AsSet
def properSubset_atomList(v_1,v_2):
    v_1AsSet =VtoTupleList(v_1)
    v_2AsSet =VtoTupleList(v_2)
    
    #print (v_1AsSet)
    #ensure SUBSET
    if v_1AsSet==v_2AsSet:
        return False
    subset=v_1AsSet.issubset(v_2AsSet)
    return subset


def CTMtoSCP(results, f):  
    return [(result,f) for result in results]


def predictionsModelsGamma_lenient(predictions,gamma):
    for i in gamma:
        predHolds=False
        #some prediction is in gamma for that attribute
        for prediction in predictions[i]:
            if prediction in gamma[i]:
                predHolds=True
        #some prediction required by gamma was not met
        if not predHolds:
            return False
    return True

def predictionsModelsGamma_strict(predictions,gamma):
    for i in gamma:
        #some prediction is in gamma for that attribute
        for prediction in predictions[i]:
            if prediction not in gamma[i]:
                return False
    return True
































