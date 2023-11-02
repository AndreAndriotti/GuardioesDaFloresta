import pygame
from scenes.Menu import Menu
from scenes.Gameplay import Gameplay
from scenes.Ranking import Ranking

WIDTH = 1280
HEIGHT = 720

game_state = "intro-menu"

pygame.init()
display = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Guardiões da Floresta')
clock = pygame.time.Clock()
font = pygame.font.Font(None, 50)

def main(game_state):
    while True:
        if game_state == "intro-menu" or game_state == "main-menu":
            game_state = Menu(display, clock, font, game_state)
        elif game_state == "gameplay":
            Gameplay(display, clock, font)
        elif game_state == "ranking":
            game_state = Ranking(display, clock, font)

if __name__ == "__main__":
    main(game_state)