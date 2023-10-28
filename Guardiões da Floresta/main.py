import pygame
from pygame.locals import QUIT
from sys import exit
from random import randint
from math import sqrt
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
    trees_default_qtt = trees_qtt
    fire_cooldown = Cooldown(5)
    
    return display, clock, keys_pressed, trees_qtt, trees_default_qtt, fire_cooldown

def CreateObjects(display, trees_qtt):
    firefighter_size = (38,66)
    pascal = FireFighter(display, "Pascal", ((WIDTH // 2), (HEIGHT // 2 - 30)), firefighter_size)
    ruby = FireFighter(display, "Ruby", ((WIDTH // 2), (HEIGHT // 2 + 30)), firefighter_size)

    tree_size = (187,243)
    forest = []
    for t in range(trees_qtt):
        new_tree = Tree(display, (TREES_POSITION[t][0], TREES_POSITION[t][1]), tree_size)
        forest.append(new_tree)

    return pascal, ruby, forest

def FireFighterInteractions(firefighter, trees_default_qtt):
    if len(firefighter.nearby_objects) > 0:
        object = firefighter.nearby_objects[0]
    
        if firefighter.is_interacting:
            if firefighter.state == "put-out-fire": 
                if firefighter.put_out_fire_cooldown.IsReady():
                    if object.state == "on-fire":
                        firefighter.PutOutFire(object)
                        trees_default_qtt += 1

        else:  
            if object.name == "tree":
                if object.state == "on-fire":
                    firefighter.StartPutOutFire()
    
    return trees_default_qtt

def HandleEvents(keys_pressed, pascal, ruby, trees_default_qtt):
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.KEYDOWN:
            key_pressed = event.key
            keys_pressed.add(key_pressed)

            if key_pressed == pygame.K_ESCAPE:
                pygame.quit()
                exit()  

        if event.type == pygame.KEYUP:
            key_released = event.key
            keys_pressed.discard(key_released)

            if key_released == pygame.K_SPACE:
                pascal.is_interacting = False

            if key_released == pygame.K_RETURN:
                ruby.is_interacting = False
        
    if pygame.K_SPACE in keys_pressed:
            trees_default_qtt = FireFighterInteractions(pascal, trees_default_qtt)
    
    if pygame.K_RETURN in keys_pressed:
            trees_default_qtt = FireFighterInteractions(ruby, trees_default_qtt)
    
    return trees_default_qtt

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

def SetFireOnTree(forest, fire_cooldown, trees_qtt, trees_default_qtt):
    if fire_cooldown.IsReady():
        if trees_default_qtt > 0:
            tree_sorted = forest[randint(0,trees_qtt-1)]
            while (tree_sorted.state != "default"):
                tree_sorted = forest[randint(0,trees_qtt-1)]
            
            tree_sorted.SetFire()
            trees_default_qtt -= 1
            fire_cooldown.Reset()
    
    return trees_default_qtt

def CharTrees(forest):
    for tree in forest:
        if tree.state == "on-fire":
            if tree.char_cooldown.IsReady():
                tree.Char()

def CalcDistance(x1, y1, x2, y2):
    return sqrt((x1 - x2)**2 + (y1 - y2)**2)

def CalcPivot(object):
    object_pivot = []
    object_pivot.append(object.x + object.width // 2)
    object_pivot.append(object.y + object.length // 2)
    return object_pivot

def CheckTreesDistances(firefighter, forest):
    for tree in forest:
        firefighter_pivot = CalcPivot(firefighter)
        tree_pivot = CalcPivot(tree)
        distance = CalcDistance(firefighter_pivot[0], firefighter_pivot[1], tree_pivot[0], tree_pivot[1])

        if distance <= 100:
            if tree not in firefighter.nearby_objects:
                firefighter.nearby_objects.append(tree)
        else:
            if tree in firefighter.nearby_objects:
                firefighter.nearby_objects.remove(tree)

def main():
    display, clock, keys_pressed, trees_qtt, trees_default_qtt, fire_cooldown = Start()
    pascal, ruby, forest = CreateObjects(display, trees_qtt)

    while True:
        
        trees_default_qtt = HandleEvents(keys_pressed, pascal, ruby, trees_default_qtt)
        MoveFireFighters(keys_pressed, pascal, ruby)
        CheckTreesDistances(pascal, forest)
        CheckTreesDistances(ruby, forest)
        trees_default_qtt = SetFireOnTree(forest, fire_cooldown, trees_qtt, trees_default_qtt)
        CharTrees(forest)

        display.fill(GREEN)
        DrawObjects(pascal, ruby, forest)

        clock.tick(60)
        pygame.display.update()

if __name__ == "__main__":
    main()