import db
import re
import cleaner
from crawler import Crawler
# from requests.packages import urllib3
import time
# urllib3.disable_warnings()
from fileUtil import FileUtil


def crawlEastMoney():
    db.initDb()
    etfListUrl="http://fund.eastmoney.com/ETFN_jzzzl.html"
    eftHistUrl="http://api.fund.eastmoney.com/f10/lsjz?callback={0}&fundCode={1}&pageIndex=1&pageSize={3}&startDate=&endDate=&_={2}"
    callback='jQuery18303575276080195784_1602819402553'
    crawler=Crawler(**{'referer':'http://fundf10.eastmoney.com/'})
    # 获取etf列表
    html=crawler.downloadHtml(etfListUrl)
    items=cleaner.getEtfList(html)
    db.insertList(items)
    # 插入etf历史净值
    db.clear('fund_hist')
    for item in items:
        code=item['code']
        print(code)
        ts=int(time.time())
        # 获取历史净值记录条数
        url=eftHistUrl.format(callback,code,ts,1)
        content=crawler.downloadHtml(url)
        size=cleaner.getHistCount(content,callback)
        # 一次性获取所有历史净值
        url=eftHistUrl.format(callback,code,ts,size)
        content=crawler.downloadHtml(url)
        items=cleaner.getHistList(content,callback,code)
        db.insertHistList(items)


def crawlXimalaya():
    # 爬取的文档名字
    albumPath='D:\\lldxx\\'
    htmlUrl='https://www.ximalaya.com/ertong/33647650/'
    apiUrl='https://www.ximalaya.com/revision/play/v1/audio?id={0}&ptype=1'
    crawler=Crawler()
    # 获取所有的trackName和trackId
    content=crawler.downloadHtml(htmlUrl)
    idList=cleaner.getAlbumIdList(content)
    # print(idList)
    for item in idList:
        sections=item[1].split('/')
        trackId=sections[len(sections)-1]
        url=apiUrl.format(trackId)
        # 获取每个track的下载路径
        data=crawler.getJson(url)
        audioUrl=data['data']['src']
        # 下载并保存track
        data=crawler.downloadFile(audioUrl)
        FileUtil.writeFile(albumPath,'{0}.m4a'.format(item[0]),data.content)


if __name__=="__main__":
    crawlXimalaya()
    
    
    
