# -*- coding:utf-8 -*-
import deal_with_docs;
import add_space;
import merge_input;
import deal_with_sentence;
import get_jlmlmr_input;
import os;

if __name__=="__main__":
    dataset="tac2010";
    #add_space.run(dataset+"_docs");
    deal_with_docs.run(dataset);
    
    list_dirs = os.walk(dataset+"_filter");
    for root, dirs, files in list_dirs: 
        for d in dirs: 
            srcpath=os.path.join(root, d);
            merge_input.run(os.path.join(srcpath,"input.origin"),os.path.join(srcpath,"input"));
            deal_with_sentence.run(os.path.join(srcpath,"input"),os.path.join(srcpath,"time_sentence_filterSentence"),"");
            get_jlmlmr_input.run(os.path.join(srcpath,"time_sentence_filterSentence"),srcpath);
            if (os.path.exists(os.path.join(srcpath,d))):
                os.remove(os.path.join(srcpath,d))
            if (os.path.exists(os.path.join(srcpath,d+".order"))):
                os.remove(os.path.join(srcpath,d+".order"))
            if (os.path.exists(os.path.join(srcpath,d+".ori_sentence"))):
                os.remove(os.path.join(srcpath,d+".ori_sentence"))
            if (os.path.exists(os.path.join(srcpath,d+".time_order"))):
                os.remove(os.path.join(srcpath,d+".time_order"))
            os.rename(os.path.join(srcpath,"input_1.txt"), os.path.join(srcpath,d));
            os.rename(os.path.join(srcpath,"order_1.txt"), os.path.join(srcpath,d+".order"));
            os.rename(os.path.join(srcpath,"ori_sentence_1.txt"), os.path.join(srcpath,d+".ori_sentence"));
            os.rename(os.path.join(srcpath,"time_order_1.txt"), os.path.join(srcpath,d+".time_order"));
            print("已处理"+d+"主题...")