from flask import Blueprint
from flask import g
import json
from flask import Response,request
from server.controller import basicController
from server.service.inputService import InputService,RunService
input_opt = Blueprint('input_opt', __name__, static_url_path='/resources', static_folder='resources')


@input_opt.route('/main', methods=['GET'])
@basicController.CheckUserSession()
def main():
    return InputService().main()


@input_opt.route('/run', methods=['POST'])
@basicController.CheckUserSession()
def run():
    response = Response(status=200, mimetype='json')
    para = json.loads(request.form['source'])
    taskid = RunService(para).set_result_name().main()
    response.response = json.dumps({
        'status': 'ok',
        'taskid': taskid
    })
    return response
