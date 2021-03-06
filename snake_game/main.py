import pygame
from pygame import time
import random

size = 30
width = 800
height = 600
bg = pygame.image.load('resources/background.jpg')

class Apple:
    def __init__(self):
        self.app_block = pygame.image.load('resources/apple_1.jpg')
        self.app_x = size
        self.app_y = size

    def draw_app(self, screen):
        screen.blit(self.app_block, (self.app_x, self.app_y))
        pygame.display.flip()

    def move_app(self, screen):
        self.app_x = random.randint(0,(round(width/size)-1))*size
        self.app_y = random.randint(0,(round(height/size)-1))*size

class Snake:
    def __init__(self, length): 
        self.length = length
        self.block = pygame.image.load("resources/block.jpg")
        self.x = [size]*length
        self.y = [size]*length
        self.direction = 'down'

    def draw(self, screen):
        #screen.fill((0,0,0))
        screen.blit(bg, (0,0))
        for i in range(self.length):
            screen.blit(self.block, (self.x[i], self.y[i]))
        pygame.display.flip()

    def increase_length(self, screen):
        self.length += 1
        self.x.append(0)
        self.y.append(0)

    def move_up(self, screen):
        self.direction = 'up'

    def move_down(self, screen):
        self.direction = 'down'

    def move_left(self, screen):
        self.direction = 'left'

    def move_right(self, screen):
        self.direction = 'right'

    def walk(self, screen):
        for i in range(self.length-1, 0, -1):
            self.x[i] = self.x[i-1]
            self.y[i] = self.y[i-1]

        if self.direction == 'up':
            self.y[0] += -size
            self.draw(screen)
        elif self.direction == 'down':
            self.y[0] += size
            self.draw(screen)
        elif self.direction == 'left':
            self.x[0] += -size
            self.draw(screen)
        elif self.direction == 'right':
            self.x[0] += size
            self.draw(screen)

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Game")
        pygame.mixer.init()
        #Making it a class member so it can be access later on in the program/other class functions
        self.screen = pygame.display.set_mode((width, height))
        #self.screen.fill((0, 0, 0))
        self.snake = Snake(1)
        self.snake.draw(self.screen)
        self.apple = Apple()
        self.apple.draw_app(self.screen)

    def is_collision(self, x1, x2, y1, y2):
        if  y1 == y2:
            if x1 == x2:
                return True
        return False
 
    def is_snake_col(self, x1, y1, other_x, other_y):
        for i in range(len(other_x)):
            if x1 == other_x[i] and y1 == other_y[i]:
                return True
        return False

    def render_background(self):
        self.screen.blit(bg, (0, 0))
        pygame.display.flip()

    def play(self):
        self.render_background()
        self.snake.walk(self.screen)
        self.apple.draw_app(self.screen)
        self.display_score()

        if self.is_collision(self.apple.app_x, self.snake.x[0], self.apple.app_y, self.snake.y[0]):
            self.apple.move_app(self.screen)
            self.snake.increase_length(self.screen)

        if self.is_snake_col(self.snake.x[0], self.snake.y[0], self.snake.x[3:], self.snake.y[3:]):
            # print([self.snake.x[0], self.snake.y[0], self.snake.x[3:], self.snake.y[3:]])
            raise 'Game over'

        # for i in range(2, self.snake.length):
        #     if self.is_collision(self.snake.x[0], self.snake.x[i], self.snake.y[0], self.snake.y[i]):
        #         print("You lose!")
        #         exit(0)
        #This method doesn't work as it checks the whole list of snake positions and has no sense of coordinates
        pygame.display.flip()

        pygame.display.flip()
        time.wait(100)

    def display_score(self):
        font = pygame.font.SysFont('arial', 30)
        score = font.render('Score: ' + str(self.snake.length), True, (255, 255, 255))
        self.screen.blit(score, (0, 0))

    def game_over(self):
        self.render_background()
        font = pygame.font.SysFont('arial', 30)
        line1 = font.render('Game Over! You scored {} points!'.format(self.snake.length), True, (255, 255, 255))
        self.screen.blit(line1, (200, 200))
        line2 = font.render('Press Enter to play again!', True, (255, 255, 255))
        self.screen.blit(line2, (250, 250))
        pygame.display.flip()

    def reset(self):
        self.snake = Snake(1)
        self.apple = Apple()

    def run(self):
        running = True
        pause = False
        while running:
            clock = pygame.time.Clock()
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    running = False
                
                if event.type == pygame.KEYDOWN:
                    if (event.key == pygame.K_UP)&(pause is False):
                        self.snake.move_up(self.screen)

                    if (event.key == pygame.K_DOWN)&(pause is False):
                        self.snake.move_down(self.screen)

                    if (event.key == pygame.K_LEFT)&(pause is False):
                        self.snake.move_left(self.screen)

                    if (event.key == pygame.K_RIGHT)&(pause is False):
                        self.snake.move_right(self.screen)
                    
                    if (event.key == pygame.K_RETURN)&(pause is True):
                        pause = False

            try:
                if not pause:
                    self.play()
            except Exception as e:
                self.game_over()
                pause = True
                self.reset()
            clock.tick(60)
        pygame.quit()

if __name__ == '__main__':
    game = Game()
    game.run()

    