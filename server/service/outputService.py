import multiprocessing
import traceback
import logging
import datetime
from server.service.basicService import *
import uuid
from model.main import main
import platform
import json
from server.utils import process_rouge_utils
from server.utils import dao_utils
from server.entities.inherit.sum import po

class OutputService(BasicService):

    pool = None
    task_dict = None
    event = None
    lock = None

    @staticmethod
    def getTaskJson():
        res_arr = []
        for item in sorted(OutputService.task_dict.items(),
                           key=lambda x: x[1].finishTime if x[1].finishTime else x[1].createTime, reverse=True):
            res = {}
            task =item[1]
            res['id'] = task.id
            res['result_name'] = task.result_name
            res['finish_time'] = task.finishTime.strftime("%Y-%m-%d %H:%M:%S") if task.finishTime else None
            res['create_time'] = task.createTime.strftime("%Y-%m-%d %H:%M:%S")
            res['paras'] = task.para
            res['status'] = task.status
            res_arr.append(res)
        return json.dumps(res_arr)

class ResultService(BasicService):

    def __init__(self, srcpath, task, dataset):
        super().__init__()
        self.srcpath = srcpath
        self.task = task
        self.dataset = dataset

    def getDBDataFromJsonData(self, db_session):
        res_dict = process_rouge_utils.get_ROUGE_from_file(self.srcpath)
        dict_1 = {key.replace('-', '_').replace('.','_'): res_dict[key] for key in res_dict}
        dict_2 = {'result_name': self.task.result_name, 'dataset':self.dataset,
                      'variable': self.task.variable, 'value': str(self.task.value),
                      'task_id': self.task.id, 'finish_time': self.task.finishTime,
                      'group': self.task.para['__group__'],
                      'method': self.task.para['__method__'], 'other_vars': json.dumps(self.task.para)}
        res_json = {
            'data': [{**dict_1, **dict_2}]
        }
        dao = dao_utils.DAO(db_session, po.Result)
        return dao.add(res_json)


class Task:

    Create = 'Create'
    Waiting = 'Waiting'
    Running = 'Running'
    Finished = 'Finished'
    Completed = 'Completed'
    Error = 'Error'

    def __init__(self, para, model_name, result_name):
        self.createTime = datetime.datetime.now()
        self.finishTime = None
        self.id = str(uuid.uuid4()).replace('-', '')
        self.para = para
        self.model_name = model_name
        self.result_name = result_name + '_id_' + self.id
        self.variable = None
        self.value = None
        self.setStatus(Task.Create)

    def set_variable(self, variable, value):
        self.variable = variable
        self.value = value

    def setStatus(self, status, task_dict=None, event=None, lock=None):
        if event:
            event.set()
        self.status = status
        if task_dict and lock:
            with lock:
                task_dict[self.id] = self
        if event:
            event.clear()

    def run(self, task_dict, event, lock):
        try:
            self.setStatus(Task.Running, task_dict=task_dict, event=event, lock=lock)
            main(self.para, self.model_name, self.result_name)
            self.setStatus(Task.Finished, task_dict=task_dict, event=event, lock=lock)
            self.finishTime = datetime.datetime.now()
            with lock:
                task_dict[self.id] = self
        except Exception as e:
            self.setStatus(Task.Error, task_dict=task_dict, event=event, lock=lock)
            logging.error(traceback.format_exc())
            raise e

    @staticmethod
    def runTask(taskid, task_dict, event, lock):
        with lock:
            task = task_dict[taskid]
        task.run(task_dict, event, lock)
