import requests
import json


class Crawler(object):
    def __init__(self, **kwargs):
        self.headers = {
            'User-Agent':
            "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36"
        }
        if (kwargs is not None):
            for k, v in kwargs.items():
                self.headers[k] = v

    def _decodeContent(self, resp):
        charset = 'utf-8'
        encs = requests.utils.get_encodings_from_content(resp.text)
        if (len(encs) > 0):
            charset = encs[0]
        # print(encs)
        resp.encoding = charset
        return resp.text

    def request(self, url, method='post', data=None):
        '''
        发送Post,Get请求
        '''
        resp = requests.request(url=url,
                                method=method,
                                headers=self.headers,
                                data=data)
        result = self._decodeContent(resp)
        return result

    def getJson(self, url, data):
        '''
        获取Json内容
        '''
        text = self.request(url, 'get', data)
        return json.loads(text)

    def downloadFile(self, url):
        '''
        下载文件
        '''
        resp = requests.get(url, headers=self.headers)
        return resp
