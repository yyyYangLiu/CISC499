'''
2. Constant Folding & Flow of Control Optimization
author: Yanyu Yang 20075550
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


# Constant Folding & Flow of Control Optimization
def constant_opti(argu):
    
    if "if" in argu[0]:
        return branch_opti(argu, argu[0])
    else:
        if len(argu) > 2:
            return arithmetic_opti(argu)
        return argu


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
# input format: ['if', 0, '>=', 'r1']
def branch_opti(argu_list, argu):
    num1 = argu[1]
    num2 = argu[3]
    operator = argu[2]
    
    if "if" in argu and is_number(num1) and is_number(num2) and condition_dict[operator](num1, num2) == False:
        return []
    
    return argu_list[-1]

    
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
    t1 = ["r0", "+", 1, 2]
    output1 = constant_opti(t1)
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

    set_labels = {"L1": [["r0", "+", 1, 2], [["if","2","<", "0"], ["goto", "L"]]], "L2": ["r1", "cos", 45]}
    set_jumps = {"J1": "L1", "J2": "L3", "J3": "L1"} # go through each instruction to get this set: jump to: label_x
    t5 = unreachable_label(set_labels, set_jumps)
    print(t5)

    
main()
