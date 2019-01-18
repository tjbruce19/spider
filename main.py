# -*- coding: utf-8 -*-
import os
import sys
import re
from lxml import etree
import csv
import codecs
import wx
from spider.urlSpider import *
from spider.dataStorage import *
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from spider.urlMongoDB import *
from spider.urlParser import *
from spider.spiderProxy import *
from spider.urlLogger import UrlLogger
import random
import yaml
import os
import js2xml
import asyncio
import threading
from queue import Queue
from spider.myQueue import Worker,ThreadQueue
import time


spider = UrlSpider()

def spider_playlist_thread(url_cat,**kwargs):
    q = Queue()
    threads = []
    def put_in_queue(i):
        play_list = spider.get_info_from_playList(url_cat,cat=kwargs["cat"],page=str(i*35)+"-"+str((i+1)*35),offset=i*35)
        q.put(play_list)
    for i in range(3):
        t = threading.Thread(target=put_in_queue,args=(i,))
        t.start()
        threads.append(t)
    for t in threads:
        t.join()
    results = []
    for _ in range(3):
        results = results + q.get()
    return results

def spider_playlist_thread_queue(url_cat,**kwargs):
    results = []
    q_thread = Queue()
    for i in range(38):
        # q_thread.put((spider.get_info_from_playList,(url_cat,{"cat":kwargs["cat"]},{"page":str(i*35)+"-"+str((i+1)*35)},{"offset":i*35})))
        q_thread.put((spider.get_info_from_playList, (
        url_cat,),{"cat": kwargs["cat"], "page": str(i * 35) + "-" + str((i + 1) * 35), "offset": i * 35}))
        # q_thread.put((spider.get_info_from_playList,(url_cat,)))
    for j in range(3):
        Worker(q_thread)
    q_thread.join()
    for n in range(Worker.res_queue.qsize()):
        results = results + Worker.res_queue.get()


def main():
    # 歌单所属类别的href
    mongo_cat_col = DataStorage("163music", "playlist_category")
    # link_map = spider.get_playlist_cat()
    # print(link_map)
    # mongo_cat_col.replace_to_mongo(link_map)
    cat_dic = mongo_cat_col.find_one_data({})
    print(cat_dic)
    for _key, _value in cat_dic.items():
        # print(_key,_value)
        # play_list = spider.get_info_from_playList(spider.main_url + _value,cat=_key,offset=0)
        play_list = spider_playlist_thread(spider.main_url + _value,cat=_key)
        print(play_list)
        mongo_playlist_col = DataStorage("163music", _key)
        for _dic in play_list:
            mongo_playlist_col.update_or_insert_one_to_mongo(_dic, {"title": _dic["title"], 'author': _dic["author"]})

    # for _key, _value in cat_dic.items():
    #     mongo_playlist_col = DataStorage("163music", _key)
    #     for play_list in mongo_playlist_col.find_data({}):
    #         playlist_info_dic = spider.get_detail_info_from_playList(spider.main_url + play_list["play_href"])
    #         mongo_playlist_col.update_or_insert_one_to_mongo(playlist_info_dic, {"title": play_list["title"], 'author': play_list["author"]})

def add(a,b,*args,**kwargs):
    print("======123========")
    print(a)
    print(args)
    print(kwargs)
    print("======321=======")
    return a+b

def test():
    spider = UrlSpider()
    url_parser = UrlParser()
    spider_proxy = SpiderProxy()
    # spider_proxy.test()
    # spider.test()
    url_parser.test()
    # spider_playlist_thread_queue("http://123123",cat="huayu")
    thread_q = ThreadQueue()
    url_cat = "11111"
    kwargs = {}
    kwargs["cat"] = "huayu"
    func_list = []
    args_list = []
    kwargs_list = []
    for n in range(3):
        # func_list.append(spider.add)
        # args_list.append((n,))
        # kwargs_list.append({"b":n+1})

        func_list.append(spider.get_info_from_playList)
        args_list.append((url_cat,))
        kwargs_list.append({"cat": kwargs["cat"], "page": str(n * 35) + "-" + str((n + 1) * 35), "offset": n * 35})
    thread_q.concurrency_func_with_thread_queue(func_list,args_list,kwargs_list,1)
    print(Worker.res_queue.qsize())


    # url_log = UrlLogger(__name__)
    # url_log.file_handler("test.log")
    # url_log.logger.info("123123")

    # a = yaml.load(open("proxy-resource.yml"))
    # print(a)
    # mongo_playlist_col = DataStorage("163music", "华语")
    # # data_list = mongo_playlist_col.find_data({})
    # for play_list in mongo_playlist_col.find_data({}):
    #     print(play_list)
    #     playlist_info_dic = spider.get_detail_info_from_playList(spider.main_url + play_list["play_href"])
    #     print(playlist_info_dic)
    #     mongo_playlist_col.update_or_insert_one_to_mongo(playlist_info_dic,
    #                                                      {"title": play_list["title"], 'author': play_list["author"]})
    #     break






if __name__ == "__main__":
    # main()
    test()





