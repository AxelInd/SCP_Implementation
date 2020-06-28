# Code in this file is modified from the code available publicly at:
#https://wilkelab.org/classes/SDS348/2019_spring/labs/lab13-solution.html

import os
os.chdir("../")
from SCPFramework import CTM
from SCPFramework import CognitiveOperation
#the insertion operation. Only used in scoring and alignment
NONE=CognitiveOperation.m_insertionOperation()




# THE SET OF COGNITIVE OPERATIONS APPROPRIATE TO THE SUPPRESSION TASK
ADDAB = CognitiveOperation.m_addAB()
WC = CognitiveOperation.m_wc()
SEMANTIC = CognitiveOperation.m_semantic()
ABDUCIBLES=CognitiveOperation.m_addAbducibles(maxLength=4)
DELETE=CognitiveOperation.m_deleteo()

s_i=['$s_\text{WST}$']
c = CTM.CTM()
c.setSi(s_i)
c.appendm(ADDAB)
c.appendm(WC)
c.appendm(SEMANTIC)

d = CTM.CTM()
d.setSi(s_i)
d.appendm(ADDAB)
d.appendm(ABDUCIBLES)
d.appendm(WC)
d.appendm(SEMANTIC)

TH=CognitiveOperation.m_dummyOperation('th')

e = CTM.CTM()
e.setSi(s_i)
e.appendm(TH)


f = CTM.CTM()
f.setSi(s_i)
f.appendm(ADDAB)
f.appendm(TH)
f.appendm(WC)
f.appendm(SEMANTIC)

print (c)
print (d)

#major changes
# added insertionCosts, matchRewards, mismatchCosts 
# removed gap_penalty, match_award, mismatch_penalty
# match = matchRewards[]
# mismatchCosts=mismatchCosts[type(alpha)]+ mismatchCosts[type(beta)]

#initialization: top row: cost = cost[-1]+cost of inserting the operation in the top row
# first col: cost = cost[-1]+cost of inserting the operation in the first col




insertionCosts={CognitiveOperation.m_addAB: -1,
                CognitiveOperation.m_wc: -1,
                CognitiveOperation.m_semantic: -1,
                CognitiveOperation.m_addAbducibles: -1,
                CognitiveOperation.m_deleteo:-1,
                CognitiveOperation.m_dummyOperation:-5,
                list: -1
                }
matchRewards={CognitiveOperation.m_addAB: 1,
                CognitiveOperation.m_wc: 1,
                CognitiveOperation.m_semantic:1,
                CognitiveOperation.m_addAbducibles: 1,
                CognitiveOperation.m_deleteo:1,
                CognitiveOperation.m_dummyOperation:5,
                list: 3}

# A function for making a matrix of zeroes
def zeros(rows, cols):
    # Define an empty list
    retval = []
    # Set up the rows of the matrix
    for x in range(rows):
        # For each row, add an empty list
        retval.append([])
        # Set up the columns in each row
        for y in range(cols):
            # Add a zero to each column in each row
            retval[-1].append(0)
    # Return the matrix of zeros
    return retval

# A function for determining the score between any two bases in alignment
def match_score(alpha, beta):
    if type(alpha) == type(beta):
        return matchRewards[type(alpha)]
    elif isinstance(alpha,CognitiveOperation.m_insertionOperation):
        return insertionCosts[type(beta)]
    elif isinstance(beta,CognitiveOperation.m_insertionOperation):
        return insertionCosts[type(alpha)]
    else:
        return  (insertionCosts[type(alpha)]+ insertionCosts[type(beta)])/2


def needleman_wunsch(seq1, seq2):
    
    # Store length of two sequences
    n = len(seq1)  
    m = len(seq2)
    
    # Generate matrix of zeros to store scores
    score = zeros(m+1, n+1)
   
    # Calculate score table
    
    # Fill out first column
    score[0][0]=0
    for i in range(1, m + 1):
        
        score[i][0] = score[i-1][0]+ insertionCosts[type(seq2[i-1])]
        #score[i][0] = insertionCosts
    
    # Fill out first row
    for j in range(1, n + 1):
        score[0][j] = score[0][j-1]+ insertionCosts[type(seq1[j-1])]
    
    # Fill out all other values in the score matrix
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            # Calculate the score by checking the top, left, and diagonal cells
            match = score[i - 1][j - 1] + match_score(seq1[j-1], seq2[i-1])
            delete = score[i - 1][j] + insertionCosts[type(seq2[i-1])]
            insert = score[i][j - 1] + insertionCosts[type(seq1[j-1])]
            # Record the maximum score from the three possible scores calculated above
            score[i][j] = max(match, delete, insert)
    
    # Traceback and compute the alignment 
    
    
    #THIS IS WHERE WE MAKE BIG CHANGES!
    # Create variables to store alignment
    al1 = CTM.CTM()
    al2 = CTM.CTM()
    al1.si==None
    al2.si==None
    
    # Start from the bottom right cell in matrix
    i = m
    j = n
    
    # We'll use i and j to keep track of where we are in the matrix, just like above
    while i > 0 and j > 0: # end touching the top or the left edge
        score_current = score[i][j]
        score_diagonal = score[i-1][j-1]
        score_up = score[i][j-1]
        score_left = score[i-1][j]
        
        # Check to figure out which cell the current score was calculated from,
        # then update i and j to correspond to that cell.
        if score_current == score_diagonal + match_score(seq1[j-1], seq2[i-1]):
            al1.appendm(seq1[j-1])
            al2.appendm(seq2[i-1])
            i -= 1
            j -= 1
        elif score_current == score_up + insertionCosts[type(seq1[j-1])]:
            al1.appendm(seq1[j-1])
            al2.appendm(NONE)
            j -= 1
        elif score_current == score_left +  insertionCosts[type(seq2[i-1])]:
            al1.appendm(NONE)
            al2.appendm(seq2[i-1])
            i -= 1

    # Finish tracing up to the top left cell
    while j > 0:
        al1.appendm(seq1[j-1])
        al2.appendm(NONE)
        j -= 1
    while i > 0:
        al1.appendm(seq2[i-1])
        al2.appendm(NONE)
        i -= 1
    
    # Since we traversed the score matrix from the bottom right, our two sequences will be reversed.
    # These two lines reverse the order of the characters in each sequence.
    al1.NMTransformation()
    al2.NMTransformation()
    return(al1, al2, score)

"""
the bottom right entry in the table
"""
def maxScore(matrix):
    #optimal global alignment is always last entry
    return matrix[-1][-1]

def printAlignment(align1,align2):
    print ("\n>>Optimal Alignment<<")
    if len(align1)!=len(align2):
        print ("Lengths do not match!")
        return []
    for i in range(0, len(align1)):
        print ("{}{:>20}".format(str(align1[i]),str(align2[i])))
"""
Transform a matrix into a latex table with the first row given by r, and the first col given by c
"""
def matrixAsLatexRC(matrix, r, c):
    s='\\begin{table}\n'
    s+='\\begin{center}\n'
    s+='\\begin{tabular}{'
    s+='c | '
    s+='c '* ((len(matrix[0])))
    s+='}\n & & '
    for j in range (0,len(r)):
        s+=str(r[j])+ (' & ' if j!=len(r)-1 else '')
    s+="\\\\\n"
    s+="\\hline\n"
    for i in range (0,len(matrix)):
        if i>=1:
            s+= str(c[i-1])+' & '
        else:
            s+=' & '
        for j in range (0, len(matrix[0])):
            s+=str(matrix[i][j])+ (' & ' if j!=len(matrix[0])-1 else '')
        s+=('' if i==len(matrix)-1 else '\\\\')+ '\n'
    s+='\\end{tabular}\n'   
    s+='\caption{no caption}\n'
    s+='\label{tbl:needsAName}\n'
    s+='\end{center}\n' 
    s+='\end{table}\n'
   
    return s

"""
output1, output2, scoreMatrix = needleman_wunsch(seq1, seq2)
print(output1, "\n", output2)
"""
"""
#align the related SCPs
output1, output2, scoreMatrix = needleman_wunsch(c, d)
print(output1)
print(output2)

for i in scoreMatrix:
    print (i)

print ("score for alignment:", maxScore(scoreMatrix))

printAlignment(output1,output2)

#align the unrelated SCPs
output1, output2, scoreMatrix = needleman_wunsch(c, f)
print(output1)
print(output2)

for i in scoreMatrix:
    print (i)
"""

output1, output2, scoreMatrix = needleman_wunsch(d, d)

print ("score for alignment:", maxScore(scoreMatrix))

printAlignment(output1,output2)

#uncomment to see the socring matrix as a LaTex table
#print (matrixAsLatexRC(scoreMatrix,d,d))


