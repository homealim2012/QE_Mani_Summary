# -*- coding:utf-8 -*-

import nltk
import os, sys
import string
import re
import shutil
from lxml import html
import time
from datetime import datetime

#usage: python deal_with_duc2007_data.py duc2007Folder outputFolder

def write_file(fileTimeList, fileContentList, filePath):
    if len(fileTimeList) != len(fileContentList):
        raise Exception("write_file length is different!")
    outing = open(filePath, 'w', encoding='utf-8')
    for i in range(len(fileTimeList)):
        outing.write(fileTimeList[i]+"\t"+fileContentList[i]+"\n")
    outing.close()

def getStringFromList(strList):
    info = ""
    for i in range(len(strList)):
        info += strList[i].strip("\n").strip() + " "
    return info.strip()

def getFileTimeAndContentInfo(filePath):
    htmlStr = ""
    for line in open(filePath, 'r', encoding='utf-8'):
        htmlStr += line.strip('\n')
    tree = html.fromstring(htmlStr)
    
    fileTime = ""
    fileHeadline = ""
    fileContent = ""
    if os.path.basename(filePath).find("APW") != -1: #APW file
        fileTime = getStringFromList(tree.xpath("//html/body/doc/date_time/text()"))
        #get time, get content
        if fileTime.find("/") != -1:
            fileTime = datetime.strptime(fileTime, '%m/%d/%Y %H:%M:%S').strftime("%Y%m%d%H%M%S000")
            fileContent = getStringFromList(tree.xpath("//html/body/doc/text/text()"))
        elif fileTime.find("-") != -1:
            try:
                fileTime = datetime.strptime(fileTime, '%Y-%m-%d %H:%M:%S').strftime("%Y%m%d%H%M%S000")
            except:
                try:
                    fileTime = datetime.strptime(fileTime, '%Y-%d-%m %H:%M:%S').strftime("%Y%m%d%H%M%S000")
                except:
                    fileTime = datetime.strptime(fileTime, '%Y-%m-%d %H:%M').strftime("%Y%m%d%H%M%S000")
            fileContent = getStringFromList(tree.xpath("//html/body/doc/text/p/text()"))
        else:
            raise Exception("APW file fileTime error! "+fileTime)
        #get headline
        fileHeadline = getStringFromList(tree.xpath("//html/body/doc/headline/text()"))
        fileHeadline += "." #补上句号
    elif os.path.basename(filePath).find("NYT") != -1: #NYT file
        #get time
        fileTime = getStringFromList(tree.xpath("//html/body/doc/date_time/text()"))
        if fileTime.find("-") != -1:
            fileTime = datetime.strptime(fileTime, '%Y-%m-%d %H:%M').strftime("%Y%m%d%H%M%S000")
        else:
            raise Exception("NYT file fileTime error! "+fileTime)
        #get headline
        fileHeadline = getStringFromList(tree.xpath("//html/body/doc/headline/text()"))
        fileHeadline += "." #补上句号
        #get content
        fileContent = getStringFromList(tree.xpath("//html/body/doc/text/p/text()"))
    elif os.path.basename(filePath).find("XIE") != -1: #XIE file
        #get time
        fileTime = getStringFromList(tree.xpath("//html/body/doc/date_time/text()"))
        if fileTime.find("-") != -1 and fileTime.find(":") != -1:
            fileTime = datetime.strptime(fileTime, '%Y-%m-%d %H:%M').strftime("%Y%m%d%H%M%S000")
        elif fileTime.find("-") != -1:
            fileTime = datetime.strptime(fileTime, '%Y-%m-%d').strftime("%Y%m%d%H%M%S000")
        else:
            raise Exception("NYT file fileTime error! "+fileTime)
        #get headline
        fileHeadline = getStringFromList(tree.xpath("//html/body/doc/headline/text()"))
        fileHeadline += "." #补上句号
        #get content
        fileContent = getStringFromList(tree.xpath("//html/body/doc/text/p/text()"))
    else:
        raise Exception("It is not a APW or a NYT file or a XIE file. "+filePath)
    return (fileTime, fileHeadline+" "+fileContent)

def run(ducFolder,outputFolder):
    if not os.path.isdir(outputFolder):
        os.mkdir(outputFolder)
    folders = os.listdir(ducFolder)
    for folder in folders: #乱序
        if os.path.isdir(os.path.join(ducFolder, folder)):
            #make dir
            if not os.path.isdir(os.path.join(outputFolder, folder)):
                os.mkdir(os.path.join(outputFolder, folder))
            #get files
            fileTimeList = []
            fileContentList = []
            files = os.listdir(os.path.join(ducFolder, folder))
            for file in files:
                if not os.path.isdir(os.path.join(ducFolder, folder, file)):
                    filePath = os.path.join(ducFolder, folder, file)
                    [fileTime, fileContent] = getFileTimeAndContentInfo(filePath)
                    fileTimeList.append(fileTime)
                    fileContentList.append(fileContent)
            #write to input
            write_file(fileTimeList, fileContentList, os.path.join(outputFolder, folder, "input.origin"))

if __name__ == '__main__':
    ducFolder = sys.argv[1]
    outputFolder = sys.argv[2]
    run(ducFolder,outputFolder);