import sys

sys.path.append(".")

from src.crawler import Crawler
import re

crawler = Crawler()
prefix = "https://www.cma.org.cn"
with open("./result.txt", "a") as f:
    for i in range(11):
        url = "https://www.cma.org.cn/col/col1542/index.html?uid=4346&pageNum={0}".format(
            (i + 1))
        # print(url + "\n")
        r = crawler.request(url, method='get')
        #<a href="/art/2018/6/8/art_1542_263.html" target="_blank">便秘临床路径</a>
        items = re.findall("<a.*?href=\"(.*?)\".*? target=\"_blank\"", r)
        print(len(items))
        print("-----\n")
        for item in items:
            item = prefix + item
            print("url:", item)
            r2 = crawler.request(item, method='get')
            #<p>附件：<a href="/module/download/downfile.jsp?classid=0&filename=2744946c3924484685880c1e225222d1.docx"><img src="/module/jslib/icons/word.png"/>便秘临床路径（2017县医院适用版）.docx</a>
            item2 = re.findall("附件.*?<a href=\"(.*?)\">", r2)
            for item in item2:
                item = prefix + item
                print(item)
                f.write(item + "\n")
