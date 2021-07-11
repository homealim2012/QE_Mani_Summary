# -*- coding:utf-8 -*-

import nltk
import os, sys
import shutil
from lxml import html
import time
from datetime import datetime

#usage: python deal_with_duc2005_data.py duc2005Folder outputFolder

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
    if os.path.basename(filePath).find("FT") != -1: #FT file
        #get time
        fileTime = getStringFromList(tree.xpath("//html/body/doc/date/text()"))
        if len(fileTime) != 6:
            raise Exception("fileTime is not 6 length!")
        if fileTime[0] == '0':
            fileTime = "20" + fileTime + "000000000"
        else:
            fileTime = "19" + fileTime + "000000000"
        #get headline
        fileHeadline = getStringFromList(tree.xpath("//html/body/doc/headline/text()"))
        fileHeadline += "." #补上句号
        #get content
        fileContent = getStringFromList(tree.xpath("//html/body/doc/text/text()"))
    elif os.path.basename(filePath).find("LA") != -1: #LA file
        #get time
        fileTime = getStringFromList(tree.xpath("//html/body/doc/date/p/text()"))
        timePieces = fileTime.split(',')
        if len(timePieces) != 4:
            raise Exception("len(timePieces) != 4, "+filePath+", fileTime: "+fileTime)
        fileTime = datetime.strptime(timePieces[0]+","+timePieces[1], '%B %d, %Y').strftime("%Y%m%d%H%M%S000")
        #get headline
        fileHeadline = getStringFromList(tree.xpath("//html/body/doc/headline/p/text()"))
        fileHeadline += "." #补上句号
        #get content
        fileContent = getStringFromList(tree.xpath("//html/body/doc/text/p/text()"))
    else:
        raise Exception("It is not a FT or a LA file. "+filePath)
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