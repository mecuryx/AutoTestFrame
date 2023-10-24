import requests
import readConfig as readConfig
from common.Log import MyLog
from common import common

# 创建读取配置文件对象
localReadConfig = readConfig.ReadConfig()

class ConfigHttp:
    # 获取http相关配置
    def __init__(self):
        global host, port, timeout
        host = localReadConfig.get_http("baseurl")
        port = localReadConfig.get_http("port")
        timeout = localReadConfig.get_http("timeout")
        self.logger = MyLog.get_log().get_logger()
        self.headers = {}
        self.params = {}
        self.data = {}
        self.url = None
        self.files = {}

    def set_url(self, url):
        self.url = host + url

    def set_headers(self, header):
        self.headers = eval(header)

    def set_params(self, param):
        self.params = param

    def set_data(self, data):
        self.data = data

    def set_files(self, file):
        self.files = file

    '''
        data:传入需要配置的用例，列表类型
        id:用例序号
    '''
    def config(self,data,id):
        testCase=data[id]
        self.logger.info('开始执行' + testCase[0])
        self.set_url(testCase[1])
        self.set_headers(testCase[3])
        self.set_data(testCase[4])
    # GET请求
    def get(self):
        try:
            response = requests.get(self.url, params=self.params, headers=self.headers, timeout=float(timeout))
            # response.raise_for_status()
            return response
        except TimeoutError:
            self.logger.error("Time out!")
            return None

    # POST请求
    def post(self):
        try:
            response = requests.post(self.url, headers=self.headers, data=self.data, files=self.files, timeout=float(timeout))
            # response.raise_for_status()
            return response
        except TimeoutError:
            self.logger.error("Time out!")
            return None
