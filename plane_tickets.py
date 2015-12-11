# coding=utf-8

import requests
import json


def plane(p):
    head = {
        'Host': 'www.tuniu.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:42.0) Gecko/20100101 Firefox/42.0',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
        'Accept-Encoding': 'gzip, deflate',
        'X-Requested-With': 'XMLHttpRequest',
        'Cookie': '__utma=1.912680409.1447606328.1448807946.1449547048.9; __utmz=1.1448807946.8.6.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; Hm_lvt_51d49a7cda10d5dd86537755f081cc02=1448418895,1448429213,1448807946,1449547049; _tact=MWMxZjYwY2MtMzczNy0yZTY3LWY0YmItZjU0OThhZDhkYThj; _tacz2=taccsr%3Dwww.baidu.com%7Ctacccn%3D%28referral%29%7Ctaccmd%3D%28none%29%7Ctaccct%3D%28none%29%7Ctaccrt%3D%28none%29; _taca=1447606327678.1448807945567.1449547048365.10; MOBILE_APP_SETTING_STATE=CLOSE; tuniu_channel=MTAwLDAsZDdiY2U0NTViYjViMDFhNWExYzk1YTM2ZjZiNDEyY2Q%3D; air_departCityName=5p2t5bee; air_destCityName=6L+Q5Z+O; air_departCityCode=MzQwMg==; air_destCityCode=MjYxMw==; tuniu_partner=MTAwLDAsLDI2OWJhMjJhNDAxOWQyNDRjYzNkMGU4ODZkMjQ1NGFk; p_phone_400=4007-999-999; tuniuuser_citycode=MzQwMg%3D%3D; SERVERID=dnionC; __utmb=1.3.10.1449547048; __utmc=1; MOBILE_APP_SETTING_OPEN=1; Hm_lpvt_51d49a7cda10d5dd86537755f081cc02=1449547265; OLBSESSID=jb60ba8qaa4femb7tm269g44o6; _tacau=MCw2Yjc2MmQ0Mi1iMWU5LTUxOGQtMzM4YS0xZjE1NGZlMzc4NWIs; _tacb=MmFiYTE0YjktZWE0ZC05NTViLWVhOGUtZjI5ZmJmZGI0MTBm; _tacc=1',
        'Connection': 'keep-alive'
    }
    # fp = open('/home/UsefulTools/UsefulTools_web/static/city_airport.txt', 'r')
    fp = open('./static/city_airport.txt', 'r')
    st = fp.read()
    city = st.split('|')
    i = 0
    cityName = []
    cityCode = []
    for j in range(0, 213):
        cityName.append(city[i])
        i += 1
        cityCode.append(city[i])
        i += 1
    fp.close()

    LC = p['1'].encode('utf-8')
    DC = p['2'].encode('utf-8')
    Date = p['3'].encode('utf-8')
    for i in range(0, 213):
        if LC == cityName[i]:
            lc_id = cityCode[i]
        if DC == cityName[i]:
            dc_id = cityCode[i]
    url = 'http://www.tuniu.com/yii.php?r=airticket/ticketList/QueryTickets&singleOrPkgTrip=1&orgCityCode='+lc_id \
          +'&dstCityCode='+dc_id+'&departureDate='+Date
    jscontent = requests.get(url, headers=head).content
    if jscontent != '':
        jsDict = json.loads(jscontent)
        jsData = jsDict['data']
        if jsData:
            jsList = jsData['list']
            return jsList
        else:
            jsList = {}
            return jsList
