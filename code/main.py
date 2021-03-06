import os
import sqlite3
import sys
import pygame
from random import randint
from time import sleep
from core.window import Window, InputBox
from core.database import Database
from pygame.locals import Color, QUIT, MOUSEBUTTONDOWN, USEREVENT, USEREVENT

d = Database()


class Game(Window):
    """
    To-Do:

    - InputBox
    - game center
    - 設定選單
    - 細節部分
      ．名稱文字至中問題
    """

    def __init__(self):
        self.title = "打怪遊戲"
        self.version = ""

        super().__init__(self.title)

        self.story_game = {
            "1-0": "遊戲教學"
        }

        self.events = {
            "start_button": lambda: self.event_start_button(),
            "add_user": lambda: self.event_add_user(),
            "users": lambda: self.event_users(),
            "add_user_to_users": lambda: self.event_user_database(),
            "back_name": lambda: self.event_add_user(),
            "main_menu": lambda: self.event_main_menu(),
            "admin_password": lambda: self.event_admin_button(),
            "settings": lambda: self.event_settings_menu()
        }

    def event_click(self, event, pos1, pos2, action, obj=None):
        if event.type == MOUSEBUTTONDOWN:
            if pos1[0] < pygame.mouse.get_pos()[0] < pos2[0] and pos1[1] < pygame.mouse.get_pos()[1] < pos2[1]:
                if obj != None:
                    self.events[action](obj)
                else:
                    self.events[action]()

            # 除錯用
            else:
                print(pygame.mouse.get_pos())

    def event_quit(self, event):
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    def event_users(self):
        self.new_page("選擇使用者", (40, 43, 48))
        self.add_text(f"{self.title} {self.version}", 20, (35, 20), "黑體粗")

        # 進入管理員模式 | 未完成
        self.add_text(f"＞　進入管理員模式", 12, (295, 430), "黑體")

        # 設定按鈕 | 未完成
        self.add_image("./res/images/settings.png", (20, 20), 650, 30)

        # 選擇使用者
        self.add_text(f"請選擇使用者", 26, (275, 110), "黑體")

        if d.get_data("users") == "[資料庫] 錯誤 > 找不到資料庫或資料庫已毀損":
            self.add_image("./res/images/empty_player.png", (100, 125), 300, 185)

            while True:
                for event in pygame.event.get():
                    self.event_click(event, (302, 190), (398, 285), "add_user")
                    self.event_click(event, (293, 430), (406, 446), "admin_password")
                    self.event_click(event, (650, 28), (669, 46), "settings")
                    self.event_quit(event)
        else:
            # 文字至中問題 | 未完成

            self.username = d.get_data("users")[0]
            self.add_image("./res/images/player.png", (100, 125), 300, 185)
            self.add_text(self.username, 20, (335, 300), "黑體")

            while True:
                for event in pygame.event.get():
                    self.event_click(event, (302, 190), (398, 285), "main_menu")
                    self.event_click(event, (293, 430), (406, 446), "admin_password")
                    self.event_quit(event)

    def event_add_user(self):
        self.new_page("新增使用者", (40, 43, 48))
        clock = pygame.time.Clock()
        input_box1 = InputBox(250, 250, 140, 32)
        input_boxes = [input_box1]
        username = None

        while True:
            self.add_text(f"{self.title} {self.version}", 20, (35, 20), "黑體粗")

            for event in pygame.event.get():
                self.event_quit(event)
                self.event_click(event, (650, 28), (669, 45), "users")
                for box in input_boxes:
                    username = box.handle_event(event)

            if username is not None:
                print(username)
                break

            self.new_page("新增使用者", (40, 43, 48))
            self.add_text(f"玩家名稱", 15, (250, 225), "黑體")
            self.add_text(f"＊　輸入後按 Enter", 12, (295, 430), "黑體")
            self.add_image("./res/images/new_users.png", (75, 75), 320, 110)
            self.add_image("./res/images/back.png", (20, 20), 650, 30)

            for box in input_boxes:
                box.update()

            for box in input_boxes:
                box.draw(self.surface)

            pygame.display.flip()
            clock.tick(1000)

        # 輸入名字後
        self.new_page("新增使用者", (40, 43, 48))
        self.add_text(f"{self.title} {self.version}", 20, (35, 20), "黑體粗")
        self.add_text(f"確定要取名為 {username} 嗎？", 20, (250, 200), "黑體")
        self.add_image("./res/images/newuser_button.png", (94, 38), 300, 250)
        self.add_image("./res/images/back.png", (20, 20), 650, 30)
        self.username = username

        while True:
            for event in pygame.event.get():
                self.event_quit(event)
                self.event_click(event, (299, 250),
                                 (391, 285), "add_user_to_users")
                self.event_click(event, (650, 28), (669, 45), "back_name")

    def event_user_database(self):
        d.dbinit("users", (self.username,))
        d.dbinit("settings", ("ON",), self.username)
        d.dbinit("userinfo", (self.username, randint(1000, 9999), 0,), self.username)
        self.event_users()

    def event_start_button(self):
        # story_game = "1-0"
        # pygame.display.set_caption(
        #     f"{self.title} - {self.story_game[story_game]}")
        # pygame.display.update()
        print("開始遊戲")

    def event_admin_button(self):
        clock = pygame.time.Clock()
        input_box1 = InputBox(250, 250, 140, 32)
        input_boxes = [input_box1]
        password = None

        while True:
            self.add_text("管理員模式", 20, (35, 20), "黑體粗")
            self.add_text("請輸入密碼", 26, (283, 110), "黑體粗")
            self.add_image("./res/images/back.png", (20, 20), 650, 30)

            # 輸入框/提示
            self.add_text(f"＊　輸入後按 Enter", 12, (295, 430), "黑體")

            for event in pygame.event.get():
                self.event_quit(event)
                self.event_click(event, (650, 28), (669, 45), "users")
                for box in input_boxes:
                    password = box.handle_event(event)

            if password is not None:
                if password != "0000":
                    self.new_page("密碼錯誤", (40, 43, 48))
                    self.add_text("密碼錯誤", 26, (283, 110), "黑體粗")
                    sleep(1)
                    password = None
                else:
                    # 未完成
                    pass

            self.new_page("管理員模式密碼", (40, 43, 48))
            for box in input_boxes:
                box.update()

            for box in input_boxes:
                box.draw(self.surface)

            pygame.display.flip()
            clock.tick(70)

    def event_main_menu(self):
        self.new_page("遊戲主選單", (40, 43, 48))

        self.add_text(f"{self.title} {self.version}", 20, (190, 20), "黑體粗")

        self.add_image("./res/images/gray_background.png", (150, 480), 0, 0)
        self.add_image("./res/images/news.png", (485, 250), 192, 94)
        self.add_image("./res/images/player.png", (30, 40), 645, 20)
        self.add_image("./res/images/start_button.png", (110, 35), 368, 409)
        self.add_image("./res/images/settings.png", (20, 20), 45, 418)
        self.add_text("設定", 15, (75, 417), "黑體粗")
    
    def event_settings_menu(self):
        self.new_page("設定", (40, 43, 48))

    def story_0(self):
        """
        故事設定：
        """

        pass


def main():
    g = Game()
    g.event_users()


if __name__ == "__main__":
    main()
