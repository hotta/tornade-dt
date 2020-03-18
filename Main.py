import json
import logging
import os
import tornado.ioloop
import mysql.connector

from tornado.web import RequestHandler
from tornado.options import options
from contextlib import closing

accect_ctlc = False

def signal_handler(signum, frame):
    global accect_ctlc
    accect_ctlc = True

def try_exit(): 
    global accect_ctlc
    if accect_ctlc:
        tornado.ioloop.IOLoop.instance().stop()

class MainHandler(RequestHandler):
    """
    画面表示
    """

    def get(self):
        logging.info("MainHandler [get]")

        self.render("index.html")


class InitHandler(RequestHandler):

    def post(self):
        list = []
        result = {
            'data': list
        }

        self.write(json.dumps(result, ensure_ascii=False))


class SearchHandler(RequestHandler):
    """
    データ検索
    """

    def post(self):
        """
        データをJSON形式で返します
        :return:
        """
        logging.info("SearchHandler [post]")

        searchName = self.get_argument("searchName")

        with closing(mysql.connector.connect(
            host="localhost",
            port="3306",
            user="root",
            password="",
            database="db01"
        )) as conn:

            c = conn.cursor(dictionary=True)

            # SQL組み立て
            sql = "SELECT C.NO, C.NAME, C.SEX, C.AGE, C.KIND_CD, K.KIND_NAME, C.FAVORITE FROM TBLCAT C"
            sql += " LEFT OUTER JOIN MSTKIND K ON ( C.KIND_CD = K.KIND_CD)"
            sql += " WHERE C.NAME LIKE '" + searchName + "%'"

            list = []
            c.execute(sql)
            for r in c.fetchall():
                list.append({
                    "no": r['NO'],
                    "name": r['NAME'],
                    "sex": r['SEX'],
                    "age": r['AGE'],
                    "kind_name": r['KIND_NAME'],
                    "favorite": r['FAVORITE'],
                })

        result = {
            'data': list
        }

        self.write(json.dumps(result, ensure_ascii=False))


app = tornado.web.Application([
    (r"/", MainHandler),
    (r"/init", InitHandler),
    (r"/search", SearchHandler),
],
    template_path=os.path.join(os.getcwd(), "templates"),
    static_path=os.path.join(os.getcwd(), "static"),
)

if __name__ == "__main__":
    options.parse_command_line()
    app.listen(8080)
    logging.info("server started")
    tornado.ioloop.PeriodicCallback(try_exit, 100).start() 
    tornado.ioloop.IOLoop.instance().start()
