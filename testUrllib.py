# -*- coding = utf-8 -*-
# @Time : 2021/7/4 10:38
# @Author : ChuanYu
# @File : testUrllib.py
# @Software PyCharm

import requests
import re
from bs4 import BeautifulSoup

url = "http://apps.webofknowledge.com/full_record.do?product=WOS&search_mode=GeneralSearch&qid=1&SID=D35u57dAGH7fDjXW1Sy&page=1&doc=1"
headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Cache-Control": "max-age=0",
            "Connection": "keep-alive",
            "Cookie": "_gcl_au=1.1.545216862.1625395117; _hjid=ed9da7e2-b787-4791-974a-712d772748f1; ak_bmsc=226FE290EC27F3A8037C4E2C58F4CD2A~000000000000000000000000000000~YAAQbIFtaFHDLnV6AQAAJuVBdgwF2X4Cyu68RuiCBtYuPxd1Q9fBikqLgC7UZb4xhw5DZ28+IdA2TAfngvX1AU2tJRqGZT6b4SDSc9S9ENdVpii9LK19PBSBCLAJw13LcqA4vYyQ5UcEM0kIsN+qLEqR7AaE6oH4tu44mP5nI4BuXakSacDv3dRPfZD3f2UuJkhiuTcY681p7o53WTlZLs/4tbTpBNRoQ5ackVmgka85IF+SoJFgSvMvH6FFeQb25ANNzsrT5Y6zqrmC1Tf+lm7s5VpRnR1oycyS3e+ZmaEHr3sB0UeaVvhPJvXI0QOrVDs+MYYlSvnGfzEL3g==; _sp_ses.630e=*; _hjAbsoluteSessionInProgress=0; dotmatics.elementalKey=SLsLWlMhrHnTjDerSrlG; _hjTLDTest=1; _abck=D175EF2F31DD891456228246BF74C491~-1~YAAQtazbF70D9Th6AQAABEtFdgb668ALkxiUUQcmmSVNhNq+TSWa4SfnlUfqsMVv1rDFC6eqrjEGIcrpetW3KFZvOyKXUO6pbzTV5NLz0m6yXEyy4bqC1qWI0WkAWaIQ8WsbYi47twhvmLz/WtPysuzRyWA+uSBC1lbzy2enIWDBJi0CJLEd3F2O+vogoPq0eWH0qHwo91o8xo5ZNuw5JRAsN60AXrVj6cGJL07h+pX7tEpIoeZOcwzaZkh3rFSD6IQstEv41GVO/sAgGQMM6P5EvGv3aZzfmyfSFeG5RwClkoCOpq9RP8zpVGLUaeJfgAen6On2UeDCFgUfJjVQjDfj1AP5WFp21kbavjceiwbgKkEohBQV2m0CO45q~-1~-1~-1; JSESSIONID=AC1FDA18769395D1CA7D4658E6315FD4; _sp_id.630e=714a74d5-27b0-42be-9040-0b23dc3e17f3.1625395117.9.1625481912.1625460207.dacc10c9-4487-42f2-985b-9cf781fbe4c5; bm_sv=266129EEC0D3B0E6A65CEC40890813D7~YY9FOr1+RqaENqXOvVMWkC9uSmhJc8yhlfJqOwdEMyCYVBebV7Q3WwUiMBN+livccCNl9E9YxBWDsamK4nzSWcdRuAJnGEFICH+n1ePBbb7l7JOgmkX5wLz/28art6LSSneZ449XAwuo2aYyeOBDdfeus16G1LpOEgrI4o6+gZg=; bm_sz=B2D36A3498EACF6F24F212CDD38BEF0A~YAAQtazbF3YE9Th6AQAA2JtFdgygO64CdtRDgctSZVKzIqoPLT/dx7Y8dXMZMTWpTbKqBBGD5hzTwtpAGVyBvwJzVaHlYHhCi4I4SfZGEDNYKFDmEYslxS0ANIJP8GFnrKbII7sdNpE6hB5CxE7f0+Of6PHeN5dWbKgk+TtuaoV1/aRewTyDBDKg0LdPy7uKJtMOoFBwU3peZAjc9g==; RT=\"z=1&dm=webofknowledge.com&si=e6370cf5-f2dc-45ab-bad7-9b85c94e1972&ss=kqqhtnsj&sl=4&tt=tvu&bcn=%2F%2F684fc536.akstat.io%2F&ld=4ya8&ul=5117\"",
            "Host": "apps.webofknowledge.com",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.106 Safari/537.36"}
params = {
            "product": "WOS",
            "SID": "D35u57dAGH7fDjXW1Sy",
            "search_mode": "GeneralSearch",
            "prID": "24c13da7-2dd2-43cf-af16-0954e2ec2c1e"}

req = requests.get(url, headers=headers, params=params)
html = req.text
bs = BeautifulSoup(html, "html.parser")
# 获取文章标题
findTitle = re.compile(r'<input type="hidden" name="00N70000002BdnX" value="(.*?)"/>')
a = re.findall(findTitle, html)
title = a[0]
print("标题：", title)
# 获取文章作者
findAuthor = re.compile(r'alt="查找此作者的更多记录">(.*?)</a>(.*?)<sup><b>')
b = re.findall(findAuthor, html)
i = 0
author = ""
for j in b:
    author += j[0]
    author += j[1]
    i += 1
    if i==len(b):
        continue
    author += ','
print("作者：", author)
# 获取文章摘要
findAbstract = re.compile(r'<p class="FR_field">(.*?)</p>')
c = re.findall(findAbstract, html)
abstract = c[0]
print("摘要：", abstract)
f = open(r'C:\Users\蒋川宇\Desktop\123.txt', 'w')
print(title, file=f)
print(author, file=f)
print(abstract, file=f)
f.close()