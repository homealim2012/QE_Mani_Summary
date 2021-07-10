import numpy as np
import numpy.matlib
from model.method.BaseMethod import BaseMethod

class ManifoldRanking(BaseMethod):

    @staticmethod
    def ManifoldRanking_W(W: np.matrix, a: float, threshold: float = 0.00001, max_iter: int = 100) -> np.matrix:
        D = np.matlib.zeros((np.size(W, axis=0), np.size(W, axis=0)))
        sum_W = np.sum(W, axis=0)
        for i, a_sum_W in enumerate(np.array(sum_W)[0]):
            D[i, i] = a_sum_W
        S = np.sqrt(D) ** -1 * W * np.sqrt(D) ** -1
        f = np.random.rand(np.size(W, axis=0), 1)
        y = np.matlib.zeros((np.size(W, axis=0), 1))
        y[0] = 1
        for i in range(max_iter):
            f1 = f
            f = a * S * f + (1 - a) * y
            if np.linalg.norm(f1-f) < threshold:
                break
        return f

    def __init__(self, duc_year, result_name):
        super().__init__(duc_year, result_name)
        self.mean_rate = 1
        self.var_rate = 1
        self.total_summary_sentence_num = 25
        self.use_this_topic_df = 0
        self.use_mean = 1
        self.only_mean_topic = 0
        self.Amr = 0.8
        self.w = 8
        self.diagonal_value = 1
        self.ori_cos_rate = 0.9
        self.P_rate = 0.4
        self.overlap_rate = 0.1
        self.is_extend_textrank_query = 1
        self.use_ori_topic_for_textrank = 1
        self.textrank_d = 0.6
        self.texttank_c = 100
        self.texttank_qe_rate = 0.4
        self.is_extend_mani_query = 0
        self.use_ori_topic_for_mani = 1
        self.mani_c = 100
        self.mani_qe_rate = 0.4

    def get_sentence_score(self, _, tfidf_topic: np.matrix, tfidf_matrix: np.matrix, topic_no: str, __):

        if self.is_extend_textrank_query == 1:
            from model.method.TextRank import TextRank
            W = self.get_sim_W_from_tfidf_matrix(tfidf_matrix, tfidf_topic, topic_no)
            if self.use_ori_topic_for_textrank == 1:
                b = 1 - BaseMethod.cos_dist(tfidf_matrix[1:,:], tfidf_matrix[0,:])
            else:
                b = 1 - BaseMethod.cos_dist(tfidf_matrix[1:,:], tfidf_topic)
            M = TextRank.get_M(W[1:, 1:], b, self.textrank_d)
            P = TextRank.TextRank_M(M)
            WW = tfidf_matrix[1:tfidf_matrix.shape[0],:]
            S = np.matrix(np.diag(np.array((WW * np.ones((WW.shape[1], 1))).T)[0])) ** (-1) * WW
            y = S.T*P
            sort_index = np.argsort(np.array(-y.T)[0])
            tfidf_topic[0, sort_index[0: self.texttank_c]] = tfidf_topic[0, sort_index[0: self.texttank_c]] + self.texttank_qe_rate

        if self.is_extend_mani_query == 1:
            if self.use_ori_topic_for_mani == 1:
                W = self.get_sim_W_from_tfidf_matrix(tfidf_matrix, tfidf_matrix[0, :], topic_no)
            else:
                W = self.get_sim_W_from_tfidf_matrix(tfidf_matrix, tfidf_topic, topic_no)
            score_DD = ManifoldRanking.ManifoldRanking_W(W, self.Amr)
            WW = tfidf_matrix[1:tfidf_matrix.shape[0], :]
            S = np.matrix(np.diag(np.array((WW * np.ones((WW.shape[1], 1))).T)[0])) ** (-1) * WW
            y = S.T*score_DD[1:np.size(score_DD)]
            sort_index = np.argsort(np.array(-y.T)[0])
            tfidf_topic[0, sort_index[0: self.mani_c]] = tfidf_topic[0, sort_index[0: self.mani_c]] + self.mani_qe_rate

        W = self.get_sim_W_from_tfidf_matrix(tfidf_matrix, tfidf_topic, topic_no)
        score_DD = ManifoldRanking.ManifoldRanking_W(W, self.Amr)
        score_DD[0][0] = 0
        SS = np.matrix(np.diag(np.array((W * np.ones((W.shape[0], 1))).T)[0])) ** (-1) * W
        res_sentence_score, res_sentence_index = self.get_sentences_from_score_mmr(score_DD, SS)

        return res_sentence_index,res_sentence_score

    def get_sentences_from_score_mmr(self, score_DD: np.matrix, SS: np.matrix):
        res_sentence_index=[]
        res_sentence_score=[]
        for j in range(self.total_summary_sentence_num):
            temp_select_index = np.argmax(score_DD)
            temp_value = score_DD[temp_select_index,0]
            Inf_value = np.matlib.zeros((len(score_DD), 1))
            Inf_value[temp_select_index]=np.inf
            res_sentence_score.append(temp_value)
            res_sentence_index.append(temp_select_index-1)
            score_DD=score_DD-self.w*SS[:,temp_select_index]*temp_value-Inf_value
        return (res_sentence_score, res_sentence_index)