'''
4. Common Subexpression Elimination
eg. x1:=y+z -> x1:=y+z 
    x2:=y+z   x2:=x1
    
Placed after the constant folding

Author: Yanyu Yang 20075550

'''

# optimize for each block in the program
def general_sub_eliminate(program):

    for label in program:
        program[label] = common_sub_eliminate(program[label])

    return program

        
# optimize one single block
def common_sub_eliminate(block):
    existed_instruction = {}
    new_block = []
    
    for i in range(len(block)):
        r = block[i][0]
        value = str(block[i][1:]) #key = "["+", 1, 2]", value = r
        new_ins = []
        
        if value in existed_instruction and value != "goto" and value !="if":
            new_ins.append(r)
            new_ins.append(existed_instruction[value])
        else:
            new_ins = block[i]
            
        existed_instruction[value] = r
        new_block.append(new_ins)

    return new_block
            
                
def main():

    program = {'L0': [['r0', 'cos', 7], ['if', 'r3', '>', 'r1'], ['if', 'r2', '>', 'r4'], ['goto', 'L1']],
               'L1': [['r2', 'ln', 6], ['if', 2, '==', 'r2'], ['r0', '-', 'r2', 'r2'],['r1', 'e', 3]],
               'L2': [['r2', 'cos', 2], ['r1', 'sin', 'r3'], ['r2', '%', 3, 'r2'],['r0', 'ln', 8]],
               'L3': [['r0', '/', 'r4', 6], ['if', 2, '<', 6], ['r1', 'ln', 'r1']],
               'L4': [["x", "+", 1, 2],["y", "cos", 45], ["z","+", 1, 2]]}
    
    output1 = general_sub_eliminate(program)
    print(output1)
    

#main()
'''
    test_block = [["x", "+", 1, 2],["y", "cos", 45], ["z","+", 1, 2]]
    t1 = common_sub_eliminate(test_block)
    print(t1)
    
'''
