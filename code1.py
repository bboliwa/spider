# -*- coding: utf-8 -*-

"""
用 wos 高级检索，用 TS="" 检索关键字
"""

import re
import xlrd
import xlwt
import requests

SID = "C1C8C5dmaXvfryp8Uhx"
url = "http://apps.webofknowledge.com/WOS_AdvancedSearch_input.do;jsessionid=6652E1D41DBE64AA3D01391830A102CC?product=WOS&search_mode=AdvancedSearch&replaceSetId=&goToPageLoc=SearchHistoryTableBanner&SID=C1C8C5dmaXvfryp8Uhx&errorQid=704#SearchHistoryTableBanner"
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
    "search_mode": "GeneralSearch",
    "SID": SID}

"""
    !TODO assginee: 海大
    根据爬取规则.doc
    完成 Filter1，Filter2 对应爬取规则.doc完相关， 部分相关
    完成 yourgetTopicList1，yourgetTopicList2 对应完全相关， 部分相关
    代码可以重构，
"""

# def yourFilter2(str):
#     return (str + ' AND (swarm* OR collective*) AND ("Artificial intelligence" OR decision* OR multipurpose OR coordination OR algorithm OR UAV OR bionics* OR *model OR *robotics) AND (*drone* OR kilobot OR self-organizing OR "task allocation" OR decentralized OR flock* OR motion* OR PRM OR *state OR inspired* OR Vicsek OR Couzin OR multi-robot OR SPPs OR "probabilistic roadmap" OR "decentralized"))')

def yourFilter(str):
    return (str + ' AND (swarm OR "collective behavior")')

# def yourgetTopicList2(file_address):
#     fs = xlrd.open_workbook(file_address)
#     sheet1 = fs.sheet_by_index(0)
#     i = 0
#     list = []
#     while i < sheet1.nrows:
#         list.append("TS = (" + yourFilter(str(sheet1.row_values(i)[0])) + ")")
#         i += 1
#     return list

def yourgetTopicList(file_address):
    fs = xlrd.open_workbook(file_address)
    sheet1 = fs.sheet_by_index(0)
    i = 0
    list = []
    while i<sheet1.nrows:
        list.append("TS = (" + yourFilter(str(sheet1.row_values(i)[0])) + ")")
        i += 1
    return list

def sendPostReq(url):
    from_data = {
        "product": "WOS",
        "input_invalid_notice": "检索错误: 请输入检索词。",
        "input_invalid_notice_limits: ": "<br/>注意: 滚动框中显示的字段必须至少与一个其他检索字段相组配。",
        "SID": SID,
        "action": "search",
        "replaceSetId:": "",
        "goToPageLoc": "SearchHistoryTableBanner",
        "value(input1)": "TS = (cow pectoralis AND (collective* AND decision*))",
        "value(searchOp)": "search",
        "value(select2)": "LA",
        "value(input2)": "",
        "value(select3)": "DT",
        "value(input3)": "",
        "value(limitCount)": "14",
        "limitStatus": "expanded",
        "ss_lemmatization": "on",
        "ss_spellchecking": "Suggest",
        "SinceLastVisit_UTC": "",
        "SinceLastVisit_DATE": "",
        "period": "Range Selection",
        "range": "ALL",
        "startYear": "1965",
        "endYear": "2021",
        "editions": "SCI",
        "editions": "SSCI",
        "editions": "AHCI",
        "editions": "ISTP",
        "editions": "ISSHP",
        "editions": "BSCI",
        "editions": "BHCI",
        "editions": "ESCI",
        "update_back2search_link_param": "yes",
        "ss_query_language": "",
        "rs_sort_by": "PY.D;LD.D;SO.A;VL.D;PG.A;AU.A"}
    req_1 = requests.post(url, data=from_data, headers=headers)
    html_1 = req_1.text
    print(html_1)
    find_jsessionid = re.compile(r'.do;(.*?)?search_mode=')
    a = re.findall(find_jsessionid, html_1)
    url = "http://apps.webofknowledge.com/summary.do;" + a[0] + "product=WOS&doc=1&qid=708&SID=C1C8C5dmaXvfryp8Uhx&search_mode=AdvancedSearch&update_back2search_link_param=yes"
    req_2 = requests.get(url, headers=headers, params=params)
    html_2 = req_2.text
    find_sid = re.compile(r'SID=(.*?)&')
    b = re.findall(find_sid, html_2)
    sid = "http://apps.webofknowledge.com/full_record.do?product=WOS&search_mode=AdvancedSearch&qid=708&SID=" + b[0] + "&page=1&doc="
    find_count = re.compile(r'FINAL_DISPLAY_RESULTS_COUNT = (.*?);</script>')
    c = re.findall(find_count, html_2)
    storePapers(sid, int(c[0]))

def storePapers(link, count):
    book = xlwt.Workbook(encoding='utf-8')
    sheet = book.add_sheet('date', cell_overwrite_ok=True)
    i = 1
    if count<=5:
        total = count
    else:
        total = 5
    while i<=total:
        url = link + str(i)
        req = requests.get(url, headers=headers, params=params)
        html = req.text
        findTitle = re.compile(r'<input type="hidden" name="00N70000002BdnX" value="(.*?)"/>')
        a = re.findall(findTitle, html)
        title = a[0]
        findAuthor = re.compile(r'alt="查找此作者的更多记录">(.*?)</a>(.*?)<sup><b>')
        b = re.findall(findAuthor, html)
        j = 0
        author = ""
        for k in b:
            author += k[0]
            author += k[1]
            j += 1
            if j == len(b):
                continue
            author += ';'
        findAbstract = re.compile(r'<p class="FR_field">(.*?)</p>')
        c = re.findall(findAbstract, html)
        if len(c):
            abstract = c[0]
            abstract = abstract.replace("<span class=\"hitHilite\">", "")
            abstract = abstract.replace("</span>", "")
        else:
            abstract = ''
        store = title + "/          /" + author + "/          /" + abstract
        sheet.write(0, i, store)
        i += 1
    book.save(r'C:\Users\蒋川宇\Desktop\123.xls')

sendPostReq(url)