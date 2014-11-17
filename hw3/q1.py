import re
import string
import sys



def probabilities(dict,tags,sentence,p):
  '''
tags is a list of tags for the sentence.
  for ex,['S','VB','NNS','IN','DT','NN','E']
dict is percentages
sentence is a list of words in the sentence in order.
  ["time","flies","like,"an","arrow"]
p is the possibility,initial p is 1.0
p(t1...t5)=
  p(t1|S)p(w1|t1)p(t2|t1)p(w2|t2)..p(w5|t5)p(E|t5)
  '''

  num_tag=len(tags)
  for i in range(1,num_tag):
    #p*=p(t_k|t_k-1)*p(w_k|t_k)
    
    if tags[i]!='E':
      p*= dict[tags[i]+"|"+tags[i-1]]*dict[sentence[i-1]+'|'+tags[i]]
    else:
      p*= dict[tags[i]+"|"+tags[i-1]]

  return p

def makeList(st):
  for c in string.punctuation:
    st=st.replace(c," ")
  st=st.split(" ")
  return st

def addTags(st):
  '''
  add START AND END tags to st
  '''
  return "S "+st+" E"


def main( ):
  prob={'time|NN':7.0727,
        'time|VB':0.0005,
        'time|JJ':0,
        'flies|VBZ':0.4754,
        'flies|NNS':0.1610,
        'like|IN': 2.6512,
        'like|VB':2.8413,
        'like|RB':0.5086,
        'an|DT':1.4192,
        'arrow|NN':0.0215,
        'NN|S':0.6823,
        'VB|S':0.5294,
        'JJ|S':0.8033,
        'VBZ|NN':3.9005,
        'VBZ|VB':0.0566,
        'VBZ|JJ':2.0934,
        'NNS|NN':1.6076,
        'NNS|VB':0.6566,
        'NNS|JJ':2.4383,
        'IN|VBZ':8.5862,
        'IN|NNS':21.8302,
        'VB|VBZ':0.7002,
        'VB|NNS':11.1406,
        'RB|VBZ':15.0350,
        'RB|NNS':6.4721,
        'DT|IN':31.4263,
        'DT|VB':15.2649,
        'DT|RB':5.3113,
        'NN|DT':38.0170,
        'E|NN':0.2069
        }

  sentence="time flies like an arrow?"
  tag1="VB NNS IN DT NN"
  tag2="JJ VBZ VB DT NN"

  print sentence
  sentence=makeList(sentence)

  print "the probability of ",tag1,":"
  tag1=makeList(addTags(tag1))
  print probabilities(prob,tag1,sentence,1.0)
  print
  print "the probability of ",tag2,":"
  tag2=makeList(addTags(tag2))
  print probabilities(prob,tag2,sentence,1.0)



if __name__=='__main__':
  main()
