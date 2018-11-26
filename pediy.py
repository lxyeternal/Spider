from bs4 import BeautifulSoup
from urllib.request import urlopen
import random
import requests
import time
import thread6
import re


"""

2018-11-26

author:郭文博

"""
def get_url(url,headers):       #   首先是获取到主页面所有的主题链接网址

    Theme = {}


    """
        模拟浏览器来获取网页的html代码
        """


    timout = random.choice(range(80,100))

    request = requests.get(url,headers = headers)

    if(request.status_code!=200):

        print("获取网址失败")

    html = BeautifulSoup(request.text,"html.parser")

    theme = html.find_all("div",{"class":"card px-0"})

    for i in theme:

        themecontant = i.find_all("a")

        for j in themecontant:

            href = j['href']

            themeString = j.string

            if(themeString == None):

                continue

            themestring = themeString.strip()

            Theme[themestring] = href


    return  Theme





def get_topic_url(url,urldist,headers):    #   获取每一个主题的所有话题的URL

    themeitemurl = {}

    listurl = []

    for value in urldist.values():

        themeurl = url + value

        # print(themeurl)

        request = requests.get(themeurl,headers = headers)

        if (request.status_code != 200):

            # print("获取网址失败")

            continue

        else:

            html = BeautifulSoup(request.text, "html.parser")

            urlhtml = html.find_all("nav")

            for i in urlhtml:

                urlcontant = i.find_all("li",{"class":"page-item"})

                for j in urlcontant:

                    itemhref = j.find_all("a")

                    for j in itemhref:

                        href = j['href']

                        themeString = j.string

                        if (themeString == None):

                            continue

                        themestring = themeString.strip()

                        themeitemurl[themestring] = href

        listurl.append(themeitemurl)

    return listurl


def get_contanturl(url,listurl,headers):        #  获取每个话题的url

    contanturl = {}

    contanturllist = []

    for i in listurl:

        for values in i.values():

            URL = url + values

            request = requests.get(URL,headers = headers)

            if(request.status_code != 200):

                continue

            html = BeautifulSoup(request.text,"html.parser")

            htmlurl = html.find_all("tr")

            for k in htmlurl:

                htmlhref = k.find_all("div",{"class":"subject"})

                for href  in htmlhref:

                    a = href.find_all("a")

                    lena = len(a)

                    if(lena>1):

                        # print(a[1])

                        topicstring = a[1].string

                        if (topicstring == None):

                            continue

                        Topicstring = topicstring.strip()

                        contanturl[Topicstring] = a[1]['href']

                    else:

                        # print(a[0])

                        topicstring = a[0].string

                        if (topicstring == None):
                            continue

                        Topicstring = topicstring.strip()

                        contanturl[Topicstring] = a[0]['href']

        contanturllist.append(contanturl)

        # print(contanturllist)

    return contanturllist


def get_contant(url,urllist,headers):         #   获取每一个话题的所有论坛回复

    contant = {}

    contantlist = []

    for i in urllist:

        for values in i.values():

            contanturl = url + values

            request = requests.get(contanturl,headers = headers)

            if(request.status_code != 200):

                continue

            html = BeautifulSoup(request.text,"html.parser")

            Name = html.find_all("tr",{"class":"post"})


            for k in Name:

                contantkey = ''

                contantvalue = ''

                td = k.find_all("td",{"class":"px-0"})

                for TD in td:

                    span = TD.find_all("span",{"class":"username font-weight-bold"})

                    Contant = TD.find_all("div",{"class":"message mt-1 break-all"})

                    for Span in span:

                        name = Span.find_all("a")

                        contantkey = name[0].string.strip()

                    for contantstring in Contant:

                        # reply = contantstring.find_all("div",{"class":"message mt-1 break-all"})

                        contantvalue = contantstring[0].string.strip()


                    contant[contantkey] = contantvalue

            print(contant)

        contantlist.append(contant)

    return contantlist

if __name__ == "__main__":

    url = "https://bbs.pediy.com/"

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.235'
    }

    Theme = get_url(url,headers)

    # lentheme = len(Theme)

    topicurl = get_topic_url(url,Theme,headers)

    topiccontanturl = get_contanturl(url,topicurl,headers)








