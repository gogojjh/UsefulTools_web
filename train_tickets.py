# coding=utf-8

import json
import requests
import urllib2
import re


def train(p):
    fp = open('./static/city_station.txt', 'r')
    t = fp.read()
    q = t.split('@')
    fp.close()
    sta_name_gbk = []
    sta_code = []
    sta_name = []
    for i in range(1, 2098):
        sta_info = q[i].split('|')
        sta_name_gbk.append(sta_info[1])
        sta_code.append(sta_info[2])
    for each in sta_name_gbk:
        sta_name.append(each.decode('utf8'))
    LC = p['1'].encode('utf-8')
    DC = p['2'].encode('utf-8')
    Date = p['3']
    ETime = p['4'][0:5]
    LTime = p['4'][7:12]
    TYPE = p['5']
    lc_code = ''
    dc_code = ''
    for i in range(1, 2097):
        sta_code[i] = sta_code[i].encode('utf-8')
        sta_name[i] = sta_name[i].encode('utf-8')
    for i in range(1, 2097):
        if LC == sta_name[i]:
            lc_code = sta_code[i]
        if DC == sta_name[i]:
            dc_code = sta_code[i]
    if not lc_code:
        lc = LC[0:-3]
        for i in range(1, 2097):
            if lc == sta_name[i]:
                lc_code = sta_code[i]
    if not dc_code:
        dc = DC[0:-3]
        for i in range(1, 2097):
            if dc == sta_name[i]:
                dc_code = sta_code[i]
    head = {
        'Host': 'kyfw.12306.cn',
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:31.0) Gecko/20100101 Firefox/31.0',
        'Accept': '*/*',
        'Accept-Language': 'zh-cn,zh;q=0.8,en-us;q=0.5,en;q=0.3',
        'Accept-Encoding': 'gzip, deflate',
        'If-Modified-Since': '0',
        'Cache-Control': 'no-cache',
        'X-Requested-With': 'XMLHttpRequest',
        'Referer': 'https://kyfw.12306.cn/otn/leftTicket/init',
        'Cookie': 'JSESSIONID=0A01D967FCFDA6C9B963F8AE575B642AE37ECF6864; __NRF=86A7CBA739653C1CC2C3C3AA7C88A1E3; BIGipServerotn=1742274826.64545.0000; _jc_save_fromStation=%u4E0A%u6D77%2CSHH; _jc_save_toStation=%u5317%u4EAC%2CBJP; _jc_save_fromDate=2015-12-12; _jc_save_toDate=2015-12-10; _jc_save_wfdc_flag=dc',
        'Connection': 'keep-alive'
    }
    lc_code = lc_code.encode('utf-8')
    dc_code = dc_code.encode('utf-8')
    Date = Date.encode('utf-8')
    url = 'http://www.12306.cn/opn/lcxxcx/query?purpose_codes=ADULT&queryDate='+Date+'&from_station='+lc_code+'&to_station='+dc_code
    jscontent = requests.get(url, headers=head).content
    jsDict = json.loads(jscontent)
    jsData = jsDict['data']
    TrainInfo = jsData['datas']
    train_info = []
    for e in TrainInfo:
        if (LC in e['from_station_name'].encode('utf-8')) & (DC in e['to_station_name'].encode('utf-8')):
            if ETime <= e['start_time']:
                if LTime >= e['start_time']:
                    if TYPE == '0':
                        train_info.append(e)
                    elif TYPE == '1':
                        if (e['station_train_code'][0:1] == 'G') or (e['station_train_code'][0:1] == 'D'):
                            train_info.append(e)
                    elif TYPE == '2':
                        if (e['station_train_code'][0:1] != 'G') and (e['station_train_code'][0:1] != 'D'):
                            train_info.append(e)
    return train_info



