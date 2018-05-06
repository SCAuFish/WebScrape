#Test
#Basic introduction:
#https://sites.google.com/view/cshenportfolio/computer-science-studies
from urllib.request import urlopen
from urllib.request import quote
from bs4 import BeautifulSoup as BS
import json
import re


#entryName should be without slash
def getIP(entryName):
    url = ("https://zh.wikipedia.org/w/index.php?title="\
            +entryName+"&offset=&limit=500&action=history")
    #print('url is', url)
    htmlFile = urlopen(url)
    BSObject = BS(htmlFile, "html.parser")

    #Find the anonymous user's IP addrewss
    allIPs = BSObject.findAll("a", {"class":"mw-userlink mw-anonuserlink"})
    pureIPSet = set()
    for IP in allIPs:
        pureIP = IP.find("bdi").contents[0]
        pureIPSet.add(pureIP)
    return pureIPSet

'''Get the country name based on the IP address
   The api used now, freegeoip, is going to stop service in August
   this year. Hopefully, there'll be a new site relacing it!
   '''
def getCountryName(IPString):
    try:
        response = urlopen('https://freegeoip.net/json/'+IPString)\
                .read().decode('utf-8')
    except:
        return None

    jsonResponse = json.loads(response)
    return jsonResponse.get("country_name")

'''Get all subwebpages under current webpage and add them to entrySet
   if the subwebpage is not in banSet
   '''
def getAllEntry(startEntry, entrySet, banSet):
    try:
        #This website means that it will search only through Chinese
        #wikipedia
        response = urlopen('https://zh.wikipedia.org/wiki/'\
                +startEntry)
        responseParser = BS(response, 'html.parser')
        bTags=responseParser\
                .find('div', id="bodyContent")\
                .findAll('a', href=re.compile("^(/wiki/).*$"))
        for bTag in bTags:
            link=bTag.attrs['href']
            link=link.replace('/wiki/','')
            if link not in banSet:
                entrySet.add(link)
    except Exception as e:
        print('Exception while getting entries')
        print(e)

if __name__=='__main__':
    countryDict=dict()
    #Somehow, we need to transform the utf-8 str to str
    startEntry = quote('中国')
    entrySet=set()
    visitedSet=set()
    entrySet.add(startEntry)
    totalCount = 0;

    while(len(entrySet)>0 and totalCount < 10000):
        toVisit = entrySet.pop()
        try:
            IPSets = getIP(toVisit)
            visitedSet.add(toVisit)
            #print('Looking on Entry: '+toVisit)
            #print(IPSets)
            for IP in IPSets:
                cname = getCountryName(IP)
                #Add the country name to statistics dictionary
                countryDict[cname] = \
                    1 if cname not in countryDict else countryDict[cname]+1
                totalCount+=1
                #print(cname+':'+IP)
            getAllEntry(toVisit, entrySet, visitedSet)
        except Exception as e:
            print(e)
            #print('but I am too lazy to deal with it')

        print(totalCount)

    print(countryDict)



