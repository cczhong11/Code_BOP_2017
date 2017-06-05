import jieba
import jieba.analyse
import jieba.posseg as pseg
import re


class Ques(object):
    timeee=['年','月','日','时','分']
    timeee2=['年','月','日','时','分','路']
    loceee = ['省','市','县','区','路','道','东','西','左','右']#
    locz = ['坐落','位于']
    zwm=['长','官','者','人','工']
    numz = ['一', '二', '三', '四', '五', '六', '七', '八', '九', '十', '百', '千', '万', '和', '与']
    def __init__(self,param=None):
        self.q = ''
        self.answerdict = []
        self.answerindex = []
        self.score = []
        self.tag = ''
        self.qqdict = {}
        self.keyword = ''
        self.keyword2 = ''
        self.have_key = False
        self.get_english = False
        self.jiafen = {}
        self.w_commonword = 2
        self.w_humkeyword = 30
        self.w_humkeyword2 = 90
        self.humhum = 40
        self.w_tcommonword = 2
        self.w_tkeyword = 30
        self.w_tkeyword2 = 90
        self.thum = 40
        self.w_ncommonword = 2
        if param!=None:
            self.w_commonword=param[0]
            self.w_humkeyword = param[1]
            self.w_humkeyword2 = param[2]
            self.humhum = param[3]

    def scoreQ(self,stopword=None):
        str1c = jieba.analyse.extract_tags(self.q)
        strl = jieba.lcut(self.q)
        str1d = pseg.cut(self.q)# 词性
        lastn = ''
        lastv = ''
        flag = 0
        tmp = []
        if stopword != None:
            for i in strl:
                if i not in stopword:
                    tmp.append(i)
            strl = tmp
        if self.tag == '5hum':
            vindex = 0
            lastni = 0
            lastvi = 0
            for i, j in str1d:
                vindex = vindex + 1
                if i == "《":
                    flag = 1
                    continue
                if i == "》":
                    flag = 0
                if flag == 1 :
                    lastn = ''
                    lastv = ''
                    continue
                if j[0] == 'n' and i != "职位":
                    lastn = i
                    lastni = vindex
                if j[0] == 'v' and i not in ['来','是']:
                    lastv = i
                    lastvi = vindex
            if lastni>lastvi:
                self.keyword = lastv
                self.keyword2 = lastn
            else:
                self.keyword2 = lastv
                self.keyword = lastn
            if self.keyword!='':                
                self.qqdict[self.keyword] = self.w_humkeyword
           
            if self.keyword2!='':
                #self.keyword2 = lastn
                self.qqdict[self.keyword2] = self.w_humkeyword2
            for i in range(len(strl)):
                if strl[i] not in self.qqdict.keys() and strl[i] not in ['，','？']:
                    self.qqdict[strl[i]] = self.w_commonword
                #if strl[i] in str1c:
                #    self.qqdict[strl[i]] = self.qqdict[strl[i]] +
        elif self.tag == '1time':
            vindex = 0
            lastni = 0
            lastvi = 0
            for i, j in str1d:
                vindex = vindex + 1
                if i == "《":
                    flag = 1
                    continue
                if i == "》":
                    flag = 0
                if flag == 1 :
                    lastn = ''
                    lastv = ''
                    continue
                if j[0] == 'n' and i not in ["时候","时间"]:
                    lastn = i
                    lastni = vindex
                if j[0] == 'v' and i not in ['来','是','开','到']:
                    lastv = i
                    lastvi = vindex
            if lastni>lastvi:
                self.keyword = lastv
                self.keyword2 = lastn
            else:
                self.keyword2 = lastv
                self.keyword = lastn
            if self.keyword!='':                
                self.qqdict[self.keyword] = self.w_tkeyword
           
            if self.keyword2!='':
                #self.keyword2 = lastn
                self.qqdict[self.keyword2] = self.w_tkeyword2
            for i in range(len(strl)):
                if strl[i] not in self.qqdict.keys() and strl[i] not in ['，','？']:
                    self.qqdict[strl[i]] = self.w_tcommonword
                
        elif self.tag == '2num':
            vindex = 0
            lastni = 0
            lastvi = 0
            for i, j in str1d:
                vindex = vindex + 1
                if i == "《":
                    flag = 1
                    continue
                if i == "》":
                    flag = 0
                if flag == 1 :
                    lastn = ''
                    lastv = ''
                    continue
                if j[0] == 'm' and len(i) == 2 and i[0] == '几':
                    lastn = i[1]
                    lastni = vindex
                if j[0] == 'n' or  j == 'eng' and i not in ["时候","时间",'地方','位置']:
                    lastn = i
                    lastni = vindex
                if j[0] == 'v' and i not in ['来','是','开','到','有']:
                    lastv = i
                    lastvi = vindex
            if lastni>lastvi:
                self.keyword = lastv
                self.keyword2 = lastn
            else:
                self.keyword2 = lastv
                self.keyword = lastn
            if self.keyword!='':                
                self.qqdict[self.keyword] = self.w_tkeyword
           
            if self.keyword2!='':
                #self.keyword2 = lastn
                self.qqdict[self.keyword2] = self.w_tkeyword2
            for i in range(len(strl)):
                if strl[i] not in self.qqdict.keys() and strl[i] not in ['，','？']:
                    self.qqdict[strl[i]] = self.w_tcommonword
        elif self.tag == '3ent':
            for i, j in str1d:                
                if j[0] == 'n' :#and not panduan(i,['址','位置']):
                    lastn = i
                if j[0] == 'v' and i!='是':
                    lastv = i
            if lastn!='':
                self.keyword = lastn                
                self.qqdict[lastn] = 45
            else:
                pass            
            #self.qqdict[lastv] = 30
            for i in range(len(strl)):
                if strl[i] not in self.qqdict.keys():
                    self.qqdict[strl[i]] = 2
                if strl[i] in str1c:
                    self.qqdict[strl[i]] = self.qqdict[strl[i]] +2
        elif self.tag == '4loc':
            for i, j in str1d:                
                if j[0] == 'n' :#and not panduan(i,['址','位置']):
                    lastn = i
                if j[0] == 'v' and i!='是':
                    lastv = i
            if lastn!='':
                self.keyword = lastn                
                self.qqdict[lastn] = 45
            else:
                pass
            #self.qqdict[lastv] = 30
            for i in range(len(strl)):
                if strl[i] not in self.qqdict.keys():
                    self.qqdict[strl[i]] = 2
                if strl[i] in str1c:
                    self.qqdict[strl[i]] = self.qqdict[strl[i]] +2
        elif  self.tag == '6des':
            lastnn = ''
            for i, j in str1d:                
                if j[0] == 'n' :#and not panduan(i,['文','语']):
                    lastnn = lastn
                    lastn = i
                if j[0] == 'v' and i!='是':
                    lastv = i
            if lastn!='':
                self.keyword = lastn           
                self.qqdict[lastn] = 45
                self.qqdict[lastnn] = 10
            else:
                pass
            if panduan(self.q,['英语','英文','译','拼音','读']):
                self.get_english=True
            #self.qqdict[lastv] = 50
            for i in range(len(strl)):
                if strl[i] not in self.qqdict.keys():
                    self.qqdict[strl[i]] = 5
                if strl[i] in str1c:
                    self.qqdict[strl[i]] = self.qqdict[strl[i]] +5
        else:
            for i, j in str1d:                
                if j[0] == 'n' :#and not panduan(i,['址','位置']):
                    lastn = i
                if j[0] == 'v' and i!='是':
                    lastv = i
            if lastn!='':
                self.keyword = lastn                
                self.qqdict[lastn] = 45
            else:
                pass
            #self.qqdict[lastv] = 30
            for i in range(len(strl)):
                if strl[i] not in self.qqdict.keys():
                    self.qqdict[strl[i]] = 2
                if strl[i] in str1c:
                    self.qqdict[strl[i]] = self.qqdict[strl[i]] +2
    def read_alla(self):
        for i in self.answerdict:
            if self.keyword2 in i:
                self.have_key = True
                break
    def scoreA(self,model=None):        
        o = 0
        for l2 in self.answerdict:
            c = 0
            self.jiafen[o]=[]
            if self.tag == '5hum':
                if '：' in l2:
                    c = 20
                    self.jiafen[o].append("冒号")
                for i in self.qqdict.keys():
                    if i in l2 and i not in ['','的','是']:
                        c = c + self.qqdict[i]
                        self.jiafen[o].append(i)
                
                if self.keyword2 in l2:
                    c = c + 10
                zz = jieba.lcut(l2)
                if model == None:
                    for k in self.keyword2:
                        if k in l2 and k not in ['者','人','任']:
                            c = c + 60
                            self.jiafen[o].append(k)
                            break
            elif self.tag == '1time':
                for i in self.qqdict.keys():
                    if i in l2 :
                        c = c + self.qqdict[i]
                        self.jiafen[o].append(i)
                ti = 0
                ki = 0
                for j in self.timeee:
                    if j in l2:
                        c = c + self.thum
                        self.jiafen[o].append(j)
                        ti = l2.index(j)
                        break
                #if not self.have_key:
                if self.keyword2 in l2:
                    c = c + 20
                for k in self.keyword:
                    if k in l2:
                        c = c + self.thum/10
                        self.jiafen[o].append(k)
                        ki = l2.index(k)
                        break
                for k in self.keyword2:
                    if k in l2 and k not in ['者','人','任']:
                        c = c + self.thum
                        self.jiafen[o].append(k)
                        ki = l2.index(k)
                        break
                #if ti*ki != 0:
                #    if abs(ki-ti)<6:
                #        c = c + 10*(10-ti+ki)
                #        self.jiafen[o].append("distance"+str(20-ti+ki))
            elif self.tag == "4loc":
                for i in self.qqdict.keys():
                    if i in l2:
                        c = c + self.qqdict[i]
                for j in self.loceee:
                    if j in l2:
                        #print(j+" "+l2)
                        c = c + 60
                        break
                for j in self.locz:
                    if j in l2:
                        #print(j+" "+l2)
                        c = c + 60
                        break
                if not self.have_key:
                    for k in self.keyword:
                        if k in l2:
                            c = c + 50
            elif self.tag == '3ent':
                if '：' in l2:
                    c = 20
                    self.jiafen[o].append("冒号")
                for i in self.qqdict.keys():
                    if i in l2:
                        c = c + self.qqdict[i]
                        self.jiafen[o].append(i)
                l2 = l2.replace("，",'')
                if panduan(self.q,['什么是','是什么','指什么']):
                    kk = self.q.replace("什么",'')
                    kk = kk.replace("是",'')
                    kk = kk.replace("指",'')
                    kk = kk.replace("？",'')   
                    kk = kk.replace("定义",'')
                    kk = kk.replace("的",'')
                    kk = kk.replace("地","")                 
                    s = "^"+kk           
                    l2 = l2.replace("，",'')
                    try:
                        if len(re.findall(s+"是",l2))>0:                        
                            c = c + 15
                            self.jiafen[o].append("定义")
                        if len(re.findall(s,l2))>0:                        
                            c = c + 12         
                            self.jiafen[o].append("定义")               
                        elif kk+'是' in l2:
                            c = c + 5
                            self.jiafen[o].append("定义")
                    except:
                        c = c
                if not self.have_key:
                    for k in self.keyword:
                        if k in l2:
                            c = c + 50
                            self.jiafen[o].append(k)
            elif self.tag == '2num':
                l2 = re.sub("\[\d+\]","",l2)
                l2 = re.sub(" ","",l2)
                if "、" in l2 and panduan(self.q,["哪些","哪几"]):
                    c = c + 20
                    self.jiafen[o].append("顿号")
                if "：" in l2 :
                    c = c + 10
                    self.jiafen[o].append("冒号")
                if len(re.findall('[0-9]',l2))>0 or panduan(l2,self.numz):
                        c = c + 50
                        self.jiafen[o].append("数字")
                for i in self.qqdict.keys():
                    if i in l2:
                        c = c + self.qqdict[i]
                        self.jiafen[o].append(i)
                for j in self.timeee2:
                    if j in l2 and not panduan(l2,['有时']) and len(re.findall('[0-9]+'+"名",l2))==0:
                        c = c - 50
                        self.jiafen[o].append("-时间"+j)
                        break
                if not self.have_key:
                    for k in self.keyword2:
                        if k in l2:
                            c = c + self.w_humkeyword2
                            self.jiafen[o].append(k)
            elif self.tag == '6des':
                if '：' in l2:
                    c = 20
                if self.get_english:
                    if len(re.findall('[A-z]',l2))>0:
                        c = c + 20
                for i in self.qqdict.keys():
                    if i in l2:
                        c = c + self.qqdict[i]
                if not self.have_key:
                    for k in self.keyword:
                        if k in l2:
                            c = c + 50
            else:
                if '：' in l2:
                    c = 20
                for i in self.qqdict.keys():
                    if i in l2:
                        c = c + self.qqdict[i]
                if not self.have_key:
                    for k in self.keyword:
                        if k in l2:
                            c = c + 50            
            self.score.append(c)
            o = o + 1

    def judge(self):        
        for i,j in enumerate(self.score):
            if j == max(self.score):          
                if i not in self.answerindex:
                    return False
        return True
    def rescore(self):
        win = 1
        if self.tag == '5hum':
            z = [i for i in range(len(self.score)) if self.score[i] >= 30]
            for kk in self.answerindex:
                if kk not in z:
                    win = 0
                    break
            #print(z)            
            for k in z:
                if panduan(self.q,['第一','目前']):
                    if panduan(self.answerdict[k],['首','创','现']):
                        self.score[k] = self.score[k]+self.humhum
                str1d = pseg.cut(self.answerdict[k])
                for i,j in str1d:                    
                    if j == 'nr' or j == 'eng':
                        self.score[k] = self.score[k]+self.humhum
                        self.jiafen[k].append(i)
                        break
        elif self.tag == '1time':
            z = [i for i in range(len(self.score)) if self.score[i] >= 30]
            for kk in self.answerindex:
                if kk not in z:
                    win = 0
                    break
            #print(z)            
            for k in z:
                if panduan(self.q,['创立','开办','追','建立','破土动工']):
                    if panduan(self.answerdict[k],['开办','创','现','始']):
                        self.score[k] = self.score[k]+self.thum
                        self.jiafen[k].append("同义词")
        elif self.tag == '2num':
            z = [i for i in range(len(self.score)) if self.score[i] >= 30]
            for kk in self.answerindex:
                if kk not in z:
                    win = 0
                    break
            for k in z:
                if panduan(self.q,['人']):
                    if len(re.findall('[0-9]+名|\d+人',self.answerdict[k])) >0:
                        self.score[k] = self.score[k]+self.thum
                        self.jiafen[k].append("同义词")
                if panduan(self.q,['多大']):
                    if panduan(self.answerdict[k],['亩','平方']):
                        self.score[k] = self.score[k]+self.thum
                        self.jiafen[k].append("同义词")
                if panduan(self.q,['钱','贵']):
                    if panduan(self.answerdict[k],['元','$']):
                        self.score[k] = self.score[k]+self.thum
                        self.jiafen[k].append("同义词")
                if panduan(self.q,['长','宽','高']):
                    if panduan(self.answerdict[k],['分钟','米','m']):
                        self.score[k] = self.score[k]+self.thum
                        self.jiafen[k].append("同义词")
        elif self.tag == '3ent':
            z = [i for i in range(len(self.score)) if self.score[i] >= 30]
            for kk in self.answerindex:
                if kk not in z:
                    win = 0
                    break
        return win
def panduan(word,list):
    for i in list:
        if i in word:
            return True
    return False 