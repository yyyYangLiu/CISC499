'''
2. Constant Folding & Flow of Control Optimization
Author: Yanyu Yang 20075550
'''
import operator
import math

operator_dict = {
                '+' : operator.add,
                '-' : operator.sub,
                '*' : operator.mul,
                '/' : operator.truediv,
                '%' : operator.mod,
                '**': operator.pow
                }

condition_dict = {
                '>' : operator.gt,
                '<=': operator.le,
                '<' : operator.lt,
                '>=': operator.ge,
                '==': operator.eq}

function_dict = {
                'e' : math.exp,
                'ln': math.log,
                'squart_root': math.sqrt,
                'cos': math.cos,
                'sin': math.sin,
                }


# determine whether the string is a number
def is_number(s):
    
    try:
        float(s)
        return True
    except ValueError:
        pass
    
    return False


# optimize for each block
def general_constant_opti(program):

    # case1 and case2
    for label in program:
        program[label] = constant_opti(program[label])

    # case3
    unreachable_labels = get_goto_labels(program)
    for label in unreachable_labels:
        if label in program:
            del program[unreachable_labels[label]]

    return program


# returns the set of labels after "goto"
def get_goto_labels(program):
    
    goto_set = {}
    for label in program:
        for i in program[label]:
            if "goto" == i[0]:
                goto_set[label+"jumps_to"] = i[1]
                
    return goto_set
                
    
# Constant Folding & Flow of Control Optimization
# input a block: 2D list; returns updated block
def constant_opti(block):

    # case1
    for i in range(len(block)):
        if len(block[i]) > 2:
            block[i] = arithmetic_opti(block[i])

    # case2   
    block = branch_opti(block)

    return block


# Case1: compute operations on constants at compile time
def arithmetic_opti(argu):
    
    r = argu[0]
    result_list = []
    operator = argu[1]
    function = argu[1]
    
    # 2 arguments; arithmetic operations & power operation (eg. r = 1 * 1.2)
    # input foramt: ['r0', '**', 3, 1.3]
    if operator in operator_dict:
        operand_1 = argu[2]
        operand_2 = argu[3]
        if is_number(operand_1) and is_number(operand_2):
            result = operator_dict[operator](operand_1, operand_2)
            result_list.append(r)
            result_list.append(result)
            return result_list

    # 1 argument; functions (eg. r = cos(45.0))
    # input foramt: ['r0', 'cos', 45]
    if function in function_dict:
        parameter = argu[2]
        if is_number(parameter):        
            result = function_dict[function](parameter)
            result_list.append(r)
            result_list.append(result)
            return result_list
        
    return argu


# Case2: eliminate the instruction and operations if the condition is always false
# input format:  block: [['r0', 0.7539022543433046], ['if', '4', '>', '3'], ['if', '5', '>', '4'], ['goto', 'L1']]
def branch_opti(block):
    for index in range(len(block)-1, -1, -1):
        if index == len(block)-1 and "if" in block[index][0]:
            block.pop(index)
        else:
            if "if" in block[index][0]:
                if is_number(block[index][1]) and is_number(block[index][3]):
                    if condition_dict[block[index][2]](block[index][1], block[index][3]) == False:
                        block.pop(index)
                        block.pop(index+1)
                    else:
                        block.pop(index)
    return block
                          
    
# Case3: eliminating unreachable code: how to determine if the block can be reached or not? when the code is not jump_to, but also executed
# return labels of unreachable labeled blocks 
def unreachable_label(set_labels, set_jumps):
    
    jumps_to_list = []
    for i in set_jumps:
        jumps_to_list.append(set_jumps[i])

    unreach_block = []  
    for label in set_labels:
        if label not in jumps_to_list:
            unreach_block.append(label)
            
    return unreach_block


def main():

    program = {'L0': [['r0', '**', 'r1', 7], ['if', 'r3', '>', 'r1'], ['if', 'r2', '>', 'r4'], ['goto', 'L1']],
               'L1': [['r2', 'ln', 6], ['if', 2, '==', 'r2'], ['r0', '-', 'r2', 'r2'], ['r1', 'e', 3]],
               'L2': [['r2', 'cos', 2], ['r1', 'sin', 'r3'], ['r2', '%', 3, 'r2'], ['r0', 'ln', 8]],
               'L3': [['r0', '/', 'r4', 6], ['if', 2, '<', 6], ['r1', 'ln', 'r1']]}
    output1 = general_constant_opti(program)
    print(output1)
    
    set_labels = {"L1": [["r0", "+", 1, 2], [["if","2","<", "0"], ["goto", "L"]]], "L2": ["r1", "cos", 45]}
    set_jumps = {"J1": "L1", "J2": "L3", "J3": "L1"} # go through each instruction to get this set: jump to: label_x
    t5 = unreachable_label(set_labels, set_jumps)
    print(t5)


#main()
'''
d = {'L0': [['r0', 'cos', 7], ['if', 'r3', '>', 'r1'], ['if', 'r2', '>', 'r4'], ['goto', 'L1']],
      'L1': [['r2', 'ln', 6], ['if', 2, '==', 'r2'], ['r0', '-', 'r2', 'r2'], ['r1', 'e', 3]],
     'L2': [['r2', 'cos', 2], ['r1', 'sin', 'r3'], ['r2', '%', 3, 'r2']]}
     
#t1 = ["r0", "+", 1, 2]
output1 = general_constant_opti(d)
print(output1)


t2 = ["r1", "cos", 45]
output2 = constant_opti(t2)
print(output2)

t3 = [["if","2",">", "0"], ["goto", "L"]]
output3 = constant_opti(t3)
print(output3)

t4 = [["if","2","<", "0"], ["if","2",">", "0"], ["goto", "L"]]
output4 = constant_opti(t4)
print(output4)
'''
