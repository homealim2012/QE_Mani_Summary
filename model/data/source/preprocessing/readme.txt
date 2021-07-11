1、 DUC2005： 解压DUC2005_Summarization_Documents.zip ，并选取duc2005_docs.tar.gz\duc2005_docs 文件夹放至本目录
    DUC2006： 解压DUC2006_Summarization_Documents.tgz ，并选取duc2006_docs.tar.gz\duc2006_docs 文件夹放至本目录
    DUC2007： 解压DUC2007_Summarization_Documents.tgz ，并选取duc2007_testdocs.tar.gz\duc2007_testdocs\main文件夹放至本目录，并重命名为duc2007_docs
    TAC2008： 解压TAC2008_Update_Summarization_Documents.tgz ，并选取UpdateSumm08_test_docs_files.tar.gz\UpdateSumm08_test_docs_files文件夹放至本目录，并重命名为tac2008_docs
    TAC2009： 解压TAC2008_Update_Summarization_Documents.tgz ，并选取UpdateSumm09_test_docs_files.tar.gz\UpdateSumm09_test_docs_files文件夹放至本目录，并重命名为tac2008_docs

2、 duc200{5|6|7}_topic_statements.sgml 和 tac200{8|9}_topics.xml.txt 作为查询句

3、 安装python需要的安装包，并配置需要运行的数据集， 运行 deal_with_docs.py 以及 run_deal_with_data.py

4、将doc200{5|6|7}_filter 移动到data/source/DUC200{5|6|7} 中
   （TAC：将tac200{8|9}_filter 移动到data/source/TAC200{8|9} 中）