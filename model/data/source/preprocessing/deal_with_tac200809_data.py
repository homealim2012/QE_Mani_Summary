# -*- coding:utf-8 -*-

import nltk
import os, sys
import string
import re
import shutil
from lxml import html
import time
from datetime import datetime

#usage: python deal_with_tac200809_data.py tac2008(09)Folder outputFolder
not_include_update = True

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
    
    fileTime = re.findall(r".*_(\d{8}).*",filePath)[0] + '000000' + '000'       
    
    fileContent = getStringFromList(tree.xpath("//html/body/doc/text/p/text()"))
    if fileContent == "":
        fileContent = getStringFromList(tree.xpath("//html/body/doc/text/text()"))  
    #get headline
    fileHeadline = getStringFromList(tree.xpath("//html/body/doc/headline/text()"))
    fileHeadline += "." #补上句号

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
            
            sub_folders = os.listdir(os.path.join(ducFolder, folder))
            
            #get files
            fileTimeList = []
            fileContentList = []
            for sub_folder in sub_folders:
                if not_include_update and sub_folder.endswith('B'):
                    continue
                files = os.listdir(os.path.join(ducFolder, folder, sub_folder))
                for file in files:
                    if not os.path.isdir(os.path.join(ducFolder, folder, sub_folder, file)):
                        filePath = os.path.join(ducFolder, folder, sub_folder, file)
                        [fileTime, fileContent] = getFileTimeAndContentInfo(filePath)
                        fileTimeList.append(fileTime)
                        fileContentList.append(fileContent)
            #write to input
            write_file(fileTimeList, fileContentList, os.path.join(outputFolder, folder, "input.origin"))

if __name__ == '__main__':
    ducFolder = sys.argv[1]
    outputFolder = sys.argv[2]
    run(ducFolder,outputFolder);