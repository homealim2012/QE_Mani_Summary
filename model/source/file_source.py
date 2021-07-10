# coding=utf-8
from model.source.source import source
from model.cache import cache
import numpy as np
import os


class file_source(source):

    def __init__(self, duc_year, result_name):
        data_root_path = os.path.dirname(os.path.abspath(__file__))
        self.root_dir = os.path.join(data_root_path, '../data/source/')
        self.duc_year = '2005'
        self.tfidf_dir = '/tfidf/'
        self.res_folder = 'result_NMF'
        self.ori_sentence_dir = '/ori_sentence/'
        self.dst_sentence_dir = '/sentence/'
        self.word_map_all_folder = 'wordmap'
        self.word_map_duc_folder = '/duc2005_words'
        self.duc_year = duc_year
        self.res_folder = os.path.join(data_root_path, '../data/result/'
                                       + self.duc_year + '/result_' + result_name)  # 目标文件夹路径

    def write_summary_sentence_and_index(self, topic_no, res_sentence_index):
        all_sentences = self.get_all_ori_sentence(topic_no)
        all_sentences_without_topic = all_sentences[1:]
        print(res_sentence_index)
        summary_sentences = np.array(all_sentences_without_topic)[res_sentence_index].tolist()
        self.write_summary_sentences(topic_no, summary_sentences)
        self.write_summary_sentences_index(topic_no, res_sentence_index)
        return summary_sentences

    def set_root_dir(self, root_dir):
        self.root_dir = root_dir

    def init(self):
        self.tfidf_dir = self.root_dir + self.duc_year + '/tfidf/'
        self.ori_sentence_dir = self.root_dir + self.duc_year + '/' + self.duc_year.lower() + '_filter/'
        self.dst_sentence_dir = self.root_dir + self.duc_year + '/' + self.duc_year.lower() + '_filter/'
        self.word_map_all_folder = self.root_dir + 'wordmap'
        self.word_map_duc_folder = self.root_dir + self.duc_year + '/' + self.duc_year.lower() + '_words'
        return self

    def check_res_folder_exist(self):
        if not os.path.isdir(self.res_folder):
            os.makedirs(self.res_folder, exist_ok=True)

    @cache.MapCache(ori_key='topic_map')
    def load_topic_map(self):
        topic_map = []
        listing_dir = os.listdir(self.ori_sentence_dir)
        for filename in listing_dir:
            path = os.path.join(self.ori_sentence_dir, filename)
            if os.path.isdir(path):
                topic_no = filename
                topic_map.append(topic_no)
        return topic_map

    def get_all_ori_sentence(self, topic_no):
        all_sentences = []
        fidin = open(self.ori_sentence_dir + topic_no + '/' + topic_no + '.ori_sentence', 'r+',
                     encoding='utf-8')  # 包含主题句
        for tline in fidin.read().splitlines():
            all_sentences.append(tline)
        fidin.close()
        return all_sentences

    def get_all_dst_sentence(self, topic_no):
        all_dst_sentences = []
        fidin = open(self.dst_sentence_dir + topic_no + '/' + topic_no, 'r+', encoding='utf-8')
        for tline in fidin.read().splitlines(): ##消除readlines后面的‘\n’
            all_dst_sentences.append(tline)
        fidin.close()
        return all_dst_sentences

    def get_all_sentences_order(self, topic_no):
        all_sentences_order = []
        fidin = open(self.dst_sentence_dir + topic_no + '/' + topic_no + '.order', 'r+', encoding='utf-8')
        for tline in fidin.read().splitlines():
            all_sentences_order.append(int(tline))
        fidin.close()
        return all_sentences_order

    def write_summary_sentences(self, topic_no, summary_sentences):
        fid = open(self.res_folder + '/M.' + topic_no, 'w+', encoding='utf-8')
        for sentence in summary_sentences:
            fid.write('%s\n' % sentence)
        fid.close()

    def write_summary_sentences_index(self, topic_no, summary_sentences_index):
        fid = open(self.res_folder + '/I.' + topic_no, 'w+')
        for index in summary_sentences_index:
            fid.write("%d\n" % (index + 1))
        fid.close()

    def write_parameters(self, obj):
        fid = open(self.res_folder + '/parameters.txt', 'w+')
        for key in obj.__dict__:
            value = obj.__dict__[key]
            if type(value) in (str, int, float):
                fid.write(key)
                fid.write('\t')
                fid.write(str(value))
                fid.write('\n')
        fid.close()
