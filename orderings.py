#Look for #IMPLEMENT tags in this file. These tags indicate what has
#to be implemented.

import random

'''
This file will contain different variable ordering heuristics to be used within
bt_search.

var_ordering == a function with the following template
    ord_type(csp)
        ==> returns Variable 

    csp is a CSP object---the heuristic can use this to get access to the
    variables and constraints of the problem. The assigned variables can be
    accessed via methods, the values assigned can also be accessed.

    ord_type returns the next Variable to be assigned, as per the definition
    of the heuristic it implements.

val_ordering == a function with the following template
    val_ordering(csp,var)
        ==> returns [Value, Value, Value...]
    
    csp is a CSP object, var is a Variable object; the heuristic can use csp to access the constraints of the problem, and use var to access var's potential values. 

    val_ordering returns a list of all var's potential values, ordered from best value choice to worst value choice according to the heuristic.

'''


def ord_random(csp):
    '''
    ord_random(csp):
    A var_ordering function that takes a CSP object csp and returns a Variable object var at random.  var must be an unassigned variable.
    '''
    var = random.choice(csp.get_all_unasgn_vars())
    return var


def val_arbitrary(csp,var):
    '''
    val_arbitrary(csp,var):
    A val_ordering function that takes CSP object csp and Variable object var,
    and returns a value in var's current domain arbitrarily.
    '''
    return var.cur_domain()


def ord_mrv(csp):
    '''
    ord_mrv(csp):
    A var_ordering function that takes CSP object csp and returns Variable object var, 
    according to the Minimum Remaining Values (MRV) heuristic as covered in lecture.  
    MRV returns the variable with the most constrained current domain 
    (i.e., the variable with the fewest legal values).
    '''
    remaining_values = 999999999
    avail_vars = csp.get_all_unasgn_vars()  
    cur = avail_vars[0]
    for v in csp.get_all_unasgn_vars():
        if v.cur_domain_size() < remaining_values:
            remaining_values = v.cur_domain_size()
            cur = v
            
    return cur
        
        
    
    
def ord_dh(csp):
    '''
    ord_dh(csp):
    A var_ordering function that takes CSP object csp and returns Variable object var,
    according to the Degree Heuristic (DH), as covered in lecture.
    Given the constraint graph for the CSP, where each variable is a node, 
    and there exists an edge from two variable nodes v1, v2 iff there exists
    at least one constraint that includes both v1 and v2,
    DH returns the variable whose node has highest degree.
    '''    
    
    max_degree = 0
    avail_vars = csp.get_all_unasgn_vars()
    cur = avail_vars[0]		
    for v in avail_vars:
        new_degree = find_degree(csp, v)
        if new_degree > max_degree:
            cur = v
            max_degree = new_degree

    return cur    
     
    #max_dh = None
    #for i in csp.vars_to_cons:
        #if (i in csp.get_all_unasgn_vars()) and (not max_dh or len(csp.vars_to_cons[max_dh]) < len(csp.vars_to_cons[i])):
            #max_dh = i
    #return max_dh    
            

def val_lcv(csp,var):
    '''
    val_lcv(csp,var):
    A val_ordering function that takes CSP object csp and Variable object var,
    and returns a list of Values [val1,val2,val3,...]
    from var's current domain, ordered from best to worst, evaluated according to the 
    Least Constraining Value (LCV) heuristic.
    (In other words, the list will go from least constraining value in the 0th index, 
    to most constraining value in the $j-1$th index, if the variable has $j$ current domain values.) 
    The best value, according to LCV, is the one that rules out the fewest domain values in other 
    variables that share at least one constraint with var.
    '''    
    var_values = var.cur_domain()
    constraints = csp.get_cons_with_var(var)
    order = []
    #calculate minmum domain for other var for all val
    for val in var_values:
        var.assign(val);
        var_pruning = {}
        #apply constraint to all left over related vars
        for con in constraints:
            for rel_var in con.get_unasgn_vars():
                #check support for each rel_val in rel var cur domain 
                for rel_val in rel_var.cur_domain():
                    if not con.has_support(rel_var, rel_val):

                        #add pruned val to dict
                        if not rel_var in var_pruning:
                            var_pruning[rel_var] = {}
                        var_pruning[rel_var][rel_val] = True


        #calculate new min domain size for each val
        new_domain_size = {}

        #calculate
        for v in var_pruning:
            new_domain_size[v] = len(v.cur_domain()) - len(var_pruning[v])
            #print(len(v.cur_domain()), len(var_pruning[v]), new_domain_size[v])
        
        if len(new_domain_size) > 0:
            order.append(min(new_domain_size.values()))
        else:
            order.append(0)
        var.unassign()


    ret_array = var.cur_domain()[:]
    
##    print(order)
    return [x for (y,x) in sorted(zip(order,ret_array), reverse=True)]


def ord_custom(csp):
    '''
    ord_custom(csp):
    A var_ordering function that takes CSP object csp and returns Variable object var,
    according to a Heuristic of your design.  This can be a combination of the ordering heuristics 
    that you have defined above.
    
    Return variable using MRV as main heuristic and DH as a tiebreaker
    '''    
    
    max_degree = 0
    remaining_vals = 9999999
    avail_vars = csp.get_all_unasgn_vars()
    cur = avail_vars[0]		
    for v in avail_vars:
        new_degree = find_degree(csp, v)
        if new_degree > max_degree:
            cur = v
            max_degree = new_degree
            remaining_vals = v.cur_domain_size()


    return cur    
            
def find_degree(csp, v):
    cons_num = 0
    cons = csp.get_cons_with_var(v)
    for con in cons:
        n_unasgn = con.get_n_unasgn()
        if n_unasgn > 1:
            cons_num += n_unasgn               
            
    return cons_num
    
    


