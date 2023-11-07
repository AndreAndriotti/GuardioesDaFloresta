import pygame
from scenes.Menu import Menu
from scenes.Gameplay import Gameplay
from scenes.GameOver import GameOver
from scenes.Instructions import Instructions
from scenes.Ranking import Ranking

WIDTH = 1280
HEIGHT = 720

game_state = "intro-menu"
volume = 1
is_music_playing = False

pygame.init()
display = pygame.display.set_mode((WIDTH, HEIGHT))
monkey_icon = pygame.image.load("images/UI/MonkeyIcon.png")
pygame.display.set_icon(monkey_icon)
pygame.display.set_caption('Guardiões da Floresta')
clock = pygame.time.Clock()
font = pygame.font.Font(None, 50)

def main(game_state, volume, is_music_playing):
    while True:
        if game_state == "intro-menu" or game_state == "main-menu":
            game_state, volume, is_music_playing = Menu(display, clock, font, volume, is_music_playing, game_state)
        elif game_state == "gameplay":
            game_state, is_music_playing = Gameplay(display, clock, font, volume)
        elif game_state == "game-over":
            game_state, is_music_playing = GameOver(display, clock, font, volume)
        elif game_state == "instructions":
            game_state = Instructions(display, clock, volume)
        elif game_state == "ranking":
            game_state = Ranking(display, clock, font, volume)

if __name__ == "__main__":
    main(game_state, volume, is_music_playing)