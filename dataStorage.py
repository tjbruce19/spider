# -*- coding: utf-8 -*-
import csv
import codecs
from spider.urlMongoDB import UrlMongoDB

class DataStorage():
    def __init__(self,db_name,collection_name=None,server_ip=None,port=None):
        if server_ip is None:
            server_ip = "localhost"
        if port is None:
            port = "27017"
        self.server_ip = server_ip
        self.port = port
        if collection_name is None:
            self.mongo_db = UrlMongoDB(db_name=db_name, server_ip=self.server_ip, port=self.port)
        else:
            self.mongo_collection = UrlMongoDB(db_name=db_name, server_ip=self.server_ip, port=self.port,
                                               collection_name=collection_name)


    def save_to_csv(self, data, csv_name):
        if isinstance(data,list) and isinstance(data[0],dict):
            headers = ["title","author","play_href","author_href"]
            with codecs.open(csv_name,"a", encoding="utf-8") as f:
                # 标头在这里传入，作为第一行数据
                writer = csv.DictWriter(f, headers)
                writer.writeheader()
                # 还可以写入多行
                writer.writerows(data)

    def read_from_csv(self, csv_name):
        with open(csv_name, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            for row in reader:
                print(row)

    def add_to_mongo(self,data):
        if isinstance(data,dict):
            self.mongo_collection.add_data(data)
        elif isinstance(data, list):
            if isinstance(data[0], dict):
                for _data in data:
                    self.mongo_collection.add_data(_data)
            else:
                print("type of data is not list/dict!")
        else:
            print("type of data is not dict or list!")

    def replace_to_mongo(self,data):
        if isinstance(data,dict):
            # print(111111)
            self.mongo_collection.replace_data(data)
        elif isinstance(data, list):
            if isinstance(data[0], dict):
                for _data in data:
                    print(_data)
                    # print(33333)
                    self.mongo_collection.replace_data(_data)
            else:
                print("type of data is not list/dict!")
        else:
            print("type of data is not dict or list!")

    def find_one_data(self, data_dic):
        data = self.mongo_collection.find_one_data(data_dic)
        return data

    def find_data(self,query_dic):
        data_list = self.mongo_collection.find_record(query_dic)
        return data_list

    def update_or_insert_one_to_mongo(self,update_data,query_dic):
        """
        update one record of collection
        :param update_data:
        :param query_key:
        :return:
        """
        if self.mongo_collection.find_one_record(query_dic) is None:
            self.mongo_collection.add_data(update_data)
        elif self.mongo_collection.find_one_record(query_dic) == update_data:
            print("record is same, skip update!")
        else:
            self.mongo_collection.update_one_record(query_dic, update_data)