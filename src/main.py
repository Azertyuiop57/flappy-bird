import pygame

BG_IMAGE = pygame.image.load("assets/images/background-day.png")
WIDTH, HEIGHT = BG_IMAGE.get_width(), BG_IMAGE.get_height()

BIRD_IMAGE = pygame.image.load("assets/images/bird.png")

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Flappy Bird de chez Wish")

    def draw_screen(self):
        self.screen.blit(BG_IMAGE, (0, 0))
        self.screen.blit(BIRD_IMAGE, (50, 150))

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
            self.draw_screen()
            pygame.display.update()

def main():
    game = Game()
    game.run()

if __name__ == "__main__":
    main()