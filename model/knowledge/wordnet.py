import os
from easydict import EasyDict as edict
import json
import numpy as np

class WordNet:

    def __init__(self, word_map_all_folder):
        self.word_map_all_folder = word_map_all_folder
        self.sim_rate = 1
        self.a = 1
        self.max_dis = 4
        self.max_sim_word_count = 5000
        self.wordmap = {}
        self.folder = ''
        self.map_stem_to_treetagger, self.map_treetagger_to_stem = self.get_map_stem_to_treetagger()
        self.wordmap_all = self.get_word_map_all();

    def set_word_map_all_folder(self, word_map_all_folder):
        self.word_map_all_folder=word_map_all_folder
        return self
        
    def set_folder(self, folder):
        self.folder=folder
        return self
        
    def set_max_sim_word_count(self, max_sim_word_count):
        self.max_sim_word_count=max_sim_word_count
        return self
        
    def set_max_dis(self, max_dis):
        self.max_dis=max_dis
        return self
        
    def set_a(self, a):
        self.a=a
        return self
        
    def set_sim_rate(self, sim_rate):
        self.sim_rate=sim_rate
        return self
        
    def set_use_stem(self, use_stem):
        self.use_stem = use_stem;
        return self

    def set_wordmap(self, wordmap):
        self.wordmap = wordmap
        return self

    def get_new_topic_tfidf(self, tfidf_topic):
        word_arr = sorted(self.wordmap.keys())
        topic_word_arr = np.array(list(word_arr))[np.array(tfidf_topic)[0,:] > 0]
        self.sim_word_map = self.sim_word_list_adapter(topic_word_arr)
        tfidf = np.zeros((np.sum(np.array(tfidf_topic)[0,:] > 0), tfidf_topic.shape[1]))
        ori_map = {}
        for k, key in enumerate(self.sim_word_map):
            ori_map[key] = k

        for key in self.sim_word_map:
            sub_map = self.sim_word_map[key]
            for sub_key in self.sim_word_map[key]:
                if self.wordmap.__contains__(sub_key):
                    tfidf[ori_map[key], self.wordmap[sub_key]] = tfidf_topic[0, self.wordmap[key]] * sub_map[sub_key]
        new_tfidf_topic = self.sim_rate * np.max(tfidf, axis=0) + tfidf_topic
        return new_tfidf_topic

    def sim_word_list_adapter(self, topic_word_arr):
        sim_word_map={}
        f_count = open(os.path.join(self.folder, 'word_count.json'))
        w = edict(json.load(f_count))
        f_count.close()
        for ori_word in topic_word_arr:
            temp = edict()
            temp.ori = ori_word
            if not self.wordmap_all.__contains__(ori_word):
                if not self.map_stem_to_treetagger.__contains__(ori_word):
                    continue
                else:
                    ori_word=self.map_stem_to_treetagger[ori_word]

            if not w.count_map.__contains__(ori_word):
                continue

            count_info=np.array(w.count_map[ori_word])
            if sum(count_info[count_info[:,0] <= self.max_dis, 1])>=self.max_sim_word_count:
                continue
            f_word = open(os.path.join(self.folder, '_' + ori_word + '.json'))
            s = json.load(f_word)
            f_word.close()
            sim_list = s['sim_map'][ori_word]
            for a_sim_list in sim_list:
                a_sim_list = edict(a_sim_list)
                if a_sim_list.sim <= self.max_dis:
                    if a_sim_list.word != ori_word:
                        if not sim_word_map.__contains__(temp.ori):
                            sim_word_map[temp.ori]={}

                        temp.dst = a_sim_list.word
                        temp.sim = self.a / (self.a + a_sim_list.sim)
                        sub_map=sim_word_map[temp.ori]
                        sub_map[temp.dst]=temp.sim
                        if not self.map_treetagger_to_stem.__contains__(a_sim_list.word):
                            continue

                        dst_list = self.map_treetagger_to_stem[a_sim_list.word]
                        for dst in dst_list:
                            temp.dst=dst
                            if self.wordmap_all.__contains__(temp.dst):
                                continue
                            temp.sim = self.a / (self.a + a_sim_list.sim);
                            sub_map = sim_word_map[temp.ori]
                            sub_map[temp.dst] = temp.sim
        return sim_word_map

    def get_word_map_all(self):
        #加载wordmap文件
        wordmap_all = {}
        path_word_map_all = os.path.join(self.word_map_all_folder, 'wordmap')
        fidin = open(path_word_map_all);
        for i, line in enumerate(fidin.read().splitlines()):
            wordmap_all[line]=i;
        return wordmap_all

    def get_map_stem_to_treetagger(self):
        #加载wordmap文件
        map_stem_to_treetagger = {}
        map_treetagger_to_stem = {}
        path_word_map = os.path.join(self.word_map_all_folder, 'map_stem_to_treetagger')
        fidin = open(path_word_map)
        for tline in fidin.read().splitlines():
            S = tline.split('\t')
            map_stem_to_treetagger[S[0]] = S[1]
            if not map_treetagger_to_stem.__contains__(S[1]):
                map_treetagger_to_stem[S[1]] = []
            map_treetagger_to_stem[S[1]].append(S[0])
        return map_stem_to_treetagger, map_treetagger_to_stem
