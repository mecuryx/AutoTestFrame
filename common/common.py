import os
from xlrd import open_workbook
from xml.etree import ElementTree as ElementTree
from common.Log import MyLog
import readConfig

#localConfigHttp = configHttp.ConfigHttp()
logger = MyLog.get_log().get_logger()

# 从excel文件中读取测试用例
def get_xls(xls_name, sheet_name):
    cls = []     # 每条用例数据放入list
    # 获取xls文件路径
    xlsPath = os.path.join(readConfig.proDir, "testFile", xls_name)
    file = open_workbook(xlsPath)
    sheet = file.sheet_by_name(sheet_name)
    # 根据sheet获取行
    nrows = sheet.nrows
    for i in range(nrows):
        if sheet.row_values(i)[0] != u'case_name':
            cls.append(sheet.row_values(i))
    return cls


# 从xml文件中读取sql语句
database = {}


# 返回sql字典  格式为database{
#                           db1{
#                               tb1
#                                   {
#                                       sql1{sqlId:sql},
#                                       ...
#                                   }
#                                ...
#                               }
#                           ...
#                           }
def set_xml():
    if len(database) == 0:
        sql_path = os.path.join(proDir, "testFile", "SQL.xml")
        tree = ElementTree.parse(sql_path)
        for db in tree.findall("database"):
            db_name = db.get("name")
            # print(db_name)
            table = {}
            for tb in db.getchildren():
                table_name = tb.get("name")
                # print(table_name)
                sql = {}
                for sqlData in tb.getchildren():
                    sql_id = sqlData.get("id")
                    # print(sql_id)
                    sql[sql_id] = sqlData.text
                table[table_name] = sql
            database[db_name] = table


# 获取指定表字典
def get_xml_dict(database_name, table_name):
    set_xml()
    database_dict = database.get(database_name).get(table_name)
    return database_dict


# 获取指定sql
def get_sql(database_name, table_name, sql_id):
    db = get_xml_dict(database_name, table_name)
    sql = db.get(sql_id)
    return sql
