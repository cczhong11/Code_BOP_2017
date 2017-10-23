# 1. read all questions and answers in
# 2. cut the words and summary the common words 词性
# 3. 关键词统计
import jieba.analyse
import jieba
import codecs
import jieba.posseg as pseg
import pandas as pd

fulldict = {}#save all the answers
answerdict={}# save index of answers to the questions
qdict={}# save questions 
question = 0# questions number
aindex = 0# answer index
lastq = ''#last questions
wordwrapcount={}#from full list
str1c=''
rdict={}
qqdict={}# save question words index
right={}
wrong={}
def wordwrap_tag(str1,str2):
    '''return count'''
    timeflag = 0
    str1c = jieba.analyse.extract_tags(str1)
    str2c = jieba.analyse.extract_tags(str2)
    count = 0
    return count
def handlerl2(l2,q):
    global qqdict
    c = 0
    for i in qqdict.keys():
        if i in l2:
            c = c + qqdict[i]
    right[q].append(c)        

def handlewl2(l2,q):
    global qqdict
    c = 0
    for i in qqdict.keys():
        if i in l2:
            c = c + qqdict[i]
    wrong[q].append(c)

def handlerq0(q):
    global qqdict
    str1c = pseg.cut(q)
    strl = jieba.lcut(qdict[question])
    k = len(strl)
    for i, j in str1c:
        if j[0] == 'r':
            k = strl.index(i)        
    for i in range(len(strl)):
        qqdict[strl[i]] = 2*(k-i)      

def handlerq(q):
    global qqdict
    str1c = jieba.analyse.textrank(q)
    strl = jieba.lcut(q)
    str1d = pseg.cut(q)# 词性
    c = 0
    k = len(strl)
    #for i, j in str1d:
    #    if j[0] == 'n':
    #        k = strl.index(i)   
    for i in range(len(strl)):
        if strl[i] in str1c:
            qqdict[strl[i]] = 10 - str1c.index(strl[i])#+20-k+i
    
def add_line(line):
    '''add answer to the dict'''    
    global fulldict, answerdict, question, aindex, lastq, qdict, wordwrapcount, str1c,rdict,qqdict
    
    l = line.split("\t")
    if l[1]!=lastq:
        aindex = 0
        question = question+1
        lastq = l[1]
        qdict[question]=lastq
        fulldict[question]=[]
        wordwrapcount[question]=[]        
        rdict[question]=[]        
        qqdict = {}
        handlerq(qdict[question])
        right[question]=[]
        wrong[question]=[]

    if l[0]=='1':
        answerdict[question] = aindex
        handlerl2(l[2],question)
    else:
        handlewl2(l[2],question)
    fulldict[question].append(l[2])
    
    #wordwrapcount[question].append(wordwrap_tag(qdict[question],l[2]))12
    aindex = aindex+1


with open("ent_tag_full.txt", 'r') as file1:
        result = file1.readlines()
        [add_line(o) for o in result]
#r = pd.DataFrame(right)
#w = pd.DataFrame(wrong)
#rr = pd.value_counts(r.loc[:,0].values,sort=True)
#ww = pd.value_counts(w.loc[:,0].values,sort=True)
count = 0
zcount = 0
for i in right.keys():
    flag = 0
    zcount = zcount+1
    for j in wrong[i]:
        if len(right[i])!=0 and right[i][0]<j:
            flag = 1
            break
    if flag == 0:
        count = count+1
    
print(count/zcount)