import sys
# from os import path
# pathname = path.dirname(path.dirname(path.abspath(__file__)))
sys.path.append(".")

from src.crawler import Crawler
from src.fileUtil import FileUtil
import re
from bs4 import BeautifulSoup




#  本网站只能每类爬取前10页的内容？

urlPrefix = "http://ypk.39.net"
crawler = Crawler()
names={}

# 获取指定类药品页数
def getDrugListPageCount(cat_url):
    url=urlPrefix+cat_url
    #先爬取每一类的页数
    text = crawler.request(url, "get")
    # 解析总页数
    pages = re.findall(r"<a target='_self' href='"+url+".*?'>(.*?)</a>", text, re.S)
    totalCount=1
    if(len(pages)>2):
        totalCount=int(pages[len(pages)-1])
    return totalCount
# 爬取指定的一类药
def crawlCat(cat_name,cat_url):
    totalCount=getDrugListPageCount(cat_url)
    print("----{0} 共{1}页".format(cat_name,totalCount))
    #解析药品链接
    for  p in range(totalCount):
        url="{0}/p{1}".format(cat_url,(p+1))
        crawelDrugs(cat_name,url)
        print("----{0} 第{1}/{2}页下载完成".format(cat_name,(p+1),totalCount))
# 获取一页药品内容
def crawelDrugs(cat_name,drug_list_url):
    drugsText = crawler.request(urlPrefix+drug_list_url, "get")
    drugs=parseDrugList(drugsText)
    for drug in drugs:
        drug_url=drug[0]
        drug_name=drug[1]
        if(drug_name in names):
            names[drug_name]+=1
            drug_name="{0}({1})".format(drug_name,names[drug_name])
        else:
            names[drug_name]=1
        crawelDrug(drug_name,drug_url,cat_name)

def parseDrugList(drugsText):
    drugs=[]
    soup=BeautifulSoup(drugsText,'html.parser')
    for k in soup.find_all('a'):
        img=k.find('img')
        if(img and 'drugs-ul-img' in img.get('class')):
            drugs.append((k.get('href'),k.get('title')))
    return drugs

#爬取指定的一种药内容
def crawelDrug(drug_name,drug_url,cat_name):
    detailText=crawler.request(drug_url+'manual',"get")
    details=parseDetailText(detailText)
    if(len(details)>0 and len(details[0])>0):
        try:
            FileUtil.writeFile("D:\\drugs3\\{0}\\".format(cat_name),drug_name+".txt",details[0])
        except  Exception as e:
            print(drug_name,":",e)
    else:
        print("xxxx NoContent ----{0}--------{1}".format(drug_name,drug_url))

def parseDetailText(detailText):
    soup=BeautifulSoup(detailText,'html.parser')
    details=[]
    for k in soup.find_all('div'):
        cls=k.get('class')
        if(cls and 'screen-sort-content' in cls and 'summary-box' in cls):
            details.append(str(k))
    return details
# 爬取所有的药品信息
def do():
    cats=[ ('/ganmao', '感冒发热'), ('/pifu', '皮肤用药'), 
('/weichang', '肠胃用药'),
('/wuguan', '五官用药'), 
('/huxixitong', '呼吸系统类'), ('/jiating', '家庭常备'), 
('/nanke', '男科用药'), ('/fuke', '妇科用药'), ('/erke', '儿科用药'), ('/wssjyy', '维生素及营养类'), ('/xinnaoxueguan', '心脑血管'), ('/gandanyi', '肝胆胰用药'), 
('/shenbing', '肾病'), ('/neifenmi', '内分泌失常'), ('/shenjing', '神经_精神'), 
('/zhongliu', '肿瘤科'), ('/mianyi', '风湿免疫科'), ('/jishengchong', '抗寄生虫类'), 
('/dianjiezhi', '水电解质及酸碱平衡'), ('/xueye', '血液疾病类'), ('/jiehe', '抗结核及麻风类'), ('/xingbingyongyao', '性病用药')]

    for cat in cats:
        cat_name=cat[1]
        cat_url=cat[0]
        crawlCat(cat_name,cat_url)

do()
