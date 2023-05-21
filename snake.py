
import pygame, sys, random
from pygame.math import Vector2

class FRUIT:
    def __init__(self) -> None:
        self.random()
    
    def random(self):
        self.x = random.randint(0, cell_number - 1)
        self.y = random.randint(0, cell_number - 1)
        self.pos = Vector2(self.x, self.y)

    def make_fruit(self):

        # create rectangle 
        fruit_rect = pygame.Rect(self.pos.x * cell_size, self.pos.y * cell_size, cell_size, cell_size)
        # draw rectangle
        screen.blit(apple, fruit_rect)
        # pygame.draw.rect(screen, pygame.Color('crimson'), fruit_rect)

class SNAKE:
    def __init__(self) -> None:
        self.body = [Vector2(8, 20), Vector2(7, 20), Vector2(6, 20)]
        self.direction = Vector2(0, 0)
        self.new_block = False

    def make_snake(self):
        for block in self.body:
            x = block.x * cell_size
            y = block.y * cell_size

            snake_rect = pygame.Rect(x, y, cell_size, cell_size)

            pygame.draw.rect(screen, (219,112,147), snake_rect)

    def move_snake(self):
        if self.new_block == True:
            body_copy = self.body[:]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]
            self.new_block = False
        else:
            body_copy = self.body[:-1]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]
    
    def add_snake(self):
        self.new_block = True

    def reset(self):
        self.body = [Vector2(8, 20), Vector2(7, 20), Vector2(6, 20)]
        self.direction = Vector2(0, 0)

class MAIN_GAME:
    def __init__(self) -> None:
        self.snake = SNAKE()
        self.fruit = FRUIT()

    def draw(self):
        self.snake.make_snake()
        self.fruit.make_fruit()
        self.score()

    def update(self):
        self.snake.move_snake()
        self.collision()
        self.bounderies()

    def collision(self):
        if self.snake.body[0] == self.fruit.pos:
            self.fruit.random()
            self.snake.add_snake()
        
    def bounderies(self):
        # check if snake outside of the screen
        if not 0 <= self.snake.body[0].x < cell_number or not 0 <= self.snake.body[0].y < cell_number:
            self.snake.reset()

        # check if snake hits itself
        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.snake.reset()


    def score(self):
        score_text = str(len(self.snake.body) - 3)
        score_surface = game_font.render(score_text, True, (56, 74, 12))
        score_x = cell_size * cell_number - 60
        score_y = cell_size * cell_number - 40
        score_rect = score_surface.get_rect(center = (score_x, score_y))
        screen.blit(score_surface, score_rect)



pygame.init()

cell_size = 30
cell_number = 30
screen = pygame.display.set_mode((cell_size * cell_number, cell_size * cell_number))
clock = pygame.time.Clock()
game_font = pygame.font.Font(None, 25)
apple = pygame.image.load('Pygame/apple.png').convert_alpha()

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 150)

fruit = FRUIT()
snake = SNAKE()
main_game = MAIN_GAME()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == SCREEN_UPDATE:
            main_game.update()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if main_game.snake.direction.y != 1:
                    main_game.snake.direction = Vector2(0, -1)
            if event.key == pygame.K_DOWN:
                if main_game.snake.direction.y != -1:
                    main_game.snake.direction = Vector2(0, 1)
            if event.key == pygame.K_LEFT:
                if main_game.snake.direction.x != 1:
                    main_game.snake.direction = Vector2(-1, 0)
            if event.key == pygame.K_RIGHT:
                if main_game.snake.direction.x != -1:
                    main_game.snake.direction = Vector2(1, 0)

    screen.fill(pygame.Color('pink'))
    main_game.draw()

    pygame.display.update()
    clock.tick(60)