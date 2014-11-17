import sys
#sys.setrecursionlimit(10000)

#The code is implemented in recursion.
#Observe whole procedure: set NEED_VERBOSE to 1
NEED_VERBOSE=0

sentence="a dog ate pizza with a fork in a kitchen"
rules=[["S",["NP","VP"],1.0],
       ["NP",["DET","N"],0.4],
       ["NP",["N"],0.3],
       ["NP",["NP","PP"],0.3],
       ["VP",["V","NP"],0.8],
       ["VP",["V","XP"],0.2],
       ["PP",["IN","NP"],1.0],
       ["XP",["NP","PP"],1.0],
       ["DET",["a"],1.0],
       ["N",["dog"],0.1],
       ["N",["pizza"],0.2],
       ["N",["fork"],0.4],
       ["N",["kitchen"],0.3],
       ["V",["ate"],1.0],
       ["IN",["with"],0.4],
       ["IN",["in"],0.6]]

time_visit_cal=0
time_beta=0

def makeList(parent,left_child,right_child):
    #to store whole parse
    #prefer storing info to left child
    return [parent,left_child,right_child]

def is_Terminal(symbol):
    '''
    tell whether the symbol is terminal symbol
    '''
    if symbol=="a" or symbol=="dog" or symbol=="pizza" or symbol=="fork" or symbol=="kitchen" or symbol=="ate" or symbol=="with" or symbol=="in":
        return 1
    else:
        return 0

def is_Start(symbol):
    '''
    tell whether the symbol is Start symbol
    '''
    if symbol=="S":
        return 1
    else:
        return 0

def split_Stc(sentence):
    '''
    split the sentence into words
    '''
    new_stc=sentence.split()
    return new_stc

def cal_beta(ele_ex,ele_pos,rules):
    global time_visit_cal
    time_visit_cal=time_visit_cal+1
    tmp_case=[]
    flag_2=0
    flag_1=0
    for rule in rules:
        if is_Terminal(rule[1][0]):
            continue
        if flag_2==1 and flag_1==2:
            break
        if len(rule[1])==2 and flag_2==0:
            if ele_ex[1][0]==rule[1][0] and ele_pos[1][0]==rule[1][1]:
                tmp_case.append([rule[2]*ele_ex[0]*ele_pos[0],makeList(rule[0],ele_ex[1],ele_pos[1])])
                flag_2=flag_2+1
        if len(rule[1])==1 and flag_1<2:
            if ele_ex[1][0]==rule[1][0]:
                flag_1+=1
                tmp=cal_beta([ele_ex[0]*rule[2],makeList(rule[0],ele_ex[1],None)],ele_pos,rules)
                if tmp!=0:
                    tmp_case+=tmp
            if ele_pos[1][0]==rule[1][0]:
                flag_1+=1
                tmp_pos=[ele_pos[0]*rule[2],makeList(rule[0],ele_pos[1],None)]
                tmp=cal_beta(ele_ex,tmp_pos,rules)
                if tmp!=0:
                    tmp_case+=tmp
    if len(tmp_case)==0:
        return 0
    return tmp_case


def verbose(tmp_case,case):
    print "here return"
    if len(tmp_case)==0:
        print "NONE"
    for ele in tmp_case:
        print "beta_",ele[1][0],"(",case[0],",",case[1],")=",ele[0]

def beta(case):
    #case is [p,d] p,d is the index of terminal
    #recursion : USING A DOWN-UP idea
    #if the parse is failed, drop it by setting it to zero
    global time_beta
    time_beta+=1
    global time_visit_cal
    if NEED_VERBOSE:
        print "new_beta"
        print "current terminal range is (",sentence[case[0]],",",sentence[case[1]],")"

    if case[0]==case[1]:
        if NEED_VERBOSE:
            print "beta:same"
        for i in range(len(rules)):
            if rules[i][1][0]==sentence[case[0]] and len(rules[i][1])==1:
                tmp_case=[ [ rules[i][2],makeList(rules[i][0],[rules[i][1][0]],None) ] ]
                if NEED_VERBOSE:
                    verbose(tmp_case,case)
                return tmp_case#[first element is prob(beta), second is [antec nonterminal,current terminal/nonterminal]]
        print "ERROR:cannot find the prob for terminal"
        return 0

    tmp_case=[]
    for d in range(case[0],case[1]):
        tmp_ex=0
        tmp_pos=0
        tmp_ex=beta([case[0],d])
        tmp_pos=beta([d+1,case[1]])
        if len(tmp_ex)==0 or len(tmp_pos)==0:
            if NEED_VERBOSE:
                print "drop (",case[0],",",d,") and (",d+1,",",case[1],")"
                if len(tmp_ex)==0:
                    print "because cannot find the parse for (",case[0],",",d,")"
                else:
                    print "because cannot find the parse for (",d,",",case[1],")"
            #print "in invalid"
            continue
        for ele_ex in tmp_ex:
            for ele_pos in tmp_pos:
                time_visit_cal=0
                tmp_beta=cal_beta(ele_ex,ele_pos,rules)
                if tmp_beta!=0:
                    tmp_case+=tmp_beta
    if NEED_VERBOSE:
        verbose(tmp_case,case)
    return tmp_case

def print_parse(list):
    if is_Terminal(list[0]):
        return
    if list[2]!=None:
        print "[",list[0],"->(",list[1][0],",",list[2][0],")]"
        print_parse(list[1])
        print_parse(list[2])
    else:
        print "[",list[0],"->(",list[1][0],")]"
        print_parse(list[1])


def inside():
    final_beta=0
    final_beta_lst=beta([0,len(sentence)-1])
    for ele in final_beta_lst:
        if is_Start(ele[1][0]):
            print ""
            print "Print one possible parse"
            print_parse(ele[1])
            final_beta+=ele[0]
    return final_beta

sentence=split_Stc(sentence)
beta=inside()
print "the inside probability is ",beta
