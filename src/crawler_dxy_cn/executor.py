import sys
# from os import path
# pathname = path.dirname(path.dirname(path.abspath(__file__)))
sys.path.append(".")

from src.crawler import Crawler
from dataHandler import getItems
from src.fileUtil import FileUtil
import re

#  本网站只能每类爬取前10页的内容？

urlPrefix = "http://drugs.dxy.cn"
crawler = Crawler()
#获取所有的药品类型
def getCatUrls():
    items=getItems(urlPrefix)
    # 所有类别链接
    urls=[]
    for k in items:
        item=items[k]
        for child in item['subItems']:
            urls.append((child['name'],child['url']))
    return urls
# 获取指定类药品页数
def getDrugListPageCount(cat_url):
    #先爬取每一类的页数
    text = crawler.request(urlPrefix+cat_url, "get")
    # 解析总页数
    pages = re.findall(r'<a href="'+cat_url+'\?page=.*?">(.*?)</a>', text, re.S)
    totalCount=1
    if(len(pages)>2):
        totalCount=int(pages[len(pages)-2])
    return totalCount
# 爬取指定的一类药
def crawlCat(name_url):
    cat_name=name_url[0]
    cat_url=name_url[1]
    totalCount=getDrugListPageCount(cat_url)
    print("----{0} 共{1}页".format(cat_name,totalCount))
    #解析药品链接
    for  p in range(totalCount):
        drug_list_url="{0}?page={1}".format(cat_url,(p+1))
        crawelDrugs(cat_name,drug_list_url)
        print("----{0} 第{1}/{2}页下载完成".format(cat_name,(p+1),totalCount))
# 获取一页药品内容
def crawelDrugs(cat_name,drug_list_url):
    drugsText = crawler.request(urlPrefix+drug_list_url, "get")
    drugs=re.findall(r'<a href="(/drug/.*?)">(.*?)</a>', drugsText, re.S)
    for drug in drugs:
        drug_url=drug[0]
        drug_name=drug[1]
        crawelDrug(drug_name,drug_url,cat_name)

#爬取指定的一种药内容
def crawelDrug(drug_name,drug_url,cat_name):
    drug_name=drug_name.replace("<!-- --> - <!-- -->","_")
    detailText=crawler.request(urlPrefix+drug_url,"get")
    detail=re.findall(r'(<div class="container-middle">.*?)<div class="container-right">', detailText, re.S)
    if(len(detail)>0):
        try:
            FileUtil.writeFile("D:\\drugs\\{0}\\".format(cat_name),drug_name+".txt",detail[0])
        except  Exception as e:
            print(drug_name,":",e)
    else:
        print("xxxx NoContent ----{0}--------{1}".format(drug_name,drug_url))
# 爬取所有的药品信息
def do():
    urls=getCatUrls()
    # 爬取每类的药品列表
    for  name_url in urls: 
        crawlCat(name_url)

# 
# crawelDrugs("ABC","/category/6FO9JRKee7oGjg4ueqcElw==?page=12")
# crawelDrug("西尼地平胶囊_湖南九典制药股份有限公司","/drug/pT7MVacemepepmvNHyLDdQPozNg==","钙通道阻滞剂")


