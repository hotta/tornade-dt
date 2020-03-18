import json
import logging
import os
import tornado.ioloop
import mysql.connector

from tornado.web import RequestHandler
from tornado.options import options
from contextlib import closing

from Utils.MySQLUtil import MySQLUtil

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
    """
    一覧初期化用
    """

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
    def initialize(self):
        logging.info("SearchHandler [initialize]")

    def post(self):
        """
        データをJSON形式で返します
        :return:
        """
        logging.info("SearchHandler [post]")

        search_name = self.get_argument("searchName")
        mysql = MySQLUtil()
        data_list = mysql.get_data(search_name=search_name)

        result = {
            'data': data_list
        }

        self.write(json.dumps(result, ensure_ascii=False))


class GetRecordHandler(RequestHandler):
    """
    プライマリキーを指定してデータ取得
    """

    def initialize(self):
        logging.info("GetRecordHandler [initialize]")

    def post(self):
        logging.info("GetRecordHandler [post]")
        param = json.loads(self.request.body)

        no = str(param["no"])

        mysql = MySQLUtil()
        result = mysql.get_data(no=no)

        self.write(json.dumps(result, ensure_ascii=False))


class RegistHandler(RequestHandler):
    """
    データ登録
    """

    def initialize(self):
        logging.info("RegistHandler [initialize]")

    def post(self):
        logging.info("RegistHandler [post]")

        mysql = MySQLUtil()

        param = json.loads(self.request.body)
        no = mysql.get_next_no()

        data = [
            no,
            param["name"],
            param["sex"],
            param["age"],
            param["kind_cd"],
            param["favorite"],
        ]
        mysql.insert_data(data)

        result = {
            'result': "success"
        }

        self.write(json.dumps(result, ensure_ascii=False))


class UpdateHandler(RequestHandler):
    """
    更新
    """
    def initialize(self):
        logging.info("UpdateHandler [initialize]")

    def post(self):
        logging.info("UpdateHandler [post]")

        mysql = MySQLUtil()

        param = json.loads(self.request.body)

        data = [
            param["name"],
            param["sex"],
            param["age"],
            param["kind_cd"],
            param["favorite"],
            param["no"],
        ]
        mysql.update_data(data)

        result = {
            'result': "success"
        }

        self.write(json.dumps(result, ensure_ascii=False))


class DeleteHandler(RequestHandler):
    """
    削除
    """

    def initialize(self):
        logging.info("RegistHandler [initialize]")

    def post(self):

        logging.info("RegistHandler [post]")

        mysql = MySQLUtil()

        param = json.loads(self.request.body)
        no = str(param["no"])

        mysql.delete_data(no)

        result = {
            'result': "success"
        }

        self.write(json.dumps(result, ensure_ascii=False))

app = tornado.web.Application([
    (r"/", MainHandler),
    (r"/init", InitHandler),
    (r"/search", SearchHandler),
    (r"/getRecord", GetRecordHandler),
    (r"/regist", RegistHandler),
    (r"/update", UpdateHandler),
    (r"/delete", DeleteHandler),
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
