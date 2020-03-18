import json
import logging
import os
import tornado.ioloop
import mysql.connector

from tornado.web import RequestHandler
from tornado.options import options
from contextlib import closing

from Utils.MySQLUtil import MySQLUtil

accept_ctlc = False

def signal_handler(signum, frame):
    global accept_ctlc
    accept_ctlc = True

def try_exit(): 
    global accept_ctlc
    if accept_ctlc:
        tornado.ioloop.IOLoop.instance().stop()

class BaseRequestHandler(RequestHandler):
    """https://stackoverflow.com/questions/35254742/tornado-server-enable-cors-requests
    
    Arguments:
        RequestHandler {[type]} -- [description]
    """
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')

    def options(self):
        self.set_status(204)
        self.finish()

class MainHandler(BaseRequestHandler):
    """
    画面表示
    """

    def get(self):
        logging.info("MainHandler [get]")

        self.render("index.html")


class InitHandler(BaseRequestHandler):
    """
    一覧初期化用
    """

    def post(self):
        list = []
        result = {
            'data': list
        }

        self.write(json.dumps(result, ensure_ascii=False))


class SearchHandler(BaseRequestHandler):
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


class GetRecordHandler(BaseRequestHandler):
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


class RegistHandler(BaseRequestHandler):
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


class UpdateHandler(BaseRequestHandler):
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


class DeleteHandler(BaseRequestHandler):
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
