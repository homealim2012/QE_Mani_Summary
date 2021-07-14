# coding: utf-8
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import redis as res
import server.settings
import logging
import datetime
import os

def connectDB(config):

    if getattr(server.settings, 'engine', None):
        return

    echo = True if config.PUB_CONF.db.get('echo', False) else False
    if config.PUB_CONF.db.type == 'mysql':
        url = 'mysql+mysqlconnector://{user}:{password}@{host}:{port}/{database}'.format(**config.PUB_CONF.db)
        server.settings.engine = create_engine(url, pool_size=20, echo=echo, pool_timeout=300,  # 池中没有线程最多等待的时间，否则报错（秒）
                                               pool_recycle=600)  # 多久之后对线程池中的线程进行一次连接的回收（重置）（秒）
        print('connect to mysql server')
    else:
        url = 'sqlite:///data/{database}.db'.format(**config.PUB_CONF.db)
        server.settings.engine = create_engine(url, echo=echo)
        print('connect to sqlite server')

    server.settings.Session = sessionmaker(server.settings.engine)

def connectRedis(config):

    if not config.PUB_CONF.redis.enable:
        return

    if getattr(server.settings, 'redis', None):
        return

    re = res.Redis(host=config.PUB_CONF.redis.host,
                     port=config.PUB_CONF.redis.port,
                     db=config.PUB_CONF.redis.db,
                     password=config.PUB_CONF.redis.password)
    server.settings.redis = re
    print('connect to redis server')

def configure_logging(config):

    log_filename = datetime.datetime.now().strftime('%Y-%m-%d') + '.log'
    formatter = logging.Formatter('%(asctime)s : %(levelname)s : %(message)s')

    fh = logging.FileHandler(filename=os.path.join(config.PUB_CONF.log.logPath, 'server-'+log_filename))
    fh.setLevel(logging.WARNING)
    fh.setFormatter(formatter)
    logging.getLogger().addHandler(fh)

def configure_config(config):
    server.settings.config = config
