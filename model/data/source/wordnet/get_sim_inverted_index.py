# -*- coding:utf-8 -*-
'''
Created on 2019年1月26日

@author: stone
'''

count = 0

if __name__=="__main__":
    import nltk
    import collections
    from datetime import datetime
    import json

    count_map = {}

    def sim_word(word1, word2):
        synsets1 = nltk.corpus.wordnet.synsets(word1)
        synsets2 = nltk.corpus.wordnet.synsets(word2)
        min_dis = 100
        for a_syn_1 in synsets1:
            for a_syn_2 in synsets2:
                temp_dis = a_syn_2.shortest_path_distance(a_syn_1, simulate_root=a_syn_2._needs_root())
                # temp_sim=a_syn_1.wup_similarity(a_syn_2);
                # shortest_path_distance()
                if (temp_dis == None):
                    temp_dis = 100;
                if (temp_dis < min_dis):
                    min_dis = temp_dis;
        return min_dis;


    def read_text(filepath):
        file_object = open(filepath)
        try:
            all_the_text = file_object.read();
        finally:
            file_object.close()
        return all_the_text;


    def get_sim_matrix(words):
        for i in range(len(words)):
            file_dst_obj = open("wordnet_json\_" + words[i] + '.json', "w", encoding='UTF-8')
            sim_list = []
            value_list = []
            for j in range(len(words)):
                sim_value = 0 if i == j else sim_word(words[i], words[j])
                value_list.append(sim_value) if sim_value <= 10 else None
                sim_list.append({'word': words[j], 'sim': sim_value}) if sim_value <= 10 else None
                global count
                count = count + 1
                if count % 1000 == 0:
                    total_time_end = datetime.now()
                    print("正在计算第" + str(count) + "个词语相似度,用时" + str(total_time_end - total_time_start))
            sim_map = {words[i]: sim_list}
            c = collections.Counter(value_list)
            count_map[words[i]] = sorted([(key, c[key]) for key in c.keys()])
            file_dst_obj.write(json.dumps({'sim_map': sim_map}))
            file_dst_obj.close()

    total_time_start = datetime.now()
    all_text=read_text('wordmap.txt')
    words=all_text.split('\n')
    get_sim_matrix(words)

    f = open('wordnet_json/word_count.mat', 'w', encoding='UTF-8')
    f.write(json.dumps({'count_map', count_map}))
    f.close()
