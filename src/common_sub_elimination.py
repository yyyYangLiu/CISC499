'''
4. Common Subexpression Elimination
eg. x1:=y+z -> x1:=y+z 
    x2:=y+z   x2:=x1
'''

def common_sub_eliminate(block):
    existed_instruction = {}
    new_block = []
    
    for i in range(len(block)):
        value = ''.join(block[i][2:])
        if value in existed_instruction:
            new_ins = block[i][0] + ':=' + existed_instruction[value]
        else:
            new_ins = ''.join(block[i])
        existed_instruction[value] = block[i][0]
        new_block.append(new_ins)
        
    return new_block
            
                
def main():
    
    block = [["x",":=","1","+","2"],
             ["y",":=","cos", "(", "45", ")"],
             ["z",":=","1","+","2"]
            ]
    t1 = common_sub_eliminate(block)
    print(t1)

main()
