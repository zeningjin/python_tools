import pymongo

def create_col(myclient, db_name, col_name):
    """
        创建数据库和创建集合
    :param myclient:
    :param db_name:
    :param col_name:
    :return:
    """
    dblist = myclient.list_database_names()
    if db_name in dblist:
        print(db_name, "数据库已经存在")
    mydb = myclient[db_name]
    collist = mydb.list_collection_names()
    if col_name in collist:
        print(col_name, "集合已经存在已经存在")
    mycol = mydb["sites"]
    return mycol


def insert_data(myclient, db_name, col_name, data={}):
    """
        往mongodb数据库中插数据
    :param myclient:
    :param data:
    :param mycol:
    :return:
    """
    mydb = myclient[db_name]
    mycol = mydb[col_name]
    data1 = [
        {"name": "Taobao", "alexa": "100", "url": "https://www.taobao.com"},
        {"name": "QQ", "alexa": "101", "url": "https://www.qq.com"},
        {"name": "Facebook", "alexa": "10", "url": "https://www.facebook.com"},
        {"name": "知乎", "alexa": "103", "url": "https://www.zhihu.com"},
        {"name": "Github", "alexa": "109", "url": "https://www.github.com"}
    ]
    data2 = {"name": "RUNOOB", "alexa": "10000", "url": "https://www.runoob.com"}
    x = mycol.insert_many(data1)
    print("插入数据数据成功", x.inserted_ids)
    x = mycol.insert_one(data2)
    print("插入数据数据成功", x.inserted_id)
    return None


def select_data(myclient, db_name, col_name, data={}):
    """
        查询
    :param myclient:
    :param db_name:
    :param col_name:
    :param data:
    :return:
    """
    data2 = {"name": "RUNOOB", "alexa": "10000", "url": "https://www.runoob.com"}
    mydb = myclient[db_name]
    mycol = mydb[col_name]
    # 将要返回的字段对应值设置为 1
    for x in mycol.find({}, {"_id": 0, "name": 1, "alexa": 1}):
        print(x)
    # 条件查询 还可以正则和大于 小于等查询
    myquery = {"name": "RUNOOB"}
    mydoc = mycol.find(myquery)
    for x in mydoc:
        print(x)
    return None


def update_data(myclient, db_name, col_name, data={}):
    """
        修改数据
    :param myclient:
    :param db_name:
    :param col_name:
    :param data:
    :return:
    """
    mydb = myclient[db_name]
    mycol = mydb[col_name]

    # 将 alexa 字段的值 10000 改为 12345:
    myquery = {"alexa": "10000"}
    newvalues = {"$set": {"alexa": "12345"}}
    mycol.update_one(myquery, newvalues)
    # 输出修改后的  "sites"  集合
    for x in mycol.find():
        print(x)

    # 以 F 开头的 name 字段，并将匹配到所有记录的 alexa 字段修改为 123：
    myquery = {"name": {"$regex": "^F"}}
    newvalues = {"$set": {"alexa": "123"}}
    x = mycol.update_many(myquery, newvalues)
    print(x.modified_count, "文档已修改")
    return None

def delete_data(myclient, db_name, col_name, data={}):
    """
        删除某个数据
    :param myclient:
    :param db_name:
    :param col_name:
    :param data:
    :return:
    """
    mydb = myclient[db_name]
    mycol = mydb[col_name]

    # 删除一条
    myquery = {"name": "Taobao"}
    mycol.delete_one(myquery)
    # 删除后输出
    for x in mycol.find():
        print(x)

    # 批量删除
    myquery = {"name": {"$regex": "^F"}}
    x = mycol.delete_many(myquery)
    print(x.deleted_count, "个文档已删除")


if __name__ == '__main__':
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    create_col(myclient, "web", "infor")
    # insert_data(myclient, "web", "infor")
    select_data(myclient, "web", "infor")
    # update_data(myclient, "web", "infor")
    # delete_data(myclient, "web", "infor")