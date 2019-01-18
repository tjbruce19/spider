from spider.urlParser import UrlParser
from spider.urlLogger import UrlLogger
from spider.spiderProxy import SpiderProxy
import random
import yaml

class SpiderCommon():
    url_log = UrlLogger(__name__)
    url_log.file_handler("a.log")
    def __init__(self):
        self.url_parser = UrlParser()
        self.spider_proxy = SpiderProxy()
        self.main_url = "https://music.163.com"
        self.proxy_dic = self.spider_proxy._get_proxy_from_pool()

    def spider_contents_in_one_page(self,base_url,xpath_dic,*args,**kwargs):
        if not isinstance(xpath_dic,dict):
            self.url_log.logger.exception("参数xpath_dic类型错误",exc_info=True)
        proxy = kwargs.get("proxy")
        headers = kwargs.get("headers")
        spider_cont = []
        content = self.url_parser.request_url(base_url, proxy=proxy, headers=headers)
        if not content:
            return content
        for xpath_key,xpath_value in xpath_dic.items():
            spider_cont.append(self.url_parser.url_parser(content, xpath=xpath_value))
        self.url_log.logger.info("页面(%s)爬取完毕。。。。。",args)
        return spider_cont