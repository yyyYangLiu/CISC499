'''
Author: Yan He
1. Algebraic Simplification
3. Single Assignment Form
5. Copy Propagation
'''
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
  new_name_ls=[]
  # get all the LHS of instruction and put into argu_list
  #print(argu_list)
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
        new_name_ls.append(new_name)
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

  return argu_list,new_name_ls

  
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

  ls,new_name_ls=single_assign(ls)

  ls=copy_propagation(ls)

  # after optimization, transform it
  ls=transform(ls)
  #print("after transform",ls)
  return ls,new_name_ls