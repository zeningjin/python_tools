import MySQLdb

conn = MySQLdb.connect(
    db="clothes",
    user="root",
    passwd="123456",
    host="localhost",
    port=3306,
    charset="utf8"
)
cursor = conn.cursor()


# 插入数据
def insert_data(data1, data2):
    sql = "insert into ct_goods_size(size,goodsSku_id) values('{}','{}')".format(data1, data2)
    cursor.execute(sql)
    conn.commit()


# 修改数据
def updata_data(data1, data2):
    sql = "update ct_goods_size set size=%s,goodsSku_id=%s"
    cursor.execute(sql, (data1, data2))
    conn.commit()


# 读取数据
def get_datas():
    sql = "select * from ct_goods_size"
    cursor.execute(sql)
    return cursor.fetchall()


if __name__ == '__main__':
    sizes = ['M', 'L', 'XL']
    for goodsSku_id1 in range(11, 58):
        for size1 in sizes:
            size1 = str(size1)
            insert_data(size1, goodsSku_id1)
        print(goodsSku_id1)
