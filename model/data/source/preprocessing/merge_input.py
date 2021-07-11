# -*- coding:utf-8 -*-
'''
Created on 2017年8月2日

@author: John
'''
import os
import sys
import string

#时间戳相同的行，进行合并
#usage: python merge_input.py ${nowFolder}/input.origin ${nowFolder}/input 

def read_input(filePath):
    timeContentList = []
    for line in open(filePath, 'r', encoding="utf-8"):
        line = line.strip('\n').strip()
        content = line.split('\t')
        timeContentList.append((content[0], content[1]))
    return timeContentList

def write_file(filePath, outputList):
    outing = open(filePath, 'w', encoding="utf-8")
    for i in range(len(outputList)):
        outing.write(outputList[i][0]+"\t"+outputList[i][1]+"\n")
    outing.close()
    
    
def run(inputFile,outputFile):
    timeContentList = read_input(inputFile)
    # sort timeContentList, according to time from small to big
    timeContentListSort = sorted(timeContentList, key=lambda x: x[0])
    
    timeContentListSortMerge = []
    lastTimeStamp = "2017"
    for i in range(len(timeContentListSort)):
        if timeContentListSort[i][0] != lastTimeStamp:
            timeContentListSortMerge.append(timeContentListSort[i])
        else: #重复，需要merge
            timeContentListSortMerge[len(timeContentListSortMerge)-1] = (timeContentListSortMerge[len(timeContentListSortMerge)-1][0], timeContentListSortMerge[len(timeContentListSortMerge)-1][1]+" "+timeContentListSort[i][1])
        lastTimeStamp = timeContentListSort[i][0]
    
    write_file(outputFile, timeContentListSortMerge)

if __name__=="__main__":
    inputFile = sys.argv[1]
    outputFile = sys.argv[2]
    run(inputFile,outputFile)