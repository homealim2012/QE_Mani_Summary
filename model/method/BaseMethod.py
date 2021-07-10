# coding=utf-8
import numpy as np
import os
from model.knowledge.wordnet import WordNet
from model.cache import cache
from model.source.file_source import file_source
from model.utils import ProgressBar

class BaseMethod:

    def __init__(self, duc_year, result_name):
        self.duc_year = duc_year
        self.result_name = result_name
        self.use_sim_word = 1
        self.a = 1
        self.sim_rate = 1
        self.max_dis = 4
        self.max_word_count=5000
        root_path = os.path.dirname(os.path.abspath(__file__))
        self.word_map_all_folder = os.path.join(root_path, '../data/source/wordnet')
        self.sim_word_folder = os.path.join(root_path, '../data/source/wordnet/wordnet_json')

    def init(self):
        self.source = file_source(self.duc_year, self.result_name).init()
        cache.MapCache.map_cache = {}
        self.topic_map = self.source.load_topic_map()
        self.df_map, self.all_topic_sentences_num = self.get_df_map()
        self.tfidf_sim_word_map = self.load_tfidf_sim_word_map()
        return self

    def run(self):
        self.source.check_res_folder_exist()
        self.source.write_parameters(self)
        for topic_no in self.topic_map:
            tfidf_matrix, doc_sentence_num, wordmap = self.load_this_topic_tfidf_matrix(topic_no)
            if(self.use_sim_word==1):
                new_tfidf_topic=self.tfidf_sim_word_map[topic_no];
            else:
                new_tfidf_topic = tfidf_matrix[0,:].copy()
            new_tfidf_topic = self.mean_extension(new_tfidf_topic, tfidf_matrix)
            new_tfidf_topic = self.var_extension(new_tfidf_topic, tfidf_matrix)
            res_sentence_index,_ = self.get_sentence_score(doc_sentence_num,new_tfidf_topic,tfidf_matrix,topic_no,wordmap)
            self.source.write_summary_sentence_and_index(topic_no,res_sentence_index)

    def mean_extension(self, tfidf_topic, tfidf_matrix):
        new_tfidf_topic = tfidf_topic
        if self.mean_rate > 0:
            new_tfidf_topic += self.mean_rate * np.mean(tfidf_matrix[1:,:],axis=0)
        return new_tfidf_topic

    def var_extension(self, tfidf_topic, tfidf_matrix):
        new_tfidf_topic = tfidf_topic
        if self.var_rate > 0:
            new_tfidf_topic += self.var_rate * np.var(tfidf_matrix[1:,:],axis=0, ddof=1)
        return new_tfidf_topic

    @cache.MapCache(ori_key='df_map')
    def get_df_map(self):
        df_map = {}
        all_topic_sentences_num = 0
        for i, topic_no in enumerate(self.topic_map):
            all_dst_sentences = self.source.get_all_dst_sentence(topic_no)
            for sentence in all_dst_sentences:
                words = set(sentence.split(' '))
                for word in words:
                    if word != '':
                        df_map[word] = df_map[word] + 1 if df_map.__contains__(word) else 1
            ProgressBar.progress_bar(i+1, len(self.topic_map), '加载df_map')
            all_topic_sentences_num = all_topic_sentences_num + len(all_dst_sentences)
        print('\n')
        return df_map, all_topic_sentences_num
    
    @cache.SimWordMapCache(ori_key='sim_word_map')
    def load_tfidf_sim_word_map(self):
        tfidf_sim_word_map={}
        if self.use_sim_word == 0:
            return tfidf_sim_word_map
        for i, topic_no in enumerate(self.topic_map):
            tfidf_matrix,_,wordmap=self.load_this_topic_tfidf_matrix(topic_no)
            tfidf_topic=tfidf_matrix[0,:]
            new_tfidf_topic=self.get_new_sim_word_tfidf_topic(tfidf_topic, wordmap)
            tfidf_sim_word_map[topic_no]=new_tfidf_topic
            ProgressBar.progress_bar(i+1, len(self.topic_map), '加载tfidf_sim_word_map')
        print('\n')
        return tfidf_sim_word_map
    
    def get_new_sim_word_tfidf_topic(self, tfidf_topic, wordmap):
        all_wordmap=WordNet(self.word_map_all_folder).set_a(self.a).set_wordmap(wordmap)\
            .set_max_dis(self.max_dis)\
            .set_sim_rate(self.sim_rate)\
            .set_max_sim_word_count(self.max_word_count)\
            .set_folder(self.sim_word_folder)

        new_tfidf_topic=all_wordmap.get_new_topic_tfidf(tfidf_topic)
        return new_tfidf_topic

    def load_this_topic_tfidf_matrix(self, topic_no):
        all_dst_sentences = self.source.get_all_dst_sentence(topic_no)
        wordmap = self.get_word_map_from_dst_sentence(all_dst_sentences)
        doc_sentence_num = len(all_dst_sentences) - 1
        tfidf_matrix = self.get_tfidf(wordmap, all_dst_sentences)
        return tfidf_matrix, doc_sentence_num, wordmap

    def get_word_map_from_dst_sentence(self, all_dst_sentences):
        wordmap = {}
        for dst_sentence in all_dst_sentences:
            words = dst_sentence.split(' ')
            for word in words:
                if word != '':
                    wordmap[word]=1
        for i, word in enumerate(sorted(wordmap.keys())):
            wordmap[word]=i
        return wordmap

    def get_df(self, wordmap):
        df = np.zeros((1,len(wordmap)))
        for i,word in enumerate(sorted(wordmap.keys())):
            if self.df_map.__contains__(word):
                df[0,i] = self.df_map[word]
        return df

    def get_tfidf(self, wordmap, all_dst_sentences):
        df=self.get_df(wordmap)
        df_all=np.repeat(df, len(all_dst_sentences), axis=0)
        tf_idf=np.zeros((len(all_dst_sentences),len(wordmap)))
        for i in range(len(all_dst_sentences)):
            words = all_dst_sentences[i].split(' ')
            for j,word in enumerate(words):
                if word != '':
                    tf_idf[i,wordmap[word]]=tf_idf[i,wordmap[word]] + 1
            tf_idf[i,:]=tf_idf[i,:]/len(words)
        filter_words=['say','year','mr','u']
        for filter_word in filter_words:
            if wordmap.__contains__(filter_word):
                tf_idf[:,wordmap[filter_word]]=0
        tf_idf= tf_idf * np.log(self.all_topic_sentences_num / (df_all + 1))
        return np.mat(tf_idf)

    def get_sim_W_from_tfidf_matrix(self, tfidf_matrix: np.matrix, tfidf_topic: np.matrix, topic_no: str):
        A = np.r_[tfidf_topic, tfidf_matrix[1:, :]]
        size_Ar = np.size(A, axis=0)
        W1 = 1 - BaseMethod.cos_dist(A, A)
        W1[np.isnan(W1)] = 0
        for i in range(size_Ar):
            W1[i, i] = self.diagonal_value

        W = self.ori_cos_rate * W1
        if self.P_rate > 0:
            P = self.get_sentences_P(size_Ar, topic_no)
            for i in range(size_Ar):
                P[i, i] = self.diagonal_value
            W = W + self.P_rate * P

        if self.overlap_rate > 0:
            is_word_matrix = (tfidf_matrix > 0).astype(float)
            len_matrix1 = np.repeat(np.sum(is_word_matrix, 1), size_Ar, axis=1)
            len_matrix2 = np.repeat(np.sum(is_word_matrix.T, 0), size_Ar, axis=0)
            W3 = np.divide(is_word_matrix * is_word_matrix.T,
                           np.where(len_matrix1 < len_matrix2, len_matrix1, len_matrix2))
            W3[np.isnan(W3)] = 0
            for i in range(size_Ar):
                W3[i, i] = self.diagonal_value
            W = W + self.overlap_rate * W3
        return W

    def get_sentences_P(self, doc_number: int, topic_no: str):
        P = np.eye(doc_number);
        all_sentences_order = self.source.get_all_sentences_order(topic_no)
        all_sentences_order_index = self.get_all_sentences_order_index(all_sentences_order)
        n = 4
        for i in range(1, doc_number):
            for j in range(1, n + 1):
                if i - j >= 0 and all_sentences_order_index[i] == all_sentences_order_index[i - j]:
                    P[i, i - j] = 0.1 ** j
                if i + j < doc_number and all_sentences_order_index[i] == all_sentences_order_index[i + j]:
                    P[i, i + j] = 0.1 ** j
        return P

    def get_all_sentences_order_index(_, all_sentences_order):
        all_sentences_order_index = np.zeros((len(all_sentences_order)))
        index=0
        order=1
        for i in range(len(all_sentences_order_index)):
            if order==all_sentences_order[i]:
                all_sentences_order_index[i]=index
                order=order+1
            else:
                order=1
                index=index+1
                all_sentences_order_index[i]=index
                order=order+1
        return all_sentences_order_index

    @staticmethod
    def cos_dist(X: np.matrix, Y: np.matrix):
        normA = np.power(np.sum(np.power(np.abs(X),2), 1) , (1 / 2))
        normB = np.power(np.sum(np.power(np.abs(Y),2), 1) , (1 / 2))
        D = 1 - np.divide(X * Y.T, (normA * normB.T))
        return D
