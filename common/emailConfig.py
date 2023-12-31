import os
import sys
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime
import threading
import readConfig
from common.Log import MyLog
import zipfile
import glob

localReadConfig = readConfig.ReadConfig()

class Email:
    # 读取配置
    def __init__(self):
        global host, user, password, port, sender, title, content
        host = localReadConfig.get_email("mail_host")
        user = localReadConfig.get_email("mail_user")
        password = localReadConfig.get_email("mail_pass")
        port = localReadConfig.get_email("mail_port")
        sender = localReadConfig.get_email("sender")
        title = localReadConfig.get_email("subject")
        content = localReadConfig.get_email("content")
        self.value = localReadConfig.get_email("receiver")
        self.receiver = []
        # get receiver list
        for n in str(self.value).split(";"):
            self.receiver.append(n)
        # defined email subject
        #date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.subject = title
        self.log = MyLog.get_log()
        self.logger = self.log.get_logger()
        self.msg = MIMEMultipart('mixed')

    # 设置发送标题、发送和接收人
    def config_header(self):
        self.msg['subject'] = self.subject
        self.msg['from'] = sender
        self.msg['to'] = ";".join(self.receiver)   #;用于拼接列表项

    def config_content(self):
        content_plain = MIMEText(content, 'plain', 'utf-8')
        self.msg.attach(content_plain)

    # 打包并压缩result目录下的测试结果文件和测试报告，命名为test.zip，并添加为附件
    def config_file(self):
        # if the file content is not null, then config the email file
        resultPath = self.log.get_result_path()
        zipPath = os.path.join(readConfig.proDir, "result", "test.zip")
        # zip file
        zipFiles = []
        files = self.listFiles(resultPath,zipFiles)
        f = zipfile.ZipFile(zipPath, 'w', zipfile.ZIP_DEFLATED)
        for file in files:
            f.write(file)
        f.close()

        reportFile = open(zipPath, 'rb').read()
        filehtml = MIMEText(reportFile, 'base64', 'utf-8')
        filehtml['Content-Type'] = 'application/octet-stream'
        filehtml['Content-Disposition'] = 'attachment; filename="test.zip"'
        self.msg.attach(filehtml)

    # 遍历所有文件
    def listFiles(self,path,zipFiles):
        files = glob.glob(path + r'\*')
        for file in files:
            if os.path.isdir(file):
                self.listFiles(file,zipFiles)
            else:
                zipFiles.append(file)
        return zipFiles
    '''
    def check_file(self):
        reportPath = self.log.get_report_path()
        if os.path.isfile(reportPath) and not os.stat(reportPath) == 0:
            return True
        else:
            return False
    '''
    # 发送邮件
    def send_email(self):
        self.config_header()
        self.config_content()
        self.config_file()
        try:
            smtp = smtplib.SMTP()
            smtp.connect(host, port)
            smtp.login(user, password)
            smtp.sendmail(sender, self.receiver, self.msg.as_string())
            smtp.quit()
            self.logger.info("The test report has send to developer by email.")
        except Exception as ex:
            self.logger.error(str(ex))

# 自定义发送邮件类
class MyEmail:
    email = None
    mutex = threading.Lock()

    def __init__(self):
        pass
    @staticmethod
    def get_email():     # 发送邮件方法加锁
        if MyEmail.email is None:
            MyEmail.mutex.acquire()
            MyEmail.email = Email()
            MyEmail.mutex.release()
        return MyEmail.email

if __name__ == "__main__":
    email = MyEmail.get_email()
    email.send_email()
