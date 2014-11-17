'''
Wen Chen
assignment : NLP HW2 PROBLEM 3
README: In the code,
    1. I take all numbers in the text different.
    2. For possessive case of third person. For e.x., Alice's, I take it as Alice0s, so that the word is difference with Alice, and also won't be separated into two words when removing the punctuations.
    3. Running the code, you will obtain all trigram probabilities for both train and test set.
'''


import string
import math

tri_list=[]
prob={} #the dictionary to count probability of all words.
count_uni={}
count_tri={} #the occurrence of continuous 3 words
count_bi={} #the occurrence of continuous 2 words
prob_tri={}#the relative frequencies of p(w_n|w_n-1,w_n-1)
prob_bi={} # the relative frequencies of p(w_n|w_n-1)

def file_read(fileName):
    '''
        read in file
        '''
    file=open(fileName,'r')
    train=file.read()
    return train


def make_sentence(train):
    #split the train set into sentences, taking each sentence as one element.
    #Add markers BEGIN and END
    train=train.split("\n")
    for i in range(len(train)):
        train[i]="BEGIN BEGIN "+train[i]+" END"
    return train

def make_word(trainSentence):
    #split the train set into words, taking each word as one element
    #data structure now: {[A,B,C..],[],...}
    for  i in range(len(trainSentence)):
        trainSentence[i]=trainSentence[i].split()
    return trainSentence

def punc_remove(train):
    ''' remove punctuation and split
        '''
    train=train.replace("\'s","0s") #the possessive case of third person
    for c in string.punctuation:
        train=train.replace(c," ")
    return train

def occurrence(trainWord):
    ''' count for the occurrence of each word
        '''
    totalWord=0
    for ele in trainWord:
        for e in ele:
            totalWord+=1
            if e in count_uni:
                count_uni[e]+=1
            else:
                count_uni[e]=1
    return totalWord


def probability_uni(trainWord,totalWord):
    '''calculate the probability of each word
        '''
    
    for ele,num in count_uni.items():
        prob[ele]=1.0*num/totalWord
#print ele,":",prob[ele]


def c_abc(trainWord):
    # get all possible c(w_n-2,w_n-1,w_n)
    def print_lst():
        print "---------------------------"
        print " The trigram extraction is:"
        for ele in tri_list:
            print ele
        print "---------------------------"
    for stc in trainWord:
        for i in range(2, len(stc)):
            if stc[i-2]+" "+stc[i-1]+" "+stc[i] in count_tri:
                count_tri[stc[i-2]+" "+stc[i-1]+" "+stc[i]]+=1
            else:
                tri_list.append(stc[i-2]+" "+stc[i-1]+" "+stc[i])
                count_tri[stc[i-2]+" "+stc[i-1]+" "+stc[i]]=1
    print_lst()

#print count_tri


def c_ab(trainWord):
    #get all possible c(w_n-2,w_n-1)
    for stc in trainWord:
        for i in range(1,len(stc)-1):
            if stc[i-1]+" "+stc[i] in count_bi:
                count_bi[stc[i-1]+" "+stc[i]]+=1
            else:
                count_bi[stc[i-1]+" "+stc[i]]=1
    #print count_bi


def frequency_trigram():
    #get the relative frequencies
    def print_dict():
        print "---------------------------"
        print "the frequencies is:"
        for item, number in prob_tri.items():
            print "p(",item,")=",number
        print "---------------------------"
    
    for item,number in count_tri.items():
        name=item.split(" ")
        prob_item=name[2]+"|"+name[1]+","+name[0]
        if prob_item not in prob_tri:
            prob_tri[prob_item]=1.0*count_tri[item]/count_bi[name[0]+" "+name[1]]
    print_dict()


def frequency_bigram():
    for item,number in count_bi.items():
        name=item.split(" ")
        prob_item=name[1]+"|"+name[0]
        prob_bi[prob_item]=1.0*number/count_uni[name[0]]
#print prob_bi

def print_ele(lst):
    #print the list element by element
    #for test the codes only
    for element in lst:
        print element



def prob_sentence(probility,sentence):
    '''
        Get the probability of a sentence
        p(w1,..,wn)=p(w1|START,START)...p(END|wn-1,wn-2)
        The probility is a dictionary, each item is [A|B,C => prob]
        return the probability and the number of words in the sentence
        '''
    pp=1.0 #the perplexity
    stc_splt=punc_remove(sentence).split()
    for i in range(2,len(stc_splt)):
        pp*=probility[stc_splt[i]+"|"+stc_splt[i-1]+","+stc_splt[i-2]]
    return pp,len(stc_splt)




def perplexity(train_prob_tri,test_prob_tri):
    '''
        train_prob_tri: the probabilities from training set
        
        '''
    sentences=make_sentence(file_read("hw2-test.txt"))
    pp_test=1.0
    for st in sentences:
        print
        print st
        pp,num=prob_sentence(train_prob_tri,st)
        pp_test*=pp
        pp=math.pow(pp,-1.0/num)
        print "perplexity is ", pp
    pp_test=math.pow(pp_test,-1.0/len(test_prob_tri))
    print "---------"
    print "for whole test, the perplexity is",pp_test
    print "---------"



def difference():
    '''
       In case there is some words in test set that is not in training set.
    
    '''
    a=0
    for item in prob_tri:
        if item not in train_prob_tri:
            a+=1
    return a



def run_file(filename):
    '''
        get the probability based on trigram for files
        '''
    trainSet=punc_remove(file_read(filename))
    trainSentence=make_sentence(trainSet)
    trainWord=make_word(trainSentence)
    totalWord=occurrence(trainWord)
    probability_uni(trainWord,totalWord)
    c_abc(trainWord)
    c_ab(trainWord)
    #frequency_bigram()
    frequency_trigram()


print "Question 3 (a)"
print "FOR TRAIN SET"
run_file("hw2-train.txt")
train_prob=prob
train_prob_bi=prob_bi
train_prob_tri=prob_tri

print ""
print "-------------"
print "FOR TEST SET"
run_file("hw2-test.txt")



print "Question 3 (b)"
OOV=difference()
if OOV==0:
    perplexity(train_prob_tri,prob_tri)




