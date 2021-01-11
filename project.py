import pygame as pg
import csv
import random
import os


DATA_DIR = 'data'

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
        self.gravity = random.choice([-0.1, 0.1])

    def update(self):
        self.velocity[1] += self.gravity
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]

        if not self.rect.colliderect(screen_rect):
            self.kill()


class Board:
    def __init__(self, width, height):

        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        self.left = 10
        self.top = 10
        self.cell_size = 30

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, screen):
        for i in range(self.height):
            for j in range(self.width):
                pg.draw.rect(screen, (0, 0, 0), (self.cell_size * j + self.left,
                                                           self.cell_size * i + self.top,
                                                           self.cell_size,
                                                           self.cell_size), 1)

    def get_cell(self, mouse_pos):
        if mouse_pos[0] > self.left and mouse_pos[1] > self.top:
            x = ((mouse_pos[0] - self.left) // self.cell_size) + 1
            y = ((mouse_pos[1] - self.top) // self.cell_size) + 1

            if x <= self.width and y <= self.height:
                return x, y


class User:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((500, 500))
        self.done = False

        self.start = True
        self.question = False

        self.startrect = pg.Rect(50, 50, 200, 32)
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

        self.ballonimage = pg.image.load(os.path.join(DATA_DIR, 'ballon.png'))
        self.ballonimagerect = self.ballonimage.get_rect()

        self.board_width, self.board_height = 7, 6
        self.boardleft, self.boardtop, self.cellsize = 50, 100, 50
        self.board_creature_rect = pg.Rect(self.boardleft, self.boardtop,
                                           self.cellsize * self.board_width, self.cellsize * self.board_height)

        self.ballon = MovingCreature(self.screen, self.board_creature_rect, self.ballonimage, self.ballonimagerect)

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

                    if event.type == pg.KEYDOWN:
                        if event.key == pg.K_LEFT and self.ballon.are_coordinates_correct(self.ballon.get_coords(), 'left'):
                            self.ballon.change_coords('x', -50)
                        if event.key == pg.K_RIGHT and self.ballon.are_coordinates_correct(self.ballon.get_coords(), 'right'):
                            self.ballon.change_coords('x', 50)
                        if event.key == pg.K_UP and self.ballon.are_coordinates_correct(self.ballon.get_coords(), 'top'):
                            self.ballon.change_coords('y', -50)
                        if event.key == pg.K_DOWN and self.ballon.are_coordinates_correct(self.ballon.get_coords(), 'bottom'):
                            self.ballon.change_coords('y', 50)


                self.ballon._redraw_screen()
                txt_surface = self.font.render('Задать вопрос', True, self.color)
                self.screen.blit(txt_surface, (self.startrect.x + 30, self.startrect.y + 10))
                pg.draw.rect(self.screen, pg.Color('red'), self.startrect, 2)

                board = Board(self.board_width, self.board_height)
                board.set_view(self.boardleft, self.boardtop, self.cellsize)
                board.render(self.screen)

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


class MovingCreature():
    def __init__(self, screen, rect, image, imagerect):
        self.running = False
        self.screen = screen
        self.x, self.y = 50, 100
        self.rect = rect
        self.image = image
        self.imagerect = imagerect

    def are_coordinates_correct(self, coords, task):
        x, y = coords
        if task == 'left':
            if x != self.rect.left:
                return True
        elif task == 'right':
            if (x + self.imagerect.w) != self.rect.right:
                return True
        elif task == 'top':
            if y != self.rect.top:
                return True
        elif task == 'bottom':
            if (y + self.imagerect.w) != self.rect.bottom:
                return True
        return False

    def _redraw_screen(self):
        self._draw_creature((self.x, self.y))
        #pg.display.flip()

    def _draw_creature(self, position):
        self.screen.blit(self.image, position)

    def get_coords(self):
        return self.x, self.y

    def change_coords(self, xy, n):
        if xy == 'x':
            self.x += n
        if xy == 'y':
            self.y += n


demo = User()
demo.main()

