import pymongo

class UrlMongoDB():
    def __init__(self, db_name, server_ip="localhost", port="27017", collection_name=None):
        self.db_name = db_name
        self.myclient = pymongo.MongoClient("mongodb://"+server_ip + ":" + port +"/")
        self.mongo_db = self.myclient[self.db_name]
        if collection_name is not None:
            self.mongo_collection = self.mongo_db[collection_name]

    def add_data(self,add_data_dict):
        self.mongo_collection.insert_one(add_data_dict)

    def replace_data(self,new_data_dict):
        if self.mongo_collection.find_one(new_data_dict) is None:
            data = self.mongo_collection.find_one_and_replace({},new_data_dict)
        else:
            print("相同，无需替换")

    def find_one_data(self,data_dict):
        data_dict["_id"] = 0
        data = self.mongo_collection.find_one({},data_dict)
        return data

    def find_one_record(self,query_dic):
        data = self.mongo_collection.find_one(query_dic,{"_id":0})
        return data
        # print(data[0])

    def find_record(self,query_dic):
        data_list = self.mongo_collection.find(query_dic, {"_id": 0})
        return data_list

    def update_one_record(self,query_dic,update_dic):
        if not isinstance(query_dic,dict) or not isinstance(update_dic,dict):
            raise IOError("%s and %s is not dict type!" % (query_dic,update_dic))
        new_dic = {"$set": update_dic}
        old_record = self.find_one_record(query_dic)
        self.mongo_collection.update_one(query_dic, new_dic)
        new_record = self.find_one_record(query_dic)
        print("update success！\nbefore update:%s\nafter update:%s" % (old_record,new_record))

    def modify_data(self):
        pass

    def sort_data(self):
        pass

    def delete_data(self):
        pass
