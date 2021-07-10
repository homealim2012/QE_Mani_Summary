# coding: utf-8
from sqlalchemy.ext.declarative import declarative_base
from server.entities.auto.sum import po
from server.utils import convert_utils

Base = declarative_base()
metadata = Base.metadata

def to_dict(self):
    return {c.name: convert_utils.convert_obj2dict(getattr(self, c.name, None)) for c in self.__table__.columns}

Base.to_dict = to_dict;

class Result(po.Result,Base):
    pass
