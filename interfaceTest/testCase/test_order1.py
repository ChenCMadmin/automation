import json
import unittest
import paramunittest
import urllib.parse
from interfaceTest import geturlParams, readExcel
from interfaceTest.common.configHttp import RunMain
from interfaceTest.readExcel import code

geturl = geturlParams.geturlParams().get_Url()# 调用我们的geturlParams获取我们拼接的URL
login_xls = readExcel.readExcel().get_xls('cainiaotaojin.xlsx', 'order1')
@paramunittest.parametrized(*login_xls)     #参数化
class testUser(unittest.TestCase):
    def setParameters(self, case_name, path, query, method, expect, headers):
        """
        set params
        :param case_name:
        :param path
        :param query
        :param method
        :param expect
        :param headers
        :return:
        """
        self.case_name = str(case_name)
        self.path = str(path)
        self.query = str(query)
        self.method = str(method)
        self.ass = code(expect)
        self.headers = eval(headers)

    def description(self):
        """
        test report description
        :return:
        """
        self.case_name

    @classmethod
    def setUpClass(cls):  # 开始的时候全程就调用一次，一定要用 @classmethod 装饰器装饰

        #获取订单编号orderNum
        global orderNum
        data = readExcel.readExcel().get_xls('cainiaotaojin.xlsx', 'order')[0]
        url1 = "http://www.xxx.com/login?"
        new_url = url1 + data[2]
        data1 = dict(urllib.parse.parse_qsl(urllib.parse.urlsplit(new_url).query))  # 将一个完整的URL中的name=&pwd=转换为{'name':'xxx','pwd':'bbb'}
        url = ''.join([geturl, data[1]])  # 完整的接口
        info = RunMain().run_main(data[3], url, data1, eval(data[5]))  # 根据Excel中的method调用run_main来进行requests请求，并拿到响应文本
        order = json.loads(info)  # 将响应转换为字典格式
        orderNum = order["data"]["orderNum"]

    @classmethod
    def tearDownClass(cls):  # 执行结束后的时候全程就调用一次，一定要用 @classmethod 装饰器装饰
        pass

    def setUp(self):
        """

        :return:
        """
        print(self.case_name + "->测试开始:" + self.path + "?" + self.query)

    def test01case(self):
        self.checkResult()

    def tearDown(self):
        print("测试结束，输出log完结\n" + info)

    def checkResult(self):# 调用接口获取响应文本断言
        """
        check test result
        :return:
        """
        global info
        url1 = "http://www.xxx.com/login?"
        new_url = url1 + self.query + orderNum
        data1 = dict(urllib.parse.parse_qsl(urllib.parse.urlsplit(new_url).query))# 将一个完整的URL中的name=&pwd=转换为{'name':'xxx','pwd':'bbb'}
        url = ''.join([geturl, self.path])# 完整的接口
        info = RunMain().run_main(self.method, url, data1, self.headers)# 根据Excel中的method调用run_main来进行requests请求，并拿到响应文本
        self.assertIn(self.ass, info)# 响应内容断言

if __name__ == '__main__':
    testUser()
