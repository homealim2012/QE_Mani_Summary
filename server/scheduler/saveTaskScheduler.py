# coding: utf-8

from server.scheduler import runScheduler
import pickle
from server.service.outputService import OutputService
import logging

@runScheduler.scheduler.scheduler.scheduled_job(trigger='interval', id='saveTask', seconds=300, args=[OutputService.task_dict])
def saveTask(task_dict):
    if task_dict != None:
        with open('data/task.dumps', 'wb') as f:
            res_dict = []
            for key in task_dict:
                res_dict.append((key, task_dict[key]))
            pickle.dump(res_dict, f)
            logging.info("Task 已保存")
