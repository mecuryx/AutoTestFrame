import logging
from datetime import datetime
import threading
import readConfig
import os

class Log:
    def __init__(self):
        global logPath, resultPath, proDir
        self.logger = logging.getLogger("logger")
        self.logger.setLevel(logging.INFO)
        if not self.logger.handlers:    #列表不为空
            proDir = readConfig.proDir
            resultPath = os.path.join(proDir, "result")
            # 测试结果目录不存在时新建
            if not os.path.exists(resultPath):
                os.mkdir(resultPath)
            # 日志目录使用当前时间
            logPath = os.path.join(resultPath, str(datetime.now().strftime("%Y%m%d%H%M%S")))
            # 日志目录不存在时新建
            if not os.path.exists(logPath):
                os.mkdir(logPath)
            # 日志文件处理对象
            handler = logging.FileHandler(os.path.join(logPath, "output.log"),encoding="utf-8",mode="a")
            eHandler = logging.FileHandler(os.path.join(logPath, "error.log"),encoding="utf-8",mode="a")
            eHandler.setLevel(logging.ERROR)  # 定义错误日志等级
            # 格式化
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            eHandler.setFormatter(formatter)
            self.logger.addHandler(handler)
            self.logger.addHandler(eHandler)
            handler.close()
            eHandler.close()

    def get_logger(self):
        return self.logger
    '''
    def get_report_path(self):
        reportPath = os.path.join(logPath,"report.html")
        return reportPath
    '''
    def get_result_path(self):
        return logPath

class MyLog:
    log = None
    # 定义
    mutex = threading.Lock()

    def __init__(self):
        pass

    @staticmethod
    def get_log():
        if MyLog.log is None:
            MyLog.mutex.acquire()    # 获取锁
            MyLog.log = Log()
            MyLog.mutex.release()   # 释放锁

        return MyLog.log

if __name__ == '__main__':
    logger = MyLog.get_log().get_logger()
    logger.info('haha')