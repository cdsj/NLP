'''
Wen Chen
ID: wc23
Assignment: NLP HW1
Email: wc23@indiana.edu
Import the hw1.py
'''

import hw1
import math
from copy import deepcopy

#define global vars
ZERO=0.0001
hw1.a_3(hw1.text)
prob3=deepcopy(hw1.prob)

extra="The sun never set on the British Empire because the British Empire is in the East and the sun sets in the West. Queen Victoria was the longest queen. She sat on a thorn for 63 years. He reclining years and finally the end of her life were exemplatory of a great personality. Her death was the final event which ended her reign. "
prob4=hw1.a_3(extra)



def print_dict(inp):
	for a,b in inp.items():
		print a,":",b


def KL(p,q):
	Divergence=0
	for letter,prob in p.items():
		#consider the zero-situations:
		if prob==0:
			prob=ZERO
		if q[letter]==0:
			prob2=ZERO
		else:
			prob2=q[letter]
		ratio=prob/prob2
		Divergence+=prob*(math.log(ratio,2))
	return Divergence



"--------------EXTRA PROBLEM START HERE--------"
print "PROBABILITY FOR THE LETTERS IN EXTRA PROBLEM: "
print_dict(prob4)
print "PROBABILITY FOR THE LETTERS IN PROBLEM 3: "
print_dict(prob3)
#KL divergence
#1. D(text||extra)
print "D(text||extra) IS "
print KL(prob3,prob4)

#2. D(extra||text)
print "D(extra||text) IS "
print KL(prob4,prob3)

#1. start
