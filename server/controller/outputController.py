# coding=utf-8
from flask import Blueprint
from flask import g
import traceback
import logging
import os
import time
import datetime
from flask import Response, render_template, request
from server.controller import basicController
from server.service.outputService import OutputService,Task,ResultService
import model.main
output_opt = Blueprint('output_opt', __name__, static_url_path='/resources', static_folder='resources')

@output_opt.route('/getDate')
@basicController.CheckUserSession()
def getDate():
    def generate():
        while True:
            thistime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            yield 'data:%s\n\n' % thistime
            time.sleep(1)

    response = Response(generate(), mimetype='text/event-stream')
    return response

@output_opt.route('/main')
@basicController.CheckUserSession()
def main():
    return render_template('Output/main.html')

@output_opt.route('/getResult', methods=['POST','GET'])
@basicController.CheckUserSession()
def getResult():
    if request.method == 'POST':
        duc_year = request.form.get('duc_year', None)
        result_name = request.form.get('result_name', None)
        try:
            data_root_path = os.path.dirname(os.path.abspath(__file__))
            path = os.path.join(data_root_path, "../../model/data/result/"+duc_year+"-output/ROUGE_"+result_name+".out")
            f = open(path, 'r')
            content = f.read()
            f.close()
        except Exception as e:
            logging.error(traceback.format_exc())
            content = 'error'
        return Response(content, mimetype='text/html')
    elif request.method == 'GET':
        result_name = request.args.get("result_name")
        try:
            data_root_path = os.path.dirname(os.path.abspath(__file__))
            path = os.path.join(data_root_path, "../../model/data/result/DUC2005-output/ROUGE_" + result_name + ".out")
            f = open(path, 'r')
            content = f.read()
            f.close()
        except:
            logging.error(traceback.format_exc())
            content = '文件无法打开'
        return render_template('Output/result.html', initParas=content, result_name=result_name)

@output_opt.route('/info')
@basicController.CheckUserSession()
def info():
    def getInfo():
        while True:
            yield 'data:%s\n\n' % OutputService.getTaskJson()
            time.sleep(2)
            OutputService.event.wait(timeout=10)

    return Response(getInfo(), mimetype='text/event-stream')

@output_opt.route('/rmTask', methods=['POST','GET'])
@basicController.CheckUserSession()
def rmTask():
    taskid = request.form['taskid']
    response = Response()
    with OutputService.lock:
        task = OutputService.task_dict[taskid]
    if task.status in (Task.Running, Task.Create, Task.Waiting):
        response.response = '正在队列或者正在运行的任务无法删除'
    else:
        with OutputService.lock:
            del OutputService.task_dict[taskid]
        response.response = '删除成功'
    return response

@output_opt.route('/removeOld', methods=['POST','GET'])
def removeOld():
    fail_arr = []
    success_arr = []
    for taskid in list(OutputService.task_dict.keys()):
        with OutputService.lock:
            task = OutputService.task_dict[taskid]
        if task.status == Task.Finished:
            try:
                data_root_path = os.path.dirname(os.path.abspath(__file__))
                for a_dataset in task.para.get('__datasets__',['DUC2005', 'DUC2006', 'DUC2007']):
                    srcpath = os.path.join(data_root_path,
                                           "../../model/data/result/" + a_dataset + "-output/ROUGE_" + task.result_name + ".out")
                    res = ResultService(srcpath, task, a_dataset).main()
                if res['status'] == 'ok':
                    task.setStatus(Task.Completed,OutputService.task_dict,OutputService.event,OutputService.lock)
                    success_arr.append(taskid)
            except Exception as e:
                logging.error(traceback.format_exc())
                fail_arr.append(taskid)
        if task.status == Task.Completed:
            if (datetime.datetime.now() - task.finishTime).days > 2:
                with OutputService.lock:
                    del OutputService.task_dict[taskid]
        elif task.status == Task.Error:
            with OutputService.lock:
                del OutputService.task_dict[taskid]
    if len(fail_arr) > 0 and len(success_arr) == 0:
        return Response('更新失败，失败id：' + str(fail_arr))
    elif len(fail_arr) == 0 and len(success_arr) > 0:
        return Response('更新成功，数据已写入数据库')
    elif len(fail_arr) > 0 and len(success_arr) > 0:
        return Response('部分更新成功，失败id：' + str(fail_arr))
    else:
        return Response('没有数据，无需更新')


