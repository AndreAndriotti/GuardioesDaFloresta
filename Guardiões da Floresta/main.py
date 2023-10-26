import pygame
from pygame.locals import QUIT
from sys import exit
from random import randint
from gameobjects.FireFighter import FireFighter
from gameobjects.Tree import Tree
from gameobjects.Cooldown import Cooldown

WIDTH = 1280
HEIGHT = 720
GREEN = (0,76,8)

TREES_POSITION = [[40,20], [320,60], [640,10], [1040,30], [190,250], 
                  [830,140], [40,410], [320,470], [740,380], [1070,300]]


def Start():
    pygame.init()
    display = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Guardiões da Floresta')
    clock = pygame.time.Clock()
    keys_pressed = set()
    trees_qtt = 10
    fire_cooldown = Cooldown(5)
    
    return display, clock, keys_pressed, trees_qtt, fire_cooldown

def CreateObjects(display, trees_qtt):
    pascal = FireFighter(display, "Pascal", (WIDTH // 2), (HEIGHT // 2 - 30))
    ruby = FireFighter(display, "Ruby", (WIDTH // 2), (HEIGHT // 2 + 30))

    forest = []
    for t in range(trees_qtt):
        new_tree = Tree(display, TREES_POSITION[t][0], TREES_POSITION[t][1])
        forest.append(new_tree)

    return pascal, ruby, forest

def HandleEvents(keys_pressed):
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

def MoveFireFighters(keys_pressed, pascal, ruby):
    isPascalMoving = any(key in keys_pressed for key in pascal.walk_keys)
    isRubyMoving = any(key in keys_pressed for key in ruby.walk_keys)

    if isPascalMoving:
        for key in keys_pressed:
            pascal.Walk(key)

    if isRubyMoving:
        for key in keys_pressed:
            ruby.Walk(key)


def DrawObjects(ruby, pascal, forest):
    ruby.Draw()
    pascal.Draw()
    for tree in forest:
        tree.Draw()

def SetFireOnTree(forest, fire_cooldown, trees_qtt):
    if fire_cooldown.IsReady():
        #tree_sorted = forest[randint(0,trees_qtt)]
        if forest[0].state == "default":
            forest[0].SetFire()
        else:
            forest[0].PutOutFire()
        fire_cooldown.Reset()


def main():
    display, clock, keys_pressed, trees_qtt, fire_cooldown = Start()
    pascal, ruby, forest = CreateObjects(display, trees_qtt)

    while True:
        
        HandleEvents(keys_pressed)
        MoveFireFighters(keys_pressed, pascal, ruby)
        SetFireOnTree(forest, fire_cooldown, trees_qtt)
        
        display.fill(GREEN)
        DrawObjects(pascal, ruby, forest)

        clock.tick(60)
        pygame.display.update()

if __name__ == "__main__":
    main()