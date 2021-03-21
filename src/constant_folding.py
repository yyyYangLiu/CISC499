'''
2. Constant Folding & Flow of Control Optimization
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
        return arithmetic_opti(argu)


# Case1: compute operations on constants at compile time
def arithmetic_opti(argu):

    # 2 arguments; arithmetic operations & power operation (eg. r = 1 * 1.2)
    if argu[3] in operator_dict and is_number(argu[2]) and is_number(argu[4]):
        new_argu = str( operator_dict[argu[3]](float(argu[2]), float(argu[4])) )
        return argu[0] + argu[1] + new_argu

    # 1 argument; functions (eg. r = cos(45.0))
    if argu[2] in function_dict and is_number(argu[4]):
        new_argu = str( function_dict[argu[2]](float(argu[4])) )
        return argu[0] + argu[1] + new_argu


# Case2: eliminate the instruction and operations if the condition is always false
def branch_opti(argu_list, argu):
    if "if" in argu and is_number(argu[1]) and is_number(argu[3]) and condition_dict[argu[2]](float(argu[1]), float(argu[3])) == False:
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
    t1 = ["x",":=","1","+","2"]
    output1 = constant_opti(t1)
    print(output1)

    t2 = ["x",":=","cos", "(", "45", ")"]
    output2 = constant_opti(t2)
    print(output2)

    t3 = [["if","2","<", "0"], ["goto", "L"]]
    output3 = constant_opti(t3)
    print(output3)

    t4 = [["if","2",">", "0"], ["if","2",">", "0"], ["goto", "L"]]
    output4 = constant_opti(t4)
    print(output4)

    set_labels = {"L1": [["x",":=","1","+","2"], [["if","2","<", "0"], ["goto", "L"]]], "L2": ["x",":=","cos", "(", "45", ")"]}
    set_jumps = {"J1": "L1", "J2": "L3", "J3": "L1"}
    t5 = unreachable_label(set_labels, set_jumps)
    print(t5)

    
main()
