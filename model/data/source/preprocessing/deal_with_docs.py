# -*- coding:utf-8 -*-

import deal_with_duc2005_data;
import deal_with_duc2006_data;
import deal_with_duc2007_data;
import deal_with_tac200809_data;
import deal_with_topic_statements;
import deal_with_tac_topic_statements;


def run(dataset):
    if(dataset=="duc2005"):
        deal_with_duc2005_data.run(dataset+"_docs",dataset+"_filter");
    elif(dataset=="duc2006"):
        deal_with_duc2006_data.run(dataset+"_docs",dataset+"_filter");
    elif(dataset=="duc2007"):
        deal_with_duc2007_data.run(dataset+"_docs",dataset+"_filter");
    elif(dataset=='tac2008' or dataset=='tac2009'):
        deal_with_tac200809_data.run(dataset+"_docs",dataset+"_filter");
    
    if(dataset=="duc2005" or dataset=="duc2006" or dataset=="duc2007"):
        deal_with_topic_statements.run(dataset+"_topic_statements.sgml",dataset+"_filter");
    elif(dataset=='tac2008' or dataset=='tac2009'):
        deal_with_tac_topic_statements.run(dataset+"_topics.xml.txt",dataset+"_filter");
    else:
        print("no need to deal with topic");
    
if __name__=="__main__":
    run("tac2009");       
    