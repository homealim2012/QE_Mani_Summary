# coding: utf-8
from sqlalchemy import Column, DECIMAL, DateTime, String, Text
from sqlalchemy.dialects.mysql import BIGINT
from sqlalchemy.ext.declarative import declarative_base

Base = object



class Result(Base):
    __tablename__ = 'result'

    id = Column(BIGINT(20), primary_key=True)
    task_id = Column(String(40))
    group = Column(String(255))
    result_name = Column(String(255))
    finish_time = Column(DateTime)
    dataset = Column(String(100))
    method = Column(String(255))
    variable = Column(String(255))
    value = Column(String(255))
    other_vars = Column(Text)
    ROUGE_1_P = Column('ROUGE-1-P', DECIMAL(10, 5))
    ROUGE_1_R = Column('ROUGE-1-R', DECIMAL(10, 5))
    ROUGE_1_F = Column('ROUGE-1-F', DECIMAL(10, 5))
    ROUGE_2_P = Column('ROUGE-2-P', DECIMAL(10, 5))
    ROUGE_2_R = Column('ROUGE-2-R', DECIMAL(10, 5))
    ROUGE_2_F = Column('ROUGE-2-F', DECIMAL(10, 5))
    ROUGE_3_P = Column('ROUGE-3-P', DECIMAL(10, 5))
    ROUGE_3_R = Column('ROUGE-3-R', DECIMAL(10, 5))
    ROUGE_3_F = Column('ROUGE-3-F', DECIMAL(10, 5))
    ROUGE_4_P = Column('ROUGE-4-P', DECIMAL(10, 5))
    ROUGE_4_R = Column('ROUGE-4-R', DECIMAL(10, 5))
    ROUGE_4_F = Column('ROUGE-4-F', DECIMAL(10, 5))
    ROUGE_L_P = Column('ROUGE-L-P', DECIMAL(10, 5))
    ROUGE_L_R = Column('ROUGE-L-R', DECIMAL(10, 5))
    ROUGE_L_F = Column('ROUGE-L-F', DECIMAL(10, 5))
    ROUGE_W_1_2_P = Column('ROUGE-W-1.2-P', DECIMAL(10, 5))
    ROUGE_W_1_2_R = Column('ROUGE-W-1.2-R', DECIMAL(10, 5))
    ROUGE_W_1_2_F = Column('ROUGE-W-1.2-F', DECIMAL(10, 5))
    ROUGE_SU4_P = Column('ROUGE-SU4-P', DECIMAL(10, 5))
    ROUGE_SU4_R = Column('ROUGE-SU4-R', DECIMAL(10, 5))
    ROUGE_SU4_F = Column('ROUGE-SU4-F', DECIMAL(10, 5))
