#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import platform
import re
import sys
import time
import urllib
import execjs
import requests
from lxml import html

#from . import spellcheck

try:
    import vlc
except ImportError:
    pass
except OSError:
    pass  # `pip install python-vlc` needed

try:
    import pyttsx3
except ImportError:
    pass

#有道翻译
def translateYoudao(source):
    #print("=" * 49)
    print("正在翻译 ：" + source + " ...")
    #print()
    strTasnslate = ""

    #######################
    #     Parse Text      #
    #######################
    source = urllib.parse.quote(source)
    url = "https://youdao.com/result?word={}&lang=en".format(source)
    page = requests.get(url)
    print(page.text)
    tree = html.fromstring(page.text)

    xpath = '//div[@id="catalogue_author"]//li[@class="word-exp-ce mcols-layout"]'
    results = tree.xpath(xpath)
    # Print 有道翻译 for word
    if results:
        #print("有道翻译")
        #print("-"*49)
        strTasnslate = str(results[0].xpath('./div/div/div/a/text()')[0]);
        #for el in results:
        #    print(' '.join(el.xpath('./div/div/div/a/text()')))
        #print()

    xpath = '//div[@id="catalogue_paraphrasing"]//li[@class="mcols-layout"]'
    results = tree.xpath(xpath)
    # Print 网络翻译 for word
    if results:
        #print("网络翻译")
        #print("-"*49)
        strTasnslate = str(results[0].xpath('./div//text()')[1]).strip();
        #for el in results:
        #    print(' '.join(el.xpath('./div//text()')))
        #print()
        
    xpath = '//div[@id="catalogue_author"]//div[@class="fanyi dict-module"]'
    results = tree.xpath(xpath)
    # Print 翻译 for word
    if results:
        #print("普通翻译")
        #print("-"*49)
        #for el in results:
        #    print(' | '.join(el.xpath('./div/p[@class="trans-content"]/text()')))

        strTasnslate = str(results[0].xpath('./div/p[@class="trans-content"]/text()')[0]).strip()
        #print()

    #print("=" * 49)
   
    print( "翻译结果 ：" + strTasnslate)
    return strTasnslate


#百度翻译
def translateBaidu(source):
    strTasnslate = ""

    #######################
    #     Parse Text      #
    #######################
   
    headers = {
    'Accept': '*/*',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Connection': 'keep-alive',
    'Content-Length': '136',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Host': 'fanyi.baidu.com',
    'Origin': 'https://fanyi.baidu.com',
    'Referer': 'https://fanyi.baidu.com/?aldtype=16047',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="98", "Google Chrome";v="98"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'X-Requested-With': 'XMLHttpRequest',
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36 Core/1.94.202.400 QQBrowser/11.9.5355.400",
    "Cookie": "BIDUPSID=9D8F27DF4616646ECCE5CF1A39729450; PSTM=1691550591; BAIDUID=9D8F27DF4616646E2786A701B1D959AA:FG=1; REALTIME_TRANS_SWITCH=1; HISTORY_SWITCH=1; FANYI_WORD_SWITCH=1; SOUND_SPD_SWITCH=1; SOUND_PREFER_SWITCH=1; BDUSS=Nkem9NMTJsS2xZWEY0LTBxeEVFbnp2ZlQtclgzY09nNlpiLXNpcG42YUZjeXRsSVFBQUFBJCQAAAAAAAAAAAEAAACin-1E0KHH4LrNMjAxNAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAIXmA2WF5gNlM2; BDUSS_BFESS=Nkem9NMTJsS2xZWEY0LTBxeEVFbnp2ZlQtclgzY09nNlpiLXNpcG42YUZjeXRsSVFBQUFBJCQAAAAAAAAAAAEAAACin-1E0KHH4LrNMjAxNAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAIXmA2WF5gNlM2; APPGUIDE_10_6_7=1; APPGUIDE_10_6_9=1; MCITY=-340%3A; H_WISE_SIDS=39944_39939_39996_40008_40016_40042; H_WISE_SIDS_BFESS=39944_39939_39996_40008_40016_40042; Hm_lvt_64ecd82404c51e03dc91cb9e8c025574=1703659353,1703759557,1703836840; H_PS_PSSID=39939_39996_40008_40016_40042_40072; BDORZ=FFFB88E999055A3F8A630C64834BD6D0; PSINO=6; ZFY=ALzSkBnk8o:A:AdZNg:AbHslXay6703JEstu3qA:BUhG5WQ:C; BAIDUID_BFESS=9D8F27DF4616646E2786A701B1D959AA:FG=1; delPer=0; BDRCVFR[S_ukKV6dOkf]=mk3SLVN4HKm; BDRCVFR[dG2JNJb_ajR]=mk3SLVN4HKm; BDRCVFR[-pGxjrCMryR]=mk3SLVN4HKm; __bid_n=18ba82fc4389824a9c168a; Hm_lpvt_64ecd82404c51e03dc91cb9e8c025574=1704244945; ab_sr=1.0.1_YTU0NWM5ZjRiYzk3M2FjZTljYjZjMDUyOTdjMmI5NDRiY2E1ZGEyOWNmODMyODM4MmRlYjgzMDE0OWNlODU3Y2VlNjJkODA5OGI0N2U5M2Y5Nzc5MmU5NTEyYjEzM2ZiYTcyMWFhOGFjMzEyN2UwYjQ5NzhmYjgwNTFjMGEwNDBmODI4ZjRlNDJlNmI0OTE5ZjM3MDk4NmYwOTBmNDk3MzM4M2RlN2Q0Y2E3MTFjZmI1Zjk0ZDE0ZTBhZTBhM2Zh",
    "Acs-Token": "1704193663872_1704243581514_rXFUFRBo/EBNAGpSPFCixwkFWY52PhKpdsY/PAJeWYRh85HYVgyeJUWm1WuqV7zNi/0qsdXEh6kbeCZNOHb1hxZCtO13RSVGkdmeT910h3bGV8vaDnq0MyE4ZywW6zqDDlCK888DzMveKS/gpvWMmYcyr3pWTIEXQSXDpgMAbkcsLeYX4eT9Ang4/42s21nROHzALHDMRo7+vdivJFavZlxyaeT17QTuGD487h7wakX8Ke8BePhWhM6MtXSY4Pwp8Ot6vndJeVjYs9MB1MZhtiGDDxJeTdloNQLeLLcSWrJq7hVzIKVd7HMmJl15Bqv6NimPWASf5NGm+IgJR+fGPVCvLpRSMkCHPfpqiiAlf7oB4APfFQYbWTDFBIaETQOZa0cdN2n1gvgb0+3DcLVbc0StJg+yKCFcI0xI27LhqZEkn7THcfG120k6mTUE2w4+0VS9w64R+zg9OBVhlQLlUqZmmdCSlVe4pMgEr4pzbDc4SM1RONrCNNCxNYZrrZEvjmaNkuT0NDFggqVUB/SsdA=="
    }
    url = "https://fanyi.baidu.com/v2transapi"
    
    #读取js文件并调用函数生成sign
    with open("./tool/BaiduFanyi.js", "r", encoding="utf-8") as f:
        ctx = execjs.compile(f.read())
        sign = ctx.call("e", source)
    
    data = {
    "query": source,
    "simple_means_flag": 3,
    "sign": sign,
    "token": "fc5204fbffe251714c1a98123dc302df",
    "domain": "common",
    "from": "zh",
    "to": "en",
    "ts": "1704243581493",
    }

    response = requests.post(url, data=data, headers=headers)
    dic_obj = response.json()

    strTasnslate = dic_obj["trans_result"]["data"][0]["dst"]
    return strTasnslate