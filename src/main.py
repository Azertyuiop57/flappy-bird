import pygame

BG_IMAGE = pygame.image.load("assets/images/background-day.png")
WIDTH, HEIGHT = BG_IMAGE.get_width(), BG_IMAGE.get_height()

BIRD_IMAGE = pygame.image.load("assets/images/bird.png")

BASE_IMAGE = pygame.image.load("assets/images/base.png")
BASE_HEIGHT = HEIGHT-BASE_IMAGE.get_height()

GAMEOVER_IMAGE = pygame.image.load("assets/images/gameover.png")
PIPE_IMAGE = pygame.image.load("assets/images/pipe.png")

class Bird:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.gravity = 0.5 # Force de la gravité
        self.y_velocity = 0
        self.jump_force = 10 # Force du saut de l'oiseau

    def update(self):
        if self.y_velocity > -10: # Limite de vitesse max
            self.y_velocity -= self.gravity
        self.y -= self.y_velocity

    def draw(self, screen):
        screen.blit(BIRD_IMAGE, (self.x, self.y))
        
    def jump(self):
        self.y_velocity = self.jump_force

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Flappy Bird de chez Wish")
        self.bird = Bird(50, BASE_HEIGHT//2)

    def draw_screen(self):
        self.screen.blit(BG_IMAGE, (0, 0))
        self.screen.blit(BASE_IMAGE, (0, BASE_HEIGHT))
        self.bird.draw(self.screen)
    
    def run(self):
        clock = pygame.time.Clock()
        running = True
        while running:
            clock.tick(60) # Limiter les FPS à 60 par seconde
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                        self.bird.jump()
                        
            self.bird.update()
            self.draw_screen()
            pygame.display.update()

        pygame.quit()

def main():
    game = Game()
    game.run()

if __name__ == "__main__":
    main()