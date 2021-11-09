import sys

sys.path.append(".")

import time
from src.crawler_eastmoney import db
from src import cleaner
from src.crawler import Crawler


def crawlEastMoney():
    db.initDb()
    etfListUrl = "http://fund.eastmoney.com/ETFN_jzzzl.html"
    eftHistUrl = "http://api.fund.eastmoney.com/f10/lsjz?callback={0}&fundCode={1}&pageIndex=1&pageSize={3}&startDate=&endDate=&_={2}"
    callback = 'jQuery18303575276080195784_1602819402553'
    crawler = Crawler(**{'referer': 'http://fundf10.eastmoney.com/'})
    # 获取etf列表
    html = crawler.request(etfListUrl, 'get')
    items = cleaner.getEtfList(html)
    db.insertList(items)
    # 插入etf历史净值
    db.clear('fund_hist')
    for item in items:
        code = item['code']
        print(code)
        ts = int(time.time())
        # 获取历史净值记录条数
        url = eftHistUrl.format(callback, code, ts, 1)
        content = crawler.request(url, 'get')
        size = cleaner.getHistCount(content, callback)
        # 一次性获取所有历史净值
        url = eftHistUrl.format(callback, code, ts, size)
        content = crawler.request(url, 'get')
        items = cleaner.getHistList(content, callback, code)
        db.insertHistList(items)
