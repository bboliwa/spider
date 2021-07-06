# -*- coding: utf-8 -*-

import re
import time
from bs4 import BeautifulSoup
import os
import sys
import requests


"""
用wos高级检索，用TS=""检索关键字 

"""


class WosAdvancedQuerySpider():
    ##url = "http://apps.webofknowledge.com/Search.do?product=UA&SID=E2vkMLiOafta1P4IqfG&search_mode=GeneralSearch&prID=2b9c5e49-0594-4052-a2a2-d7f3f4be2954"

    SID= "E2vkMLiOafta1P4IqfG"

    SEARCH_PREFIX = "TS="

    TOPIC_FILE = "./topic"
    COOKIE = 'SHIB_FED="ChineseFederation"; SHIB_IDP="https://idp.hust.edu.cn/idp/shibboleth"; SHIB_ID="Sh_Huazhong"; _gcl_au=1.1.638956658.1625455080; _hjid=93aa5ca8-6125-4818-88f0-5b159488e325; dotmatics.elementalKey=SLsLWlMhrHnTjDerSrlG; SID="E2vkMLiOafta1P4IqfG"; CUSTOMER="Huazhong University of Science and Technology"; E_GROUP_NAME="Huazhong University of Science and Technology"; _sp_ses.630e=*; _hjTLDTest=1; _hjAbsoluteSessionInProgress=0; ak_bmsc=20C6E0A05BC913A16CB5896BC70C8537~000000000000000000000000000000~YAAQVVDGy2ya6ft5AQAAHmGjeQwb8DlpgrxvdYY3b7bhsowfyUJ7JebXt1lb+rg8fbMAVIK05mLP2pat/14EPOE7LxuoO/pZXcdXW+w6OMhWREeF9nUXqONaQ6W/0cFj8BBjQDUD7LCsXWWg+Ghb4Kn9qcfCs7QjBe/DTxEpn6O4rLGTCZZHVjFIqjOirGRvN1efFjwXwkpOSLRbDfUCySssOF4zMbOgU3c/yFUjJLJ2GKErn71NJMqyzNr5Ri10AIsQ3id1/Tt+Qs350g/G0g9kGUOj2SJl+Q/U0BHcB7FgAkSxH02tvckNjyS/Twomm41fdEoHrBvVAQ6mc7ZIRdTRjUwRj06XIfPEMQ==; _sp_id.630e=128eac1b-02d6-4a1f-b42b-6c956dc196db.1625455024.5.1625538399.1625466198.5ef85ffd-eb4c-4100-8f1c-dffadf4e5595; bm_sz=51BF625A841326D23281CC7CB158A1A0~YAAQVVDGy3ua6ft5AQAA3uKjeQyo5so9bdc71mDea1LZePIVjtrEBQ9W6tW3xgC9fKdUBkGBpGdrke4BuVUKdJ529DHu4l2oX8OeRUFulSlXI8vOVVo+cGOgQfWi1rTiL+J+BRALXkPyKwmyY77W1wGI2D2tY3fK1pkhJlBV4hum0pnGkW0er0/Gbqb3ihQqX90IRb764KTbAhOFdg==; bm_sv=6B43BB68D6D0756746C4087BA87AA0E5~doCiB0WiJ/Bm1NT0/6QVuJedSXUvx9GnV8/MJT1/Km/7kZWilLpuF3E7yOGF/1R2JqlTk4vGLjTwm0XDTkmn0viuxQjQY4z0hHWXjB4sGZKwlZrxB1CG3N855Nj9qzYsgfMPEGz+Se1kRyCZ3US/Onl6wyuGIOb6K3XXhJlBsyc=; RT="z=1&dm=webofknowledge.com&si=a899bdad-e314-4764-a1c6-e0dddef7824b&ss=kqrfj7kk&sl=3&tt=g0j&bcn=//684d0d3d.akstat.io/&ul=9zoo&hd=a18u" ',

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


    """
        !TODO assginee: 海大
        根据爬取规则.doc
        完成 Filter1，Filter2 对应爬取规则.doc完相关， 部分相关
        完成 yourgetTopicList1，yourgetTopicList2 对应完全相关， 部分相关
        代码可以重构，
    """
    ##! TODO   assginee: 海大
    ##def yourFilter2(self, str):

    ##! TODO   assginee: 海大
    def yourFilter(self, str):
        ## apply default rules to filter
        ## example:
        ## "Acinonyx jubatus" AND swarm OR "collective behavior" --> TS= ("Acinonyx jubatus" AND (swarm OR "collective behavior") )
        pass

    ##! TODO   assginee: 海大
    ## yourgetTopicList2(self):

    ##! TODO   assginee: 海大
    def yourgetTopicList(self):
        ## fs = open(TOPIC_FILE)

        ## for line in fs:
        ## line = defaultFilter(line)

        ## return  [ 'TS=("Accipitriformes" AND (swarm OR "collective behavior") ) ' ,
        #       'TS=( "Acinonyx jubatus" AND (swarm OR "collective behavior"   ) '
        # ]
        pass






    def sendPostReq(self):
        ##topicList = yourgetTopicList()
        ## remove next line if yourgetTopicList implemented
        topicList = ['TS=("Accipitriformes" AND (swarm OR "collective behavior") )']
        topic = topicList[0]

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
            "value(input1)": topic,    ##  topic as keyword
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

        req = requests.post(url = POST_URL,
                            params = POST_PARA,
                            headers=WosAdvancedQuerySpider.HEADER)

        status_code = req.status_code
        if status_code != 200:
            ## error handler
            pass

        html = req.text
        ## this response contains search history tab
        ## tab [href == https://apps.webofknowledge.com/summary.do]
        ## summary.do 即改关键词的论文list的 url
        return html




    ##!TODO   assginee: 海大
    ## 按照docs/爬取规则.docx两类（强，弱）每个关键词爬取5篇论文元数据（文章，摘要，exclude 论文pdf）
    ## 形成 强弱excel表格
    ## excel的定义 在docs/爬取规则.docx 第二个tab
    ## def parse(self, html):
        ## your implementation

    ## def ...


