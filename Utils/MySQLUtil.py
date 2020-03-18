import mysql.connector
import logging
from contextlib import closing


class MySQLUtil:
    """
    MySQL 操作用クラス
    """

    def __init__(self, host="localhost", port="3306", user="root", password="", database="db01"):
        self.config = {
            "host": host,
            "port": port,
            "user": user,
            "password": password,
            "database": database
        }

    def insert_data(self, data):
        """
        データを登録します
        :param data:
        :return:
        """

        with closing(mysql.connector.connect(**self.config)) as conn:

            c = conn.cursor()
            # データ登録
            sql = "INSERT INTO TBLCAT VALUES (%s,%s,%s,%s,%s,%s)"
            c.execute(sql, data)

            c.close()
            conn.commit()

    def update_data(self, data):
        """
        データを更新します
        :param data:
        :return:
        """

        with closing(mysql.connector.connect(**self.config)) as conn:

            c = conn.cursor()
            # データ登録
            sql = "UPDATE TBLCAT SET NAME = %s, " \
                  " SEX = %s, " \
                  " AGE = %s, " \
                  " KIND_CD = %s, " \
                  " FAVORITE = %s " \
                  "WHERE " \
                  " NO = %s"

            c.execute(sql, data)

            c.close()
            conn.commit()

    def delete_data(self, no):
        """
        データを削除します
        :return:
        """

        logging.info("delete_data")
        with closing(mysql.connector.connect(**self.config)) as conn:

            c = conn.cursor()

            # データクリア
            sql = "DELETE FROM TBLCAT WHERE NO = '" + no + "'"
            c.execute(sql)
            c.close()
            conn.commit()

    def get_data(self, no="", search_name=""):
        """
        データを取得します
        :return:
        """
        result = []

        with closing(mysql.connector.connect(**self.config)) as conn:

            c = conn.cursor(dictionary=True)

            # SQL組み立て
            sql = "SELECT C.NO, C.NAME, C.SEX, C.AGE, C.KIND_CD, K.KIND_NAME, C.FAVORITE FROM TBLCAT C"
            sql += " LEFT OUTER JOIN MSTKIND K ON ( C.KIND_CD = K.KIND_CD)"
            if no != "":
                sql += " WHERE NO = '" + no + "'"
            else:
                sql += " WHERE C.NAME LIKE '" + search_name + "%'"

            sql += " ORDER BY NO"

            c.execute(sql)
            for r in c.fetchall():
                result.append({
                    "no": r['NO'],
                    "name": r['NAME'],
                    "sex": r['SEX'],
                    "age": r['AGE'],
                    "kind_cd": r['KIND_CD'],
                    "kind_name": r['KIND_NAME'],
                    "favorite": r['FAVORITE'],
                })

        return result

    def get_next_no(self):
        """
        ユーザー毎にカレンダーIDの最大値＋１を返します
        :return:
        """
        result = 0

        with closing(mysql.connector.connect(**self.config)) as conn:

            c = conn.cursor(dictionary=True)

            sql = "SELECT MAX(NO) + 1 AS NO FROM TBLCAT"

            c.execute(sql)

            result = c.fetchone()

        return result[r"NO"]
