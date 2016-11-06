#Look for #IMPLEMENT tags in this file. These tags indicate what has
#to be implemented to complete the hitori models.  

'''
Construct and return hitori CSP models.
'''

from cspbase import *
import itertools

def hitori_csp_model_1(initial_hitori_board):
    '''Return a CSP object representing a hitori CSP problem along 
       with an array of variables for the problem. That is return

       hitori_csp, variable_array

       where hitori_csp is a csp representing hitori using model_1
       and variable_array is a list of lists

       [ [  ]
         [  ]
         .
         .
         .
         [  ] ]

       such that variable_array[i][j] is the Variable (object) that
       you built to represent the value to be placed in cell i,j of
       the hitori board (indexed from (0,0) to (8,8))

       
       
       The input board is specified as a list of n lists. Each of the
       n lists represents a row of the board. Each item in the list 
       represents a cell, and will contain a number between 1--n.
       E.g., the board
    
       -------------------  
       |1|3|4|1|
       |3|1|2|4|
       |2|4|2|3|
       |1|2|3|2|
       -------------------
       would be represented by the list of lists
       
       [[1,3,4,1],
       [3,1,2,4],
       [2,4,2,3],
       [1,2,3,2]]
       
       This routine returns Model_1 which consists of a variable for
       each cell of the board, with domain equal to {0,i}, with i being
       the initial value of the cell in the board. 
       
       Model_1 also contains BINARY CONSTRAINTS OF NOT-EQUAL between
       all relevant variables (e.g., all pairs of variables in the
       same row, etc.)
       
       All of the constraints of Model_1 MUST BE binary constraints 
       (i.e., constraints whose scope includes exactly two variables).
    '''

##IMPLEMENT
    variable_array = calc_variable_array_2d(initial_hitori_board)
    lin_array = []
    for row in variable_array:
        lin_array.extend(row)    
        
    hitori_csp = CSP("hitori_csp", lin_array)        
    BinaryColumnConstraintArray = create_binary_col_constr(variable_array)
    BinaryRowConstraintArray = create_binary_row_constr(variable_array)
    all_constraints = []
    all_constraints.extend(BinaryColumnConstraintArray)
    all_constraints.extend(BinaryRowConstraintArray)

    for c in all_constraints:
        hitori_csp.add_constraint(c)
        
    return hitori_csp,variable_array
def create_binary_row_constr(variable_array):
    constraint_array = []
    length = len(variable_array)
    
    domain = []
    for i in range(length+1):
        domain.append(i)    
    for row in variable_array:
        for pivot_i in range(length):
            for compare_i in range(length):
                if not pivot_i == compare_i:
                    c = Constraint("BinaryRowCons" + str(row)+":"+str(pivot_i)+","+str(compare_i), [row[pivot_i], row[compare_i]])
                    constraint_tuples = []
                    domains = [row[pivot_i].domain(), row[compare_i].domain()]
                    for perm in binary_filter(itertools.product(*domains), compare_i, pivot_i):
                        constraint_tuples.append(tuple(perm))                    
                    c.add_satisfying_tuples(constraint_tuples)
                    constraint_array.append(c)
                    
    return constraint_array
    

        
def create_binary_col_constr(variable_array):
    constraint_array = []
    length = len(variable_array)
    
    domain = []
    for i in range(length+1):
        domain.append(i)   
        
        
    for col_i in range(length):
        col = []
        for row in variable_array:
            col.append(row[col_i])       
            
        for pivot_i in range(length):
            for compare_i in range(length):
                if not pivot_i == compare_i:
                    c = Constraint("BinaryColCons" + str(col_i)+":"+str(pivot_i)+","+str(compare_i), [variable_array[pivot_i][col_i], variable_array[compare_i][col_i]])
                    constraint_tuples = []
                    domains = [variable_array[pivot_i][col_i].domain(), variable_array[compare_i][col_i].domain()]
                    
                    for con in binary_filter(itertools.product(*domains), pivot_i, compare_i):
                        constraint_tuples.append(tuple(con))                                        
                    c.add_satisfying_tuples(constraint_tuples)
                    constraint_array.append(c)    
                    
    return constraint_array
def binary_filter(perms, i, j):
    ret = []
    for perm in perms:
        conflict = False
        if perm[0] == 0 and perm[1] == 0 and abs(i-j) == 1:
            conflict = True
        if perm[0] != 0 and perm[1] == perm[0]:
            conflict = True
        if not conflict:
            ret.append(perm)
    return ret

    
def calc_variable_array_2d(initial_hitori_board):
    variable_array = []
    for row in range(len(initial_hitori_board)):
        r = []
        for col in range(len(initial_hitori_board)):
            name = str(row)+","+str(col)
            r.append(Variable(name, domain=[0, initial_hitori_board[row][col]]))
        variable_array.append(r)
    return variable_array
    
                                          
    
    
##############################

def hitori_csp_model_2(initial_hitori_board):
    '''Return a CSP object representing a hitori CSP problem along 
       with an array of variables for the problem. That is return

       hitori_csp, variable_array

       where hitori_csp is a csp representing hitori using model_1
       and variable_array is a list of lists

       [ [  ]
         [  ]
         .
         .
         .
         [  ] ]

       such that variable_array[i][j] is the Variable (object) that
       you built to represent the value to be placed in cell i,j of
       the hitori board (indexed from (0,0) to (8,8))

       
       
       The input board is specified as a list of n lists. Each of the
       n lists represents a row of the board. Each item in the list 
       represents a cell, and will contain a number between 1--n.
       E.g., the board
    
       -------------------  
       |1|3|4|1|
       |3|1|2|4|
       |2|4|2|3|
       |1|2|3|2|
       -------------------
       would be represented by the list of lists
       
       [[1,3,4,1],
       [3,1,2,4],
       [2,4,2,3],
       [1,2,3,2]]

       The input board takes the same input format (a list of n lists 
       specifying the board as hitori_csp_model_1).
   
       The variables of model_2 are the same as for model_1: a variable
       for each cell of the board, with domain equal to {0,i}, where i is
       the initial value of the cell.

       However, model_2 has different constraints.  In particular, instead
       of binary not-equals constraints, model_2 has 2n n-ary constraints
       that resemble a modified all-different constraint.  Each constraint
       is over n variables.  For any given row (resp. column), that 
       constraint will incorporate both the adjacent black squares and 
       no repeated numbers rules.
       
    '''

    ##IMPLEMENT
    variable_array = calc_variable_array_2d(initial_hitori_board)
    lin_array = []
    for row in variable_array:
        lin_array.extend(row)    
        
    hitori_csp = CSP("hitori_csp", lin_array)    
    
    BinaryColumnConstraintArray = create_nnary_col_constr(variable_array)
    BinaryRowConstraintArray = create_nnary_row_constr(variable_array)
    all_constraints = []
    all_constraints.extend(BinaryColumnConstraintArray)
    all_constraints.extend(BinaryRowConstraintArray)
    for c in all_constraints:
        hitori_csp.add_constraint(c)
        
    return hitori_csp,variable_array

def filter_row_or_col(perm_list):
    ret = []
    
    for perm in perm_list:
        
        conflict = False
        for i,val in enumerate(perm):
            if val <0 or val > len(perm):
                conflict = True
            if val == 0:
                
                if i > 0 and perm[i-1] == 0:
                    conflict = True
                    break
                if i < len(perm)-1 and perm[i+1] == 0:
                    conflict = True
                    break
            else:
                if i < len(perm)-1:
                    for val2_i in range(i+1, len(perm)):
                        val2 = perm[val2_i]
                        if val == val2:
                            conflict = True
                            break
            if(conflict):
                break
        if not conflict:
            ret.append(tuple(perm))

    return ret
                
                    
                        
                
def create_nnary_row_constr(variable_array):
    constraint_array = []
    length = len(variable_array)
    domain = []
    for i in range(length+1):
        domain.append(i)       
    for row in variable_array:
        for pivot_i in range(length):
            for compare_i in range(length):
                if not pivot_i == compare_i:
                    c = Constraint("NnaryRowCons" + str(row)+":"+str(pivot_i)+","+str(compare_i), row)
                    constraint_tuples = []
                    
                    domains = []
                    for var in row:
                        domains.append(var.domain())

                    for tup in filter_row_or_col(itertools.product(*domains)):
                        constraint_tuples.append(tup)                    
                    c.add_satisfying_tuples(constraint_tuples)
                    constraint_array.append(c)
    return constraint_array
    
def create_nnary_col_constr(variable_array):
    constraint_array = []
    length = len(variable_array)
    
    domain = []
    for i in range(length+1):
        domain.append(i)   
        
    for col_i in range(length):
        col = []
        for row in variable_array:
            col.append(row[col_i])        
        for pivot_i in range(length):
            for compare_i in range(length):
                if not pivot_i == compare_i:
                    
                    c = Constraint("BinaryColCons" + str(col_i)+":"+str(pivot_i)+","+str(compare_i), col)
                    constraint_tuples = []
                    
                    domains = []
                    for var in col:
                        domains.append(var.domain())

                    for tup in filter_row_or_col(itertools.product(*domains)):
                        constraint_tuples.append(tup)                    
                    c.add_satisfying_tuples(constraint_tuples)
                    constraint_array.append(c)
                    
    return constraint_array


