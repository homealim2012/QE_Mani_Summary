# coding: utf-8

from flask import Flask, request, session, Response, render_template
import server.utils.config_utils
import server.settings
from datetime import datetime
import logging
import json
import pickle
import os
from flask import g
import traceback
import multiprocessing
import platform
from server.scheduler import runScheduler
from server.service.outputService import OutputService
from server.controller.basicController import basic_opt
from server.controller.loginController import login_opt
from server.controller.inputController import input_opt
from server.controller.outputController import output_opt
app = Flask(__name__, static_url_path='/resources', static_folder='resources')
app.register_blueprint(basic_opt, url_prefix="/")
app.register_blueprint(login_opt, url_prefix="/")
app.register_blueprint(input_opt, url_prefix="/Input")
app.register_blueprint(output_opt, url_prefix="/Output")
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

@app.before_request
def get_json_response():
    response = Response()
    response.headers['Access-Control-Allow-Origin'] = 'http://localhost:8080'
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    response.headers["Content-Type"] = "text/xml; charset=utf-8"
    response.mimetype = 'application/json'
    g.json_response = response

@app.teardown_request
def teardown_request(exc):
    logging.error(traceback.format_exc())

@app.errorhandler(500)
def internal_server_error(e):
    response = g.json_response;
    #logging.error(traceback.format_exc()) -- 500 错误post
    response.response = json.dumps({'status': 'fail', 'reason': '内部错误'}, ensure_ascii=False)
    return response

def get_current_time(session):
    current_time = datetime.now()
    # 获取当前时间
    if 'current_time' not in session:
        session['current_time'] = current_time
    return current_time

def load_task():
    try:
        with open('data/task.dumps', 'rb') as f:
            load_list = pickle.load(f)
            for element in load_list:
                OutputService.task_dict[element[0]] = element[1]
    except:
        logging.info('没有task文件')

def load_config(conf='conf/%s.yaml'%'server'):
    config = server.utils.config_utils.load_config(conf)
    server.settings.configure_logging(config)
    server.settings.connectDB(config)
    server.settings.connectRedis(config)
    server.settings.configure_config(config)
    load_task()
    runScheduler.init_scheduler(app)
    return config

def load_multiprocessing_manager(conf='conf/%s.yaml'%'server'):
    config = server.utils.config_utils.load_config(conf)
    logging.error('init new pool')
    if not OutputService.pool:
        logging.error('new pool start')
        mgr = multiprocessing.Manager()
        OutputService.task_dict = mgr.dict()
        OutputService.event = mgr.Event()
        OutputService.lock = mgr.RLock()
        OutputService.pool = multiprocessing.Pool(config.PUB_CONF.pool.maxWorkers)

if __name__ == '__main__' and multiprocessing.current_process().name == 'MainProcess':
    load_multiprocessing_manager('conf/%s.yaml' % os.environ.get('conf', 'server'))
    config = load_config('conf/%s.yaml' % os.environ.get('conf', 'server'))
    app.run(host='0.0.0.0', port=8089, debug=False)

