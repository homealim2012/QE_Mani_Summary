1、first you need to pip install easydict==1.9 and pip install numpy==1.18.1
2、run main.py, the first parameter of the function is to set the parameters of the model
3、if use_sim_word =1 , you need to run data/source/wordnet/get_sim_inverted_index.py to get word similarity matrix.
4、 if you need to use ROUGE, please to search "windows ROUGE" for more help.

单独运行main.py时 需要将该文件移动到model文件夹外
