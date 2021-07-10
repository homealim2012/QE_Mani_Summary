from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import utils.dao_utils
from server.entities.inherit.sum import po

if __name__ == '__main__':
    url = 'mysql+mysqlconnector://user:user@localhost:3306/auto_summary';
    engine = create_engine(url,pool_size=20,pool_timeout=300,pool_recycle=600)
    Session = sessionmaker(engine)
    conn = engine.connect()
    db_session = Session(bind=conn)
    try:
        query = {
            'columns': ['variable', 'value', 'ROUGE_1_F', 'ROUGE_2_F', 'ROUGE_W_1_2_F', 'ROUGE_SU4_F'],
            'filter': [
                {'field': 'finish_time', 'type': '>', 'content': '2020-3-1'},
                {'field': 'dataset', 'type': '==', 'content': 'DUC2005'},
                {'field': 'variable', 'type': '==', 'content': 'texttank_qe_rate'},
            ],
            'orderBy': ['id']
        }
        dao_util = utils.dao_utils.DAO(db_session, po.Result)
        res = dao_util.query(query)
        res_1 = ''
        res_4 = ''
        for a_data in res['data']:
            res_1 += '(' + str(a_data['value']) + ',' + str(a_data['ROUGE_1_F']) + ')'
            res_4 += '(' + str(a_data['value']) + ',' + str(a_data['ROUGE_SU4_F']) + ')'
        print(res_1)
        print(res_4)
    except Exception as t:
        db_session.rollback()
        raise t
    finally:
        db_session.close()
        conn.close()
