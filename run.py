import pytest
import os
import readConfig
import logging
import allure
from common.Log import MyLog
from common.emailConfig import MyEmail

localReadConfig = readConfig.ReadConfig()


class App():
    caseList = []    # 待执行测试用例
    def __init__(self):
        self.caseListFile = os.path.join(readConfig.proDir, "caselist.txt")   # 测试用例文件
        self.log = MyLog.get_log()
        self.logger = self.log.get_logger()
        self.email = MyEmail.get_email()

    # 获取没有注释的用例文件
    def set_case_list(self):
        fb = open(self.caseListFile)
        for value in fb.readlines():
            data = str(value)
            if data != '' and not data.startswith("#"):
                test_case_path = os.path.join(readConfig.proDir, "testCase", data)+'.py'
                self.caseList.append(test_case_path.replace("\n", ""))
        fb.close()

    def run(self):
        send_or_not = localReadConfig.get_email('send_or_not')
        commands = ['-s','-v']    # pytest命令
        hasCase = 1
        try:
            self.set_case_list()
            self.logger.info("********TEST START********")
            # 拼接caseList中的文件路径,没有测试用例需要执行时不运行命令
            if len(self.caseList) == 0:
                hasCase = 0
                self.logger.info("无测试用例需要执行！")
                return
            for case in self.caseList:
                commands.append(case)
            result_path = self.log.get_result_path()
            #report_path = os.path.join(result_path,"html-report")
            allure_path = os.path.join(result_path,"allure-report")
            # --html',os.path.join(result_path, "report.html")
            commands.append('--alluredir='+os.path.join(allure_path,"json"))   # allure报告
            pytest.main(commands)
            os.system(r"allure generate " +os.path.join(allure_path,"json")+' -o '+os.path.join(allure_path,"html")+' --clean')
        except Exception as ex:
            self.logger.error(str(ex))
        finally:
            self.logger.info("*********TEST END*********")
            # 发送邮件
            if int(send_or_not) == 1 and hasCase == 1:
                self.email.send_email()
            elif int(send_or_not) == 0:
                self.logger.info("Doesn't send report email!")
            else:
                self.logger.info("Unknown state.")

if __name__ == '__main__':
    app = App()
    app.run()