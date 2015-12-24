# coding=utf8

import json
import requests
from pymongo import MongoClient
import time


def run():
    client = MongoClient()
    db = client.cdec
    db.cdec.drop()

    head = {
        'Host': 'dota2.vpgame.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:42.0) Gecko/20100101 Firefox/42.0',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
        'Accept-Encoding': 'gzip, deflate',
        'X-Requested-With': 'XMLHttpRequest',
        'Referer': 'http://dota2.vpgame.com/league/season/505.html',
        'Cookie': 'VPLang=zh_cn; VPTimeZone=Asia%2FChongqing; Hm_lvt_2e2626841280635cc9322ed4817ffce5=1448277535,1448277571,1448277622,1448461941; Hm_lvt_20c4cdf230856f4a4479a32ec8b13dd6=1448277529; VPSSO=4c5059ba9ed15b7c91228d1bd85d506dd7af041ca%3A4%3A%7Bi%3A0%3Bs%3A7%3A%223957696%22%3Bi%3A1%3Bs%3A11%3A%22pilipala195%22%3Bi%3A2%3Bi%3A518400%3Bi%3A3%3Ba%3A0%3A%7B%7D%7D; VPSessionID=2t1jggph5c47cpk2g4ttvn0kn6; Hm_lpvt_2e2626841280635cc9322ed4817ffce5=1448462040',
        'Connection': 'keep-alive'
    }
    url = 'http://dota2.vpgame.com/api/dota2LeagueMatch-rank.html?pageSize=10&showType=' +\
          'page&type=overview&season_id=589&_=1450924655551&DotaLeagueSeasonMemberStatistics_page=1'
    ht = requests.get(url, headers=head).content
    jsDict = json.loads(ht)
    jsPage = jsDict['page']
    total_page = jsPage['totalPage']+1
    for i in range(1, total_page):
        url = 'http://dota2.vpgame.com/api/dota2LeagueMatch-rank.html?pageSize=10&showType=' +\
              'page&type=overview&season_id=589&_=1450924655551&DotaLeagueSeasonMemberStatistics_page='+str(i)
        ht = requests.get(url, headers=head).content
        jsDict = json.loads(ht)
        jsData = jsDict['data']
        for each in jsData:
            if each['tags']:
                jsTags = each['tags']
                jsId = jsTags[0]
                st = ''
                if jsId['note']:
                    st += jsId['note']+'   '
                    name = jsId['note']
                else:
                    st += each['nickname']+'   '
                    name = each['nickname']
                jsLeague = each['league']
                data_dic = {
                    'name': name,
                    'rank': str(jsLeague['rank']),
                    'score': jsLeague['score'],
                    'wins': jsLeague['wins'],
                    'losses': jsLeague['losses'],
                    'win_rate': str(jsLeague['win_rate']),
                    'kda': jsLeague['avg_kda'],
                    'position': jsLeague['position']
                }
                db.cdec.insert_one(data_dic)
    print 1

while (True):
    run()
    time.sleep(3600)
