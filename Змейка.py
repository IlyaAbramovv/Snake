import pygame
import sys
import random

height = 480
width = 640
FPS = 12
clock = pygame.time.Clock()
overgame = False

high_score_path = 'data/high_score_save.txt'
record = '0'

# Реализация паузы
def pause():
    global running
    paused = 1
    while paused:
        surface.blit(image_grass, (0, 0))
        font = pygame.font.Font(None, 45)
        text = font.render('Пауза', 1, (255, 255, 255))
        surface.blit(text, (285, 250))
        text = font.render('Нажмите "Esc" чтобы продолжить', 1, (255, 255, 255))
        surface.blit(text, (80, 300))

        # Выход из паузы если нажали escape
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    paused = False
            elif event.type == pygame.QUIT:
                sys.exit()
        pygame.display.flip()

    # Отрисовка змейки
    surface.blit(image_grass, (0, 0))
    snake.move_snake_head()
    snake.move_snake_body()
    snake.draw_snake()
    snake.draw_apple()
    snake.show_score()
    snake.check_for_death()
    pygame.display.flip()
    clock.tick(1)

# Конец игры
def game_over():
    global running
    global overgame

    overgame = True
    running = False

pygame.init()
pygame.font.init()
surface = pygame.display.set_mode((width, height))
pygame.display.set_caption('Змейка')


# Класс змейки
class Snake():

    def __init__(self):
        self.RIGHT = 10
        self.LEFT = -10
        self.UP = 20
        self.DOWN = -20

        self.score = 0
        # Начальная позиция головы
        self.head_position = [height / 2, width / 2]
        # Тело змейки состоит из головы и 1 части
        self.snake_body = [[height / 2, width / 2], [height / 2 - 10, width / 2 - 10]]
        # Изначальное направление
        self.direction = self.RIGHT

        self.change_direction = self.direction

    # Вывод счета
    def show_score(self):
        font = pygame.font.Font(None, 25)
        text = font.render('Счет: {}'.format(self.score), 1, (255, 255, 255))
        surface.blit(text, (10, 20))

    # Сменить направление, если оно не противоположно текущему
    def change_direction_control(self, change_dir):
        self.change_direction = change_dir
        if self.direction / self.change_direction != -1:
            self.direction = self.change_direction
        else:
            self.change_direction = self.direction

    # Реализация движения головы
    def move_snake_head(self):
        if self.direction == self.RIGHT or self.direction == self.LEFT:
            self.head_position[0] += self.direction
        elif self.direction == self.UP or self.direction == self.DOWN:
            self.head_position[1] -= self.direction / 2

    # Реализация движения тела
    def move_snake_body(self):
        global score
        self.snake_body.insert(0, list(self.head_position))
        if (self.head_position[0] == self.apple_pos[0] and self.head_position[1] == self.apple_pos[1]):
            self.generate_apple()
            self.draw_apple()
            self.score += 1

        else:
            self.snake_body.pop()

    # Отрисовка змейки
    def draw_snake(self):
        surface.blit(image_grass, (0, 0))
        f = self.snake_body[0]
        if self.direction == self.RIGHT:
            surface.blit(head_right, (f[0], f[1]))
        elif self.direction == self.LEFT:
            surface.blit(head_left, (f[0], f[1]))
        elif self.direction == self.UP:
            surface.blit(head_up, (f[0], f[1]))
        elif self.direction == self.DOWN:
            surface.blit(head_down, (f[0], f[1]))

        for i in self.snake_body[1:]:
            surface.blit(image_snake_body, (i[0], i[1]))

    # Проверка на выход из поля или поедание себя
    def check_for_death(self):
        if (self.head_position[0] > width - 10 or self.head_position[0] < 0 or
            self.head_position[1] > height - 10 or self.head_position[1] < 0):
            game_over()
        for block in self.snake_body[1:]:
            if (block[0] == self.head_position[0] and
                    block[1] == self.head_position[1]):
                game_over()

    # Генерация положения яблока на экране
    def generate_apple(self):
        self.apple_pos = (random.randrange(1, width / 10) * 10, random.randrange(1, height / 10) * 10)
        # Механизм вывода яблока строка по координатам, кратным 10

    # Отрисовка яблока
    def draw_apple(self):
        surface.blit(image_apple, (self.apple_pos[0], self.apple_pos[1]))

surface.fill((255, 218, 185))
font = pygame.font.Font(None, 45)
text = font.render('Нажмите пробел', 1, (0, 0, 100))
surface.blit(text, (210, 240))

# Загрузка спрайтов
image_grass = pygame.image.load('data/grass.png')
image_apple = pygame.image.load('data/apple.png')
image_snake_body = pygame.image.load('data/snake_body.png')
head_left = pygame.image.load('data/snake_head_left.png')
head_right = pygame.image.load('data/snake_head_right.png')
head_up = pygame.image.load('data/snake_head_up.png')
head_down = pygame.image.load('data/snake_head_down.png')

pygame.display.flip()

# Игровой цикл
while 1:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # Запустить игру при нажатии пробела
                surface.blit(image_grass, (0, 0))
                snake = Snake()
                change_dir = 10
                running = True
                snake.generate_apple()
                # Часть с самой змейкой
                while running:
                    for event in pygame.event.get():
                        if event.type == pygame.KEYDOWN:
                            # Смена направления осуществляется при нажатии стрелочек или букв wasd
                            if event.key == pygame.K_RIGHT or event.key == ord('d'):
                                change_dir = 10
                            elif event.key == pygame.K_LEFT or event.key == ord('a'):
                                change_dir = -10
                            elif event.key == pygame.K_UP or event.key == ord('w'):
                                change_dir = 20
                            elif event.key == pygame.K_DOWN or event.key == ord('s'):
                                change_dir = -20
                            elif event.key == pygame.K_ESCAPE:
                                pause()
                        elif event.type == pygame.QUIT:
                            sys.exit()

                    snake.change_direction_control(change_dir)

                    surface.blit(image_grass, (0, 0))
                    snake.move_snake_head()
                    snake.move_snake_body()
                    snake.draw_snake()
                    snake.draw_apple()
                    snake.show_score()
                    snake.check_for_death()
                    pygame.display.flip()
                    clock.tick(FPS)
        elif event.type == pygame.QUIT:
            sys.exit()
            # Выход из игры

    # Отрисовка экрана смерти
    if overgame:
        high_score_file = open(high_score_path)
        high_score_text = high_score_file.read()
        high_score_file.close()

        surface.fill((255, 255, 255))
        surface.blit(image_grass, (0, 0))
        font = pygame.font.Font(None, 35)
        text = font.render('Вы проиграли', 1, (255, 255, 255))
        surface.blit(text, (220, 200))
        text = font.render('Ваш счет: {}'.format(snake.score), 1, (255, 255, 255))
        surface.blit(text, (220, 240))

        if int(high_score_text) >= snake.score:
            record = 'Ваш рекорд: ' + high_score_text
        else:
            with open(high_score_path, 'w') as h:
                h.write(str(snake.score))

        text = font.render(record, 1, (255, 255, 255))
        surface.blit(text, (220, 280))

        text = font.render('Нажмите пробел чтобы продолжить', 1, (255, 255, 255))
        surface.blit(text, (100, 320))

    pygame.display.flip()











