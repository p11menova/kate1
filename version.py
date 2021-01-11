import pygame as pg


class User:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((500, 500))
        self.startrect = pg.Rect(200, 100, 140, 32)

        self.questionrect = pg.Rect(50, 70, 300, 200)
        self.input_box = pg.Rect(100, 100, 200, 100)
        self.done = False
        pg.display.set_caption("ИЗНАЧАЛЬНОЕ ПОЛЕ")
        self.start = True
        self.question = False
        self.active = False
        self.text = ''
        self.color_inactive = pg.Color('lightskyblue3')
        self.color_active = pg.Color('dodgerblue2')
        self.color = self.color_inactive

    def makequestion(self):
        self.question = True
        self.start = False

    def main(self):
        while not self.done:
            self.screen.fill((255, 255, 255))
            if self.start:
                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        self.done = True
                    if event.type == pg.MOUSEBUTTONDOWN:
                        if self.startrect.collidepoint(event.pos):
                            self.makequestion()
                pg.draw.rect(self.screen, pg.Color('red'), self.startrect, 2)
            elif self.question:
                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        done = True
                    if event.type == pg.MOUSEBUTTONDOWN:
                        # If the user clicked on the input_box rect.
                        if self.input_box.collidepoint(event.pos):
                            # Toggle the active variable.
                            self.active = not self.active
                        else:
                            self.active = False

                        self.color = self.color_active if self.active else self.color_inactive
                    if event.type == pg.KEYDOWN:
                        if self.active:
                            if event.key == pg.K_RETURN:
                                print(self.text)
                                self.text = ''
                            elif event.key == pg.K_BACKSPACE:
                                self.text = self.text[:-1]
                            else:
                                self.text += event.unicode
                pg.draw.rect(self.screen, pg.Color('yellow'), self.questionrect, 3)
                font = pg.font.Font(None, 32)

                pg.draw.rect(self.screen, pg.Color('purple'), self.input_box, 2)
                txt_surface = font.render(self.text, True, self.color)
                width = max(200, txt_surface.get_width() + 10)
                self.input_box.w = width
                self.screen.blit(txt_surface, (self.input_box.x + 5, self.input_box.y + 5))

            pg.display.flip()


demo = User()
demo.main()

