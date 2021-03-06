import os
import shutil
from time import sleep
from core import Database, Window

d = Database()
w = Window("打怪遊戲", "720x480")


class Game():
    def __init__(self):
        pass

    # 未完成
    def game_0_0(self):
        w.add_label("測試 (0-0)", "80", "8")


class Main():
    def __init__(self):
        self.g = Game()
        self.users()
        self.get()

    def get(self):
        os.path.dirname(f"./Data/{self.user}/userinfo.db")
        userinfo = d.get_data("userinfo", self.user)
        settings = d.get_data("settings", self.user)

        if userinfo == 0:
            self.un, self.uid = self.userdata()
        else:
            self.un, self.uid, self.pg = userinfo[0], userinfo[1], userinfo[2]

        settings = d.get_data("settings", self.user)
        try:
            self.s_story = " ".join(settings[0])
        except TypeError:
            d.create_data("settings", ("O"), self.user)

            print(self.lines("設定檔損毀，已重新回復為預設值"))
            sleep(0.5)
            settings = d.get_data("settings", self.user)
            self.s_story = " ".join(settings[0])

        self.menu_options = {
            "A": lambda self: self.start(),
            "B": lambda self: self.settings_menu(),
            "Q": lambda self: self.quit()
        }

        self.progress_options = {
            0: lambda self: self.g.game_0_0(),
        }

        self.settings_options = {
            "A": lambda self: self.setting_story(),
            "B": lambda self: self.cheat_code(),
            "C": lambda self: self.del_save(),
            "Q": lambda self: self.quit()
        }

        self.cheatcodes = {
            "HELLOWORLD": lambda self: self.cheat_helloworld()
        }

    def lines(self, text):
        a = "——"*len(f" {text}")
        return f"\n{a}\n {text}\n{a}"

    def menus(self, *text):
        str1 = ""
        for string in text:
            str1 += f"｜ {string}\n"

        return str1

    # 未完成
    def users(self):
        # print(self.lines("請選擇使用者"))
        self.user = "kanbo"

    def userdata(self):
        print("你好，歡迎遊玩本遊戲！\n遊玩前需要填入些基本資料，方便遊戲進行：\n")

        while True:
            while True:
                un = str(input("||  請輸入你的遊戲名稱："))
                if un == "":
                    print("(X) 遊戲名稱不可留白\n")
                else:
                    break

            while True:
                try:
                    uid0 = str(input("\n||  請輸入你的遊戲 ID (共四碼)："))
                    if uid0 == "":
                        print("(X) 遊戲 ID 不可留白")
                    uid = int(uid0)

                    if len(uid0) < 4 and uid0 != "":
                        print("(X) 遊戲 ID 未達所需長度")
                    elif len(uid0) > 4 and uid0 != "":
                        print("(X) 遊戲 ID 超過所需長度")
                    else:
                        break
                except ValueError:
                    if uid0 != "":
                        print("(X) 遊戲 ID 不可含非數字字元")
                    if len(uid0) < 4 and uid0 != "":
                        print("(X) 遊戲 ID 未達所需長度")
                    elif len(uid0) > 4 and uid0 != "":
                        print("(X) 遊戲 ID 超過所需長度")

            print("\n* 請注意，一旦進行遊戲，除非刪除紀錄，否則以上內容無法再次更改。")
            option = input("\n確認資料是正確的嗎？(輸入 X 重新更改) \n")

            if option == "x":
                continue
            else:
                break

        print("正在建立資料中...")
        sleep(1)
        d.create_data("userinfo", (un, uid, 0), self.user)
        d.create_data("settings", ("O"), self.user)
        self.get()

        print("已完成，正式開始遊戲")
        sleep(1)
        return un, uid

    def show_menu(self):
        print(self.lines(f"歡迎你！{self.un} #{self.uid}"))
        print(self.menus("A. 開始遊戲", "B. 設定", "Q. 離開"))

    def start(self):
        self.progress_options[self.pg](self)

    def settings_menu(self):
        while True:
            print(self.lines(f"遊戲設定"))
            print(self.menus(f"A. 遊戲劇情 ({self.s_story})",
                  "B. 密技碼", "C. 刪除記錄", "Q. 離開"))
            option = str(input("請選擇一個選項 > "))

            try:
                status = self.settings_options[option.upper()](self)
                if status == 0:
                    break
                elif status == -1:
                    return 0
            except KeyError:
                continue

    def settings_onoff(self):
        onoff = str(input("||  是否開啟 (O 為開啟/X 為關閉)：")).upper()

        if onoff == "O" or onoff == "X":
            print("\n正在更改設定...")
            sleep(1)
            print("更改完成！")
            sleep(1)

            return 0, onoff
        elif onoff == "":
            return 1, onoff
        elif onoff == "Q":
            return 0, self.s_story
        else:
            print("(X) 輸入格式錯誤\n")
            return 1, onoff

    def setting_story(self):
        print(f"\n遊戲劇情 (目前為 {self.s_story})\n開啟或關閉遊戲劇情的顯示\n")

        while True:
            status, onoff = self.settings_onoff()
            if status == 0:
                d.create_data("settings", (onoff), self.user)
                settings = d.get_data("settings", self.user)
                self.s_story = settings[0]
                break
            else:
                continue

    def cheat_code(self):
        print("\n密技碼 \n可透過密技碼更改遊戲的內容\n")

        while True:
            cheatcode = str(input("||  請輸入密技碼：")).upper()
            if cheatcode == "":
                continue
            else:
                break

        print("\n正在套用密技碼...")
        sleep(2)

        if cheatcode in self.cheatcodes:
            print(self.cheatcodes[cheatcode](self))
            sleep(3)
        else:
            print("無此密技碼。")
            sleep(2)
    
    def cheat_helloworld(self):
        return f"\n密技碼：HELLOWORLD{self.lines('Python 最高！ (・∀・)')}"

    def del_save(self):
        while True:
            print("\n* 請注意：刪除記錄後將無法再回復")
            onoff = str(input("||  是否刪除記錄 (O 為刪除/X 為不刪除)：")).upper()

            if onoff == "O":
                print("\n正在刪除記錄...")
                sleep(1)

                shutil.rmtree(f"./Data/{self.user}")
                print("刪除完成，遊戲將關閉。感謝您的遊玩！")
                sleep(1)

                return -1
            elif onoff == "X":
                break
            elif onoff == "":
                continue
            else:
                print("(X) 輸入格式錯誤\n")

    def quit(self):
        return 0


if __name__ == "__main__":
    m = Main()

    w.add_label("打怪遊戲", "80", "5")
    w.add_button("開始遊戲", "10", "1")
    w.add_button("設定", "10", "1")

    while True:
        m.show_menu()
        option = str(input("請選擇一個選項 > "))
        try:
            status = m.menu_options[option.upper()](m)
            if status == 0:
                break
        except KeyError:
            continue
