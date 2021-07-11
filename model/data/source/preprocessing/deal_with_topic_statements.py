# -*- coding:utf-8 -*-

import nltk
import os, sys
import string
import re
import shutil
from lxml import html
import time
from datetime import datetime

#usage: python deal_with_topic_statements.py ${dataset}_topic_statements.sgml ${dataset}_filter

EnglishPunc = string.punctuation
splitWordsFilePath = "split_words.txt"

def read_file(filePath):
    infoList = []
    for line in open(filePath, 'r', encoding='utf-8'):
        line = line.strip("\n").strip()
        infoList.append(line)
    return infoList

def write_adding_file(filePath, info):
    contentList = read_file(filePath)
    outing = open(filePath, 'w', encoding='utf-8')
    for i in range(len(contentList)):
        outing.write(contentList[i]+"\n")
    outing.write(info+"\n")
    outing.close()

def filterPunc(info):
    info = re.sub(r'\n' ," ", info)
    result = ""
    for i in range(len(info)):
        if info[i] not in EnglishPunc:
            result += info[i]
        else:
            result += " "
    return result.strip()

def getWordmapList(filePath):
    wordmap = []
    if len(filePath) == 0:
        return wordmap
    for line in open(filePath, 'r', encoding="utf-8"):
        wordmap.append(line.strip('\n').strip())
    return wordmap

def replaceSplitWordsToPeriod(text): #将从句进行划分，把that, who, what等替换为空格
    splitWords = getWordmapList(splitWordsFilePath)
    for i in range(len(splitWords)):
        text = re.sub("(^| )"+splitWords[i]+"( |$)", " ", text)
    return text.strip()

def getFileInfo(filePath):
    sgmlStr = ""
    for line in open(filePath, 'r', encoding='utf-8'):
        sgmlStr += line.strip('\n') + " " # add space
    
    folderNameList = re.findall(r"<num>\s*(.*?)\s*</num>", sgmlStr)
    titleList = re.findall(r"<title>\s*(.*?)\s*</title>", sgmlStr)
    narrList = re.findall(r"<narr>\s*(.*?)\s*</narr>", sgmlStr)

    return (folderNameList, titleList, narrList)

def run(topicFilePath,outputFolder):
    (folderNameList, titleList, narrList) = getFileInfo(topicFilePath)
    for i in range(len(folderNameList)):
        info = "10000000000000000\t" + replaceSplitWordsToPeriod(filterPunc(titleList[i])) + " " + replaceSplitWordsToPeriod(filterPunc(narrList[i])) + "."
        write_adding_file(os.path.join(outputFolder, folderNameList[i], "input.origin"), info)

if  __name__=="__main__":
    topicFilePath = sys.argv[1];
    outputFolder = sys.argv[2];
    run(topicFilePath,outputFolder);
