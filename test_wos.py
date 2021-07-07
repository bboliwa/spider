# -*- coding = utf-8 -*-


import requests
import re
import unittest
import wos_advanced_query_spider as wosad



"""
add unit test for wos_advanced feature
"""
class TestWos(unittest.TestCase):

    def test_doSpider(self):
        spider = wosad.WosAdvancedQuerySpider()
        spider.doSpider()




    def test_storePapers(self):
        spider = wosad.WosAdvancedQuerySpider()
        test_url = "https://apps.webofknowledge.com/full_record.do?locale=en_US&errorKey=&search_mode=AdvancedSearch&qid=38&log_event=no&log_event=yes&product=UA&colName=DIIDW&SID=5BxdZewZT5RVCdTpvsG&recordID=202124406N&viewType=fullRecord&doc=1&page=1"
        spider.storePapers(test_url,1)






