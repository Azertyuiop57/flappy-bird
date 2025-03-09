import pygame
import math

BG_IMAGE = pygame.image.load("assets/images/background-day.png")
WIDTH, HEIGHT = BG_IMAGE.get_width(), BG_IMAGE.get_height()

BIRD_IMAGES = [
    pygame.image.load("assets/images/bird1.png"),
    pygame.image.load("assets/images/bird2.png"),
    pygame.image.load("assets/images/bird3.png")
]

BASE_IMAGE = pygame.image.load("assets/images/base.png")
BASE_HEIGHT = HEIGHT-BASE_IMAGE.get_height()

GAMEOVER_IMAGE = pygame.image.load("assets/images/gameover.png")
PIPE_IMAGE = pygame.image.load("assets/images/pipe.png")
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

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Flappy Bird de chez Wish")
        self.bird = Bird(50, BASE_HEIGHT//2, BIRD_IMAGES, BASE_HEIGHT)
        self.is_game_over = False
        self.game_started = False
        self.counter = 0

    def draw_screen(self):
        self.screen.blit(BG_IMAGE, (0, 0))
        self.screen.blit(BASE_IMAGE, (0, BASE_HEIGHT))
        if not self.game_started:
            self.screen.blit(STARTING_MESSAGE, (WIDTH//2-STARTING_MESSAGE.get_width()//2, math.cos(self.counter / 20) * 5 + BASE_HEIGHT//2-STARTING_MESSAGE.get_height()//2))
        else:
            self.bird.draw(self.screen)
            
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
                            self.is_game_over = False

                        self.bird.jump()
            
            if not self.is_game_over and self.game_started:
                self.is_game_over = self.bird.update()
            self.draw_screen()
            pygame.display.update()

        pygame.quit()

def main():
    game = Game()
    game.run()

if __name__ == "__main__":
    main()