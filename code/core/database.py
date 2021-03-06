import os
import sqlite3


class Database():

    def __init__(self):
        self.datatype = {
            # 使用者
            "users": ("(NAME text)", "(?)"),

            # 使用者資料
            "userinfo": ("(NAME text, ID integer, PROGRESS integer)",
                         "(?, ?, ?)"),
            "settings": ("(STORY text)", "(?)"),
            # "settings": ("(AT integer, DE integer)", "(?, ?)"),
        }
    
    def dbinit(self, filename, data, user=""):
        """
        資料庫初始化
        * filename > 文件名稱 (無須加副檔名 .db)
        * data > 放入資料 (請參考 self.datatype)
        * user > 適用之使用者 (留白則為全體共用)
        """

        if user == "":
            try:
                os.unlink(f"./data/{filename}.db")
            except FileNotFoundError:
                pass

            conn = sqlite3.connect(f"./data/{filename}.db")
        else:
            try:
                os.unlink(f"./data/{user}/{filename}.db")
            except FileNotFoundError:
                pass

            try:
                conn = sqlite3.connect(f"./data/{user}/{filename}.db")
            except sqlite3.OperationalError:
                os.makedirs(f"./data/{user}")
                conn = sqlite3.connect(f"./data/{user}/{filename}.db")

        cur = conn.cursor()
        cur.execute(f"""CREATE TABLE {filename.upper()}
            {self.datatype[filename][0]}""")
        conn.commit()

        fn = filename.upper()
        ft = self.datatype[filename][1]

        cur.execute(f"INSERT INTO {fn} VALUES {ft}", data)
        conn.commit()

        conn.close()

    def get_data(self, filename, user=""):
        """
        獲取資料庫資料
        * filename > 文件名稱 (無須加副檔名 .db)
        * user > 使用者名稱 (留白則自動導向至 data 資料夾)
        """

        try:
            if user == "":
                conn = sqlite3.connect(f"./data/{filename}.db")
                cur = conn.cursor()
            else:
                while True:
                    try:
                        conn = sqlite3.connect(f"./data/{user}/{filename}.db")
                        cur = conn.cursor()
                        break
                    except sqlite3.OperationalError:
                        os.makedirs(f"./data/{user}")
            cur.execute(f"SELECT * FROM {filename.upper()}")
        except sqlite3.OperationalError:
            conn.close()
            if user == "":
                os.unlink(f"./data/{filename}.db")
            else:
                os.unlink(f"./data/{user}/{filename}.db")
            return "[資料庫] 錯誤 > 找不到資料庫或資料庫已毀損"

        for word in cur.fetchall():
            if word is None:
                return "[資料庫] 錯誤 > 資料庫損毀，請重新建置"
            return word

if __name__ == "__main__":
    pass
