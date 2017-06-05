import os
LTP_DATA_DIR = 'C:/Users/zhongtc/Desktop/wenjiao/ltp-data-v3.3.1/ltp_data/'  # ltp模型目录的路径
ner_model_path = os.path.join(LTP_DATA_DIR, 'ner.model')  # 命名实体识别模型路径，模型名称为`pos.model`
cws_model_path = os.path.join(LTP_DATA_DIR, 'cws.model')  # 分词模型路径，模型名称为`cws.model`
pos_model_path = os.path.join(LTP_DATA_DIR, 'pos.model')  # 词性标注模型路径，模型名称为`pos.model`
import jieba
from pyltp import NamedEntityRecognizer
from pyltp import Postagger
from pyltp import Segmentor
segmentor = Segmentor()  # 初始化实例
segmentor.load(cws_model_path)  # 加载模型
words = segmentor.segment('1950年-1953年，安徽大学做了哪些调整？')  # 分词
#str1 = '1949年，中国人民解放军攻占重庆后，11技工学校发生了什么变化？'
#words = list(jieba.cut(str1.strip()))
postagger = Postagger() # 初始化实例
postagger.load(pos_model_path)  # 加载模型
recognizer = NamedEntityRecognizer() # 初始化实例
recognizer.load(ner_model_path)  # 加载模型

postags = postagger.postag(words)  # 词性标注
netags = recognizer.recognize(words,postags)  # 命名实体识别

print('\t'.join(netags))
words = segmentor.segment('莫阿大学龙化石有哪几部分组成？')  # 分词
postags = postagger.postag(words)  # 词性标注
netags = recognizer.recognize(words,postags)  # 命名实体识别

print('\t'.join(netags))

recognizer.release()  # 释放模型
postagger.release()  
#segmentor.release()