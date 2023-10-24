import os
import codecs
import configparser

proDir = os.path.split(os.path.realpath(__file__))[0]    # 项目根路径
configPath = os.path.join(proDir, "config.ini")

class ReadConfig:
    def __init__(self):
        fd = open(configPath,'r', encoding='utf-8', errors='ignore')
        data = fd.read()

        #  remove BOM
        if data[:3] == codecs.BOM_UTF8:
            data = data[3:]     # 保存文件时，文件开始部分有可能会引入BOM格式相关信息，三个字节，需要移除
            file = codecs.open(configPath, "w", encoding='utf-8', errors='ignore')
            file.write(data)
            file.close()
        fd.close()

        self.cf = configparser.ConfigParser()
        self.cf.read_file(open(configPath,'r',encoding='UTF-8'))

    def get_email(self, name):
        value = self.cf.get("EMAIL", name)
        return value

    def get_http(self, name):
        value = self.cf.get("HTTP", name)
        return value

    def get_db(self, name):
        value = self.cf.get("DATABASE", name)
        return value

if __name__ == '__main__':
    rc = ReadConfig()
    print(rc.get_email("mail_host"))