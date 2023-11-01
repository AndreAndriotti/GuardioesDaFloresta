import pygame
from scenes.Menu import Menu
from scenes.Gameplay import Gameplay
from gameobjects.Shelter import Shelter

WIDTH = 1280
HEIGHT = 720

game_state = "menu"

pygame.init()
display = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Guardiões da Floresta')
clock = pygame.time.Clock()
font = pygame.font.Font(None, 50)

def main(game_state):
    if game_state == "menu":
        game_state = Menu(display, clock, font)
    if game_state == "gameplay":
        Gameplay()

if __name__ == "__main__":
    main(game_state)