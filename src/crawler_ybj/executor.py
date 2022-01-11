import sys

sys.path.append(".")

from src.crawler import Crawler
import re
import time

crawler = Crawler(ContentType="application/x-www-form-urlencoded")
url = "https://fw.ybj.beijing.gov.cn/drug/druginfo/findChiledLimit"
with open("./result.txt", "a") as f:
    for i in range(191):
        data={
            "line":1,
            "levelnum":0,
            "cpage":(i+1),
        }
        r = crawler.postJson(url, data=data)
        items=r["chiled"]
        for item in items:
            f.write("{0}\n".format(item))
        print("page {0} is downloaded!".format((i+1)))
        time.sleep(0.3)
