import os

class FileUtil(object):
    @staticmethod
    def writeFile(path, fileName, content):
        if(not os.path.exists(path)):
            os.makedirs(path)
        if(path[-1] != '\\'):
            path=path+"\\"
        with open('{0}{1}'.format(path,fileName),'w',encoding='utf-8') as f:
            f.write(content)
            f.flush()
        print(fileName,'downloaded')
    
    