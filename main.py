import codecs
from Ques import Ques
#from gensim.models import word2vec
#from gensim import models
import logging

class BOP(object):
    '''main class for bop'''
    qtag = {}
    qtag['1time'] = ['何时', '时候', '哪一年', '哪天', '时间', '何年', '哪年', '日期',]
    qtag['2num'] = ['多少', '多大', '多远', '多长', '多高', '多久', '几', '多大','多重','多宽','多深']
    qtag['3ent'] = ['哪些', '什么', '哪几', '哪个', '哪一', '还是', '哪家']#实体
    qtag['4loc'] = ['哪里', '有多远', '在哪']
    qtag['5hum'] = ['谁', '哪位']
    qtag['6des'] = ['如何', '怎么', '怎样']
    def __init__(self, answer = 1):
        self.answer = answer
        self.cur = Ques()
        self.allq = []
        self.tagdict=[]
        self.all_count = 0
        #logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
        #self.model = models.Word2Vec.load('F:/zip/med250.model.bin')
        self.stopwordset=set()
        # load stopwords set
        with open('chinastopword.txt','r',encoding='utf-8') as sw:
            for line in sw:
                self.stopwordset.add(line.strip('\n'))
    def read_file(self, path):
        '''read question for text file'''
        
        if self.answer == 1:
            flag = 0
            try:
                file1 = open(path, 'r')
                file1.read()
                file1.seek(0)
            except:
                file1 = codecs.open(path, 'r', 'utf8')
            result = file1.readlines()
            aindex = 0
            all_count = 0
            MAXQ = 100000
            for line in result:
                l = line.split("\t")
                if l[1]!=self.cur.q:
                    #if all_count>MAXQ:
                    #    break
                    all_count = all_count + 1
                    aindex = 0
                    self.allq.append(self.cur)
                    self.cur = Ques()
                    self.cur.q = l[1]
                    self.tagdict.append(self.tagq(l[1]))
                    self.cur.tag = self.tagq(l[1])
                if l[0]=='1':
                    self.cur.answerindex.append(aindex)    
                self.cur.answerdict.append(l[2])        
                aindex = aindex+1
            self.allq.append(self.cur)
            self.all_count = all_count
        if self.answer == 0:
            flag = 0
            try:
                file1 = open(path, 'r')
                file1.read()
                file1.seek(0)
            except:
                file1 = codecs.open(path, 'r', 'utf8')
            result = file1.readlines()
            aindex = 0
            all_count = 0
            MAXQ = 100000
            for line in result:
                l = line.split("\t")
                if l[0]!=self.cur.q:
                    #if all_count>MAXQ:
                    #    break
                    all_count = all_count + 1
                    aindex = 0
                    self.allq.append(self.cur)
                    self.cur = Ques()
                    self.cur.q = l[0]
                    self.tagdict.append(self.tagq(l[0]))
                    self.cur.tag = self.tagq(l[0]) 
                self.cur.answerdict.append(l[1])        
                aindex = aindex+1
            self.allq.append(self.cur)
            self.all_count = all_count
    def write_result(self):
        with open('result.txt', 'w') as file1:
            for i in self.allq:
                for j in i.score:
                    file1.write(str(j)+'\n')
    def write_tag_file(self):
        for i in self.qtag.keys():
            with open('tag/'+i+"_tag.txt", 'w') as file2:
                file2.write("")
            with open('tag/'+i+"_tag_full.txt", 'w') as file2:
                file2.write("")
        with open('qtag.txt', 'w') as file2:
            count = 0
            for i in range(len(self.allq)): 
                s = self.allq[i].tag
                if s!='':
                    
                    count=count+1
                    with open('tag/'+s+"_tag.txt", 'a') as file3:
                        try:
                            file3.write(str(i)+'\t'+self.allq[i].q+'\n')
                        except:
                            continue
                    with open('tag/'+s+"_tag_full.txt", 'a') as file3:
                        for j in range(len(self.allq[i].answerdict)):
                            try:
                                if j in self.allq[i].answerindex:
                                    file3.write('1\t'+self.allq[i].q+'\t'+self.allq[i].answerdict[j].strip()+'\n')
                                else:
                                    file3.write('0\t'+self.allq[i].q+'\t'+self.allq[i].answerdict[j].strip()+'\n')
                            except:
                                continue
                else:
                    #file2.write((str(i)+'\t'+self.allq[i].q+'\n'))
                    for j in range(len(self.allq[i].answerdict)):
                        try:
                            file2.write('0\t'+self.allq[i].q+'\t'+self.allq[i].answerdict[j].strip()+'\n')
                        except:
                            continue
            print(count)
    
    def tagq(self, str1):
        tag = ''        
        str1 = str1.replace("谁知道", "")
        str1 = str1.replace("我很好奇", "")
        str1 = str1.replace("你知道", "")
        for j in sorted(self.qtag.keys()):
            for i in self.qtag[j]:
                if i in str1:
                    tag = j
                    break
            if tag!='':
                break
        return tag
    
    def judge_all(self):
        right = 0
        wfile = open('wrong.txt','w')
        wfile2 = open('wrong2.txt','w')
        aaa = 0
        rp = 0
        for k in self.allq:
            k.scoreQ(self.stopwordset)
            k.read_alla()
            k.scoreA()
            rr = k.rescore()            
            rp = rp+rr
            if k.judge():
                right = right + 1
            else:
                for j in range(len(k.answerdict)):
                    try:
                        if j in k.answerindex:
                            wfile.write('1\t'+k.q+'\t'+k.answerdict[j].strip()+'\n')
                        else:
                            wfile.write('0\t'+k.q+'\t'+k.answerdict[j].strip()+'\n')
                    except:
                        continue
                for j in range(len(k.answerdict)):
                    try:
                        if j in k.answerindex:
                            wfile2.write('1\t'+k.q+'\t'+k.answerdict[j].strip()+str(k.score[j])+str(k.jiafen[j])+"k:"+k.keyword+"、"+k.keyword2+'\n')
                        else:
                            if k.score[j]>30:
                                wfile2.write('0\t'+k.q+'\t'+k.answerdict[j].strip()+str(k.score[j])+str(k.jiafen[j])+'\n')
                    except:
                        continue
        #print(aaa)
        wfile.close()
        wfile2.close()
        print("rp:"+str(rp/self.all_count))
        return right/self.all_count

path = "C:/Users/zhongtc/"
#path = "C:/Users/zhongtc/Documents/bop/"
#path = "E:/BoP2017_DBQA_dev_train_data/"
BB = BOP(1)
#BB.read_file(path+"BoP2017-DBQA.finalData/BoP2017-DBQA.test.txt")
#BB.read_file(path+"BoP2017_DBAQ_dev_train_data/BoP2017-DBQA.dev.txt")
#BB.write_tag_file()
BB.read_file("tag/5hum_tag_full.txt")
#BB.read_file("onlytest.txt")
#BB.read_file("wrong.txt")
#BB.read_file("qtag.txt")
p = BB.judge_all()
#BB.write_result()
z = BB.allq[1].score
print(p)