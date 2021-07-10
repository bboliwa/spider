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


    def test_doPost(self):
        spider = wosad.WosAdvancedQuerySpider()
        spider.sendPost("TS = (Accipitriformes AND (collective* AND decision*) )")

    def test_clean(self):
        spider = wosad.WosAdvancedQuerySpider()
        spider.sendPostToCleanHistory()

    def test_storePapers(self):
        spider = wosad.WosAdvancedQuerySpider()
        ##test_url = "https://apps.webofknowledge.com/full_record.do?product=UA&search_mode=AdvancedSearch&qid=1&SID=D4VOxBVl2qs1d5Cl2sI&page=1&doc=1&cacheurlFromRightClick=no"
        ##test_url = "https://apps.webofknowledge.com/full_record.do?product=UA&search_mode=AdvancedSearch&qid=17&SID=D4VOxBVl2qs1d5Cl2sI&page=1&doc=1&cacheurlFromRightClick=no"
        ##test_url = "https://apps.webofknowledge.com/full_record.do?product=UA&search_mode=AdvancedSearch&qid=83&SID=7CPPuWtCsANgjCWAltd&page=1&doc=2&locale=en_US"
        test_url = "https://apps.webofknowledge.com/full_record.do?product=UA&search_mode=AdvancedSearch&qid=14&SID=D2BJFqWT84nLBK3lqQx&page=1&doc=1&locale=en_US"

        spider.storePapers ( "Acinonyx jubatus",  [test_url],  True  )






