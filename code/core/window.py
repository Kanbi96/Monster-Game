import pygame
from pygame.locals import Color, QUIT, MOUSEBUTTONDOWN, USEREVENT, USEREVENT


class InputBox:

    def __init__(self, x, y, w, h, text=''):
        pygame.init()

        self.COLOR_INACTIVE = pygame.Color('lightskyblue3')
        self.COLOR_ACTIVE = pygame.Color('dodgerblue2')
        self.FONT = pygame.font.Font(None, 32)

        self.rect = pygame.Rect(x, y, w, h)
        self.color = self.COLOR_INACTIVE
        self.text = text
        self.txt_surface = self.FONT.render(text, True, self.color)
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            self.color = self.COLOR_ACTIVE if self.active else self.COLOR_INACTIVE
        if event.type == pygame.KEYDOWN:
            if self.active:
                print(event.key)
                if event.key == pygame.K_RETURN:
                    return self.text
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                self.txt_surface = self.FONT.render(
                    self.text, True, self.color)

    def update(self):
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        pygame.draw.rect(screen, self.color, self.rect, 2)


class Window(pygame.sprite.Sprite):

    def __init__(self, title, toggle=True):
        """
        * 變數說明
          - window_width > 視窗寬度
          - window_height > 視窗高度
          - title > 標題
          - surface > Pygame object
        """

        if toggle == False:
            return

        super().__init__()
        pygame.init()

        self.title = title
        self.window_width = 720
        self.window_height = 480
        self.surface = pygame.display.set_mode(
            (self.window_width, self.window_height))

        pygame.display.set_caption(self.title)
        pygame.display.set_icon(
            pygame.image.load("./res/images/game_icon.png"))

        self.surface.fill((40, 43, 48))
        pygame.display.update()

        self.fonts = {
            "黑體細": "./res/fonts/NotoSansCJKtc-Light.otf",
            "黑體": "./res/fonts/NotoSansCJKtc-Regular.otf",
            "黑體粗": "./res/fonts/NotoSansCJKtc-Medium.otf",
        }

        self.color = {
            "WHITE": (255, 255, 255),
            "BLACK1": (0, 0, 0),
            "BLACK2": (40, 43, 48),
            "BLACK3": (54, 57, 63)
        }

    def add_text(self, text, size, coordinate, font="黑體", color="WHITE"):
        """
        * coordinate 須回傳 tuple
        * font 均使用思源黑體（黑體細、黑體、黑體粗）
        """

        font = self.fonts[font]
        head_font = pygame.font.Font(font, size)
        text_surface = head_font.render(text, True, self.color[color])
        self.surface.blit(text_surface, coordinate)
        pygame.display.update()

    def add_image(self, path, size, coordinate):
        """
        * coordinate/size 須回傳 tuple
        """

        raw_image = pygame.image.load(path).convert_alpha()
        image = pygame.transform.scale(raw_image, size)

        self.surface.blit(image, coordinate)
        pygame.display.update()

    def add_inputbox(self, text, size, coordinate, font="黑體", color="WHITE"):
        """
        class InputBox
        """

        InputBox(250, 250, 140, 32)

        while True:
            box.handle_event(event)

            pygame.display.update()
            for box in input_boxes:
                box.update()

            for box in input_boxes:
                box.draw(self.surface)

            pygame.display.flip()
            clock.tick(70)

    def new_page(self, title, color):
        self.surface.fill(color)
        pygame.display.set_caption(f"{self.title} - {title}")
        pygame.display.update()


class Tkinter_Window():
    def __init__(self):
        pass


if __name__ == "__main__":
    pass
