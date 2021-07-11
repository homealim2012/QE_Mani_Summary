# -*- coding:utf-8 -*-
'''
Created on 2017年8月2日

@author: John
'''
import os
import sys
import string
import re
import nltk
import treetaggerwrapper
import thulac
from nltk.stem.porter import *;

#usage: python deal_with_sentence.py time_text.txt time_sentence_filterSentence.txt wordmap.txt

wordsNumLimit = 6 #每个摘要句子最少的词语数
ChineseSentenceSplitPunc = "！？。，：；"
ChineseDeletePunc = "＃＄％＆＊＋－／＜＝＞＠＼＾＿｀｜～《》「」『』【】〔〕〖〗–—…"
ChinesePunc = "！？。，、：；＃＄％＆＊＋－／＜＝＞＠＼＾＿℃｀｜～《》「」『』【】〔〕〖〗–—…＂＇（）［］｛｝〃〝〞‘’“”"
EnglishSentenceSplitPunc = "!,.?:;"
EnglishDeletePunc = "#$%&\\*+-/<=>@^_`|~'"
EnglishPunc = string.punctuation
stopwords = nltk.corpus.stopwords.words('english')
treeTagger = treetaggerwrapper.TreeTagger(TAGLANG='en')
thul = thulac.thulac(model_path="thulac_models", seg_only=True, filt=True) #分词时会过滤一些没有意义的词语
stemmer = PorterStemmer()

def read_input(filePath):
    timeList = []
    contentList = []
    for line in open(filePath, 'r', encoding="utf-8"):
        line = line.strip('\n').strip()
        content = line.split('\t')
        timeList.append(content[0])
        contentList.append(content[1])
    return (timeList, contentList)

def write_output(timeSentenceFilterSentenceFilePath, timeOrderList, sentencesList, sentencesAfterFilterList):
    if len(timeOrderList) != len(sentencesList) or len(timeOrderList) != len(sentencesAfterFilterList):
        raise Exception('Not same length', 'timeOrderList, sentencesList, sentencesAfterFilterList have the different length')
    outing = open(timeSentenceFilterSentenceFilePath, 'w', encoding="utf-8")
    for i in range(len(timeOrderList)):
        for j in range(len(timeOrderList[i])):
            outing.write(timeOrderList[i][j]+"\t"+sentencesList[i][j]+"\t"+sentencesAfterFilterList[i][j]+"\n")
    outing.close()

def markOrder(time, sentences):
    timeList = []
    order = 1
    for i in range(len(sentences)):
        timeList.append(time+"_"+str(order))
        order += 1
    return timeList

def englishDoubleQuote(matched):
    words = matched.group()[1:-1].split(" ")
    wordsNum = 0
    info = []
    for i in range(len(words)):
        if len(words[i]) > 0:
            wordsNum += 1
            info.append(words[i])
    if 0 < wordsNum and wordsNum < 5:
        return '"' + ' '.join(info) + '"'
    return " "

def chineseDoubleQuote(matched):
    wordsNum = len(matched.group()[1:-2])
    if 0 < wordsNum and wordsNum < 6:
        return matched.group()
    return " "

def textToSentences(text):
    #过滤text: 全角空格，大中小括号，双引号，疑问句
    #英文
    #text = re.sub(r'\(.*?\)' ," ", text) #去掉小括号及里面内容
    text = re.sub(r'\[.*?\]' ," ", text) #去掉中括号及里面内容
    text = re.sub(r'\{.*?\}' ," ", text) #去掉大括号及里面内容
    text = re.sub(r'\".*?\"' ,englishDoubleQuote, text) #去掉双引号以及里面的内容，但是不过滤双引号内单词数<=4的
    text = re.sub(r"''" ," ", text) #去掉连续的两个单引号
    text = re.sub(r"(^| )'( |$)" ," ", text) #去掉单独的单引号

    #中文
    text = re.sub(u'[\u3000,\xa0]',u' ', text)
    text = re.sub(r'（.*?）' ," ", text)
    text = re.sub(r'［.*?］' ," ", text) 
    text = re.sub(r'｛.*?｝' ," ", text) 
    text = re.sub(r'＇.*?＇' ," ", text) 
    text = re.sub(r'＂.*?＂' ,chineseDoubleQuote, text) 
    text = re.sub(r'〝.*?〞' ," ", text)
    text = re.sub(r'‘.*?’' ," ", text)
    text = re.sub(r'“.*?”' ," ", text)

    text = rmOrisentencePunc(text) #在ori_sentence中去掉部分标点符号

    text = re.sub(r'  +' ," ", text) #多空格合并
    text = text.strip() #去掉多余空格以及回车换行

    sentencesList = []
    info = ""
    chinesePuncNum = 0
    englishPuncNum = 0
    for i in range(len(text)):
        if text[i] not in ChineseSentenceSplitPunc and text[i] not in EnglishSentenceSplitPunc:
            info += text[i]
        else:
            if text[i] in ChineseSentenceSplitPunc:
                chinesePuncNum += 1
            else:
                englishPuncNum += 1
            if text[i] != '?' and text[i] != '？': #去掉疑问句
                sentencesList.append(info.strip())
            info = ""
    if len(info) > 0:
        sentencesList.append(info.strip())
        info = ""
    #补句号
    endingPunc = "."
    if chinesePuncNum > englishPuncNum:
        endingPunc = "。"
    for i in range(len(sentencesList)):
        sentencesList[i] += endingPunc
    return sentencesList

def rmStopwords(line):
    words = line.strip().split(" ")
    info = ""
    for i in range(len(words)):
        if words[i] not in stopwords:
            if len(info) > 0:
                info += " "
            info += words[i]
    return info

def changeTenseByTreetagger(line):
    keepTag = set(["NN", "NNS", "NP","NPS","VV", "VVD", "VVG", "VVN", "VVP", "VVZ","JJ","JJR","JJS"])   
    wordList = treeTagger.TagText(line)
    #print(wordList);
    newLine = ""
    for gword in wordList:
        words=gword.split('\t');
        if(len(words)>=3):
            if(words[1] in keepTag):
                newLine = newLine + words[2] + " "
        elif(words[0]=="<enter>"):
            newLine = newLine + words[0] + " "
    return newLine

def changeTenseByPorterStemmer(line):
    wordList = line.strip().split(' ')
    wordListAfterStemmer = [stemmer.stem(word) for word in wordList]
    newLine = ""
    for word in wordListAfterStemmer:
        if len(newLine) > 0:
            newLine += " "
        newLine += word
    return newLine

def splitSentenceToWords(sentence):
    return thul.cut(sentence, text=True)

def rmNotInWordmap(sentence, filterWordmap):
    if len(filterWordmap) == 0:
        return sentence
    info = ""
    content = sentence.split(' ')
    for i in range(len(content)):
        if content[i] in filterWordmap:
            if len(info) > 0:
                info += " "
            info += content[i]
    return info

def rmPunc(sentence):
    info = ""
    for i in range(len(sentence)):
        if sentence[i] not in ChinesePunc and sentence[i] not in EnglishPunc:
            info += sentence[i]
        else:
            info += " "
    return info

def rmOrisentencePunc(sentence): #在ori_sentence中去掉部分标点符号
    info = ""
    for i in range(len(sentence)):
        if sentence[i] not in ChineseDeletePunc and sentence[i] not in EnglishDeletePunc:
            info += sentence[i]
        else:
            info += " "
    return info

def fileterOneSentence(sentence, filterWordmap): #去标点，分词，还原时态，变小写，过滤stopwords，过滤非词典的词
    #去标点
    sentence = rmPunc(sentence)
    #分词
    sentence = splitSentenceToWords(sentence)
    #还原时态
    #sentence = changeTenseByTreetagger(sentence)
    sentence = changeTenseByPorterStemmer(sentence)
    #变小写
    sentence = sentence.lower()
    #过滤stopwords
    sentence = rmStopwords(sentence)
    #过滤非词典的词
    sentence = rmNotInWordmap(sentence, filterWordmap)
    return sentence.split(' ')

def filterSentences(sentencesList, filterWordmap, is_title=False):
    #词语数量，去标点，分词，还原时态，变小写，过滤stopwords
    time = []
    sentences = []
    sentencesAfterFilter = []
    for i in range(len(sentencesList)):
        words = fileterOneSentence(sentencesList[i], filterWordmap)
        if is_title or len(words) >= wordsNumLimit:
            sentences.append(sentencesList[i])
            sentencesAfterFilter.append(' '.join(words))
    return (sentences, sentencesAfterFilter)

def getWordmap(filePath):
    wordmap = set()
    if len(filePath) == 0:
        return wordmap
    for line in open(filePath, 'r', encoding="utf-8"):
        wordmap.add(line.strip('\n').strip())
    return wordmap

def run(timeTextFilePath,timeSentenceFilterSentenceFilePath,wordmapFilePath):
    [timeList, textList] = read_input(timeTextFilePath)
    
    sentencesList = [] #二维list
    for i in range(len(textList)):
        sentences = textToSentences(textList[i])
        sentencesList.append(sentences)
    
    filterWordmap = getWordmap(wordmapFilePath)
    
    sentencesAfterFilterList = [] #二维list
    for i in range(len(sentencesList)):
        is_title = True if i==0 else False
        [sentencesList[i], sentencesAfterFilter] = filterSentences(sentencesList[i], filterWordmap, is_title)
        sentencesAfterFilterList.append(sentencesAfterFilter)
    
    timeOrderList = [] #二维list
    for i in range(len(sentencesList)):
        timeOrder = markOrder(timeList[i], sentencesList[i])
        timeOrderList.append(timeOrder)
    
    write_output(timeSentenceFilterSentenceFilePath, timeOrderList, sentencesList, sentencesAfterFilterList)


if __name__=="__main__":
    timeTextFilePath = sys.argv[1] #输入，时间、原文的文件路径，只有一行，以\t隔开
    timeSentenceFilterSentenceFilePath = sys.argv[2] #输出，时间、句子、处理好后的句子(空格隔开词语)的文件路径，以\t隔开
    wordmapFilePath = ""
    if len(sys.argv) > 3:
        wordmapFilePath = sys.argv[3]
    run(timeTextFilePath,timeSentenceFilterSentenceFilePath,wordmapFilePath);