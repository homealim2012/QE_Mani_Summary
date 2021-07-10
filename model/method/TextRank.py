import numpy as np
import numpy.matlib
from model.method.BaseMethod import BaseMethod


class TextRank(BaseMethod):

    @staticmethod
    def TextRank_M(M:np.matrix,threshold:float = 0.00001):
        P = np.matlib.ones((np.size(M, axis=0), 1)) / np.size(M, axis=0)
        while True:
            P1 = M.T * P
            if np.linalg.norm(P1-P) < threshold:
                break
            P = P1
        return P

    @staticmethod
    def get_M(A:np.matrix, b:np.matrix, d:float):
        A = A / np.sum(A, axis=1)
        A[np.isnan(A)] = 0
        B = np.repeat(b, np.size(A,axis=0), axis=1).T
        B = B / np.sum(B, axis=1)
        B[np.isnan(B)] = 0
        M = d * A + (1 - d) * B
        return M

    def __init__(self, duc_year, result_name):
        super().__init__(duc_year, result_name)
        self.d = 0.6
        self.c = 100
        self.diagonal_value = 1
        self.use_ori_topic = 1
        self.use_mean = 1
        self.use_mean_after_extend = 0
        self.use_sim_word_after_extend = 0
        self.mean_rate = 0
        self.var_rate = 0
        self.ori_cos_rate = 1
        self.P_rate = 0
        self.overlap_rate = 0
        self.qe_textrank_method = 1
        self.is_extend_textrank_query = 1
        self.textrank_qe_rate = 0.6

        self.is_extend_mani_query = 1
        self.use_ori_topic_for_mani = 1
        self.mani_c = 100
        self.mani_qe_rate = 0.4
        self.Amr = 0.8

        self.total_summary_sentence_num = 25

    def get_sentence_score(self, _, tfidf_topic: np.matrix, tfidf_matrix: np.matrix, topic_no, __):
        A = self.get_sim_W_from_tfidf_matrix(tfidf_matrix, tfidf_topic, topic_no)
        A = A[1:np.size(A,axis=0), 1:np.size(A,axis=1)]
        if self.is_extend_textrank_query == 1:
            if self.use_ori_topic == 1:
                b = 1 - BaseMethod.cos_dist(tfidf_matrix[1:,:], tfidf_matrix[0,:])
            else:
                b = 1 - BaseMethod.cos_dist(tfidf_matrix[1:,:], tfidf_topic)
            M = TextRank.get_M(A, b, self.d)
            P = TextRank.TextRank_M(M)
            W = tfidf_matrix[1:,:]
            S = np.matrix(np.diag(np.array((W * np.ones((W.shape[1], 1))).T)[0])) ** (-1) * W
            y = S.T * P;
            sort_index = np.argsort(np.array(-y.T)[0]);
            if self.qe_textrank_method == 1:
                tfidf_topic[0, sort_index[0: self.c]] = tfidf_topic[0, sort_index[0: self.c]] + self.textrank_qe_rate;

        if self.is_extend_mani_query == 1:
            from model.method.ManifoldRanking import ManifoldRanking
            if self.use_ori_topic_for_mani == 1:
                W=self.get_sim_W_from_tfidf_matrix(tfidf_matrix, tfidf_matrix[0,:], topic_no)
            else:
                W = self.get_sim_W_from_tfidf_matrix(tfidf_matrix, tfidf_topic, topic_no)
            score_DD = ManifoldRanking.ManifoldRanking_W(W, self.Amr)
            WW = tfidf_matrix[1:,:]
            S = np.matrix(np.diag(np.array((WW * np.ones((WW.shape[1], 1))).T)[0])) ** (-1) * WW
            y = S.T*score_DD[1:np.size(score_DD)]
            sort_index = np.argsort(np.array(-y.T)[0])
            tfidf_topic[0, sort_index[0: self.mani_c]] = tfidf_topic[0, sort_index[0: self.mani_c]] + self.mani_qe_rate

        b = 1 - BaseMethod.cos_dist(tfidf_matrix[1:,:], tfidf_topic)
        M = TextRank.get_M(A, b, self.d)
        P = TextRank.TextRank_M(M)
        score_DD = P
        res_sentence_score, res_sentence_index = self.get_sentences_from_score_mmr(score_DD, A, P)

        return (res_sentence_index, res_sentence_score)

    def get_sentences_from_score_mmr(self, score_DD: np.matrix, A: np.matrix, P: np.matrix):
        A = A / np.sum(A, axis=1)
        A[np.isnan(A)] = 0
        res_sentence_index = []
        res_sentence_score = []
        for j in range(self.total_summary_sentence_num):
            temp_select_index = np.argmax(score_DD)
            temp_value = score_DD[temp_select_index]
            Inf_value = np.matlib.zeros((len(score_DD), 1))
            Inf_value[temp_select_index] = np.inf
            res_sentence_score.append(temp_value)
            res_sentence_index.append(temp_select_index)
            score_DD = score_DD - np.multiply(A[:,temp_select_index],P) - Inf_value
        return (res_sentence_score, res_sentence_index)