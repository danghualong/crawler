import re
import json


def getEtfList(html):
    html = re.findall("<table class=\"dbtable\" id=\"oTable\">(.*?)</table>",
                      html)[0]
    rows = re.findall("<tr.*?>(.*?)</tr>", html)
    items = []
    for i in range(3, len(rows)):
        cols = re.findall("<td.*?>(.*?)</td>", rows[i])
        obj = {'code': cols[3]}
        links = re.findall('<a.*?>(.*?)</a>', cols[4])
        obj['name'] = links[0]
        items.append(obj)
    return items


def getHistCount(content, callback):
    content = re.findall('{0}\((.*?)\)'.format(callback), content)
    content = content[0]
    dic = json.loads(content)
    return dic['TotalCount']


def getHistList(content, callback, code):
    content = re.findall('{0}\((.*?)\)'.format(callback), content)
    content = content[0]
    dic = json.loads(content)
    dic = dic['Data']['LSJZList']
    result = []
    for item in dic:
        result.append(
            (code, item['FSRQ'], item['DWJZ'], item['LJJZ'], item['SDATE'],
             item['ACTUALSYI'], item['NAVTYPE'], item['JZZZL'], item['SGZT'],
             item['SHZT'], item['FHFCZ'], item['FHFCBZ'], item['DTYPE'],
             item['FHSP']))
    return result


def getAlbumIdList(html):
    html = re.findall(
        "<div class=\"text _Vc\"><a title=\"(.*?)\" href=\"(.*?)\">", html)
    return html