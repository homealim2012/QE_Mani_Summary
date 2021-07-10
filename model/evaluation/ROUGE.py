# coding=utf-8
import os
import stat
import platform

class ROUGE:

    def __init__(self, duc_year, verify_name):
        data_root_path = os.path.dirname(os.path.abspath(__file__))
        self.src_root_dir = os.path.join(data_root_path, '../data/source/')
        self.res_root_dir = os.path.join(data_root_path, '../data/result/')
        self.duc_year = duc_year
        self.verify_name = verify_name
        self.model_dir = 'model'
        self.peer_dir = 'peer'
        self.topic_dir = 'sentence'
        self.verify_file_name = ''
        self.perl_file_name = ''
        self.rouge_length = 250
        self.usePeer = 0
        self.reWriteXML = 1
        self.reWritePerl = 1
        self.topic_map = {}
        self.topic_peer_map = {}

    def init(self):
        self.topic_dir = self.src_root_dir + self.duc_year + '/' + self.duc_year.lower() + '_filter/'
        self.model_dir = self.res_root_dir + self.duc_year + '/model/'
        self.peer_dir = self.res_root_dir + self.duc_year + '/peer/'
        self.perl_file_name = self.res_root_dir + 'runROUGE_' + self.duc_year + '_' + self.verify_name + '.pl'
        self.verify_file_name = self.res_root_dir + self.duc_year + '/' + 'verify_' + self.verify_name + '.xml'
        self.output_dir = self.res_root_dir + self.duc_year + '-output/'
        self.topic_map = {}
        self.topic_peer_map = {}
        return self

    def set_rouge_length(self, length):
        self.rouge_length = length
        return self

    def run(self):
        if not os.path.isfile(self.verify_file_name) or self.reWriteXML == 1:
            print('重写verify.xml文件...')
            self.get_topic_set();
            self.get_topic_map();
            if self.usePeer == 1:
                self.get_topic_peer_map()
            self.writeVerifyXML();
        if not os.path.isfile(self.perl_file_name) or self.reWritePerl == 1:
            print('重写perl文件...')
            self.writePerl();
        self.runROUGE();

    def get_topic_set(self):
        listing_dir=os.listdir(self.topic_dir)
        for filename in listing_dir:
            path = os.path.join(self.topic_dir, filename)
            if os.path.isdir(path):
                topic_no = filename
                self.topic_map[topic_no]=[];
                self.topic_peer_map[topic_no]=[];

    def get_topic_map(self):
        listing_dir=os.listdir(self.model_dir)
        for filename in listing_dir:
            path = os.path.join(self.model_dir, filename)
            if os.path.isfile(path):
                model_name = filename
                S = model_name.split('.')
                if S[len(S)-1] == 'html':
                    continue
                topic_ind = S[0] + S[3]
                if self.duc_year == 'DUC2005':
                    topic_ind = (S[0] + S[3]).lower() #2005 不需要注释，2006需要注释掉-------------------------------------------------------------------------------------------------
                self.topic_map[topic_ind].append(model_name)

    def get_topic_peer_map(self):
        listing_dir=os.listdir(self.peer_dir)
        for filename in listing_dir:
            path = os.path.join(self.peer_dir, filename)
            if os.path.isfile(path):
                model_name = filename
                S = model_name.split('.')
                if S[len(S)-1] == 'html':
                    continue
                topic_ind = S[0] + S[3];
                if self.duc_year == 'DUC2005':
                    topic_ind = (S[0] + S[3]).lower() #--------------------------------------------------------------------------------------------------------------------------------
                self.topic_peer_map[topic_ind]= self.topic_peer_map[topic_ind].append(model_name)

    def writeVerifyXML(self):
        f = open(self.verify_file_name, 'w+')
        f.write('<ROUGE-EVAL version="1.0">\n')
        for topic_no in self.topic_map:
            topic_model_files_list = self.topic_map[topic_no]
            for m in range(len(topic_model_files_list)):
                f.write('<EVAL ID="' + topic_model_files_list[m] + '">\n')
                f.write('<PEER-ROOT>')
                if self.usePeer:
                    f.write('peer')
                else:
                    f.write('result_' + self.verify_name)
                f.write('</PEER-ROOT>\n')
                f.write('<MODEL-ROOT>')
                f.write('model')
                f.write('</MODEL-ROOT>\n')
                f.write('<INPUT-FORMAT TYPE="SPL">')
                f.write('</INPUT-FORMAT>\n')
                f.write('<MODELS>\n')
                topic_model_files = self.topic_map[topic_no]
                for j in range(len(topic_model_files)):
                    if topic_model_files_list[m] == topic_model_files[j]:
                        continue
                    S = topic_model_files[j].split('.')
                    f.write('<M ID="' + S[4] + '">' + topic_model_files[j] + '</M>\n')
                f.write('</MODELS>\n')
                f.write('<PEERS>')

                topic_peer_files = self.topic_peer_map[topic_no]
                if self.usePeer:
                    for j in range(len(topic_peer_files)):
                        S = topic_peer_files[j].split('.')
                        f.write('<P ID="' + S[4] + '">' + topic_peer_files[j] +'</P>\n')
                else:
                    f.write('<P ID="P">')
                    #fprintf(fid,[topic_no]);%5种summary抽取结果   ---------------------------------------------------------------------------------------------------------------
                    f.write('M.' + topic_no);
                    f.write('</P>\n');
                S0=topic_model_files_list[m].split('.');
                #fprintf(fid,['<P ID="',S0{5},'">../model/',topic_model_files_list{m},'</P>\n']);
                f.write('</PEERS>\n')
                f.write('</EVAL>')
        f.write('</ROUGE-EVAL>\n')
        f.close();

    def writePerl(self):
        f = open(self.perl_file_name, 'w+')
        f.write('#!/usr/bin/perl\n')
        f.write('use Cwd;\n')
        f.write('$curdir=getcwd;\n')
        f.write('$ROUGE="ROUGE-1.5.5.pl";\n')
        root_path = os.path.dirname(os.path.abspath(__file__)).replace('\\', '/')
        path = root_path + '/../data/result/' + self.duc_year
        f.write('chdir("' + path + '");\n')
        f.write('$cmd="$ROUGE -e ../data -d -l ' + str(self.rouge_length) +
                      ' -n 4 -w 1.2 -m -2 4 -u -c 95 -r 1000 -f A -p 0.5 -t 0 -a ' +
                      'verify_' + self.verify_name + '.xml' + ' > ../' + self.duc_year + '-output/ROUGE_' + self.verify_name +
                      '.out";\n')
        f.write('print $cmd,"\\n";\n')
        f.write('system($cmd);')
        f.write('chdir($curdir);')
        f.close()

    def runROUGE(self):
        if not os.path.isdir(self.output_dir):
            os.makedirs(self.output_dir, exist_ok=True)
        sys = platform.system()
        if sys == 'Windows':
            #set PATH = %PATH%;E:\Program Files\ROUGE-1.5.5
            os.system((self.perl_file_name + ' &').replace('/', '\\'))
        if sys == 'Linux':
            os.chmod(self.perl_file_name, stat.S_IRWXU)
            os.system(self.perl_file_name + ' &')
