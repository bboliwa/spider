# -*- coding: utf-8 -*-

import re
import time
from bs4 import BeautifulSoup
import os
import sys
import requests
import xlwt
import logging
import urllib.parse
import queue
from threading import Thread
import threading
from random import randint
import itertools
"""
用wos高级检索，用TS=""检索关键字 

"""


class AtomicInteger():
    def __init__(self, value=0):
        self._value = int(value)
        self._lock = threading.Lock()

    def inc(self, d=1):
        with self._lock:
            self._value += int(d)
            return self._value

    def value(self):
        with self._lock:
            return self._value


class WosAdvancedQuerySpider():
    ##url = "http://apps.webofknowledge.com/Search.do?product=UA&SID=E2vkMLiOafta1P4IqfG&search_mode=GeneralSearch&prID=2b9c5e49-0594-4052-a2a2-d7f3f4be2954"

    SID= "5BxdZewZT5RVCdTpvsG"

    HOST = "https://apps.webofknowledge.com/"
    SEARCH_PREFIX = "TS="

    PARTIAL_SUBFIX = """AND (“Artificial intelligence” OR decision* OR multipurpose OR coordination OR algorithm OR UAV OR bionics* OR *model OR *robotics)  
AND (*drone* OR kilobot OR self-organizing OR “task allocation” OR decentralized OR flock* OR motion* OR PRM OR * state OR inspired * OR Vicsek OR Couzin OR multi-robot OR SPPs OR “probabilistic roadmap” OR “decentralized” )
"""

    TOPIC_FILE = "./topic"
    COOKIE = 'SHIB_FED="ChineseFederation"; SHIB_IDP="https://idp.hust.edu.cn/idp/shibboleth"; SHIB_ID="Sh_Huazhong"; _gcl_au=1.1.638956658.1625455080; _hjid=93aa5ca8-6125-4818-88f0-5b159488e325; bm_sz=845B0B9D74950A9E19B7D291D14474F9~YAAQrHJCF1z4pDh6AQAAK4EGfwy91/M4/5gJCs+ghirY/4XIyvFl5GZ/UCw9r2FIdSk/6b+NRU4vUMh+y9nq/7wQn/dF2uSOHy60Yd2iJRqty3nFb9yzeuMAMn38RcAsDU8uoptum42WhhGtEe375HJCt3h5hKA9yimdMSd5rmL7t2JAZNQlXurgqxW9DgCwZWvttk0y0Jc=; _abck=F8FAA2BD22E12EB22F635A5B4DFAC4E4~0~YAAQrHJCF134pDh6AQAAK4EGfwY1A4ugiVqezY284wYjCPgAEFV+pqjLRlDxWHDHAT+UE6m37vGcaBehVY7lJBYJ2SBUbfi+0Y/P09wVOw1Vxbg5PCTa781VMfvsgOqb9162Mw93CcjcFumdkRIU9Pz/O1Pi0hFYCZxob+PPtbl/0hFIVFRyXEl4q8p7tAxppIIOIMPobSNe2X9vyGZAdmCoOuI4WxLL/DEyd6SQosjJIX59dAigPXXhzf3D1GuOBInAy2RHaPfOtyB62QFsa9NSuCGlUh8aKGz+lV0J2U6xNms4crqaWu+BuQK5ftaX2W7qb9RwoXnwJ69FrCPQi6VICdyKarOeD+Ncp8XALnALWmuRGS8j7/1AWwel2aBoNngr3XD0JuMk7voIURk73hB/r+x6yq24TXO1Hw0UKjc=~-1~-1~-1; SID="5BxdZewZT5RVCdTpvsG"; CUSTOMER="Huazhong University of Science and Technology"; E_GROUP_NAME="Huazhong University of Science and Technology"; dotmatics.elementalKey=SLsLWlMhrHnTjDerSrlG; _hjTLDTest=1; _hjAbsoluteSessionInProgress=0; _sp_ses.630e=*; _sp_id.630e=128eac1b-02d6-4a1f-b42b-6c956dc196db.1625455024.8.1625628785.1625556301.d65fcba4-9abd-4f83-82c5-49a642d1d684; _hjDonePolls=708078; JSESSIONID=FA38CFD8E6B8FBF1DA69F36513A62C94; bm_sv=ACA15D9360CFFB33B7455AD72959E3E2~1USpehMBfMhto+yBDpLBkJOFMUW/dJsmKebXTdzkM5xA18+hmeUyGBE3PhNYuXwM9akYrxuHBsbMM6GP3Gi78oRc0h6M5wTvFPbIFzCCbp6NmNr508FmEoVWr3CrN7xtNzqr3ZIzpnh9NPyScf9FqBjjKuE5ougXlsJUu6Kv6L0=; ak_bmsc=820F4689FD2AFCB6403261F38900838A~000000000000000000000000000000~YAAQrHJCF834pDh6AQAABREHfwzgkSkheKd8FICsmQ0Uy7cekgHrB5hrUpQdVr9INl/MQF6IGz7Nb0Su6bVDCImcj8z5x7t+otIrfoG2QzoaPVRUJ51FCSBz5tipV8ww+g2lx69C3phTMkNx0x5WiT/h1xC/sUPNhMtuh8RcXfy+vxSng7hv6xfVb4KXG6cXrK0tJZMvMAWawAEGUf7el9E1FkBXtMrVjJssIN61Gq9M+4MXsOHn8qzU18Bmtm9Acf1oYVDTWz5t+uOdDW4GEEqUhBb+b684PTzIsxz5Ki25/f+tfa3ip/2te7LFE0pNvzromV9kGZfmc7Np3GtVRxh4G/igVLXxjkneBneDn/8DFK8wYhpa4nFWWIDvY1P/L7Yrul10E5RG2vC9wojIyzuAc4N24P2/E0L/yPsPO74=; RT="z=1&dm=webofknowledge.com&si=a899bdad-e314-4764-a1c6-e0dddef7824b&ss=kqsxe7w2&sl=3&tt=aqz&bcn=//b855d7f6.akstat.io/&ld=f6l&nu=50ozr6tu&cl=w42&ul=w4b"'
    HEADER = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cache-Control": "max-age=0",
        "Connection": "keep-alive",
        "Cookie": COOKIE[0],
        "Host": "apps.webofknowledge.com",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.106 Safari/537.36"}

    params = {
        "product": "UA",
        "SID": SID,
        "search_mode": "GeneralSearch",
        ## "prID": "2b9c5e49-0594-4052-a2a2-d7f3f4be2954"
    }







    ##return (bio_name + ' AND (swarm OR "collective behavior")')

    def getBioName(self,str):
        return str.split("AND")[0].strip()

    def completeFilter(self, str):
        bio_name = self.getBioName(str)
        str = "TS = (" + bio_name + "AND (collective* AND decision*) " + ")"
        return str


    def partialFilter(self, str):
        bio_name = self.getBioName(str)
        str = "TS = (" + bio_name + "AND (swarm* OR collective*)"  + self.PARTIAL_SUBFIX  + ")"
        return str


    def readTopics(self,file_address, isWeak):

        with open(file_address) as f:
            content = f.readlines()


        if isWeak == False:
            content = [  self.completeFilter( x.strip() ) for x in content  ]
        if isWeak == True:
            content = [  self.partialFilter( x.strip() ) for x in content  ]

        return content




    def sendPost(self, topic_keyword):

        POST_URL = "https://apps.webofknowledge.com/UA_AdvancedSearch.do"
        POST_PARA = {
            "product": "UA",
            "search_mode": "AdvancedSearch",
            "SID": WosAdvancedQuerySpider.SID,
            "input_invalid_notice": "Search Error: Please enter a search term.",
            "input_invalid_notice_limits": " <br/>Note: Fields displayed in scrolling boxes must be combined with at least one other search field.",
            "action": "search",
            "replaceSetId": "",
            "goToPageLoc": "SearchHistoryTableBanner",
            "value(input1)": topic_keyword,    ##  topic as keyword
            "value(searchOp)": "search",
            "limitStatus": "collapsed",
            "ss_lemmatization": "On",
            "ss_spellchecking": "Suggest",
            "SinceLastVisit_UTC": "",
            "SinceLastVisit_DATE": "",
            "period": "Range Selection",
            "range": "ALL",
            "startYear": "1950",
            "endYear": "2021",
            "editions": [
                "WOS.CCR",
                "WOS.SCI",
                "WOS.ESCI",
                "WOS.SSCI",
                "WOS.ISSHP",
                "WOS.ISTP",
                "WOS.IC",
                "WOS.AHCI",
                "BCI.BCI",
                "CSCD.CSCD",
                "DIIDW.EDerwent",
                "DIIDW.MDerwent",
                "DIIDW.CDerwent",
                "KJD.KJD",
                "MEDLINE.MEDLINE",
                "RSCI.RSCI",
                "SCIELO.SCIELO"
            ],
            "collections": [
                "WOS",
                "BCI",
                "CSCD",
                "DIIDW",
                "KJD",
                "MEDLINE",
                "RSCI",
                "SCIELO"
            ],
            "update_back2search_link_param": "yes",
            "ssStatus": "display:none",
            "ss_showsuggestions": "ON",
            "ss_query_language": "auto",
            "rs_sort_by": "PY.D;LD.D;SO.A;VL.D;PG.A;AU.A"
        }


        logging.info(str(threading.get_ident()) + " prepare to send post request")
        time.sleep(randint(1000, 3000) * 0.001)


        self.postLock.acquire()
        req = requests.post(url = POST_URL,
                            params = POST_PARA,
                            headers=WosAdvancedQuerySpider.HEADER)
        self.postLock.release()

        status_code = req.status_code
        if status_code != 200:
            ## error handler
            logging.warn(str(threading.get_ident())+"  post request status_code is not 200, code is " + status_code)
            pass
        html = ""
        html = req.text
        ## this response contains search history tab
        ## tab [href == https://apps.webofknowledge.com/summary.do]
        ## summary.do 即改关键词的论文list的 url
        return html



    def parsePosthtml(self, html):
        """
        use bs4 to parse html text
        """

        def findChild(this ,tag):
            return this[0].findChildren(tag, recursive=False)


        """
        find the href tag, search history contains multiple records,
        the first is what we want
        """
        soup = BeautifulSoup(html, "lxml")
        block_div = soup.find_all("div", {"class": "block-history"})
        table = findChild(findChild(block_div, "form"), "table" )
        first_tr = table[0].contents[7]
        second_td = first_tr.contents[3]


        href_count = str(second_td.text).strip()
        href_count = int(href_count)

        url_want = ""
        if href_count != 0:
            url_want = second_td.contents[1].contents[1].attrs['href']

        if url_want =="":
            logging.warn(str(threading.get_ident())+ " get no url of paper list page")

        url_want = urllib.parse.urljoin(WosAdvancedQuerySpider.HOST,  url_want)
        return href_count, url_want



    def doSpider(self):
        self.putTaskInCache()

        NumWorks =6
        for i in range(NumWorks):
            try:
                t= Thread(target=self.taskHandler )
                t.start()
            except Exception as e:
                logging.error(e)


        while self.pending_task.empty() is False:
            logging.info("in main, the current queue status : size = " + str( self.pending_task.qsize()  ))
            time.sleep(7)

        self.isRunning = False
        logging.info("spider task down, the main is ready to leave")

        while self.exited.value() != NumWorks:
            logging.info("wait for all workers done, exited num is " +  str(self.exited.value()))
            time.sleep(7)

        logging.info("strong type: " + str(self.strongMetric.keywordHit.value()) + " keyword hits, "+ str(self.strongMetric.paperHit.value()) + " paper hits")
        logging.info(
            "weak type: " + str(self.weakMetric.keywordHit.value()) + " keyword hits, " + str(self.weakMetric.paperHit.value()) + " paper hits")
        logging.info("Bye---------------------")


    class Metric:
        def __init__(self, isWeak):

            self.isWeak = isWeak
            self.keywordHit = AtomicInteger()
            self.paperHit = AtomicInteger()



    class Task:

        def __init__(self,  topic, isWeak, idx):
            self.topic = topic
            self.isWeak = isWeak
            self.idx = idx
            self.bioName = self.getBioName(topic)


        def getBioName(self,str):
            str = str.split("AND")[0].strip()
            str = str.split("(")[1].strip()
            str = str[1:-1]
            return str


    def taskHandler(self):

        logging.info(str(threading.get_ident()) + " is working ")
        while self.isRunning:
            try:

                time.sleep(randint(100,300)  * 0.001)



                task = self.pending_task.get(timeout=1)

                if task == None:
                    continue

                topic = task.topic
                idx = task.idx
                isWeak = task.isWeak
                logging.info(str(threading.get_ident()) +" current topic is " + topic)
                res = self.parsePosthtml(self.sendPost(topic))
                href_count, url_want = res[0], res[1]
                if href_count == 0:
                    continue

                import math
                logging.info(str(threading.get_ident())+ " send url to get paper list, url is " + url_want)


                self.upateMetric(1, min(5, href_count),isWeak )
                records = ""
                records = self.getPaperList(url_want, 5)
                self.storePapers(idx, task.bioName, records, isWeak)

            except Exception as e:
                logging.error(e)

                continue

        logging.info( str(threading.get_ident()) + " is leaving ")
        self.exited.inc()


    def putTaskInCache(self):

        for isWeak in [True,False]:
            idx = 0
            topics = self.readTopics("./topic", isWeak)
            for topic in topics:
                self.pending_task.put(self.Task(topic, isWeak, idx))
                idx = idx + 1



    def initLog(self):
        logging.basicConfig(
            level=logging.INFO,
            format='[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler("debug.log"),
                logging.StreamHandler(sys.stdout)
            ]
        )




    def __init__(self):

        self.initLog()
        self.pending_task = queue.Queue(1000)
        logging.info("hello logging is started -------------")
        self.book = xlwt.Workbook(encoding='utf-8')
        self.sheet = self.book.add_sheet('date', cell_overwrite_ok=True)
        self.isRunning = True
        self.exited = AtomicInteger()
        self.postLock = threading.Lock()

        self.weakMetric = self.Metric(True)
        self.strongMetric = self.Metric(False)

    def upateMetric(self, kw_hit, paper_hit, isWeak):
        if kw_hit != 1:
            raise Exception("unexpected parameter")

        if isWeak:
            self.weakMetric.keywordHit.inc()
            self.weakMetric.paperHit.inc(paper_hit)
        else:
            self.strongMetric.keywordHit.inc()
            self.strongMetric.paperHit.inc(paper_hit)

    class PaperInfo:
        def __init__(self, title, authors, url):
            self.title = title  ## str
            self.authors = authors ## list of str
            self.url = url


    def storePapers(self, idx,bio_name , paper_records, isWeak):

        self.sheet.write(idx, 0, bio_name)
        i=1
        for record in paper_records:
            ##abstract = self.getPaperAbstract(record.url)
            abstract = ""
            store = record.title + "        " + record.authors[0] + "       " + abstract
            self.sheet.write(idx, i, store)
            i= i+1


        if isWeak:
            self.book.save(r'./weak.xls')
        else:
            self.book.save(r'./strong.xls')


    def getPaperList(self, index_url, limited):


        html  = self.sendGet(index_url)

        soup = BeautifulSoup(html, "lxml")
        paper_records = []
        paper_tags = soup.find_all("div", {"class": "search-results-content"})

        cnt = 0
        for record in paper_tags:
            cnt = cnt + 1
            if cnt > limited:
                break
            title =  record.find("value").text
            url = record.find("a").attrs["href"] ## the first is paper ur
            url = urllib.parse.urljoin(self.HOST, url)
            items_author = record.find_all("a",  attrs= {"alt": "Find more records by this author"})
            authors = [item.text for item in items_author ]
            paper_records.append(self.PaperInfo(title, authors, url))


        return paper_records




    def sendGet(self, get_url):
        req = requests.get(get_url, headers=self.HEADER)

        status_code = req.status_code
        if status_code != 200:
            logging.warn(threading.get_ident() + " get request status_code is not 200, url is " + get_url)
        html = req.text
        return html


    def getPaperAbstract(self ,paper_url):


        html = self.sendGet(paper_url)


        soup = BeautifulSoup(html, "lxml")

        abstract = ""
        just_one_absract = 0
        for elem in soup(text=re.compile(r'^Abstract') ):
            abstract = elem.parent.nextSibling
            just_one_absract = just_one_absract + 1
        if just_one_absract != 1:
            logging.warn("find multiple abstract from paper page")

        return abstract




