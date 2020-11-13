import requests
import json
from interfaceTest.common.Log import logger

logger = logger
class RunMain():

    def send_post(self, url, data, headers):# 定义一个方法，传入需要的参数url和data
        # 参数必须按照url、data顺序传入
        result = requests.post(url=url, params=data, headers=headers)#.json()# 因为这里要封装post方法，所以这里的url和data值不能写死
        res = json.dumps(result.json(), ensure_ascii=False, sort_keys=True, indent=2)
        logger.info("\n请求地址：%s\t请求方式:%s\n请求正文：%s\n响应正文：%s\n" % (result.url, result.request.method, data, res))
        return res

    def send_get(self, url, data, headers):
        result = requests.get(url=url, params=data, headers=headers)
        res = json.dumps(result.json(), ensure_ascii=False, sort_keys=True, indent=2)
        logger.info("\n请求地址：%s\t请求方式:%s\n请求正文：%s\n响应正文：%s\n" % (result.url, result.request.method, data, res))
        return res

    def run_main(self, method, url=None, params=None, headers=None):#定义一个run_main函数，通过传过来的method来进行不同的get或post请求
        result = None
        if method == 'post':
            result = self.send_post(url, params, headers)
            # logger.info(str(result))
        elif method == 'get':
            result = self.send_get(url, params, headers)
            # logger.info(str(result))
        else:
            print("method值错误！！！")
            logger.info("method值错误！！！")
        return result
if __name__ == '__main__':#通过写死参数，来验证我们写的请求是否正确
    result = RunMain().run_main('post', 'http://106.75.239.60:8010/rank/getUserRankAndList', {'pageNo':'1','pageSize':'5'}, {"token":"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI1YTAzZDQ1NWNiNGU0OTAyYjIyM2U5ODhmOWI2ODRhNCIsImV4cCI6MjQ2NjcyNjUxOX0.dAlJ_QT16B7S9imonLhv_CQWxNYPnvbe1BUOrHOXwyo"})
    print(result)