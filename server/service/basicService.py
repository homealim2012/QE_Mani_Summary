# coding: utf-8

import json

import server.settings

class BasicService:

    def __init__(self):
        pass;

    def getDBDataFromJsonData(self, db_session):
        pass

    def main(self):
        Session = server.settings.Session
        conn = server.settings.engine.connect()
        db_session = Session(bind=conn)
        trans = conn.begin()
        try:
            res = self.getDBDataFromJsonData(db_session);
            trans.commit()
            return res
        except Exception as t:
            trans.rollback()
            raise t
        finally:
            db_session.close()
            trans.close()
            conn.close()
