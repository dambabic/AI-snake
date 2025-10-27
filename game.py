import pygame
import random
from enum import Enum
from collections import namedtuple
import numpy as np

pygame.init()
font = pygame.font.Font('arial.ttf', 25)
#font = pygame.font.SysFont('arial', 25)

CiscoLine = pygame.image.load('./images/CiscoLine.png')
CiscoLine = pygame.transform.scale(CiscoLine, (640, 2))
CiscoLine_rect = CiscoLine.get_rect()
CiscoLine_rect.topleft = (0, 400)

CiscoLine2 = pygame.image.load('./images/CiscoLine.png')
CiscoLine2 = pygame.transform.scale(CiscoLine2, (640, 2))
CiscoLine2_rect = CiscoLine2.get_rect()
CiscoLine2_rect.topleft = (0, 430)


SpeedUP = pygame.image.load('./images/SpeedUP.png')
SpeedUP = pygame.transform.scale(SpeedUP, (40, 30))
SpeedUP_rect = SpeedUP.get_rect()
SpeedUP_rect.topleft = (340, 475)

SpeedDOWN = pygame.image.load('./images/SpeedDOWN.png')
SpeedDOWN = pygame.transform.scale(SpeedDOWN, (40, 30))
SpeedDOWN_rect = SpeedDOWN.get_rect()
SpeedDOWN_rect.topleft = (260, 475)

class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4

Point = namedtuple('Point', 'x, y')

# rgb colors
WHITE = (255, 255, 255)
RED = (200,0,0)
BLUE1 = (0, 0, 255)
BLUE2 = (0, 100, 255)
BLACK = (0,0,0)
GREEN = (34, 154, 48)
BLUE3 = (0, 140, 140)
ORANGE = (206, 76, 29)

BLOCK_SIZE = 20
SPEED = 10

class SnakeGameAI:

    def __init__(self, w=640, h=480):
        self.w = 640
        self.h = 400
        self.sp = SPEED
        # init display
        self.display = pygame.display.set_mode((640, 520))
        pygame.display.set_caption('NN Demo: AI playing Snake (32x24)')
        
        self.clock = pygame.time.Clock()
        self.reset()

    def reset(self):
        # init game state
        self.direction = Direction.RIGHT

        self.head = Point(self.w/2, self.h/2)
        self.snake = [self.head,
                      Point(self.head.x-BLOCK_SIZE, self.head.y),
                      Point(self.head.x-(2*BLOCK_SIZE), self.head.y)]

        self.score = 0
        self.r = 0
        self.g = 0
        # self.sp = 10

        self.food = None
        self._place_food()
        self.frame_iteration = 0

    def _place_food(self):
        x = random.randint(0, (self.w-BLOCK_SIZE )//BLOCK_SIZE )*BLOCK_SIZE
        y = random.randint(0, (self.h-BLOCK_SIZE )//BLOCK_SIZE )*BLOCK_SIZE
        self.food = Point(x, y)
        if self.food in self.snake:
            self._place_food()

    def play_step(self, action):
        self.frame_iteration += 1
        # 1. collect user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        
        # 2. move
        self._move(action) # update the head
        self.snake.insert(0, self.head)
        
        # 3. check if game over
        reward = 0
        game_over = False
        if self.is_collision() or self.frame_iteration > 100*len(self.snake):
            game_over = True
            reward = -10
            return reward, game_over, self.score

        # 4. place new food or just move
        if self.head == self.food:
            self.score += 1
            reward = 10
            self._place_food()
        else:
            self.snake.pop()

        # Setting the speed of the game *******************************************************************************
        pos = pygame.mouse.get_pos()
        if SpeedUP_rect.collidepoint(pos) and pygame.mouse.get_pressed()[0]:
            pygame.time.delay(200)
            if self.sp == 10:
                self.sp = 20
            elif self.sp == 20:
                self.sp = 40
            elif self.sp == 40:
                self.sp = 100
            elif self.sp == 100:
                self.sp = 400

            print('Speed UP', pos, self.sp)

        if SpeedDOWN_rect.collidepoint(pos) and pygame.mouse.get_pressed()[0]:
            pygame.time.delay(200)
            if self.sp == 10:
                self.sp = 10
            elif self.sp == 20:
                self.sp = 10
            elif self.sp == 40:
                self.sp = 20
            elif self.sp == 100:
                self.sp = 40
            elif self.sp == 400:
                self.sp = 100

            print('Speed DOWN', pos, self.sp)

        GameSpeed = self.sp

        # 5. update ui and clock
        self._update_ui()
        self.clock.tick(GameSpeed)
        # 6. return game over and score
        return reward, game_over, self.score

    def is_collision(self, pt=None):
        if pt is None:
            pt = self.head
        # hits boundary
        if pt.x > self.w - BLOCK_SIZE or pt.x < 0 or pt.y > self.h - BLOCK_SIZE or pt.y < 0:
            return True
        # hits itself
        if pt in self.snake[1:]:
            return True

        return False

    def data(self, s, r, g):
        self.r = r
        self.g = g
        # self.sp = sp
        print(' Game:', g, '| Score:', s, '| Record:', r, '| Speed:', self.sp)

    def _update_ui(self):
        self.display.fill(BLACK)

        for pt in self.snake:
            pygame.draw.rect(self.display, BLUE2, pygame.Rect(pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(self.display, BLUE1, pygame.Rect(pt.x+4, pt.y+4, 12, 12))

        pygame.draw.rect(self.display, GREEN, pygame.Rect(self.food.x, self.food.y, BLOCK_SIZE, BLOCK_SIZE))

        # DIsplay text about the game
        font = pygame.font.Font('freesansbold.ttf', 22)
        text1 = font.render("AI playing Snake game", True, BLUE2)
        self.display.blit(text1, [200, 405])

        font = pygame.font.Font('arial.ttf', 16)
        text2 = font.render("Score: " + str(self.score), True, WHITE)
        self.display.blit(text2, [130, 445])

        font = pygame.font.Font('arial.ttf', 16)
        text3 = font.render("Record: "+ str(self.r), True, WHITE)
        self.display.blit(text3, [287, 445])

        font = pygame.font.Font('arial.ttf', 16)
        text4 = font.render("Game: "+ str(self.g), True, WHITE)
        self.display.blit(text4, [450, 445])

        font = pygame.font.Font('arial.ttf', 10)
        text5 = font.render("Speed", True, BLUE2)
        self.display.blit(text5, [306, 478])
        
        font = pygame.font.Font('arial.ttf', 8)
        if self.sp == 10:
            text6 = font.render("1 of 5", True, WHITE)
        elif self.sp == 20:
            text6 = font.render("2 of 5", True, WHITE)
        elif self.sp == 40:
            text6 = font.render("3 of 5", True, WHITE)
        elif self.sp == 100:
            text6 = font.render("4 of 5", True, WHITE)
        elif self.sp == 400:
            text6 = font.render("5 of 5", True, WHITE)
        self.display.blit(text6, [312, 490])

        # font = pygame.font.Font('arial.ttf', 20)
        # text6 = font.render("ooooo", True, WHITE)
        # self.display.blit(text6, [280, 497])

        # Draw status area under the game
        self.display.blit(CiscoLine, CiscoLine_rect)
        self.display.blit(CiscoLine2, CiscoLine2_rect)

        self.display.blit(SpeedUP, SpeedUP_rect)
        self.display.blit(SpeedDOWN, SpeedDOWN_rect)

        pygame.display.flip()

    def _move(self, action):
        # [straight, right, left]

        clock_wise = [Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP]
        idx = clock_wise.index(self.direction)

        if np.array_equal(action, [1, 0, 0]):
            new_dir = clock_wise[idx] # no change
        elif np.array_equal(action, [0, 1, 0]):
            next_idx = (idx + 1) % 4
            new_dir = clock_wise[next_idx] # right turn r -> d -> l -> u
        else: # [0, 0, 1]
            next_idx = (idx - 1) % 4
            new_dir = clock_wise[next_idx] # left turn r -> u -> l -> d

        self.direction = new_dir

        x = self.head.x
        y = self.head.y
        if self.direction == Direction.RIGHT:
            x += BLOCK_SIZE
        elif self.direction == Direction.LEFT:
            x -= BLOCK_SIZE
        elif self.direction == Direction.DOWN:
            y += BLOCK_SIZE
        elif self.direction == Direction.UP:
            y -= BLOCK_SIZE

        self.head = Point(x, y)
