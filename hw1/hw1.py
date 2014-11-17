'''
Wen Chen
ID: wc23
Assignment: NLP HW1
email: wc23@indiana.edu
a_3,b_3,c_3 is the function to give the solution to relative questions
'''
import string
import math
sta={}#the dictionary to count occurrence numbers of all aphabets. 
prob={}#the dictionary to count probabilties of all aphabets. 
codes={} #the dictionary to store the codes of all letters in the text
allTheLetters=string.ascii_lowercase


def a_3(text):

	#clean and unify the text
	text=text.lower()
	text=text.replace(', ',' ')
	text=text.replace('. ',' ')
	text=text.replace(" ","")



	for letter in allTheLetters: #count the occrence numbers of all letters and store the results in sta

		sta[letter]=text.count(letter)


	#count the total numbers of letters of the string, from which subtracting the numbers of digits
	numberDigits=0
	for i in text:
		if i.isdigit():
			numberDigits += 1
	numberLetters=len(text)-numberDigits #294
	print numberLetters, "hahahahaha"
    


	#calculate the probability for each letter and store the results in dictionary prob
	for letter in allTheLetters:
		prob[letter]=sta[letter]/(1.0*numberLetters)

	return prob

def b_3():
	'''
	calculate the entropy of random variable X in prob
	'''
	entropy=0
	nZero=0 #count for the number of letters that doesn't show up in the text
	for letter,p in prob.items():
		if p>0:
			entropy+=p * math.log(p,2)
		if p==0:
			nZero+=1


	entropy=-entropy

	#grab the idea from ascii to code the letters. Letter A is 00001
	code=0
	for letter in allTheLetters:
		if prob[letter]>0:
			code+=1
			binary=bin(code)
			binary=binary.replace('0b','')
			binary=int(binary)
			codes[letter]=format(binary,"005")


	print "THE SOLUTION FOR 3(B) : "
	print " THE DIGITS WE NEED FOR THE TEXT IS ",26-nZero
	print "THE ENTROPY IS", entropy
	print " SO WE NEED ",math.ceil(entropy),"BITS"
	print " GRAB THE IDEA FROM ASCII TO CODE THE LETTERS. "
	for letter,c in codes.items():
		print letter,":",codes[letter]

def c_3():
	'''
		calculate the expectation and variance of my code
	'''
	#the expectation of a random variable
	#the E[x^2]
	expectation=0
	expi2=0
	for letter,code in codes.items():
		expectation+=int(code)*prob[letter]
		expi2+=int(code)*int(code)*prob[letter]

	print expectation

	#variance
	#E[x]^2
	exp2=expectation*expectation
	variance=expi2-exp2

	print "THE SOLUTION FOR 3(C)"
	print "THE EXPECTATION IS ", expectation
	print "THE VARIANCE IS", variance





text="Bach was the most famous composer in the world, and so was Handel. Handel was half German, half Italian and half English. He was very large. Bach died from 1750 to the present. Beethoven wrote music even though he was deaf. He was so deaf he wrote loud music. He took long walks in the forest even when everyone was calling for him. Beethoven expired in 1827 and later died for this. "
a_3(text)
print "THE SOLUTION FOR 3(A) IS"
for letter,probability in prob.items():
	print letter,":",probability


b_3()
c_3()
