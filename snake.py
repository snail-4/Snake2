import pygame, sys
from pygame import math
import random
from pygame import mixer

WIDTH = 832
HEIGHT = 832
cell_size = 64
cell_number = 28
FPS = 30

clock = pygame.time.Clock()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('SNAKE')

pygame.mixer.init()
pygame.init()
mixer.music.load('apple-munch-40169.wav')
mixer.pre_init(44100, -16, 2, 512)
game_font = pygame.font.Font(None, 32)

class Main:
    def __init__(self):
        self.fruit = Fruit()
        self.snake = Snake()

    def update(self):
        self.snake.draw_snake()
        self.fruit.draw_fruit()
        self.check_collisions()
        self.check_fail()
        self.check_edges()
        self.draw_score()

    def check_collisions(self):
        if self.snake.body[0] == self.fruit.pos:
            self.fruit.randomize()
            self.snake.grow()
            mixer.music.play()

        for block in self.snake.body[1:]:
            if block == self.fruit.pos:
                self.fruit.randomize()
            
    def check_fail(self):
            for block in self.snake.body[1:]:
                if block == self.snake.body[0]:
                    self.reset()
    
    def reset(self):
        self.snake.body = [math.Vector2(5, 10), math.Vector2(4,10), math.Vector2(3, 10)]
        self.snake.direction = math.Vector2(0, 0)
        

    def check_edges(self):
        body_copy = self.snake.body
        for i in range(len(self.snake.body)):
            if body_copy[i].x >= cell_number and self.snake.direction.x == 1:
                current_pos = math.Vector2(0, self.snake.body[0].y)
                self.snake.body[i] = current_pos
                current_pos -= math.Vector2(1, 0)
            elif body_copy[i].x <=0 and self.snake.direction.x == -1:
                current_pos = math.Vector2(cell_number, self.snake.body[0].y)
                self.snake.body[i] = current_pos
                current_pos += math.Vector2(0, 1)
            elif body_copy[i].y < 0 and self.snake.direction.y ==-1:
                current_pos = math.Vector2(self.snake.body[0].x, cell_number)
                self.snake.body[i] = current_pos
                current_pos += math.Vector2(0, 1)
            elif body_copy[i].y >= cell_number and self.snake.direction.y == 1:
                current_pos = math.Vector2(self.snake.body[0].x, 0)
                self.snake.body[i] = current_pos
                current_pos += math.Vector2(1,0)

    def draw_score(self):
        sa = pygame.image.load('small_apple.png')
        score_text = str(len(self.snake.body) - 3)
        score_surface = game_font.render(score_text, True, (56, 74, 12))
        score_x = int(832 - 60)
        score_y = int(832 - 60)
        score_rect = score_surface.get_rect(center=(score_x, score_y))
        apple_rect = sa.get_rect(midright=(score_rect.left, score_rect.centery))
        bg_rect = pygame.Rect(apple_rect.left, apple_rect.top, apple_rect.width + apple_rect.width + 6, apple_rect.height)

        pygame.draw.rect(screen, (167, 209, 61), bg_rect)
        screen.blit(score_surface, score_rect)
        screen.blit(sa, apple_rect)

class Snake():
    def __init__(self):
        self.body = [math.Vector2(5, 10), math.Vector2(4,10), math.Vector2(3, 10)]
        self.direction = math.Vector2(1, 0)
        self.new_block = False

        self.head_right = pygame.image.load('alive.png')
        self.head_down = pygame.transform.rotate(self.head_right, 90)
        self.head_left = pygame.transform.rotate(self.head_down, 90)
        self.head_up = pygame.transform.rotate(self.head_left, 90)

        self.body_horizontal = pygame.image.load('body.png')
        self.body_vertical = pygame.transform.rotate(self.body_horizontal, 90)

        self.tail_right = pygame.image.load('tail.png')
        self.tail_down = pygame.transform.rotate(self.tail_right, 90)
        self.tail_left = pygame.transform.rotate(self.tail_down, 90)
        self.tail_up = pygame.transform.rotate(self.tail_left, 90)

        self.turn_br = pygame.image.load('turn.png')
        self.turn_bl = pygame.transform.rotate(self.turn_br, 90)
        self.turn_tl = pygame.transform.rotate(self.turn_bl, 90)
        self.turn_tr = pygame.transform.rotate(self.turn_tl, 90)
                

    def draw_snake(self):
            self.update_tail()
            self.update_head()
            for index, block in enumerate(self.body):
                rect = pygame.Rect(block.x*cell_number, block.y*cell_number, cell_size, cell_size)
                if index == 0:
                   screen.blit(self.head, rect)
                elif index == len(self.body) - 1:
                    screen.blit(self.tail, rect)
                else:
                    previous_block = self.body[index + 1] - block
                    next_block = self.body[index - 1] - block
                    if previous_block.x == next_block.x:
                        screen.blit(self.body_vertical, rect)
                    elif previous_block.y == next_block.y:
                        screen.blit(self.body_horizontal, rect)
                    else:
                        if previous_block.x == -1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == -1:
                            screen.blit(self.turn_br, rect)
                        elif previous_block.x == -1 and next_block.y == 1 or previous_block.y  == 1 and next_block.x == -1:
                            screen.blit(self.turn_bl, rect)
                        elif previous_block.x == 1 and next_block.y == -1 or previous_block.y  == -1 and next_block.x == 1:
                            screen.blit(self.turn_tr, rect)
                        elif previous_block.x == 1 and next_block.y == 1 or previous_block.y  == 1 and next_block.x == 1:
                            screen.blit(self.turn_tl, rect)

    def move(self):
        if self.new_block == True:
            copy_body = self.body[:]
            copy_body.insert(0, copy_body[0] + self.direction)
            self.body = copy_body
            self.new_block = False
        else:
            copy_body = self.body[:-1]
            copy_body.insert(0, copy_body[0] + self.direction)
            self.body = copy_body
        
    def grow(self):
        self.new_block = True
    
    def update_head(self):
        head_dir = self.body[1] - self.body[0]
        if head_dir.x == 1:
            self.head = self.head_left
        elif head_dir.x == -1:
            self.head = self.head_right
        elif head_dir.y == 1:
            self.head = self.head_down
        elif head_dir.y == -1:
            self.head = self.head_up
        
    def update_tail(self):
        tail_dir = self.body[-2] - self.body[-1]
        if tail_dir == math.Vector2(1, 0):
            self.tail = self.tail_right
        elif tail_dir == math.Vector2(-1, 0):
            self.tail = self.tail_left
        elif tail_dir == math.Vector2(0, 1):
            self.tail = self.tail_up
        elif tail_dir == math.Vector2(0, -1):
            self.tail = self.tail_down
            

class Fruit:
    def __init__(self):
        self.apple = pygame.image.load('apple.png')
        self.randomize()
        
    def draw_fruit(self):
        rect = pygame.Rect(self.x*cell_number, self.y*cell_number, cell_size, cell_size)
        screen.blit(self.apple, rect)
        
    def randomize(self):
        self.x = random.randint(0, cell_number - 1)
        self.y = random.randint(0, cell_number - 1)
        self.pos = math.Vector2(self.x, self.y)

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 100)
main = Main()

running = True
while running:
    for event in pygame.event.get():
        clock.tick(FPS)
        if event.type == pygame.QUIT:
            running = False
            sys.exit()
        if event.type == SCREEN_UPDATE:
            main.snake.move()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                if main.snake.direction.y != 1:
                    main.snake.direction = math.Vector2(0, -1)
            if event.key == pygame.K_a:
                if main.snake.direction.x != 1:
                    main.snake.direction = math.Vector2(-1, 0)
            if event.key == pygame.K_s:
                if main.snake.direction.y != -1:
                    main.snake.direction = math.Vector2(0, 1)
            if event.key == pygame.K_d:
                if main.snake.direction.x != -1:
                    main.snake.direction = math.Vector2(1, 0) 

    screen.fill('lime')
    main.update()
    
    pygame.display.flip()

pygame.quit()