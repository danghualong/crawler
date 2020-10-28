import requests
import re
import json

class Crawler(object):
    def __init__(self,**kwargs):
        self.headers={
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36"        
        }
        if(kwargs!=None):
            for k,v in kwargs.items():
                self.headers[k]=v
    def _decodeContent(self,resp):
        srcEncoder=resp.encoding
        encoders=re.findall("<meta.*?charset=(.*?)\"",resp.text)
        pageEncoder="utf-8"
        if(len(encoders)>0):
            pageEncoder=encoders[0]
        return resp.text.encode(srcEncoder).decode(pageEncoder)
    def downloadHtml(self,url):
        '''
        下载Html内容
        '''
        resp=requests.get(url,headers=self.headers)
        return self._decodeContent(resp)
    def request(self,url,data):
        '''
        发送Post请求
        '''
        resp=requests.request('post',url,headers=self.headers,data=data)
        return self._decodeContent(resp)
    def getJson(self,url):
        '''
        获取Json内容
        '''
        resp=requests.get(url,headers=self.headers)
        return json.loads(resp.text)
    def downloadFile(self,url):
        '''
        下载文件
        '''
        resp=requests.get(url,headers=self.headers)
        return resp
