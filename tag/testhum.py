# 1. read all questions and answers in
# 2. cut the words and summary the common words 词性
# 3. 关键词统计
import jieba.analyse
import jieba
import codecs
import jieba.posseg as pseg
import pandas as pd
from Levenshtein import *
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
nndict={}#save all n
zwm=['长','官','者','人','工']
commonss=['校长', '大学', '短期', '作者', '学院', '导演', '中学', '编剧', '教练', '第一', '作曲', '制作', '院长', '艺术', '指导', '创立', '创办', '现在', '喜欢', '政治', '中国', '总经理', '主席', '祖父', '主编', '生物', '演唱', '开发商', '工作', '国民中学', '设计', '校监', '局长', '漫画', '偶像', '首任']
commonword={}
def wordwrap_tag(str1,str2):
    '''return count'''
    timeflag = 0
    str1c = jieba.analyse.extract_tags(str1)
    str2c = jieba.analyse.extract_tags(str2)
    count = 0
    return count
def handlerl2(l2,q):
    global qqdict,commonword
    c = 0
    #str1c = pseg.cut(l2)
    #for i, j in str1c:
    #    if j[0:1]=="nr":
    #        c = c+1000
    if '：' in l2:
        c = 10 
    for i in qqdict.keys():
        if i in l2:
            c = c + qqdict[i]
            if i in commonword.keys():
                commonword[i] = commonword[i] + 1
            else:
                commonword[i] = 1
    right[q].append(c)

def handlewl2(l2,q):
    global qqdict
    c = 0
    #str1c = pseg.cut(l2)
    #for i, j in str1c:
    #    if j[0:1]=="nr":
    #        c = c+1000
    if '：' in l2:
        c = 10
    for i in qqdict.keys():
        if i in l2:
            c = c + qqdict[i]
            
    wrong[q].append(c)

def handlerl3(l2,q):
    global qqdict,commonword
    c = 0
    c = distance(str(l2),str(q))
    right[q].append(c)

def handlewl3(l2,q):
    global qqdict
    c = distance(str(l2),str(q))
    
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
    global qqdict,commonss,zwm
    str1c = jieba.analyse.extract_tags(q)
    strl = jieba.lcut(q)
    str1d = pseg.cut(q)# 词性

    c = 0
    z = 0
    k = len(strl)
    lastn=''
    lastv=''
    for i, j in str1d:
        if j[0] == 'r':
            k = strl.index(i)
        if j[0] == 'n':
            lastn = i
        if j[0] == 'v' and i!='是':
            lastv = i
    #if lastv!='':
    #    print(lastv)
    #    qqdict[lastv] = 100    
    #else:
    qqdict[lastn] = 100
    #qqdict[lastv] = 10000
    for i in range(len(strl)):
        if strl[i] not in qqdict.keys():
            qqdict[strl[i]] = 0
        if strl[i] in str1c:
            qqdict[strl[i]] = qqdict[strl[i]] +10 - str1c.index(strl[i])+20-k+i
        if strl[i] in commonss:
            #print("2")
            qqdict[strl[i]] = qqdict[strl[i]] +1000
        for kk in zwm:
            if kk in strl[i]:
                qqdict[strl[i]] = qqdict[strl[i]] +100
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



#with codecs.open("onlytest.txt", 'r','utf8') as file1:
with open("hum_tag_full.txt",'r') as file1:
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
    for kk in range(len(right[i])):
        for j in wrong[i]:
            if len(right[i])!=0 and right[i][kk]<=j:
                flag = 1
                print(qdict[i])
                break
    if flag == 0:
        count = count+1
    
print(count/zcount)
