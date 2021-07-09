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
import traceback
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

    SID= "E2otS6St8wOZpdbUMN9"

    HOST = "http://apps.webofknowledge.com/"
    SEARCH_PREFIX = "TS="

    PARTIAL_SUBFIX = """AND (“Artificial intelligence” OR decision* OR multipurpose OR coordination OR algorithm OR UAV OR bionics* OR *model OR *robotics)  
AND (*drone* OR kilobot OR self-organizing OR “task allocation” OR decentralized OR flock* OR motion* OR PRM OR * state OR inspired * OR Vicsek OR Couzin OR multi-robot OR SPPs OR “probabilistic roadmap” OR “decentralized” )
"""

    TOPIC_FILE = "./topic"
    COOKIE = 'SHIB_FED="ChineseFederation"; SHIB_IDP="http://idp.hust.edu.cn/idp/shibboleth"; SHIB_ID="Sh_Huazhong"; _gcl_au=1.1.638956658.1625455080; _hjid=93aa5ca8-6125-4818-88f0-5b159488e325; _hjDonePolls=708078; ak_bmsc=7D15CF40E7786AA7A838847D2E2D66AF~000000000000000000000000000000~YAAQdwpM2z7F1YN6AQAADFjliwwEi9kBZKAyEhaNqXJ2r0Js7r9zOK02Y8k33ITs3R4UkMQh69qyY7MjGthTeCIB01dWWs+uuAP25GbtFnK4OLVU/FCbSDlIyJWBsBpv6CkGaSZMl5taQleYyA2/TXGJDh7+qry4dwCrColClcBjkPWfVKs0y8L6iNE5g/k0pvx1xoZNTrMpHZUTDRo7+f1yW4amBGxYNOFRUXtZ/UFpRUQgjdO4iMvUL5w/pljqOeLYfWrQKr/pp4XxAqxjS3pnPH60CWJuKGgaUAh9Erwwm6mj+NHa/Xv71x6nK52QULnYLieTjgYyIdjjTsoj+cWdTbcGm3OTuUN0J3vnnadd0ME5gBGkDd1utdegCDPjCz6SLoVtbpH/dVX9u/+Egg==; _sp_ses.630e=*; _hjAbsoluteSessionInProgress=1; SID="E2otS6St8wOZpdbUMN9"; CUSTOMER="Huazhong University of Science and Technology"; E_GROUP_NAME="Huazhong University of Science and Technology"; bm_sz=55F228B01C845879F468C6DCFE559A14~YAAQlhTGy2yg5/t5AQAAJlcojAzHHa2CUVX6U4KpFGjqxahqBKP71PEANpmZ0KPrcS1LZT+n7JOEVgobsBuXVWcRRldH2+hYFCwAmnq2jyxb0pbKOdxeOeQXTCIiClK1CtDQTVyk4nifPznMqU+264jj8tmczzYiCtencXG6/SB2BhZlJj3A/tThJQHR6y+HOsqPQmJoG9k=; dotmatics.elementalKey=SLsLWlMhrHnTjDerSrlG; _hjTLDTest=1; _abck=7C24859D970674C11810A64112158E2E~0~YAAQlhTGy3Kg5/t5AQAA8BopjAYeN9Owg1u4d+BC9iYCAorOM8E5Ch0g1Rmvw6KnoMkbTdwsQPtOR/bL1zzdnG7g6lqUFfgLfXC3ONgnC0xkTBHXeWk29x9S8MafbY9A7kzmcmBi8ZmPrEMd+6oBXzDwcPE5EZGtmK3/kBk2WbzyBxYipful42fMgnwxzSAT4KRnA/YLxiY13OUGLrMsgV6KIGm3l+Zi6GSqZpdsdyPVdS519s6taATzkRLvLqBfJnv+jw8lZi7418acvOEJ6b5zftgcyXCr5KVlcbKKcEMIn/f5EQ11zOzMw7ztVbBRiKl7QzsVaXqWTG3vDr86SqnJVjpjMDIDjicuOpM4pVnIQ10y5BAHTn+t/8MU3tpFgW2hlGt7DTdXeuRxw2xNqfi6YvJ1iqlm5JRlJohsf2g=~-1~-1~-1; _sp_id.630e=c01f36c1-106f-4374-866a-da964ba6b3c7.1625844736.1.1625849142.1625844736.01a0e151-0cb2-4090-ace3-e457ff3b4d38; JSESSIONID=3ED14358ECEB92C6E890C6842F30D445; bm_sv=CC34B22ADA326B59B2EE3132DF9302F1~ZCEI7m9q7S0zxI2KZ6Vtt4Ta+jHQtwyZkSv7XneoLzIysFORAx7UeQbnAk/I4RinjZ207V3YDCXkKtSmy5oAo0+CcKgG91a1d4/KbvnwevXWh1iyfesOuj0Zm4q0oLvUIbr3ZOkO7d1E8p8jVP3pPDhlcTs5MKiykHfwmZ4FugY=; RT="z=1&dm=webofknowledge.com&si=d2bdffb0-f500-4f80-bb7b-856089faf7b1&ss=kqwfthto&sl=r&tt=89we&bcn=//684d0d38.akstat.io/&obo=8&nu=1iq64c1es&cl=4s640&ld=4s649&r=9bjbpnzc&ul=4s64a"'
    SHEET_HEADER_NAMES = ['生物名', '论文', '作者', '摘要', '出版日期', '期刊会议名称', '相关程度（1-5）']
    HEADER = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cache-Control": "max-age=0",
        "Connection": "keep-alive",
        "Cookie": COOKIE,
        "Host": "apps.webofknowledge.com",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }


    THRESHOLD = 150
    WORKER_NUM = 5



    def completeFilter(self, str):
        bio_name = str.strip()
        str = "TS = (" + bio_name + " AND (collective* AND decision*) " + ")"
        return str

    def partialFilter(self, str):
        bio_name = str.strip()
        str = "TS = (" + bio_name + " AND (swarm* OR collective*)"  + self.PARTIAL_SUBFIX  + ")"
        return str


    def readTopics(self,file_address, isWeak):

        with open(file_address) as f:
            content = f.readlines()


        topics = []
        content = [ x.strip() for x in content ]
        if isWeak == False:
            topics = [  self.completeFilter( x.strip() ) for x in content  ]
        if isWeak == True:
            topics = [  self.partialFilter( x.strip() ) for x in content  ]

        return [content, topics]




    def sendPost(self, topic_keyword):

        POST_URL = "http://apps.webofknowledge.com/UA_AdvancedSearch.do"
        POST_PARA = {
          "product":"UA",
          "search_mode":"AdvancedSearch",
          "SID" : WosAdvancedQuerySpider.SID,
          "input_invalid_notice":"Search Error: Please enter a search term.",
          "input_invalid_notice_limits":" <br/>Note: Fields displayed in scrolling boxes must be combined with at least one other search field.",
          "action":"search",
          "replaceSetId":"",
          "goToPageLoc":"SearchHistoryTableBanner",
          "value(input1)": topic_keyword,
          "value(searchOp)":"search",
          "limitStatus":"collapsed",
          "ss_lemmatization":"On",
          "ss_spellchecking":"Suggest",
          "SinceLastVisit_UTC":"",
          "SinceLastVisit_DATE":"",
          "period":"Range Selection",
          "range":"ALL",
          "startYear":"1950",
          "endYear":"2021",
          "editions":[
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
          "collections":[
            "WOS",
            "BCI",
            "CSCD",
            "DIIDW",
            "KJD",
            "MEDLINE",
            "RSCI",
            "SCIELO"
          ],
          "update_back2search_link_param":"yes",
          "ssStatus":"display:none",
          "ss_showsuggestions":"ON",
          "ss_query_language":"auto",
          "rs_sort_by":"PY.D;LD.D;SO.A;VL.D;PG.A;AU.A"
        }



        logging.info(str(threading.get_ident()) + " prepare to send post request")
        time.sleep(randint(2000, 3000) * 0.001)


        self.postLock.acquire()
        req = requests.post(url = POST_URL,
                            params = POST_PARA,
                            headers=WosAdvancedQuerySpider.HEADER)
        self.postLock.release()

        status_code = req.status_code
        if status_code != 200:
            ## error handler
            logging.warn(str(threading.get_ident())+"  post request status_code is not 200, code is " + str(status_code))
            return
        html = ""
        html = req.text
        ## this response contains search history tab
        ## tab [href == http://apps.webofknowledge.com/summary.do]
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

        NumWorks = self.WORKER_NUM
        for i in range(NumWorks):
            try:
                t= Thread(target=self.taskHandler )
                t.start()
            except Exception as e:
                logging.error(e)


        while self.pending_task.empty() is False:
            logging.info("in main, the current queue status : size = " + str( self.pending_task.qsize()  ) + " workers num : " +str( threading.active_count())  )
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

        def __init__(self,  topic, isWeak, bioName):
            self.topic = topic
            self.isWeak = isWeak
            self.bioName = bioName



    def sendPostToCleanHistory(self):
        POST_URL = "http://apps.webofknowledge.com/UA_CombineSearches.do"
        remove_item = []
        for i in range(1,101):
            remove_item.append(str(i))
        POST_PARA={
          "product":"UA",
          "prev_search_mode":"AdvancedSearch",
          "search_mode":"CombineSearches",
          "SID":WosAdvancedQuerySpider.SID,
          "action":"remove",
          "goToPageLoc":"SearchHistoryTableBanner",
          "currUrl":"http://apps.webofknowledge.com/UA_AdvancedSearch_input.do?product=UA&search_mode=AdvancedSearch&errorQid=77&replaceSetId=&goToPageLoc=SearchHistoryTableBanner&SID=%s" % WosAdvancedQuerySpider.SID,
          "dSet":remove_item
        }




        req = requests.post(url=POST_URL,
                            params =  POST_PARA,
                            headers=WosAdvancedQuerySpider.HEADER)


        status_code = req.status_code
        if status_code != 200:
            ## error handler
            logging.warn(
                str(threading.get_ident()) + "  post request to clean status_code is not 200, code is " + str(status_code))
            return
        html = ""
        html = req.text



    def taskHandler(self):

        logging.info(str(threading.get_ident()) + " is working ")
        while self.isRunning:
            try:

                time.sleep(randint(100,300)  * 0.001)

                if self.stop_world:
                    self.stop_cnt.inc(1)

                while self.stop_world:
                    logging.info(
                        str(threading.get_ident()) + " too many search records, current worker is hacked")
                    time.sleep(randint(400, 500) * 0.001)

                if self.cur_paperlist_num.value() >= WosAdvancedQuerySpider.THRESHOLD:
                    logging.info( str(threading.get_ident()) +" too many search records, stop all threads until clean is done")
                    self.stop_world = True
                    while self.stop_cnt.value() < self.WORKER_NUM:
                        logging.info(
                            str(threading.get_ident()) + "wait for all threads to stop, cur is " + self.stop_cnt.value())
                        time.sleep(randint(100, 300) * 0.001)

                    self.sendPostToCleanHistory()
                    self.stop_world = False
                    self.stop_cnt = AtomicInteger(0)
                    time.sleep(3000 * 0.001)
                    logging.info(
                        str(threading.get_ident()) + "clean is fine, restore all threads to work")

                task = self.pending_task.get(timeout=1)

                if task == None:
                    continue

                topic = task.topic
                isWeak = task.isWeak
                logging.info(str(threading.get_ident()) +" current topic is " + topic)
                res = self.parsePosthtml(self.sendPost(topic))
                href_count, url_want = res[0], res[1]
                if href_count == 0:
                    continue

                import math
                logging.info(str(threading.get_ident())+ " send url to get paper list, url is " + url_want)
                self.cur_paperlist_num.inc()

                self.upateMetric(1, min(5, href_count), isWeak )
                paper_urls = []
                paper_urls = self.getPaperList(url_want, 5)
                self.storePapers(task.bioName, paper_urls, isWeak)

            except queue.Empty:
                pass
            except ConnectionResetError as e:
                logging.error(e)
                pass
            except Exception as e:
                logging.error(e)
                loc = str(e).find("Connection aborted")
                if loc != -1:
                    self.pending_task.put(task)
                traceback.print_exc()
                pass



        logging.info( str(threading.get_ident()) + " is leaving ")
        self.exited.inc()


    def putTaskInCache(self):
        for isWeak in [False]:
            res = self.readTopics("./topic", isWeak)
            topics = res[1]
            bio_names = res[0]
            idx = 0
            for topic in topics:
                self.pending_task.put(self.Task(topic, isWeak, bio_names[idx]  ) )
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


    def initSheet(self):
        self.book = xlwt.Workbook(encoding='utf-8')
        self.sheet = self.book.add_sheet('spider_records', cell_overwrite_ok=True)
        for i in range(len(WosAdvancedQuerySpider.SHEET_HEADER_NAMES)):
            self.sheet.write(0, i, WosAdvancedQuerySpider.SHEET_HEADER_NAMES[i])

    def __init__(self):
        self.stop_world = False
        self.stop_cnt = AtomicInteger(0)
        self.initLog()
        self.allocate_row = 1
        self.allocate_lock = threading.Lock()
        self.pending_task = queue.Queue(1000)
        self.cur_paperlist_num = AtomicInteger(0)
        logging.info("hello logging is started -------------")

        self.initSheet()
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




    def storePapers(self , bio_name , paper_urls, isWeak):

        l_paper = len(paper_urls)
        self.allocate_lock.acquire()
        all_row = self.allocate_row
        self.allocate_row  = self.allocate_row + l_paper
        self.allocate_lock.release()
        crow = all_row
        for url in paper_urls:

            ## return  title, authors ,abstract, pub_date, publisher
            fileds = self.getPaperInfo(bio_name,url)

            self.sheet.write(crow, 0, bio_name)
            f_len = len(fileds)
            if f_len == 0:
                continue
            fileds[0] = str(crow - all_row + 1) +" : "+ fileds[0]
            offset = 1



            for ccol in range(f_len):
                field = fileds[ccol]
                if isinstance(field, list):
                    self.sheet.write(crow, ccol + offset, ','.join(field) )
                else:
                    self.sheet.write(crow, ccol + offset, field)
            crow= crow+1

            if isWeak:
                self.book.save(r'./weak.xls')
            else:
                self.book.save(r'./strong.xls')





    def getPaperList(self, index_url, limited):


        html  = self.sendGet(index_url)

        soup = BeautifulSoup(html, "lxml")
        url_list = []
        paper_tags = soup.find_all("div", {"class": "search-results-content"})

        cnt = 0
        for record in paper_tags:
            cnt = cnt + 1
            if cnt > limited:
                break
            url = record.find("a").attrs["href"] ## the first is paper ur
            url = urllib.parse.urljoin(self.HOST, url)
            url_list.append(url)

        return url_list




    def sendGet(self, get_url):
        req = requests.get(get_url, headers=self.HEADER)

        status_code = req.status_code
        if status_code != 200:
            logging.warn(threading.get_ident() + " get request status_code is not 200, url is " + get_url)
        html = req.text
        return html


    def getPaperInfo(self, bio_name,paper_url):

        paper_url = paper_url +"&locale=en_US"

        html = self.sendGet(paper_url)


        soup = BeautifulSoup(html, "lxml")

        abstract = ""
        just_one = 0
        res = soup(text=re.compile(r'^Abstract'))
        if len(res) == 0:
            logging.warn(str(threading.get_ident()) +" " + bio_name +" :: "  + "paper " + paper_url + ": no abstract found")
            return []
        for elem in res:
            abstract_tag = elem.parent.parent.find("p", attrs={"class", "FR_field"})
            if abstract_tag == None:
                logging.warn(str(threading.get_ident()) +" " +bio_name +" :: "  +"paper " + paper_url + ": no abstract found")
                return []
            abstract = abstract_tag.text
            just_one = just_one + 1

        if just_one > 1:
            logging.warn(str(threading.get_ident())+" " +bio_name +" :: "  +"paper " + paper_url + ": find multiple abstract from paper page")
            return []

        title = ""
        div = soup.find("div", attrs={"xmlns:ts":"http://ts.thomson.com/framework/xml/transform"})
        if div == None:
            logging.warn(str(threading.get_ident()) +" " +bio_name +" :: "  +"paper " + paper_url + ": no title found")
            return []
        title_tag  = div.find("value")
        if title_tag == None:
            logging.warn(str(threading.get_ident()) +" " +bio_name +" :: "  +"paper " + paper_url + ": no title found")
            return []
        title = title_tag.text

        authors = []
        author_tags = soup.find_all("a", attrs={"title" : "Find more records by this author" })
        l_au = len(author_tags)
        if l_au == 0:
            logging.warn(str(threading.get_ident())+" " +bio_name +" :: "  +"paper " + paper_url + ": no authors found")
            return []

        for i in range(l_au):
            authors.append(author_tags[i].text)


        publisher = ""
        div = soup.find("div", attrs={"class", "block-record-info block-record-info-source"})
        if div == None:
            logging.warn(str(threading.get_ident())+" " +bio_name +" :: "  +"paper "  + paper_url + ": no publisher found")
            return []
        span = div.find("span", attrs={"class", "sourceTitle"})
        if span == None:
            logging.warn(str(threading.get_ident())+" " +bio_name +" :: "  +"paper " + paper_url + ": no publisher found")
            return []
        publisher_tag = span.find("value")
        if publisher_tag == None:
            logging.warn(str(threading.get_ident()) +" " +bio_name +" :: "  +"paper " + paper_url + ": no publisher found")
            return []
        publisher = publisher_tag.text


        pub_date = ""
        location = div.text.find("Published")
        if location == -1:
            logging.warn(str(threading.get_ident()) +" " +bio_name +" :: "  +"paper " + paper_title + ": no published date found")
            return []
        pub_date = div.text[location + len("Published:\n"):].split("\n")[0]





        return [title, authors ,abstract, pub_date, publisher]




