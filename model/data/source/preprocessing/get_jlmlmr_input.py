# -*- coding:utf-8 -*-
'''
Created on 2017年8月2日

@author: John
'''
import os
import sys
import string

#usage: python get_jlmlmr_input.py time_sentence_filterSentence JLMLMR_running
def write_file(filePath, outputList):
    outing = open(filePath, 'w', encoding="utf-8")
    for i in range(len(outputList)):
        outing.write(outputList[i]+"\n")
    outing.close()
    
def run(timeSentenceFiltersentenceFilePath,jlmlmrRunningFolder):
    
    oriSentenceFilePath = os.path.join(jlmlmrRunningFolder, 'ori_sentence_1.txt')
    orderFilePath = os.path.join(jlmlmrRunningFolder, 'order_1.txt')
    inputFilePath = os.path.join(jlmlmrRunningFolder, 'input_1.txt')
    timeAndOrderFilePath = os.path.join(jlmlmrRunningFolder, 'time_order_1.txt')
    
    oriSentenceList = []
    orderList = []
    inputList = []
    timeAndOrderList = []
    for line in open(timeSentenceFiltersentenceFilePath, 'r', encoding="utf-8"):
        line = line.strip('\n').strip()
        content = line.split('\t')
        timeAndOrderList.append(content[0])
        orderList.append(content[0].split('_')[1])
        oriSentenceList.append(content[1])
        print(content)
        inputList.append(content[2])
        
    
    write_file(oriSentenceFilePath, oriSentenceList)
    write_file(orderFilePath, orderList)
    write_file(inputFilePath, inputList)
    write_file(timeAndOrderFilePath, timeAndOrderList)

if __name__=="__main__":
    timeSentenceFiltersentenceFilePath = sys.argv[1]
    jlmlmrRunningFolder = sys.argv[2]
    run(timeSentenceFiltersentenceFilePath,jlmlmrRunningFolder);
