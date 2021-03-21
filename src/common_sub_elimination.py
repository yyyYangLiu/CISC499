'''
4. Common Subexpression Elimination
eg. x1:=y+z -> x1:=y+z 
    x2:=y+z   x2:=x1
    
Author: Yanyu Yang 20075550
'''

def common_sub_eliminate(block):
    existed_instruction = {}
    new_block = []
    
    for i in range(len(block)):
        r = block[i][0]
        value = str(block[i][1:]) #key = "["+", 1, 2]", value = r
        new_ins = []
        
        if value in existed_instruction:
            new_ins.append(r)
            new_ins.append(existed_instruction[value])
        else:
            new_ins = block[i]
            
        existed_instruction[value] = r
        new_block.append(new_ins)

    return new_block
            
                
def main():
    
    test_block = [["x", "+", 1, 2],
                 ["y", "cos", 45],
                 ["z","+", 1, 2]]
    
    t1 = common_sub_eliminate(test_block)
    print(t1)
    

main()
