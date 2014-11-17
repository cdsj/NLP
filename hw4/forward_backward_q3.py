import pandas
from decimal import Decimal

###################
#DEFINE CONSTANTS HERE
DT=0
JJ=1
NN=2
VB=3


a=0
myth=1
iis=2
female=3
moth=4

#initial vector
v=[0.45,0.35,0.15,0.05]

#TRANSITION MATRIX
#VERTICAL: STATES(t+1)
#HORIZON: STATES(t)
P=[[0.03,0.42,0.5,0.05],[0.01,0.25,0.65,0.09],[0.07,0.03,0.15,0.75],[0.3,0.25,0.15,0.3]]

#EMISSION MATRIX
#VERTICAL: STATES
#HORIZON: signal
#coz there are two "a" in the sequence, I copy the "a" row into A for convenince
A=[[0.85,0.05,0.03,0.05],
[0.01,0.6,0.25,0.05],
[0.12,0.13,0.25,0.2],
[0.02,0.02,0.02,0.60],
[0.85,0.05,0.03,0.05],
[0.01,0.1,0.45,0.1]]


#BAUM-WELCH ALGORITHM
#grab the results according to the result of q1.py
alpha=[[0.3825, 0.017499999999999998, 0.0045, 0.0025000000000000005],
 [0.00012715, 0.09947099999999998, 0.05091875, 0.0012412500000000002],
 [0.00059222544, 0.0034786736399999994, 0.018135931249999994, 0.009504037],
  [8.346559574199999e-05, 8.0769805646e-05, 0.00013406491647, 0.010077510862259997],
   [0.002580557048445676, 0.00012893238323411196, 4.8779086150511985e-05, 0.00015676222541628697],
   [1.2914923894113332e-06, 0.00011567209850942989, 0.0006322120965270138, 2.2424474915112398e-05]]

beta=[[0.0019395098754504665, 0.0014617679913212847, 0.00032724047384760164, 0.0010736452002910442],
 [0.004681346177248, 0.0059751478022960006, 0.003411761910312, 0.00235919465188],
 [0.00259455308, 0.0044462596, 0.03432161792, 0.013903777199999998],
  [0.016309000000000004, 0.0098127, 0.022055900000000003, 0.0760594],
  [0.2723, 0.32660000000000006, 0.1462, 0.1255],
  [1, 1, 1, 1]]
#-------------------------------
###############################

#probability of signal sequence,using forward algorithm
def prob_sig_seq(alpha):
  i=len(alpha)-1
  #print alpha[i]
  P_O=0
  for j in range(len(alpha[i])):
      P_O+=alpha[i][j]
  print P_O
  return P_O

#This is the probability of being in state s_i
#at time t
# conditional on the entire observed signal sequence O from time 1 to time T
def prob_state(alpha,beta,P_O):
  gamma=[]
  for t in range(6):#signal at time t
    v=[]
    for i in range(4): #states
      tmp_v=(alpha[t][i]*beta[t][i])/(1.0*P_O)
      v.append(tmp_v)
    gamma.append(v)
  return gamma




#the probability of transition from s_i to s_j
def prob_tran(alpha,beta,P_O):
  #epsilon is a list of matrix (from time 1 to T-1)
  #the each element(or say the matrix in epsilon),
  #represents all transitions of state i to state j.

  epsilon=[]
  for t in range(5):#time
    t_epsilon=[]
    for i in range(4):
      t_i_epsilon=[]
      for j in range(4):
        tmp=(alpha[t][i]*P[i][j]*A[t+1][j]*beta[t+1][j])/(1.0*P_O)
        t_i_epsilon.append(tmp)
      t_epsilon.append(t_i_epsilon)
    epsilon.append(t_epsilon)

  return epsilon

def output_epsilon(epsilon):
  print "output the epsilon"
  for i in range(5):
    print "when t=",i+1,"the matrix of epsilon(i:row;j:column)"
    ii=["DT","JJ","NN","VB"]
    jj=['DT','JJ','NN','VB']
    df=pandas.DataFrame(epsilon[i],index=ii,columns=jj)
    print df
    print "---------"
    print ""

def output_gamma(gamma):
  print "output the gamma"
  steps=["a","myth","is","a","female","moth"]
  states=['DT','JJ','NN','VB']
  df=pandas.DataFrame(gamma,index=steps,columns=states)
  print df
  print "--------"
  print ""

def output_P_reest(P_reest):
  print "output the reestimated P"
  ii=['DT','JJ','NN','VB']
  jj=['DT','JJ','NN','VB']
  df=pandas.DataFrame(P_reest,index=ii,columns=jj)
  print df



def calc_p(gamma,epsilon,time):
  #calculate p_{ij}
  #return P_reest: a matrix, row:i,col:j
  P_reest=[]
  for i in range(4):
    P_i_reest=[]
    for j in range(4):
      denominator=0
      numerator=0
      for t in range(time-1):
        denominator+=gamma[t][i]
        numerator+=epsilon[t][i][j]
      P_i_reest.append(numerator/(1.0*denominator))
    P_reest.append(P_i_reest)
  return P_reest


def calc_a(gamma,time,observe):
  #emission 'a' shows up twice at time 1 and 4
  #observe=[a,myth,iis,female,moth]
  #the element of observe is a list of number, which indicates the time

  sum_gamma=[]
  #1. calculate the sum of gamma(i) for all t
  for i in range(4):
    t_gamma_i=0
    for t in range(time):
      t_gamma_i+=gamma[t][i]
    sum_gamma.append(t_gamma_i)

  #2. get reestimated a
  a_reset=[[0 for i in xrange(4)] for j in xrange(5)]
  for t in range(len(observe)):
      j=observe[t]
      for i in range(4): #state
          #a_reset[j][i]
          #gamma[t][i]
          #sum_gamma[i]
          a_reset[j][i]+=float(Decimal(gamma[t][i])/Decimal(sum_gamma[i]))
  return a_reset

def output_a_reest(a_reest):
  #ouput the reestimated a
  print "output the reestimated a"
  t=["a","myth","is","female","moth"]
  states=['DT','JJ','NN','VB']
  df=pandas.DataFrame(a_reest,index=t,columns=states)
  print df


#The probability of sequence O
P_O=prob_sig_seq(alpha)

#This is the joint probability of being in state si at time t
#and of being in state sj at time t + 1
#conditional on the entire observed signal sequence O from time 1 to time T
#Denote as epsilon
epsilon=prob_tran(alpha,beta,P_O)


output_epsilon(epsilon) #output the results



#This is the probability of being in state si at time t
# conditional on the entire observed signal sequence O
#from time 1 to time T .
#denote as gamma
gamma=prob_state(alpha,beta,P_O)
output_gamma(gamma)

#calculate the re-estimated P
P_reest=calc_p(gamma,epsilon,6)
output_P_reest(P_reest)

observe=[a,female,moth,iis,a,myth]

a_reest=calc_a(gamma,6,observe)
output_a_reest(a_reest)
