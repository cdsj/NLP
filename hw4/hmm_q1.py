import pandas


#DEFINE
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
[0.01,0.1,0.45,0.1],
[0.02,0.02,0.02,0.60],
[0.85,0.05,0.03,0.05],
[0.01,0.6,0.25,0.05],
[0.12,0.13,0.25,0.2]]

#a_{ik},emission,i is state number, k is the signal
#p_{ij},i=t,j=t+1

def backward(time): #take time starting at 0
  beta_T_init=[1,1,1,1]
  time_beta=[]
  time_beta.append(beta_T_init)

  t=time-1
  while t>=0 :
    tmp_beta=[]
    for i in range(4): #state get the new beta(i) at time t
      tmp_beta_i=0
      for j in range(4): #state
        tmp_beta_i+=P[i][j]*A[t+1][j]*time_beta[0][j]
      tmp_beta.append(tmp_beta_i)
    time_beta.insert(0,tmp_beta)
    t=t-1
  return time_beta






def forward(time):
  #time is the maximum time the question asks
  #get the initialization firstly

  #####a myth is a female moth#######double "a"
  alpha_1=[]
  for st in range(4):
    tmp=A[0][st]*v[st]
    alpha_1.append(tmp)
  time_alpha=[] #horizon: step ; vertical: a_{t}(j)
  time_alpha.append(alpha_1)

  for t in range(1,time): #t:step
    latest_a=[] #for the a at step t
    for j in range(4): #j:state
      tmp=0
      for i in range(4): #i
        tmp+=time_alpha[t-1][i]*P[i][j]
      latest_a.append(tmp*A[t][j])
    time_alpha.append(latest_a)

  return time_alpha




#####a myth is a female moth#######
print "FORWARD STARTS"
alpha=forward(6)
#print alpha


steps=["a","myth","is","a","female","moth"]
alpha_state=['DT','JJ','NN','VB']
df=pandas.DataFrame(alpha,index=steps,columns=alpha_state)
print df

print "So alpha_4(NN)=",alpha[3][NN]
print "alpha_3(VB)=",alpha[2][VB]
print "alpha_1(DT)=",alpha[0][DT]
print "------------"



print "BACKWARD ALGORITHM STARTS"

beta = backward(5)
#print beta


steps=["a","myth","is","a","female","moth"]
beta_state=['DT','JJ','NN','VB']
df=pandas.DataFrame(beta,index=steps,columns=beta_state)
print df
print "SO beta_4(NN) = ",beta[3][NN]
print "beta_3(NN) = ",beta[2][NN]
