import pygame
from pygame.locals import QUIT
from sys import exit
from gameobjects.FireFighter import FireFighter
from gameobjects.Tree import Tree

WIDTH = 1280
HEIGHT = 720
GREEN = (0, 76, 8)

pygame.init()
display = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Guardiões da Floresta')
clock = pygame.time.Clock()

def GenerateTrees():
    tree0 = Tree(display, (WIDTH // 10), (HEIGHT + 30))
    tree1 = Tree(display, ((WIDTH // 10) + (tree0.get_width())), (HEIGHT + 30))
    tree2 = Tree(display, ((WIDTH // 10) (tree0.get_width())), (HEIGHT + 30))
    tree3 = Tree(display, (WIDTH // 10), (HEIGHT + 30))
    tree4 = Tree(display, (WIDTH // 10), (HEIGHT // 2))
    tree5 = Tree(display, (WIDTH // 10), (HEIGHT // 2 + 30))
    tree6 = Tree(display, (WIDTH // 10), (HEIGHT // 2 + 30))
    tree7 = Tree(display, (WIDTH // 10), (HEIGHT // 2 + 30))
    tree8 = Tree(display, (WIDTH // 10), (HEIGHT // 2 + 30))
    tree9 = Tree(display, (WIDTH // 10), (HEIGHT // 2))

pascal = FireFighter(display, "Pascal", (WIDTH // 2), (HEIGHT // 2 - 30))
ruby = FireFighter(display, "Ruby", (WIDTH // 2), (HEIGHT // 2 + 30))
GenerateTrees()


keys_pressed = set()

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.KEYDOWN:
            key_pressed = event.key

            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                exit()

            keys_pressed.add(key_pressed)

        if event.type == pygame.KEYUP:
            key_released = event.key
            keys_pressed.discard(key_released)

    isPascalMoving = any(key in keys_pressed for key in pascal.walk_keys)
    isRubyMoving = any(key in keys_pressed for key in ruby.walk_keys)

    if isPascalMoving:
        for key in keys_pressed:
            pascal.Walk(key)

    if isRubyMoving:
        for key in keys_pressed:
            ruby.Walk(key)

    display.fill(GREEN)
    
    ruby.Draw()
    pascal.Draw()

    clock.tick(60)
    pygame.display.update()
