import sys
# from os import path
# pathname = path.dirname(path.dirname(path.abspath(__file__)))
sys.path.append(".")

from src.crawler import Crawler
from dataHandler import getItems
from src.fileUtil import FileUtil
import re

urlPrefix = "http://drugs.dxy.cn"
crawler = Crawler()
items=getItems(urlPrefix)
# 所有类别链接
urls=[]
for k in items:
    item=items[k]
    for child in item['subItems']:
        urls.append((child['name'],child['url']))
# 爬取每类的药瓶列表
for  name_url in urls:
    cat_name=name_url[0]
    cat_url=name_url[1]
    #先爬取每一类的页数
    text = crawler.request(urlPrefix+cat_url, "get")
    # 解析总页数
    pages = re.findall(r'<a href="'+cat_url+'\?page=.*?">(.*?)</a>', text, re.S)
    totalCount=1
    if(len(pages)>2):
        totalCount=int(pages[len(pages)-2])
    print("----{0} 共{1}页".format(cat_name,totalCount))
    #解析药品链接
    for  p in range(totalCount):
        drug_list_url="{0}?page={1}".format(cat_url,(p+1))
        drugsText = crawler.request(urlPrefix+drug_list_url, "get")
        drugs=re.findall(r'<a href="(/drug/.*?)">(.*?)</a>', drugsText, re.S)
        for drug in drugs:
            drug_url=drug[0]
            drug_name=drug[1]
            n=drug_name.index("<")
            abbr_name=drug_name
            if n>0:
                abbr_name=drug_name[:n]
            detailText=crawler.request(urlPrefix+drug_url,"get")
            detail=re.findall(r'<div class="container-middle">(.*?)<div class="container-right">', detailText, re.S)
            
            if(len(detail)>0):
                try:
                    FileUtil.writeFile("D:\\drugs\\{0}\\".format(cat_name),abbr_name+".txt",detail[0])
                except  Exception as e:
                    print(e)
            else:
                print("xxxx NoContent ----{0}--------{1}".format(drug_name,drug_url))
        
        print("----{0} 第{1}/{2}页下载完成".format(cat_name,(p+1),totalCount))



