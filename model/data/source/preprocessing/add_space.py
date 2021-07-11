# -*- coding:utf-8 -*-

import nltk
import os, sys
import string
import re
import shutil
from lxml import html
import time
from datetime import datetime

#usage: python add_space.py duc2005Folder



def write_file(fileContentList, filePath):
    outing = open(filePath, 'w', encoding='utf-8')
    for i in range(len(fileContentList)):
        outing.write(fileContentList[i]+"\n")
    outing.close()

def read_file(filePath):
    contentList = []
    for line in open(filePath, 'r', encoding='utf-8'):
        contentList.append(line.strip("\n"))
    return contentList

def addSpaceInEachLine(filePath):
    contentList = read_file(filePath)
    for i in range(len(contentList)):
        if len(contentList[i]) > 0 and contentList[i][len(contentList[i])-1] != ' ':
            contentList[i] += " "
    write_file(contentList, filePath)

def run(ducFolder):
    folders = os.listdir(ducFolder)
    for folder in folders: #乱序
        if os.path.isdir(os.path.join(ducFolder, folder)):
            #get files
            files = os.listdir(os.path.join(ducFolder, folder))
            for file in files:
                if not os.path.isdir(os.path.join(ducFolder, folder, file)):
                    filePath = os.path.join(ducFolder, folder, file)
                    fileContent = addSpaceInEachLine(filePath)
                    
if __name__=="__main__":
    ducFolder = sys.argv[1];
    run(ducFolder);
