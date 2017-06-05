import jieba.analyse
import jieba.posseg as pseg
str = "南投县立旭光高级中学在哪儿？"
str1c = pseg.cut(str)
ss = jieba.analyse.textrank(str)
k = list(str1c)
for i, j in k:
    print(i+" "+j)
print(ss)
