'''
adapting

Testing for
2.constant folding
4.eliminating subexpression

Modification Notes:
add assignment "r = 1" case in execute()
delete print section in random_program()
delete parameter "num" in execute()
main() and testing(): use "label" for execute() YY

'''
# Test File
# by Jinting Zhang
# Assignment 5 - LGP program generation structural intron removal

import random
import math
import constant_folding
import common_sub_elimination
import copy

def random_program(num, prog_length, totalLabel):
    # setting parameters
    n_calculation_reg = 3  # {r0, r1, r2} and r0 is designated as the output register
    n_input_reg = 2  # {r3, r4}
    n_operators = 6  # {+, -, *, /, %, **}
    n_constant = 5  # {1, 2, 3, 4, 5}
    constant_rate = 0.4  # An operand can be a constant with a 40% chance, however, both operands cannot be constants
    # at the same time

    # Randomly generate an LGP program with no more than [max_prog_length] instructions
    # An instruction can be represented by a list of elements,
    # An LGP program is thus a list of instructions
    program = []
    calculation_registers = ['r0', 'r1', 'r2']
    input_registers = ['r3', 'r4']
    operators = ['+', '-', '*', '/', '%', '**']
    constants = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]  # random float???
    functions = ['e', 'ln', 'cos', 'sin']
    condition = ['>', '>=', '<', '<=', '==']
    choiceOfGoto = 2
    #   print("Program length: ", prog_length)
    for i in range(0, prog_length):
        instruction = []
        if choiceOfGoto == 1 and totalLabel - 1 > num:
            instruction.append("goto")
            label_num = random.randint(0, totalLabel - 1)
            while label_num <= num:
                label_num = random.randint(0, totalLabel - 1)
            instruction.append("L" + str(label_num))
            program.append(instruction)
            choiceOfGoto = 2
        else:
            choice = random.randint(1, 3)
            if choice == 1:
                instruction.append(random.choice(calculation_registers))  # return register
                instruction.append(random.choice(operators))  # operator
                if random.random() < constant_rate:
                    instruction.append(random.choice(constants))  # first operand
                    instruction.append(random.choice(calculation_registers + input_registers))  # second operand
                else:
                    instruction.append(random.choice(calculation_registers + input_registers))  # first operand
                    if random.random() < constant_rate:
                        instruction.append(random.choice(constants))  # second operand
                    else:
                        instruction.append(random.choice(calculation_registers + input_registers))  # second operand
                program.append(instruction)
            elif choice == 2:
                instruction.append(random.choice(calculation_registers))  # return register
                instruction.append(random.choice(functions))  # function
                choiceOfNum = random.randint(1, 2)
                if choiceOfNum == 1:
                    instruction.append(random.choice(constants))
                else:
                    instruction.append(random.choice(calculation_registers + input_registers))
                program.append(instruction)
            elif choice == 3: # i != program - 1
                instruction.append('if')
                choiceOfNum = random.randint(1, 2)
                if choiceOfNum == 1:
                    instruction.append(random.choice(constants))
                else:
                    instruction.append(random.choice(calculation_registers + input_registers))
                instruction.append(random.choice(condition))
                choiceOfNum = random.randint(1, 2)
                if choiceOfNum == 1:
                    instruction.append(random.choice(constants))
                else:
                    instruction.append(random.choice(calculation_registers + input_registers))
                program.append(instruction)
                choiceOfGoto = random.randint(1, 2)

    # Print the LGP program as a list of instructions
    # An instruction should be printed as, for instance r1 = r3 + r0 or r2 = r0 * 5
    '''
    print("The randomly generated LGP program is:")
    for i in range(0, prog_length):
        if len(program[i]) == 4:
            if program[i][0] == 'if':
                print(program[i][0], program[i][1], program[i][2], program[i][3])
            else:
                print(program[i][0], "=", program[i][2], program[i][1], program[i][3])
        elif len(program[i]) == 3:
            print(program[i][0], "=", program[i][1], program[i][2])
        elif len(program[i]) == 2:
            print(program[i][0] + " " + program[i][1])
    
    return program
    '''
    program_ls = []
    #print("The randomly generated LGP program is:")
    for i in range(0, prog_length):
        program_ls.append([])
        if len(program[i]) == 4:
            if program[i][0] == 'if':
                #print(program[i][0], program[i][1], program[i][2], program[i][3])
                program_ls[i] = [program[i][0], program[i][1], program[i][2], program[i][3]]
            else:
                #print(program[i][0], "=", program[i][2], program[i][1], program[i][3])
                program_ls[i] = [program[i][0], ":=", program[i][2], program[i][1], program[i][3]]
        elif len(program[i]) == 3:
            #print(program[i][0], "=", program[i][1], program[i][2])
            program_ls[i] = [program[i][0], ":=", program[i][1], program[i][2]]
        elif len(program[i]) == 2:
            #print(program[i][0] + " " + program[i][1])
            program_ls[i] = [program[i][0], " ", program[i][1]]


    return program,program_ls


# A function defined to test if-condition
# A helper function of execute function

def test_condition(line, dic):
    if line[2] == '>':
        if (line[1] in dic) & (line[3] in dic):
            return dic[line[1]] > dic[line[3]]
        elif (line[1] in dic) & (not isinstance(line[3], str)):
            return dic[line[1]] > line[3]
        elif (not isinstance(line[1], str)) & (line[3] in dic):
            return line[1] > dic[line[3]]
        elif (not isinstance(line[1], str)) & (not isinstance(line[3], str)):
            return line[1] > line[3]

    elif line[2] == '>=':
        if (line[1] in dic) & (line[3] in dic):
            return dic[line[1]] >= dic[line[3]]
        elif (line[1] in dic) & (not isinstance(line[3], str)):
            return dic[line[1]] >= line[3]
        elif (not isinstance(line[1], str)) & (line[3] in dic):
            return line[1] >= dic[line[3]]
        elif (not isinstance(line[1], str)) & (not isinstance(line[3], str)):
            return line[1] >= line[3]

    elif line[2] == '<':
        if (line[1] in dic) & (line[3] in dic):
            return dic[line[1]] < dic[line[3]]
        elif (line[1] in dic) & (not isinstance(line[3], str)):
            return dic[line[1]] < line[3]
        elif (not isinstance(line[1], str)) & (line[3] in dic):
            return line[1] < dic[line[3]]
        elif (not isinstance(line[1], str)) & (not isinstance(line[3], str)):
            return line[1] < line[3]

    elif line[2] == '<=':
        if (line[1] in dic) & (line[3] in dic):
            return dic[line[1]] <= dic[line[3]]
        elif (line[1] in dic) & (not isinstance(line[3], str)):
            return dic[line[1]] <= line[3]
        elif (not isinstance(line[1], str)) & (line[3] in dic):
            return line[1] <= dic[line[3]]
        elif (not isinstance(line[1], str)) & (not isinstance(line[3], str)):
            return line[1] <= line[3]

    elif line[2] == '==':
        if (line[1] in dic) & (line[3] in dic):
            return dic[line[1]] == dic[line[3]]
        elif (line[1] in dic) & (not isinstance(line[3], str)):
            return dic[line[1]] == line[3]
        elif (not isinstance(line[1], str)) & (line[3] in dic):
            return line[1] == dic[line[3]]
        elif (not isinstance(line[1], str)) & (not isinstance(line[3], str)):
            return line[1] == line[3]


# Execute the random program

def execute(program, prog_length, register_dic):
    if_statement = True
    for i in range(0, prog_length):
        if if_statement:
            if len(program[i]) == 2 and program[i][0] != "goto" and program[i][0] != "if":
                if isinstance(program[i][1], str):
                    program[i][1] = register_dic[program[i][1]]
                updateDic = {program[i][0]: program[i][1]}
                register_dic.update(updateDic)
                
            if program[i][1] == "+":
                if isinstance(program[i][2], str):
                    program[i][2] = register_dic[program[i][2]]
                if isinstance(program[i][3], str):
                    program[i][3] = register_dic[program[i][3]]
                updateDic = {program[i][0]: program[i][2] + program[i][3]}
                register_dic.update(updateDic)
            if program[i][1] == "-":
                if isinstance(program[i][2], str):
                    program[i][2] = register_dic[program[i][2]]
                if isinstance(program[i][3], str):
                    program[i][3] = register_dic[program[i][3]]
                updateDic = {program[i][0]: program[i][2] - program[i][3]}
                register_dic.update(updateDic)
            if program[i][1] == "*":
                if isinstance(program[i][2], str):
                    program[i][2] = register_dic[program[i][2]]
                if isinstance(program[i][3], str):
                    program[i][3] = register_dic[program[i][3]]
                updateDic = {program[i][0]: program[i][2] * program[i][3]}
                register_dic.update(updateDic)
            if program[i][1] == "/":
                if isinstance(program[i][2], str):
                    program[i][2] = register_dic[program[i][2]]
                if isinstance(program[i][3], str):
                    program[i][3] = register_dic[program[i][3]]
                if program[i][3] == 0:
                    print("Division by zero, fail!")
                    break
                updateDic = {}
                updateDic[program[i][0]] = program[i][2] / program[i][3]
                register_dic.update(updateDic)
            if program[i][1] == "%":
                if isinstance(program[i][2], str):
                    program[i][2] = register_dic[program[i][2]]
                if isinstance(program[i][3], str):
                    program[i][3] = register_dic[program[i][3]]
                if program[i][3] == 0:
                    print("Division by zero, fail!")
                    break
                updateDic = {program[i][0]: program[i][2] % program[i][3]}
                register_dic.update(updateDic)
            if program[i][1] == "**":
                if isinstance(program[i][2], str):
                    program[i][2] = register_dic[program[i][2]]
                if isinstance(program[i][3], str):
                    program[i][3] = register_dic[program[i][3]]
                updateDic = {program[i][0]: program[i][2] ** program[i][3]}
                register_dic.update(updateDic)
            if program[i][1] == 'e':
                if isinstance(program[i][2], str):
                    program[i][2] = register_dic[program[i][2]]
                updateDic = {program[i][0]: math.exp(program[i][2])}
                register_dic.update(updateDic)
            if program[i][1] == 'ln':
                if isinstance(program[i][2], str):
                    program[i][2] = register_dic[program[i][2]]
                if program[i][2] <= 0:
                    print("ln fails!")
                    break
                updateDic = {program[i][0]: math.log(program[i][2])}
                register_dic.update(updateDic)
            if program[i][1] == 'cos':
                if isinstance(program[i][2], str):
                    program[i][2] = register_dic[program[i][2]]
                updateDic = {program[i][0]: math.cos(program[i][2])}
                register_dic.update(updateDic)
            if program[i][1] == 'sin':
                if isinstance(program[i][2], str):
                    program[i][2] = register_dic[program[i][2]]
                updateDic = {program[i][0]: math.sin(program[i][2])}
                register_dic.update(updateDic)
            if program[i][0] == 'if':
                if_statement = test_condition(program[i], register_dic)
            if program[i][0] == 'goto':
                return int(program[i][1][1:]), register_dic
        if not if_statement:
            if program[i][0] != 'if':
                if_statement = True

    return register_dic

#------------------------------------------------
def alge_opti(argu):
  if len(argu)>=4:
    if argu[0]==argu[2] and argu[3]=="+" and argu[4]=="0":
      return None
    if argu[0]==argu[2] and argu[3]=="*" and argu[4]=="1":
      return None
    if argu[3]=="*" and argu[4]=="0":
      return argu[0]+argu[1]+argu[4]
    if argu[3]=="**" and argu[4]=="2":
      return argu[0]+argu[1]+argu[2]+"*"+argu[2]
  return argu

def single_assign(argu_list):
  # step 1 record repeated elem

  # here argu_list is all the instructions and this is a 2-d list
  left_list=[]
  right_list=[]
  # get all the LHS of instruction and put into argu_list
  print(argu_list)
  for i in range(len(argu_list)):
    left_list.append(argu_list[i][0])

  left_set=list(set(left_list))

  num_len=len(left_set)
  register_list=[]
  # count number of elem and put result into register_list
  # in this case register_list is [[[0, 3, 4],'x'], [[1, 2],'a']]
  if num_len<len(left_list):
    for i in range(num_len):
      temp=[]
      var=left_set[i]
      num_elem=left_list.count(var)
      if num_elem>1:
        temp.append([j for j,x in enumerate(left_list) if x == var])
        temp.append(var)
        register_list.append(temp)
  
  # step 2 update 
  # x and a
  for i in range(len(register_list)):
    var = register_list[i][1]
    if var != "goto" and var != "if":
      new_name=""
      # change LHS x in 3 and 4 
      for j in range(len(register_list[i][0])-1):
        # take x for example, register_list[0][0] is [0,3,4],register_list[0][1] is 'x'    
        # change LHS x in 3 and 4 
        in_dex = register_list[i][0][j+1]
        new_name = register_list[i][1]+str(j)
        argu_list[in_dex][0]=new_name
        
        # change RHS, eg: all instructions (3,4] to x0， (4，end] to x1 , (2,end] to a0
        if j+2 <= len(register_list[i][0])-1:
          index_next=register_list[i][0][j+2]
        else:
          index_next=len(argu_list)-1
        
        for j in range(in_dex+1,index_next+1):
          right_list= argu_list[j][1:]
          for k in range(len(right_list)):
            if right_list[k]==var:
              argu_list[j][k+1]=new_name


  return argu_list
  
def copy_propagation(argu_list):
    for i in range(len(argu_list)):
        if argu_list[i][1]==":=" and len(argu_list[i])==3:
            # replace all i[0] to i[2] in all the RHS of following instructions
            for j in argu_list[i+1:]:
                for k in range(len(j)):
                    if k>0 and j[k]==argu_list[i][0]:
                        j[k]=argu_list[i][2]
    # call constant folding function here

    # dead code elimination
    temp_list=argu_list[:]
    for i in range(len(temp_list)):
      if temp_list[i][1]==":=" and len(temp_list[i])==3:
        # replace all i[0] to i[2] in all the RHS of following instructions
          for j in range(len(temp_list)):
            if not(i!=j and (temp_list[i][0] in temp_list[j])):
              #delete the basic block which is dead:
              del argu_list[i]
              break
    return argu_list
                    

def transform(program):
  new_ls=[] 
  for i in range(len(program)): 
    new_ls.append([])
    if len(program[i]) == 5 and program[i][1]==":=":
        new_ls[i]=[program[i][0], program[i][3], program[i][2], program[i][4]]
    elif len(program[i]) == 4 and program[i][1]==":=": 
        new_ls[i] = [program[i][0], program[i][2], program[i][3]] 
    elif program[i][0] == "goto":
        new_ls[i] = [program[i][0],program[i][2]]  
    else:
      new_ls[i] = program[i]
  return new_ls
                    
def optimization(argu_list):
  ls=[]
  for i in range(len(argu_list)):
    ls.append(alge_opti(argu_list[i]))

  ls=single_assign(ls)

  ls=copy_propagation(ls)

  # after optimization, transform it
  ls=transform(ls)
  #print("after transform",ls)
  return ls

#------------------------------------------------


def testing():
    max_prog_length = 6  # 6 instructions in total is the upper limit
    totalLabel = random.randint(1, 6)

    dic_program = {}#he
    dic_copy={}#he
    
    # generate program
    dic_program = {}
    for i in range(totalLabel):
        prog_length = random.randint(1, max_prog_length)
        program, program_ls = random_program(i, prog_length, totalLabel)#he
        label = "L" + str(i)
        dic_program[label] = program

        optim_program=optimization(program_ls)#he
        dic_copy[label]=optim_program         #he
    '''
    dic_program = {"L0": [["r0", "/", 0, 0]]}
    '''
    # optimization process
    # c = copy.deepcopy(dic_program)
    c = copy.deepcopy(dic_program)
    constant_folding.general_constant_opti(dic_copy)
    common_sub_elimination.general_sub_eliminate(dic_copy)
    

    #print
    print("\nOriginal Program:\n")# hard copy
    for i in c:
        print(i + " " + str(c[i]) + "\n")
    print("\nOptimization Program:\n")# dic_program
    for i in dic_copy:
        print(i + " " + str(dic_copy[i]) + "\n")

    # before
    register_dic = {'r0': 1.5, 'r1': 1.5, 'r2': 1.5, 'r3': 1.5, 'r4': 1.5}
    for label in c:
        program = c[label]
        execute(program, len(program), register_dic)
    print("\nOriginal result:", register_dic)

    # after
    compare_dic = {'r0': 1.5, 'r1': 1.5, 'r2': 1.5, 'r3': 1.5, 'r4': 1.5}
    for label in dic_copy:
        program = dic_copy[label]
        execute(program, len(program), compare_dic)
    print("\nOptimiza result:", compare_dic)

    return register_dic, compare_dic


# compare the result
def main():
    for i in range(3):
        register_dic, compare_dic = testing()
        if register_dic == compare_dic:
            print("\nThe results are the same!\n\n")
            

main()
