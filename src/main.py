import pygame
import math
import random

BG_IMAGE = pygame.image.load("assets/images/background-day.png")
WIDTH, HEIGHT = BG_IMAGE.get_width(), BG_IMAGE.get_height()

BIRD_IMAGES = [
    pygame.image.load("assets/images/bird1.png"),
    pygame.image.load("assets/images/bird2.png"),
    pygame.image.load("assets/images/bird3.png")
]
B_WIDTH, B_HEIGHT = BIRD_IMAGES.get_width(), BIRD_IMAGES.get_height()

BASE_IMAGE = pygame.image.load("assets/images/base.png")
BASE_HEIGHT = HEIGHT-BASE_IMAGE.get_height()

GAMEOVER_IMAGE = pygame.image.load("assets/images/gameover.png")
PIPE_IMAGE = pygame.image.load("assets/images/pipe.png")
P_WIDTH, P_HEIGHT = PIPE_IMAGE.get_width(), PIPE_IMAGE.get_height()
STARTING_MESSAGE = pygame.image.load("assets/images/message.png")

class Bird:
    def __init__(self, x, y, bird_images, base_height):
        self.x = x
        self.y = y
        self.bird_images = bird_images
        self.base_height = base_height
        self.gravity = 0.5 # Force de la gravité
        self.y_velocity = 0
        self.jump_force = 10 # Force du saut de l'oiseau
        self.y_velocity_max = -10 # Limite de vitesse max
        self.animation_speed = 10
        self.current_frame = 0
        self.frame_counter = 0

    def update(self):
        self.y_velocity -= self.gravity
        self.y -= self.y_velocity

        if self.y_velocity <= self.y_velocity_max:
            self.y_velocity = self.y_velocity_max
        
        self.frame_counter += 1
        if self.frame_counter >= self.animation_speed:
            self.frame_counter = 0
            self.current_frame = (self.current_frame + 1) % len(self.bird_images)
            
        if self.is_touching_ceiling() or self.is_colliding_with_base():
            return True
        return False

    def draw(self, screen):
        screen.blit(self.bird_images[self.current_frame], (self.x, self.y))
        
    def jump(self):
        self.y_velocity = self.jump_force

    def is_colliding_with_base(self):
        return self.y + self.bird_images[self.current_frame].get_height() > self.base_height

    def is_touching_ceiling(self):
        return self.y < 0 
    
    def is_touching_pipe(self, pipe):
        x_center = self.x + B_WIDTH // 2
        y_center = self.y + B_HEIGHT // 2
        if x_center > pipe.x - 26 and x_center < pipe.x + 26:
            if y_center > pipe.y + 75 or y_center < pipe.y - 75:
                return True
        return False

class Pipe:
    def __init__(self, x, y):
        self.x = x
        self.init_x = WIDTH
        self.y = y
        self.speed = 1

    def update(self):
        self.x -= self.speed
        if self.x < 0:
            self.x = self.init_x
            self.y = random.randint(100, BASE_HEIGHT-100)
    
    def draw(self, screen):
        screen.blit(PIPE_IMAGE, (self.x-P_WIDTH//2, self.y-P_HEIGHT//2))

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Flappy Bird de chez Wish")
        self.bird = Bird(50, BASE_HEIGHT//2, BIRD_IMAGES, BASE_HEIGHT)
        self.pipe1 = Pipe(WIDTH, random.randint(50, BASE_HEIGHT-100))
        self.pipe2 = Pipe(WIDTH//2, random.randint(50, BASE_HEIGHT-100))
        self.is_game_over = False
        self.game_started = False
        self.counter = 0

    def draw_screen(self):
        self.screen.blit(BG_IMAGE, (0, 0))
        if not self.game_started:
            self.screen.blit(STARTING_MESSAGE, (WIDTH//2-STARTING_MESSAGE.get_width()//2, math.cos(self.counter / 20) * 5 + BASE_HEIGHT//2-STARTING_MESSAGE.get_height()//2))
        else:
            self.bird.draw(self.screen)
            self.pipe1.draw(self.screen)
            self.pipe2.draw(self.screen)

        self.screen.blit(BASE_IMAGE, (0, BASE_HEIGHT))
            
        if self.is_game_over:
            self.screen.blit(GAMEOVER_IMAGE, (WIDTH//2-GAMEOVER_IMAGE.get_width()//2, math.cos(self.counter / 40) * 5 + BASE_HEIGHT//2-GAMEOVER_IMAGE.get_height()//2))
    
    def run(self):
        clock = pygame.time.Clock()
        running = True
        while running:
            self.counter += 1
            clock.tick(60) # Limiter les FPS à 60 par seconde
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                        self.game_started = True if not self.game_started else self.game_started # Commence le jeu s'il n'est pas commencé, sinon rien ne se passe.

                        if self.is_game_over:
                            self.bird = Bird(50, BASE_HEIGHT//2, BIRD_IMAGES, BASE_HEIGHT) # Créer un nouvel oiseau si le dernier est mort
                            self.pipe1 = Pipe(WIDTH, random.randint(50, BASE_HEIGHT-100))
                            self.pipe2 = Pipe(WIDTH//2, random.randint(50, BASE_HEIGHT-100))
                            self.is_game_over = False

                        self.bird.jump()
            
            if not self.is_game_over and self.game_started:
                if self.bird.update() or self.bird.is_touching_pipe(self.pipe1) or self.bird.is_touching_pipe(self.pipe2):
                    self.is_game_over = True
                self.pipe1.update()
                self.pipe2.update()
            self.draw_screen()
            pygame.display.update()

        pygame.quit()

def main():
    game = Game()
    game.run()

if __name__ == "__main__":
    main()