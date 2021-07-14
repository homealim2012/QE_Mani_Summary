from server.service.basicService import *
from server.service.outputService import OutputService, Task
from flask import render_template
import datetime
import json
import copy
import re

class InputService(BasicService):
    def getDBDataFromJsonData(self, db_session):
        initpara = json.dumps(para().__dict__)
        initpara = initpara.replace(",", "\n,")
        initpara = initpara.replace(",", "\n,")
        initpara = initpara.replace("}", "\n}")
        p = r'\[(?:.|\n)*?\]'
        arr = re.findall(p, initpara)
        for ele in arr:
            new_ele = ele.replace('\n\n', '')
            initpara = initpara.replace(ele, new_ele)
        return render_template('Input/main.html', initParas=initpara)

class RunService(BasicService):
    def __init__(self, para):
        super().__init__()
        self.para = para
        self.result_name = datetime.datetime.now().strftime('%m.%d')

    def set_result_name(self):
        self.model_name = self.para['__method__']
        self.result_name += '_method_' + self.para['__method__']
        return self

    def get_variable(self):
        for key in self.para:
            if not key.startswith('__') and type(self.para[key]) == list:
                return key

    def getDBDataFromJsonData(self, db_session):
        variable = self.get_variable()
        res = []
        if variable:
            for value in self.para[variable]:
                para = copy.deepcopy(self.para)
                para[variable] = value
                task = Task(para, self.model_name, self.result_name)
                task.set_variable(variable, value)
                with OutputService.lock:
                    OutputService.task_dict[task.id] = task
                OutputService.pool.apply_async(Task.runTask, (task.id, OutputService.task_dict,
                                                              OutputService.event, OutputService.lock))
                res.append(task.id)
        else:
            task = Task(self.para, self.model_name, self.result_name)
            with OutputService.lock:
                OutputService.task_dict[task.id] = task
            OutputService.pool.apply_async(Task.runTask, (task.id, OutputService.task_dict,
                                                          OutputService.event, OutputService.lock))
            res = task.id
        return res

class para:
    def __init__(self):
        self.__method__ = 'ManifoldRanking'
        self.__group__ = None
        self.__datasets__ = ['DUC2005','DUC2006','DUC2007']
        self.__sumlength__ = [250, 250, 250]
        self.a = 1
        self.max_dis = 4
        self.max_word_count = 5000
        self.w = 8.0
        self.Amr = 0.8
        self.use_sim_word = 1
        self.mean_rate = 1
        self.var_rate = 1
        self.P_rate = 0.4
        self.overlap_rate = 0.1
        self.ori_cos_rate = 0.9
        self.overlap_rate = 0.1
        self.is_extend_textrank_query = 1
        self.use_ori_topic_for_textrank = 1
        self.textrank_d = 0.6
        self.texttank_c = 100
        self.texttank_qe_rate = 0.4
        self.is_extend_mani_query = 1
        self.use_ori_topic_for_mani = 1
        self.mani_c = 100
        self.mani_qe_rate = 0.4
