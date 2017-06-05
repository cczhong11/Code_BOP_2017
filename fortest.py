import jieba.analyse
import jieba.posseg as pseg
str = "《社交礼仪一共有多少页"
str1c = pseg.cut(str)
ss = jieba.analyse.textrank(str)
k = list(str1c)
for i, j in k:
    print(i+" "+j)
print(ss)
