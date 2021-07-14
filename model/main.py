from model.method import ManifoldRanking, TextRank
from model.evaluation import ROUGE

def main(para, model_name, result_name):

    duc_years = para.get('__datasets__', ['DUC2005', 'DUC2006', 'DUC2007','TAC2008','TAC2009'])
    rouge_length = para.get('__sumlength__', [250, 250, 250, 100, 100])

    for i, duc_year in enumerate(duc_years):
        
        if model_name == 'ManifoldRanking':
            m = ManifoldRanking.ManifoldRanking(duc_year,result_name)
        elif model_name == 'TextRank':
            m = TextRank.TextRank(duc_year,result_name)

        for key in para:
            if not key.startswith('__'):
                setattr(m, key, para[key])

        m.init().run()

        r = ROUGE.ROUGE(duc_year,result_name)\
                 .set_rouge_length(rouge_length[i]).init()
        r.run()

if __name__ == '__main__':
    
    main({ "__datasets__": ['DUC2005', 'DUC2006', 'DUC2007'],
           "__sumlength__": [250, 250, 250],
             "a": 1, "max_dis": 4, "max_word_count": 5000
             , "w": 8.0 , "Amr": 0.8 , "use_sim_word": 0
             , "mean_rate": 1 , "var_rate": 1 , "P_rate": 0.4
             , "overlap_rate": 0.1 , "ori_cos_rate": 0.9
             , "is_extend_textrank_query": 1 , "textrank_d": 0.6
             , "texttank_c": 100 , "texttank_qe_rate": 0.4
          }, 'ManifoldRanking','result')
