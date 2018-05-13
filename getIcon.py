"""
This program gets icons from users that answer a given question in www.zhihu.com,
a Chinese version of quora
"""

from urllib.request import urlopen
from bs4 import BeautifulSoup as BS
import os
from urllib.request import urlretrieve
from shutil import rmtree
import re

savingDirectory = "downloadedIcons"
baseurl = "https://www.zhihu.com/question"

def getIconLinks(qnum):
    qurl = baseurl+"/"+qnum
    html = urlopen(qurl)
    #BSParser is an BeautifulSoup object
    BSParser = BS(html, "html.parser")
    allAnswers = BSParser.find("body").find("div", {"class":"QuestionPage"})\
            .find("div",{"class":"Question-mainColumn"}).find("div",{"class":"QuestionAnswers-answers"})\
            .find_all("div", {"class":"List-item"})
    print(len(allAnswers))
    iconLinks = []
    tag = None
    iconLink = None
    for i in range(len(allAnswers)):
        try:
            answerItem = allAnswers[i].find("div",{"class":"ContentItem AnswerItem"})
            tag = answerItem.find("img")
            iconLink=tag['src']
            if iconLink is not None:
                iconLinks.append(iconLink)
        except:
            print(i)
            print(tag)
            print("No image in one answer")
    return iconLinks

def download(iconLinks, directory):
    if os.path.exists(directory):
        if os.path.isfile(directory):
            os.remove(directory)
        else:
            rmtree(directory)
    os.makedirs(directory)
    for i in range(len(iconLinks)):
        filename = str(i)
        path = directory+"/"+filename
        urlretrieve(iconLinks[i], path)

qnum = "275615648"
links = getIconLinks(qnum)
directory = "DownloadIcons"
download(links, directory)
