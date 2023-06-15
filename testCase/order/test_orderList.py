import pytest
import allure
from common import common
from common.httpConfig import ConfigHttp
from common.Log import MyLog

logger = MyLog.get_log().get_logger()


def test_orderList():
    assert 1 == 2


def test_getAllOrders():
    testCase = common.get_xls("order_datas.xlsx","Order")

    httpConfig = ConfigHttp()
    httpConfig.config(testCase,0)
    response = httpConfig.post()
    code = response.status_code
    logger.info("返回体："+response.content.decode('utf-8'))
    logger.info("接口返回状态码为："+str(code))
    assert code == 200

if __name__ == '__main__':
    test_orderlist()



