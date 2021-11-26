import sys
sys.path.append(".")

import re
from src.fileUtil import FileUtil

def handleFile(filePath,newFilePath,fileName):
    content=''
    with open(filePath,"r", encoding='utf-8') as f:
        content=f.read()
    content=content.replace("\n","")
    content=re.sub("\s{2,}",'',content)
    content=content.replace("</p>","\n")
    content=re.sub("<br.*?/>","\n",content)
    content=re.sub('<.*?>','',content)
    FileUtil.writeFile(newFilePath,fileName,content)
    # if(not os.path.exists(newFilePath)):
    #         os.makedirs(newFilePath)
    # fileName='{0}\\{1}'.format(newFilePath,fileName)
    # with open(fileName,"w", encoding='utf-8') as f:
    #     f.write(content)
    #     f.flush()
    # print("{0} is created".format(fileName))

import os 
def handleFiles(filePath,resultPath):
    for s in os.listdir(filePath):
      tmpdir = os.path.join(filePath,s)
      if(os.path.isdir(tmpdir)):
          resultdir=os.path.join(resultPath,s)
          handleFiles(tmpdir,resultdir)
      else:
          s=s.replace(".txt",".docx")
          handleFile(tmpdir,resultPath,s)


if __name__=="__main__":
    handleFiles("D:\\drugs4","d:\\drugs5")
