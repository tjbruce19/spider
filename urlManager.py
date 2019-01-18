# -*- coding: utf-8 -*-
class UrlManager():

    def __init__(self):

        pass

    def insert_url(self, url, url_list):
        """
        insert a url to list
        :param url:
        :param url_list:
        :return:
        """
        if isinstance(url, list):
            for _url in url:
                url_list.append(_url)
        elif isinstance(url, str):
            url_list.append(url)
        else:
            print("Parameter of url's type is incorrect, should be list or string")
        return url_list

    def pop_url(self,url_list):
        """
        pop a url from list to spide
        :param url_list:
        :return:
        """


    def log_url_spide(self):
        """
        log url which have spided
        :return: list
        """
        pass