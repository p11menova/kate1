import pygame as pg
import csv
import random
import os


DATA_DIR = 'data'
GRAVITY = 0.1
all_sprites = pg.sprite.Group()

clock = pg.time.Clock()
screen_rect = (0, 0, 500, 500)


class Particle(pg.sprite.Sprite):
    fire = [pg.image.load(os.path.join(DATA_DIR, 'star.png'))]
    for scale in (5, 10, 20):
        fire.append(pg.transform.scale(fire[0], (scale, scale)))

    def __init__(self, pos, dx, dy):
        super().__init__(all_sprites)
        self.image = random.choice(self.fire)
        self.rect = self.image.get_rect()

        self.velocity = [dx, dy]
        self.rect.x, self.rect.y = pos
        self.gravity = GRAVITY

    def update(self):
        self.velocity[1] += self.gravity
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]

        if not self.rect.colliderect(screen_rect):
            self.kill()


class User:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((500, 500))
        self.done = False

        self.start = True
        self.question = False

        self.startrect = pg.Rect(200, 100, 200, 32)
        self.questionrect = pg.Rect(50, 70, 400, 200)
        self.input_box = pg.Rect(100, 200, 140, 32)

        self.font = pg.font.Font(None, 24)
        pg.display.set_caption('изначальное поле')

        self.active = False
        self.text = ''

        self.color_inactive = pg.Color('black')
        self.color_active = pg.Color('lightgreen')
        self.color = self.color_inactive

        self.myindex = 0

    def make_question(self):
        self.question = True
        self.start = False

    def create_particles(self, position):
        particle_count = 30
        numbers = range(-5, 6)
        for _ in range(particle_count):
            Particle(position, random.choice(numbers), random.choice(numbers))

    def work_w_csv(self, task):
        with open('question.csv', encoding="utf8", mode='r') as csvfile:
            reader = csv.reader(csvfile, delimiter=';', quotechar='"')
            for index, row in enumerate(reader):
                if index == self.myindex:
                    if task == 'question':
                        return row[0]
                    elif task == 'correct_answer':
                        return row[1]


    def main(self):
        while not self.done:
            self.screen.fill((255, 255, 255))
            if self.start:
                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        self.done = True
                    if event.type == pg.MOUSEBUTTONDOWN:
                        if self.startrect.collidepoint(event.pos):
                            self.make_question()
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
                                if self.text == self.work_w_csv('correct_answer'):
                                    for _ in range(5):
                                        self.create_particles((random.randint(0, 500), random.randint(0, 500)))

                                    print(self.text)
                                    print('correct')
                                self.text = ''
                                self.myindex += 1
                            elif event.key == pg.K_BACKSPACE:
                                self.text = self.text[:-1]
                            else:
                                self.text += event.unicode

                all_sprites.update()
                all_sprites.draw(self.screen)

                pg.draw.rect(self.screen, pg.Color('lightgreen'), self.questionrect, 3)
                font = pg.font.Font(None, 24)

                pg.draw.rect(self.screen, self.color, self.input_box, 2)
                txt_surface = font.render(self.text, True, self.color)
                width = max(200, txt_surface.get_width() + 10)
                self.input_box.w = width
                self.screen.blit(txt_surface, (self.input_box.x + 5, self.input_box.y + 10))
                self.screen.blit(font.render(self.work_w_csv('question'), True, pg.Color('black')), (60, 120))

            pg.display.flip()
            clock.tick(50)



demo = User()
demo.main()

