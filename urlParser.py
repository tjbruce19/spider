# -*- coding: utf-8 -*-
import requests
from lxml import etree
import requests.exceptions as reEx
from spider.urlLogger import UrlLogger

class UrlParser(object):
    url_log = UrlLogger(__name__)
    url_log.file_handler("a.log")
    def __init__(self):
        self.session = requests.Session()

        # self.url_log.file_handler("a.log")
        # print(self.url_log.logger.hasHandlers())


    def url_parser(self, content, xpath):
        tree = etree.HTML(content)
        datas = tree.xpath(xpath)
        return datas

    def request_url(self,url,proxy=None,headers=None):
        if proxy is not None:
            # print(1111)
            self.proxy = {"https": proxy}
            self.session.proxies = self.proxy
        if headers is None:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
                'Referer': 'http://music.163.com/'}

        self.session.headers = headers
        try:
            r = self.session.get(url,timeout=60)
        except reEx.ConnectionError:
            self.url_log.logger.info("抓取(%s)连接失败，更换代理重新抓取....",url)
            return False
        except reEx.ReadTimeout:
            self.url_log.logger.info("抓取(%s)超时，更换代理重新抓取....",url)
            return False
        except Exception:
            self.url_log.logger.info("抓取(%s)未知异常，重新抓取....", url)
            return False
        # print(r.status_code)
        r.encoding = 'utf-8'
        content = r.text
        return  content
    def test(self):
        self.url_log.logger.info("test log")