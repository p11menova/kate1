import pygame as pg


class User:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((500, 500))
        self.done = False

        self.start = True
        self.question = False

        self.startrect = pg.Rect(200, 100, 200, 32)
        self.questionrect = pg.Rect(50, 70, 300, 200)
        self.input_box = pg.Rect(100, 200, 140, 32)

        self.font = pg.font.Font(None, 24)
        pg.display.set_caption('изначальное поле')

        self.active = False
        self.text = ''

        self.color_inactive = pg.Color('black')
        self.color_active = pg.Color('lightgreen')
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
                txt_surface = self.font.render('Задать вопрос', True, self.color)
                self.screen.blit(txt_surface, (self.startrect.x + 30, self.startrect.y + 10))
                pg.draw.rect(self.screen, pg.Color('red'), self.startrect, 2)
            elif self.question:
                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        self.done = True
                    if event.type == pg.MOUSEBUTTONDOWN:
                        if self.input_box.collidepoint(event.pos):
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
                pg.draw.rect(self.screen, pg.Color('lightgreen'), self.questionrect, 3)
                font = pg.font.Font(None, 24)

                pg.draw.rect(self.screen, self.color, self.input_box, 2)
                txt_surface = font.render(self.text, True, self.color)
                width = max(200, txt_surface.get_width() + 10)
                self.input_box.w = width
                self.screen.blit(txt_surface, (self.input_box.x + 5, self.input_box.y + 10))
                self.screen.blit(font.render('Глубина марианской впадины?', True, pg.Color('black')), (60, 120))

            pg.display.flip()



demo = User()
demo.main()

