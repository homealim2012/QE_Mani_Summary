# coding: utf-8

from server.service.basicService import *
from flask import Response
import hashlib

class LoginService(BasicService):

    def __init__(self, username, password):
        super().__init__()
        self.username = username
        self.password = password

    def getDBDataFromJsonData(self, db_session):
        response = Response(status=200, mimetype='text/html')
        if self.checkUserAndPwd():
            response.response = 'success'
        else:
            response.response = 'fail'
        return response

    def checkUserAndPwd(self):
        password = "1E42C1B268A7E5ABB1AA9B15D880309D"
        username = "ai"
        salt = "juhefw"
        m = hashlib.md5()
        m.update((self.password + salt).encode('utf-8'))
        if username == self.username and password.lower() == m.hexdigest():
            return True;
        return False
