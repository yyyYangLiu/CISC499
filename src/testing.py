# Test File
# by Jinting Zhang
# Assignment 5 - LGP program generation structural intron removal

import random
import math
import copy
import csv

import opti1
import opti2

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
    program_copy = copy.deepcopy(program)
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
                if program[i][3] == 0:
                    print("Division by zero, fail!")
                    break
                if isinstance(program[i][2], str):
                    program[i][2] = register_dic[program[i][2]]
                if isinstance(program[i][3], str):
                    program[i][3] = register_dic[program[i][3]]
                updateDic = {}
                try:
                    updateDic[program[i][0]] = program[i][2] / program[i][3]
                except:
                    print("Zero Division Error!")
                register_dic.update(updateDic)
            if program[i][1] == "%":
                if isinstance(program[i][2], str):
                    program[i][2] = register_dic[program[i][2]]
                if isinstance(program[i][3], str):
                    program[i][3] = register_dic[program[i][3]]
                if program[i][3] == 0:
                    print("Division by zero, fail!")
                    break
                try:
                    updateDic = {program[i][0]: program[i][2] % program[i][3]}
                except:
                    print("Zero Division Error!")
                register_dic.update(updateDic)
            if program[i][1] == "**":
                if isinstance(program[i][2], str):
                    program[i][2] = register_dic[program[i][2]]
                if isinstance(program[i][3], str):
                    program[i][3] = register_dic[program[i][3]]
                try:
                    updateDic = {program[i][0]: program[i][2] ** program[i][3]}
                except:
                    print("Math error: ZeroDivisionError: 0.0 cannot be raised to a negative power! ")
                register_dic.update(updateDic)
            if program[i][1] == 'e':
                if isinstance(program[i][2], str):
                    program[i][2] = register_dic[program[i][2]]
                try:
                    updateDic = {program[i][0]: math.exp(program[i][2])}
                except:
                    print("Math error: math range error! ")
                register_dic.update(updateDic)
            if program[i][1] == 'ln':
                if isinstance(program[i][2], str):
                    program[i][2] = register_dic[program[i][2]]
                if program[i][2] <= 0:
                    print("Math Error: ln() fails!")
                    break
                try:
                    updateDic = {program[i][0]: math.log(program[i][2])}
                except:
                    print("Math Error: ln(x) where x can not be 0")
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
                if if_statement==False:
                
                  if len(program_copy)>i+1:
                    del program_copy[i+1]
                    del program_copy[i]
            '''
            #---------update yy------
            if program[i][0] == 'if': #[["if", "r1", "<", "r2"], ["r11", "r20"]]
                if_statement = test_condition(program[i], register_dic)
                if if_statement == False and program[i] != program[-1]:
                    for e in program[i+1]:
                        if isinstance(e, str) and e[0] == "r" and len(e) > 2:
                            if int(e[2:]) == 0: #'0'
                                old = e[0:2]
                                updateDic = {program[i+1][0]: register_dic[old]}
                                register_dic.update(updateDic)
                            if int(e[2:]) > 0:
                                mark = str(int(e[2:]) - 1) # after:"r1"+"1"
                                old = e[0:2]+mark
                                updateDic = {program[i+1][0]: register_dic[old]}
                                register_dic.update(updateDic) 
            #---------update yy------
            '''                    
            if program[i][0] == 'goto':
                return register_dic, program_copy, int(program[i][1][1:])
                
        if not if_statement:
            if program[i][0] != 'if':
                if_statement = True

    return register_dic, program_copy, 999

#---hy-update
def before_trans(program):
    program_ls = []
    prog_length=len(program)
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
#---hy-update


#-----YY---update
def element_length(d):
    count = 0
    for k in d:         #[['r2', 'cos', 'r2'], ['r1', '/', 7, 'r1'], ['if', 5, '<', 'r0'], ['r0', 'sin', 'r1']]
        for i in d[k]:  #['r2', 'cos', 'r2']
            count = len(i) + count
    return count
            
        
def instruction_length(d):
    count = 0
    for k in d:         #[['r2', 'cos', 'r2'], ['r1', '/', 7, 'r1'], ['if', 5, '<', 'r0'], ['r0', 'sin', 'r1']]
        count = len(d[k]) + count
    return count


# result for element reduction        
def result1(before, after):
    before_len = element_length(before)
    after_len = element_length(after)
    '''
    print("\n1. The change of total element number :\n")
    print("The length of the original random program: ", before_len,"\n")
    print("The length of the optimized program: ", after_len,"\n")
    '''
    return before_len, after_len, after_len / before_len


# result for instruction reduction         
def result2(before, after):
    before_len = instruction_length(before)
    after_len = instruction_length(after)
    '''
    print("\n2. The change of instruction number (code lines):\n")
    print("The length of the original random program: ", before_len,"\n")
    print("The length of the optimized program: ", after_len,"\n")
    '''
    return before_len, after_len, after_len / before_len


# generate a table 
def chart(name, c):
    with open(name, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(c)


# convert dictionary to string
def process_register(d1): # d1 = register set
    slist = []
    
    for i in d1:
        if isinstance(d1[i],complex) == False:
            d1[i] = round(d1[i],2)
            element = str(i) + ": " + str(d1[i])
            slist.append(element)
        else:
            print(d1[i])
            
    s1 = ", ".join(slist)
    return s1

# check the function
def compare(d1, d2):
    list2 = []
    for i in d2:
        list2.append(d2[i])
        
    if d1 == d2:
        return "Same Function"
    
    elif len(d2) >= len(d1):
        for i in d1:
            if d1[i] not in list2:
                return "Fails"
        return "Same Function with more registers for single assignment form"
        
    else:
        return "Fails"


def deleteLabel(program):
    set_jumps = {}
    for label in program:
        flag = True
        for i in program[label]:
            if "goto" == i[0] and flag:
                set_jumps[label] = i[1]
                flag = False

    unreach = []
    for L in set_jumps:
        if L < set_jumps[L]:
            key_number = int(L[1:])
            value = int(set_jumps[L][1:])
            d = value - (key_number + 1)
            for i in range(d):
                unL = key_number + (i+1)
                unreach.append("L"+str(unL))

    for label in unreach:
        if label in program:
            del program[label]

    return program
    
        
#-----YY------
    

def testing():
    max_prog_length = 6  # 6 instructions in total is the upper limit
    totalLabel = random.randint(1, 6)

    dic_program = {}#he
    dic_copy={}     #he
    new_register=[]
    # generate program
    dic_program = {}
    #---hy update
    totalList=[]
    determineList=[]
    #----hy update
    for i in range(totalLabel):
        prog_length = random.randint(1, max_prog_length)
        program, program_ls = random_program(i, prog_length, totalLabel)#he
        label = "L" + str(i)
        dic_program[label] = program


    #-----hy update-----
    c = copy.deepcopy(dic_program)
    
    # before
    register_dic = {'r0': 1.5, 'r1': 1.5, 'r2': 1.5, 'r3': 1.5, 'r4': 1.5}
    
    for label in c:
        program = c[label]
        a,pro_copy,goto_num=execute(program, len(program), register_dic)

        for elem in pro_copy:
          totalList.append(elem) 
          determineList.append(elem)   
        determineList.append("stop here")
    pro,totalList=before_trans(totalList)
    #print(pro,"\n\n",totalList)
    # ---------update 4.5----------

    # testing opti1 --------------------------------------------------------------
    after_single_program,new_name = opti1.single_assign(totalList)#he 
    count=0
    start=0
    end=0
    for i in range(len(determineList)):
      if determineList[i]=="stop here":
        label = "L" + str(count)
        end=i-count
        dic_copy[label]=after_single_program[start:end]
               
        count+=1
        start=i+1-count
        continue 
    for i in new_name:          #he
      new_register.append(i)
      
    for i in range(totalLabel): 
      label = "L" + str(i)  
      dic_copy[label] = opti1.optimization(dic_copy[label])#he
   #------------------------------------------------------------------------

      
    #optimization process 2 4
    #c = copy.deepcopy(dic_program) update
    opti2.general_constant_opti(dic_copy)
    opti2.general_sub_eliminate(dic_copy)

    '''
    #print(dic_copy)
    print("\nOriginal Program:\n")              # hard copy
    for i in c:
        print(i + " " + str(c[i]) + "\n")
    print("\nOptimization Program:\n")          # dic_program
    for i in dic_copy:
        print(i + " " + str(dic_copy[i]) + "\n")
    '''


    # before
    register_dic = {'r0': 1.5, 'r1': 1.5, 'r2': 1.5, 'r3': 1.5, 'r4': 1.5}
    exe_before = deleteLabel(c)
    for label in exe_before:
        program = c[label]
        execute(program, len(program), register_dic) # goto Label5        
    #print("\nOriginal result:", register_dic)

    # after
    compare_dic = {'r0': 1.5, 'r1': 1.5, 'r2': 1.5, 'r3': 1.5, 'r4': 1.5}
    for r in new_register:
      compare_dic[r]=1.5
      
    #print(compare_dic)
    for label in dic_copy:
        program = dic_copy[label]
        execute(program, len(program), compare_dic)
                
    #print("\nOptimiza result:", compare_dic)


    before1, after1, r1 = result1(dic_program, dic_copy)
    before2, after2, r2 = result2(dic_program, dic_copy)
    
    rp1 = str(round(100-r1*100,2))+"%"
    rp2 = str(round(100-r2*100,2))+"%"
    d1 = before1 - after1
    d2 = before2 - after2

    #print("The total elements are reduced by:", rp1, "\n")
    #print("The code lines (instruction number) are reduced by:", rp2, "\n")

    return before1, after1, rp1, before2, after2, rp2, d1, d2, register_dic, compare_dic
    
          
# show the results
def main():

    chart1 = [["The Reduction of Elements", "", "", "", ""],
              ["(change of the number of terms)", "", "", "", ""],
              ["","Length of Original Program", "Length of Optimized Program", "Length Difference", "Reduction Percentage"]]
    
    chart2 = [["The Reduction of Instructions", "", "", "", ""],
              ["(change of the number of code lines)", "", "", "", ""],
              ["","Length of Original Program", "Length of Optimized Program", "Length Difference", "Reduction Percentage"]]
    
    chart3 = [["", "Register Assignment", "Comparison"]]
    
    testing_number = 20 # modify here to change the number of testing cases 
    for i in range(testing_number):
        r1 = [] # length of elements
        r2 = [] # length of code lines
        r3 = [] # original register
        r4 = [] # result of registers after optimization

        r1.append("Test"+str(i+1))
        r2.append("Test"+str(i+1))
        r3.append("Test"+str(i+1)+" Original")
        r4.append("Test"+str(i+1)+" Optimized")
        #print("\n\nTesting ", i+1, ":\n")
        before1, after1, rp1, before2, after2, rp2, d1, d2, re1, re2 = testing()
        r1.append(before1)
        r1.append(after1)
        r1.append(d1)
        r1.append(rp1)
        
        r2.append(before2)
        r2.append(after2)
        r2.append(d2)
        r2.append(rp2)

        r_before = process_register(re1)
        r_after = process_register(re2)
        message = compare(re1, re2)

        r3.append(r_before)
        r3.append(message)
        r4.append(r_after)
        r4.append("")

        chart1.append(r1)
        chart2.append(r2)
        chart3.append(r3)
        chart3.append(r4)
        

    chart("Result_Table1.csv", chart1)
    chart("Result_Table2.csv", chart2)
    chart("Function_Check_Table3.csv", chart3)
    print("The results are in the table The_Reduction_of_Total_Elements.csv and The_Reduction_of_Instructions.csv")

main()












