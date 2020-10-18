from flask import Flask
from flask import request
import pymysql

app = Flask(__name__)


# 分页查询ranks中的昵称和分数
@app.route('/login')
def login():
    # 连接数据库
    connect = pymysql.Connect(
        host='localhost',
        port=3306,
        user='root',
        passwd='zlx,159357',
        db='wxapp',
        charset='utf8'
    )
    cursor = connect.cursor()
    # name = request.args['username']
    k = request.args['pages']
    sql = "SELECT username,score FROM `ranks` order by score desc limit %d,%d" % ((int(k) - 1) * 10, int(k) * 10)
    cursor.execute(sql)
    list1 = []
    for row in cursor.fetchall():
        list1.append({"username": row[0], "score": row[1]})
    sql = "SELECT count(*) FROM `ranks` "
    cursor.execute(sql)
    res1 = cursor.fetchall()[0]
    return {"ranks": list1, "allpages": int(int(res1[0] + 9) / 10)}


# 获得用户的排名、得分和排行榜的总页数
@app.route('/userRank')
def userRank():
    # 连接数据库
    connect = pymysql.Connect(
        host='localhost',
        port=3306,
        user='root',
        passwd='zlx,159357',
        db='wxapp',
        charset='utf8'
    )
    cursor = connect.cursor()
    name = request.args['username']
    sql = "SET @rank:=0"
    cursor.execute(sql)
    sql = "SELECT userrank,score from ( " \
          "SELECT username,score,@rank:=@rank+1 userrank FROM ranks order by score desc ) p " \
          "where username= '{}'".format(name)
    cursor.execute(sql)
    res = cursor.fetchall()[0]
    sql = "SELECT count(*) FROM `ranks` "
    cursor.execute(sql)
    res1 = cursor.fetchall()[0]
    return {"rank": res[0], "score": res[1], "allpages": int(int(res1[0] + 9) / 10)}


# 更新用户的最高分
@app.route('/updateScore')
def highScore():
    # 连接数据库
    connect = pymysql.Connect(
        host='localhost',
        port=3306,
        user='root',
        passwd='zlx,159357',
        db='wxapp',
        charset='utf8'
    )
    cursor = connect.cursor()
    name = request.args['username']
    score = request.args['highscore']
    sql = "UPDATE ranks SET score={} where username='{}'".format(score, name)
    cursor.execute(sql)
    connect.commit()
    return "ok"


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
