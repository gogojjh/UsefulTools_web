# coding=utf8

import requests
from lxml import etree
from pymongo import MongoClient
import time


def run():
    client = MongoClient()
    db = client.movieinfo
    db.movieinfo.drop()

    url = 'http://movie.douban.com/'
    head = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:42.0) Gecko/20100101 Firefox/42.0'}
    html = requests.get(url, headers=head).content
    selector = etree.HTML(html)
    movie_url = selector.xpath('//li [@class="poster"]/a/@href')
    rating = selector.xpath('//li [@class="rating"]/span/text()')

    for i in range(0, len(movie_url)):
        for j in range(i+1, len(movie_url)):
            if rating[i] < rating[j]:
                temp = rating[i]
                rating[i] = rating[j]
                rating[j] = temp
                temp = movie_url[i]
                movie_url[i] = movie_url[j]
                movie_url[j] = temp
    for i in range(0, len(movie_url)):
        if rating[i] != u'暂无评分':
            movie_html = requests.get(movie_url[i], headers=head).content
            selector = etree.HTML(movie_html)
            movie_title = selector.xpath('//span [@property="v:itemreviewed"]/text()')[0]
            print movie_title
            movie_rating = rating[i]
            movie_people = selector.xpath('//span [@property="v:votes"]/text()')[0]
            movie_summary = selector.xpath('//span [@property="v:summary"]/text()')[0]
            movie_award = selector.xpath('//ul [@class="award"]/li/text()')
            movie_comments = selector.xpath('//p [@class=""]/text()')
            movie_compeople = selector.xpath('//span [@class="votes pr5"]/text()')
            movie_info = {
                'name': movie_title,
                'rating': movie_rating,
                'comment1': movie_comments[0]
            }
            db.movieinfo.insert_one(movie_info)

while (True):
    run()
    time.sleep(3600)

