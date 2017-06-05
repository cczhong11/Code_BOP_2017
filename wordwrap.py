import codecs
import jieba
from bosonnlp import BosonNLP
import thulac
import jieba.analyse
qtag = {}
qtag['time']=['何时','时候','哪一年','哪天','时间','何年','哪年','日期']
qtag['num']=['多重','多宽','多少','多大','多远','多长','多高','多久','几','多大']
qtag['ent']=['哪些','什么','哪几','哪个','哪一','还是','哪家']#实体
qtag['loc']=['哪里','有多远','在哪']
qtag['hum']=['谁','哪位']
qtag['des']=['如何','怎么','怎样']

thu1 = thulac.thulac(seg_only=True)  #只进行分词，不进行词性标注
# 注意：在测试时请更换为您的API token
usenlp=0
nlp = BosonNLP('QpILHyod.15480.J5W8PFQpjw61')
#path = "C:/Users/zhongtc/"
path = "C:/Users/zhongtc/Documents/bop/"
#path = "E:/BoP2017_DBQA_dev_train_data/"
fulldict = {}#save all the answers
answerdict={}# save index of answers to the questions
qdict={}# save questions 
question = 0# questions number
aindex = 0# answer index
lastq = ''#last questions
wordwrapcount={}#from full list
str1c=''
def wordwrap(str1,str2):
    '''return count'''
    str1c = list(jieba.cut(str1.strip()))
    str2c = list(jieba.cut(str2.strip()))
    count = 0
    for i in str1c:
        if i in str2c:
            count = count+1
    return count
def wordwrap_tag(str1,str2):
    '''return count'''
    timeflag = 0
    for i in qtag['time']:
        if i in str1:
            timeflag = 1
    str1c = jieba.analyse.extract_tags(str1)
    str2c = jieba.analyse.extract_tags(str2)
    count = 0
    try:
        for i in ['年','月','日']:
            if i in str2:
                if timeflag==1:
                    count=count+5
    except:
        a = 0
    for i in range(len(str1c)):        
        if str1c[i] in str2c:
            if i<3:
                count = count+10-i*3
            else:
                count = count+1
    return count
def wordwrap_2(str1c,str2):
    '''return count'''
    #str1c = nlp.tag(str1.strip())[0]['word']
    str2c = nlp.tag(str2.strip())[0]['word']
    count = 0
    for i in str1c:
        if i in str2c:
            count = count+1
    return count
def wordwrap_3(str1,str2):
    '''return count'''
    str1c = thu1.cut(str1.strip())
    str2c = thu1.cut(str2.strip())
    count = 0
    for i in str1c:
        if i in str2c:
            count = count+1
    return count
def add_line(line):
    '''add answer to the dict'''    
    global fulldict, answerdict, question, aindex, lastq, qdict, wordwrapcount, str1c
    if question>3000000:
        return
    l = line.split("\t")
    if l[1]!=lastq:
        aindex=0
        question = question+1
        lastq = l[1]
        #qdict[question]=lastq
        #fulldict[question]=[]
        #answerdict[question]=[]
        #wordwrapcount[question]=[]
        #if usenlp == 1:
        #    str1c = nlp.tag(lastq.strip())[0]['word']
        #    print(str1c)
        if question%1000 == 0: 
            print(question)
    #if l[0]=='1':
    #    answerdict[question].append(aindex)
    #fulldict[question].append(l[2])
    #wordwrapcount[question].append(wordwrap_tag(qdict[question],l[2]))
    aindex = aindex+1

def write_wordwrap_to_file(kk):
    wcount=0
    with open('result2_th.txt','w') as file2:
        for k in kk.keys():
            result = kk[k]
            resulti = result.index(max(result))
            try:
                if resulti != answerdict[k]:
                    wcount = wcount + 1
                    file2.write(str(k)+'\t'+qdict[k]+'\n'+str(result[answerdict[k]])+'\t'+fulldict[k][answerdict[k]]+str(result[resulti])+'\t'+fulldict[k][resulti]+'\n')
                    file2.write(str(jieba.analyse.extract_tags(qdict[k]))+'\t'+str(jieba.analyse.extract_tags(fulldict[k][resulti]))+'\n')
            except:
                continue
                
        file2.write(str(wcount))
def test():
    with codecs.open(path+"BoP2017_DBAQ_dev_train_data/BoP2017-DBQA.dev.txt", 'r', "utf8") as file1:
        result = file1.readlines()
        [add_line(o) for o in result]
        #write_wordwrap_to_file(wordwrapcount)
def tag_q(str1):
    timeflag = 0
    tag = ''
    str1 = str1.replace("谁知道","")
    str1 = str1.replace("我很好奇","")
    str1 = str1.replace("你知道","")
    for j in qtag.keys():
        for i in qtag[j]:
            if i in str1:
                tag = j
                break
        if tag!='':
            break
    return tag
    
    return False
def test_tag():
    with codecs.open(path+"BoP2017_DBAQ_dev_train_data/BoP2017-DBQA.train.txt", 'r', "utf8") as file1:
        result = file1.readlines()
        [add_line(o) for o in result]
    for i in qtag.keys():
        with open('tag/'+i+"_tag.txt",'w') as file2:
            file2.write("")
        with open('tag/'+i+"_tag_full.txt",'w') as file2:
            file2.write("")
    with open('qtag.txt','w') as file2:
        count = 0
        for i in qdict.keys(): 
            s = tag_q(qdict[i])           
            if s!='':
                count=count+1
                with open('tag/'+s+"_tag.txt",'a') as file3:
                    file3.write(str(i)+'\t'+qdict[i]+'\n')
                with open('tag/'+s+"_tag_full.txt",'a') as file3:
                    for j in range(len(fulldict[i])):
                        try:
                            if j in answerdict[i]:
                                file3.write('1\t'+qdict[i]+'\t'+fulldict[i][j].strip()+'\n')
                            else:        
                                file3.write('0\t'+qdict[i]+'\t'+fulldict[i][j].strip()+'\n')
                        except:
                            continue
            else:
                file2.write((str(i)+'\t'+qdict[i]+'\n'))
        print(count)
test()