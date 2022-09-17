import os
import asyncio
import lxml
from pyppeteer import launch
from bs4 import BeautifulSoup
import time


#将 pyppeteer 的操作封装成 fetchUrl 函数，用于发起网络请求，获取网页源码。


async def pyppteer_fetchUrl(url):
    browser = await launch({'headless': False,'dumpio':False, 'autoClose':True})
    page = await browser.newPage()
    await page.evaluateOnNewDocument('() =>{ Object.defineProperties(navigator,'
                                     '{ webdriver:{ get: () => false } }) }')
    await page.setUserAgent(
       'Mozilla/5.0(Linux;Android6.0;Nexus5Build/MRA58N)AppleWebKit/537.36(KHTML, likeGecko)Chrome/86.0.4240.198MobileSafari/537.36'
    )
    await page.goto(url)
    await asyncio.sleep(5)
    str = await page.content()
    await browser.close()
    return str

def fetchUrl(url):
    return asyncio.get_event_loop().run_until_complete(pyppteer_fetchUrl(url))



#页数

def getPageUrl():
    for page in range(1,7):
        if page == 1:
            yield 'http://www.nhc.gov.cn/xcs/yqtb/list_gzbd.shtml'
        else:
            url = 'http://www.nhc.gov.cn/xcs/yqtb/list_gzbd_'+ str(page) +'.shtml'
            yield url

#通过 getTitleUrl 函数，获取某一页的文章列表中的每一篇文章的标题，链接，和发布日期

def getTitleUrl(html):
    time.sleep(5)
    bsobj = BeautifulSoup(html,'lxml')
    titleList = bsobj.find('div', attrs={"class":"list"}).ul.find_all("li")
    for item in titleList:
        link = "http://www.nhc.gov.cn" + item.a["href"]
        title = item.a["title"]
        date = item.span.text
        yield title, link, date

#通过 getContent 函数，获取某一篇文章的正文内容


def getContent(html):

    bsobj = BeautifulSoup(html, 'lxml')
    cnt = bsobj.find('div', attrs={"id": "xw_box"}).find_all("p")
    s = ""
    if cnt:
        for item in cnt:
            s += item.text
        return s

    return "爬取失败！"



#通过 saveFile 函数，可以将爬取到的数据保存在本地的 txt 文档里

def saveFile(path, filename, content):
    if not os.path.exists(path):
        os.makedirs(path)

    # 保存文件
    with open(path + filename + ".txt", 'w', encoding='utf-8') as f:
        f.write(content)


if "__main__" == __name__:
    for url in getPageUrl():
        s =fetchUrl(url)

        for title,link,date in getTitleUrl(s):

            print(title,link)
            #如果日期在1月21日之前，则直接退出
            mon = int(date.split("-")[1])
            day = int(date.split("-")[2])
            if mon <= 1 and day < 21:
                break

            html =fetchUrl(link)
            content = getContent(html)
            print(content)
            saveFile("G:/develop/txtmmmm/", title, content)
            print("-----"*20)
