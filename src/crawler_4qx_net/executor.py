import sys
# from os import path
# pathname = path.dirname(path.dirname(path.abspath(__file__)))
sys.path.append(".")

from src.crawler import Crawler
import re

crawler = Crawler()
urlprefix = "http://www.4qx.net/"
headers = {
    'user-agent':
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
}
result = {}
queue = []
# id=10024&drugs=1197205514", "阿莫西林"
queue.append((urlprefix + "Drugs_Manual.php?id=10026&drugs=1190307731", "青霉素"))
count = 0
while (len(queue) > 0):
    urlName = queue.pop(0)
    url = urlName[0]
    title = urlName[1]
    count += 1
    print(count, "--------:", url, '--------', title, '---------')
    text = ''
    try:
        text = crawler.request(url, "get")
    except Exception as ex:
        print(ex)
        continue
    #解析字符串
    #首先解析正文
    content = re.findall(r'<div class="main_text_1">(.*?)</div>', text, re.S)
    if (content is not None and len(content) > 0):
        fc = content[0].strip()
        with open("D:/drugs/" + title.replace("/", "-") + ".txt",
                  "w",
                  encoding="utf-8") as f:
            f.write(fc)
    #<li><a href="Drugs_Manual.php?id=4014&drugs=1226632445"></a></li>
    items = re.findall("<li><a href=\"(.*?)\">(.*?)</a>.*?</li>", text)
    for item in items:
        if (item[0].startswith("Drugs_Manual.php")):
            subUrl = urlprefix + item[0]
            if (subUrl not in result):
                result[subUrl] = item[1]
                queue.append((subUrl, item[1]))
