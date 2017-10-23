import codecs
path = "C:/Users/zhongtc/"
#path = "C:/Users/zhongtc/Documents/bop/"
qtag = {}
qtag['time']=['何时','什么时候','哪一年']
fulldict = {}#save all the answers
answerdict={}# save index of answers to the questions
qdict={}# save questions 
question = 0# questions number
aindex = 0# answer index
lastq = ''#last questions
def add_line(line):
    '''add answer to the dict'''
    global fulldict, answerdict, question, aindex, lastq, qdict
    l = line.split("\t")
    if l[1]!=lastq:
        aindex = 0
        question = question+1
        lastq = l[1]
        qdict[question]=lastq
        fulldict[question]=[]
    if l[0]=='1':
        answerdict[question] = aindex
    fulldict[question].append(l[2])
    aindex = aindex+1
with codecs.open(path+"BoP2017_DBAQ_dev_train_data/BoP2017-DBQA.train.txt", 'r', "utf8") as file1:
    with open('result.txt','w') as file2:
        result = file1.readlines()
        [add_line(o) for o in result]
        for i in range(question-1):
            print(i)
            try:
                file2.write((str(i)+'\t'+qdict[i+1]+'\t'+fulldict[i+1][answerdict[i+1]]))
                #file2.write((str(i)+'\t'+qdict[i+1]+'\n'))
            except:
                continue




