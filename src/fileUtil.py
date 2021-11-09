import os

class FileUtil(object):
    @staticmethod
    def writeFile(path,fileName,content):
        if(not os.path.exists(path)):
            os.makedirs(path)
        with open('{0}{1}'.format(path,fileName),'ab') as f:
            f.write(content)
            f.flush()
        print(fileName,'downloaded')