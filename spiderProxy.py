from spider.urlParser import *
from spider.urlMongoDB import *
import yaml
import random

class SpiderProxy():
    url_log = UrlLogger(__name__)
    url_log.file_handler("a.log")
    def __init__(self):
        # self.free_proxy_url = "https://www.xicidaili.com/wn/"
        self.url_proxy = UrlParser()
        self.proxy_mongo = UrlMongoDB("proxy",collection_name="proxy_collection")

    def _get_proxy_from_pool(self):
        proxy_list = self.get_proxy_from_mongodb()
        if len(proxy_list) == 0:
            self.url_log.logger.info("数据库中已无代理，重新抓取.....")
            proxy_list = self.spider_proxy_from_internet()
            self.replace_proxy_to_mongodb(proxy_list)
            proxy_list = self.get_proxy_from_mongodb()
        index = random.randint(0, len(proxy_list) - 1)
        return proxy_list[index]

    def _get_user_agent(self):
        with open("user-agent.yml", "r") as f:
            cont = f.read()
        user_agent_list = yaml.load(cont)
        index = random.randint(0, len(user_agent_list) - 1)
        return user_agent_list[index]

    def spider_proxy_from_internet(self):
        proxy_resource_list = yaml.load(open("proxy-resource.yml"))
        proxy_list = []
        for proxy in proxy_resource_list:
            if proxy["name"] == 'xicidaili':
                proxy_list = proxy_list + self._spider_proxy_from_xicidaili(proxy["url"])
            elif proxy["name"] == 'data5u-gngn' or proxy["name"] == 'data5u-gnpt':
                proxy_list = proxy_list + self.spider_proxy_from_data5u(proxy["url"])
        print(proxy_list)
        return proxy_list

    def _spider_proxy_from_xicidaili(self,url):
        content = self.url_proxy.request_url(url)
        proxy_ip = self.url_proxy.url_parser(content, "//tr/td[2]/text()")
        port = self.url_proxy.url_parser(content, "//tr/td[3]/text()")
        proxy_list = []
        for index in range(len(proxy_ip)):
            proxy_dic = {}
            proxy_dic["ip"] = proxy_ip[index]
            proxy_dic["port"] = port[index]
            proxy_dic["used_count"] = 0
            proxy_list.append(proxy_dic)
        return proxy_list[0:20]

    def spider_proxy_from_data5u(self,url):
        content = self.url_proxy.request_url(url)
        proxy_ip = self.url_proxy.url_parser(content, "//div/ul/li[2]/ul/span[1]/li/text()")
        port = self.url_proxy.url_parser(content, "//div/ul/li[2]/ul/span[2]/li/text()")
        type = self.url_proxy.url_parser(content, "//div/ul/li[2]/ul/span[4]/li/text()")
        proxy_list = []
        for index in range(len(proxy_ip)):
            if type[index].lower() == 'https':
                proxy_dic = {}
                proxy_dic["ip"] = proxy_ip[index]
                proxy_dic["port"] = port[index]
                proxy_dic["used_count"] = 0
                proxy_list.append(proxy_dic)
        # print(proxy_list)
        # print(proxy_ip,port,type)
        return proxy_list

    def _spider_proxy_from_proxydb(self,url):
        content = self.url_proxy.request_url(url)
        print(content)
        proxy_ip = self.url_proxy.url_parser(content, "//table/tbody/tr/td/script/text()")
        # print(proxy_ip)
        return proxy_ip

    def insert_proxy_to_mongodb(self,list):
        self.proxy_mongo.mongo_collection.insert_many(list)

    def replace_proxy_to_mongodb(self,url):
        self.proxy_mongo.mongo_collection.delete_many({})
        self.insert_proxy_to_mongodb(url)

    def delete_data_in_collection(self,query_data):
        self.proxy_mongo.mongo_collection.delete_one(query_data)

    def get_proxy_from_mongodb(self):
        proxy_list = []
        for cursor in self.proxy_mongo.mongo_collection.find({},{"_id":0}):
            proxy_list.append(cursor)
        return proxy_list

    def update_proxy_used_counter(self):
        pass
