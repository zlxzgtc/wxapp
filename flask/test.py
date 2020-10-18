import pymysql

connect = pymysql.Connect(
    host='localhost',
    port=3306,
    user='root',
    passwd='zlx,159357',
    db='wxapp',
    charset='utf8'
)
cursor = connect.cursor()
name = "酣十六"
sql = "SET @rank:=0"
cursor.execute(sql)
sql = "SELECT userrank,score from ( " \
      "SELECT username,score,@rank:=@rank+1 userrank FROM ranks order by score desc ) p " \
      "where username= '{}'".format(name)
cursor.execute(sql)
print(cursor.fetchall()[0][1])
