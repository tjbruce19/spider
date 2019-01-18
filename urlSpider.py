from spider.urlParser import UrlParser
from spider.urlLogger import UrlLogger
from spider.spiderProxy import SpiderProxy
from spider.spiderCommon import SpiderCommon
import random
import yaml

class UrlSpider():
    url_log = UrlLogger(__name__)
    url_log.file_handler("a.log")
    def __init__(self):
        self.url_parser = UrlParser()
        self.spider_proxy = SpiderProxy()
        self.spider = SpiderCommon()
        self.main_url = "https://music.163.com"
        self.proxy_dic = self.spider_proxy._get_proxy_from_pool()

    def get_playlist_cat(self):
        """
        spide play-list page
        return dict {type:href} eg.{"华语":"/discover/playlist/?cat=%E5%8D%8E%E8%AF%AD"}
        :return:dict {"华语":"/discover/playlist/?cat=%E5%8D%8E%E8%AF%AD"}
        """
        base_url = "https://music.163.com/discover/playlist/"
        xpath_dic = {"links":"//dd/a/@href", "data_cat":"//dd/a/@data-cat"}
        while True:
            proxy = "http://" + self.proxy_dic["ip"] + ":" + self.proxy_dic["port"]
            headers = {'User-Agent': self.spider_proxy._get_user_agent(), 'Referer': self.main_url + "/"}
            content = self.spider.spider_contents_in_one_page(base_url, xpath_dic,u"歌单类别", proxy=proxy,headers=headers)
            if not content:
                self.spider_proxy.delete_data_in_collection(self.proxy_dic)
                self.proxy_dic = self.spider_proxy._get_proxy_from_pool()
                self.url_log.logger.info("无效代理，更换代理")
                continue
            else:
                break
        links = content[0]
        data_cat = content[1]
        link_mapping = {}
        for index in range(len(links)):
            link_mapping[data_cat[index]] = links[index]
        self.url_log.logger.info("歌单分类爬取完毕。。。。。")
        return link_mapping

    # def get_info_from_playList(self, url_cat, play_info_list=None,**kwargs):
    #     """
    #     spide play-list page by type
    #     return dict, key included(title,author, play-list href, author href)
    #     :param url_cat:各个类别歌单的url
    #     :return: list (eg.[{"title":"我想把夏日的阳光，寄给冬日的你","author":"情思天鹅","play_href":"/playlist?id=2556383692","author_href":""},
    #                         {"title":"我想把夏日的阳光，寄给冬日的你","author":"情思天鹅","play_href":"/playlist?id=2556383692,"author_href":""}])
    #     """
    #     # print(url_cat)
    #     if kwargs is not None and kwargs != {}:
    #         self.url_log.logger.info("开始爬取%s歌单。。。。",kwargs["cat"])
    #     if play_info_list is None:
    #         play_info_list = []
    #     while True:
    #         proxy = "http://" + self.proxy_dic["ip"] + ":" + self.proxy_dic["port"]
    #         headers = {'User-Agent': self.spider_proxy._get_user_agent(), 'Referer': self.main_url + "/"}
    #         content = self.spider.spider_contents_in_one_page(url_cat, xpath_dic, u"歌单类别", proxy=proxy,
    #                                                           headers=headers)
    #         if not content:
    #             self.spider_proxy.delete_data_in_collection(self.proxy_dic)
    #             self.proxy_dic = self._get_proxy_from_pool()
    #             continue
    #         else:
    #             break
    #     # print(content)
    #     title = self.url_parser.url_parser(content, xpath="//li/p[@class='dec']/a/text()")
    #     author = self.url_parser.url_parser(content, xpath="//li/p[last()]/a/@title")
    #     play_href = self.url_parser.url_parser(content, xpath="//li/p[@class='dec']/a/@href")
    #     author_href = self.url_parser.url_parser(content, xpath="//li/p[last()]/a/@href")
    #     # print(title)
    #     # print(author)
    #     # print(href)
    #     for index in range(len(title)):
    #         play_info_dic = {}
    #         play_info_dic["title"] = title[index].encode('utf-8').decode('utf-8')
    #         play_info_dic["author"] = author[index].encode('utf-8').decode('utf-8')
    #         play_info_dic["play_href"] = play_href[index].encode('utf-8').decode('utf-8')
    #         play_info_dic["author_href"] = author_href[index].encode('utf-8').decode('utf-8')
    #         play_info_list.append(play_info_dic)
    #     if self.url_parser.url_parser(content, xpath='//div/div[@class="u-page"]/a[last()]/@class')[0].find("disabled") < 0:
    #         _href = self.url_parser.url_parser(content, xpath='//div[@class="u-page"]/a[last()]/@href')[0]
    #         # print(_href)
    #         play_info_list = self.get_info_from_playList(self.main_url + _href, play_info_list)
    #     # print(play_info_list)
    #     self.url_log.logger.info("歌单爬取完毕。。。。")
    #     return play_info_list
    def get_info_from_playList(self, url_cat,**kwargs):
        """
        spide play-list page by type
        return dict, key included(title,author, play-list href, author href)
        :param url_cat:各个类别歌单的url
        :return: list (eg.[{"title":"我想把夏日的阳光，寄给冬日的你","author":"情思天鹅","play_href":"/playlist?id=2556383692","author_href":""},
                            {"title":"我想把夏日的阳光，寄给冬日的你","author":"情思天鹅","play_href":"/playlist?id=2556383692,"author_href":""}])
        """
        # print(url_cat)
        print(url_cat)
        print(kwargs)
        if kwargs.get("offset"):
            url_cat = url_cat + "&limit=35&offset="+str(kwargs.get("offset"))
        if kwargs is not None and kwargs != {}:
            self.url_log.logger.info("开始爬取%s歌单。。。。",kwargs["cat"])
        play_info_list = []
        xpath_dic = {"title":"//li/p[@class='dec']/a/text()",
                     "author":"//li/p[last()]/a/@title",
                     "play_href":"//li/p[@class='dec']/a/@href",
                     "author_href":"//li/p[last()]/a/@href"}
        while True:
            proxy = "http://" + self.proxy_dic["ip"] + ":" + self.proxy_dic["port"]
            headers = {'User-Agent': self.spider_proxy._get_user_agent(), 'Referer': self.main_url + "/"}
            content = self.spider.spider_contents_in_one_page(url_cat, xpath_dic, kwargs["cat"],kwargs["page"], proxy=proxy,
                                                              headers=headers)
            if not content:
                self.spider_proxy.delete_data_in_collection(self.proxy_dic)
                self.proxy_dic = self.spider_proxy._get_proxy_from_pool()
                continue
            else:
                break
        title = content[0]
        author = content[1]
        play_href = content[2]
        author_href = content[3]
        # print(title)
        # print(author)
        # print(href)
        for index in range(len(title)):
            play_info_dic = {}
            play_info_dic["title"] = title[index].encode('utf-8').decode('utf-8')
            play_info_dic["author"] = author[index].encode('utf-8').decode('utf-8')
            play_info_dic["play_href"] = play_href[index].encode('utf-8').decode('utf-8')
            play_info_dic["author_href"] = author_href[index].encode('utf-8').decode('utf-8')
            play_info_list.append(play_info_dic)
        self.url_log.logger.info("歌单爬取完毕。。。。")
        return play_info_list

    def get_detail_info_from_playList(self, playlist_url):
        """
        spide detail info from playlist(almost favorite,play_count,tag,song_name,singer,album)
        :param url:
        :return:{'favorite': '2467', 'tag': ['流行', '欧美', '90后'], 'play_count': '270583', 'song_list': [{'song_name': '50 Ways to Say Goodbye', 'song_href': '/album?id=2005784', 'singer': 'Train', 'album_name': 'California 37'}]}
        """
        playlist_dic = {}
        xpath_dic = {"favorite":'//div/a[@data-res-action="fav"]/i/text()',
                     "tag":"//div/a[@class='u-tag']/i/text()",
                     "play_count":"//div/strong[@id='play-count']/text()",
                     "song_name":'//ul[@class="f-hide"]/li/a/text()',
                     "song_href":'//ul[@class="f-hide"]/li/a/@href'}
        while True:
            proxy = "http://" + self.proxy_dic["ip"] + ":" + self.proxy_dic["port"]
            headers = {'User-Agent': self.spider_proxy._get_user_agent(), 'Referer': self.main_url + "/"}
            content = self.spider.spider_contents_in_one_page(playlist_url, xpath_dic, "", proxy=proxy,
                                                              headers=headers)
            if not content:
                self.spider_proxy.delete_data_in_collection(self.proxy_dic)
                self.proxy_dic = self.spider_proxy._get_proxy_from_pool()
                continue
            else:
                break
        # print(content)
        favorite = content[0]
        tag = content[1]
        play_count = content[2]
        # print(favorite)
        playlist_dic["favorite"] = favorite[0][1:-1]
        playlist_dic["tag"] = tag
        playlist_dic["play_count"] = play_count[0]
        # print(favorite)
        # print(tag)
        # print(play_count)
        song_name = content[3]
        song_href = content[4]
        # print(song_name)
        # print(song_href)
        playlist_dic["song_list"] = []
        for index in range(len(song_name)):
            songlist_dic = {}
            songlist_dic["song_name"] = song_name[index]
            songlist_dic["song_href"] = song_href[index]
            singer, album_name, album_href = self.get_info_from_song_page(self.main_url+songlist_dic["song_href"])
            songlist_dic["singer"] = singer
            songlist_dic["album_name"] = album_name
            songlist_dic["song_href"] = album_href
            playlist_dic["song_list"].append(songlist_dic)
        # print(playlist_dic)
        return playlist_dic

    def get_info_from_song_page(self, song_url):
        """
        get info from song page
        :param song_url:
        :return:
        """
        xpath_dic = {"singer":'//div[@class="cnt"]/p[1]/span/@title',
                     "album_name":'//div[@class="cnt"]/p[2]/a/text()',
                     "album_href":'//div[@class="cnt"]/p[2]/a/@href'}
        while True:
            proxy = "http://" + self.proxy_dic["ip"] + ":" + self.proxy_dic["port"]
            headers = {'User-Agent': self.spider_proxy._get_user_agent(), 'Referer': self.main_url + "/"}
            content = self.spider.spider_contents_in_one_page(song_url, xpath_dic, "", proxy=proxy,
                                                              headers=headers)
            if not content:
                self.spider_proxy.delete_data_in_collection(self.proxy_dic)
                self.proxy_dic = self.spider_proxy._get_proxy_from_pool()
                continue
            else:
                break
        # print(content)
        singer = content[0]
        album_name = content[1]
        album_href = content[2]
        # print(singer)
        # print(album_href)
        # print(album_name)
        return singer[0], album_name[0], album_href[0]