import sys

sys.path.append(".")

from src.crawler import Crawler
from src import cleaner
from src.fileUtil import FileUtil


def crawlXimalaya():
    # 爬取的文档名字
    albumPath = 'D:\\lldxx\\'
    htmlUrl = 'https://www.ximalaya.com/ertong/33647650/'
    apiUrl = 'https://www.ximalaya.com/revision/play/v1/audio?id={0}&ptype=1'
    crawler = Crawler()
    # 获取所有的trackName和trackId
    content = crawler.request(htmlUrl, 'get')
    idList = cleaner.getAlbumIdList(content)
    # print(idList)
    for item in idList:
        sections = item[1].split('/')
        trackId = sections[len(sections) - 1]
        url = apiUrl.format(trackId)
        # 获取每个track的下载路径
        data = crawler.getJson(url)
        audioUrl = data['data']['src']
        # 下载并保存track
        data = crawler.downloadFile(audioUrl)
        FileUtil.writeFile(albumPath, '{0}.m4a'.format(item[0]), data.content)
