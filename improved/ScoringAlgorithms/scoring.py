# Code in this file is modified from the code available publicly at:
#https://wilkelab.org/classes/SDS348/2019_spring/labs/lab13-solution.html


# Use these values to calculate scores
gap_penalty = -1
match_award = 1
mismatch_penalty = -1

# Make a score matrix with these two sequences
seq1 = "ATTACA"
seq2 = "ATGCT"

#seq1 = "ATT"
#seq2 = "ATG"
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
    if alpha == beta:
        return match_award
    elif alpha == '-' or beta == '-':
        return gap_penalty
    else:
        return mismatch_penalty







def needleman_wunsch(seq1, seq2):
    
    # Store length of two sequences
    n = len(seq1)  
    m = len(seq2)
    
    # Generate matrix of zeros to store scores
    score = zeros(m+1, n+1)
   
    # Calculate score table
    
    # Fill out first column
    for i in range(0, m + 1):
        score[i][0] = gap_penalty * i
    
    # Fill out first row
    for j in range(0, n + 1):
        score[0][j] = gap_penalty * j
    
    # Fill out all other values in the score matrix
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            # Calculate the score by checking the top, left, and diagonal cells
            match = score[i - 1][j - 1] + match_score(seq1[j-1], seq2[i-1])
            delete = score[i - 1][j] + gap_penalty
            insert = score[i][j - 1] + gap_penalty
            # Record the maximum score from the three possible scores calculated above
            score[i][j] = max(match, delete, insert)
    
    # Traceback and compute the alignment 
    print ("THE MATRIX IS")
    for row in score:
        print (row)
    
    # Create variables to store alignment
    align1 = ""
    align2 = ""
    
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
            align1 += seq1[j-1]
            align2 += seq2[i-1]
            i -= 1
            j -= 1
        elif score_current == score_up + gap_penalty:
            align1 += seq1[j-1]
            align2 += '-'
            j -= 1
        elif score_current == score_left + gap_penalty:
            align1 += '-'
            align2 += seq2[i-1]
            i -= 1

    # Finish tracing up to the top left cell
    while j > 0:
        align1 += seq1[j-1]
        align2 += '-'
        j -= 1
    while i > 0:
        align1 += '-'
        align2 += seq2[i-1]
        i -= 1
    
    # Since we traversed the score matrix from the bottom right, our two sequences will be reversed.
    # These two lines reverse the order of the characters in each sequence.
    align1 = align1[::-1]
    align2 = align2[::-1]
    
    return(align1, align2, score)


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
    for i in range (0,len(matrix)):
        print (i)
        if i>=1:
            s+= c[i-1]+' & '
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
def matrixAsLatex(matrix):
    s='\\begin{table}\n'
    s+='\\begin{center}\n'
    s+='\\begin{tabular}{'
    s+='c '* len(matrix[0])
    s+='}\n & '
    s+="\n"
    for i in range (0,len(matrix)):
        
        for j in range (0, len(matrix[0])):
            s+=str(matrix[i][j])+ (' & ' if j!=len(matrix[0])-1 else '')
        s+=('' if i==len(matrix)-1 else '\\\\')+ '\n'
    s+='\\end{tabular}\n'   
    s+='\caption{no caption}\n'
    s+='\label{tbl:needsAName}\n'
    s+='\end{center}\n' 
    s+='\end{table}\n'
   
    return s   


output1, output2, matrix = needleman_wunsch(seq1, seq2)

print(output1 + "\n" + output2)


print (matrixAsLatexRC(matrix,seq1,seq2))















