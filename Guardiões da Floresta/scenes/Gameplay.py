import pygame
from pygame.locals import QUIT
from sys import exit
from random import randint
from math import sqrt
from scenes.Menu import Menu
from gameobjects.Shelter import Shelter
from gameobjects.FireFighter import FireFighter
from gameobjects.Tree import Tree
from gameobjects.Civilian import Civilian
from gameobjects.Cooldown import Cooldown

WIDTH = 1280
HEIGHT = 720

GREEN = (0,76,8)
WHITE = (255,255,255)

TREES_POSITION = [[40,20], [320,60], [640,10], [1040,30], [190,250], 
                  [830,140], [40,410], [320,470], [740,380], [1070,300]]

game_state = "menu"

pygame.init()
display = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Guardiões da Floresta')
clock = pygame.time.Clock()
font = pygame.font.Font(None, 50)

def Start():
    
    keys_pressed = set()
    trees_qtt = 10
    trees_default_qtt = trees_qtt
    fire_cooldown = Cooldown(7)
    monkeys_qtt = 0
    monkey_cooldown = Cooldown(10)
    civilians = []
    civilian_cooldown = Cooldown(5)
    
    return keys_pressed, trees_qtt, trees_default_qtt, fire_cooldown, monkeys_qtt, monkey_cooldown, civilians, civilian_cooldown

def CreateObjects(display, trees_qtt):
    shelter_size = (325,227)
    shelter = Shelter(display, ((WIDTH // 2 - shelter_size[0]//2), (HEIGHT // 2 - shelter_size[1]//2)), shelter_size) 
    
    firefighter_size = (38,66)
    pascal = FireFighter(display, "Pascal", ((WIDTH // 2 - 40), (HEIGHT // 2 + 90)), firefighter_size)
    ruby = FireFighter(display, "Ruby", ((WIDTH // 2 + 5), (HEIGHT // 2 + 90)), firefighter_size)

    tree_size = (187,243)
    forest = []
    for t in range(trees_qtt):
        new_tree = Tree(display, (TREES_POSITION[t][0], TREES_POSITION[t][1]), tree_size)
        forest.append(new_tree)

    return shelter, pascal, ruby, forest

def FireFighterInteractions(firefighter, trees_default_qtt, monkeys_qtt):
    if len(firefighter.nearby_civilians) > 0:
        civilian = firefighter.nearby_civilians[0]
    else:
        civilian = None

    if len(firefighter.nearby_objects) > 0:
        object = firefighter.nearby_objects[0]
    else:
        object = None
        
    if firefighter.is_interacting:
        if firefighter.state == "rescue-civilian":
            if firefighter.rescue_civilian_cooldown.IsReady():
                if civilian != None:
                    if civilian.state == "walk":
                        firefighter.RescueCivilian(civilian)
                        firefighter.nearby_civilians.remove(civilian)

        elif firefighter.state == "put-out-fire":
            if firefighter.put_out_fire_cooldown.IsReady():
                if object.state == "on-fire" or object.state == "on-fire-with-monkey":
                    firefighter.PutOutFire(object)
                    trees_default_qtt += 1

        elif firefighter.state == "rescue-monkey":
            if firefighter.rescue_monkey_cooldown.IsReady():
                if object.state == "with-monkey":
                    firefighter.RescueMonkey(object)
                    monkeys_qtt -= 1

    else:
        if civilian == None:
            if object != None:
                if object.name == "tree":
                    if firefighter.state != "with-monkey":
                        if object.state == "on-fire" or object.state == "on-fire-with-monkey":
                            firefighter.StartPutOutFire()

                        elif object.state == "with-monkey":
                            firefighter.StartRescueMonkey()

                elif object.name == "shelter":
                    if firefighter.state == "with-monkey":
                        firefighter.DeliverMonkey()

        else:
            if firefighter.state != "with-monkey":
                    firefighter.StartRescueCivilian()
    
    return trees_default_qtt, monkeys_qtt

def HandleEvents(keys_pressed, pascal, ruby, trees_default_qtt, monkeys_qtt):
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
                pascal.FixSpritePosition()
                if pascal.state != "with-monkey":
                    pascal.state = "default"

            if key_released == pygame.K_RETURN:
                ruby.is_interacting = False
                ruby.FixSpritePosition()
                if ruby.state != "with-monkey":
                    ruby.state = "default"
        
    if pygame.K_SPACE in keys_pressed:
            trees_default_qtt, monkeys_qtt = FireFighterInteractions(pascal, trees_default_qtt, monkeys_qtt)
    
    if pygame.K_RETURN in keys_pressed:
            trees_default_qtt, monkeys_qtt = FireFighterInteractions(ruby, trees_default_qtt, monkeys_qtt)
    
    return trees_default_qtt, monkeys_qtt

def MoveFireFighters(keys_pressed, pascal, ruby):
    isPascalMoving = any(key in keys_pressed for key in pascal.walk_keys)
    isRubyMoving = any(key in keys_pressed for key in ruby.walk_keys)

    if isPascalMoving:
        for key in keys_pressed:
            pascal.Walk(key, WIDTH, HEIGHT)

    if isRubyMoving:
        for key in keys_pressed:
            ruby.Walk(key, WIDTH, HEIGHT)

def DrawObjects(shelter, ruby, pascal, civilians, forest):
    shelter.Draw()
    ruby.Draw()
    pascal.Draw()
    for civilian in civilians:
        civilian.Draw(civilians)
    for tree in forest:
        tree.Draw()

def SetFireOnTree(forest, fire_cooldown, trees_qtt, trees_default_qtt):
    if fire_cooldown.IsReady():
        if trees_default_qtt > 0:
            tree_sorted = forest[randint(0,trees_qtt-1)]
            while (tree_sorted.state != "default" and tree_sorted.state != "with-monkey"):
                tree_sorted = forest[randint(0,trees_qtt-1)]
            
            tree_sorted.SetFire()
            trees_default_qtt -= 1
            fire_cooldown.Reset()
    
    return trees_default_qtt

def CharTrees(forest, monkeys_qtt, pascal, ruby):
    for tree in forest:
        if tree.state == "on-fire" or tree.state == "on-fire-with-monkey":
            if tree.char_cooldown.IsReady():
                tree.Char()
                if tree.state == "on-fire-with-monkey":
                    monkeys_qtt -= 1
                    UpdateGlobalScore(-30, pascal, ruby)
                else:
                    UpdateGlobalScore(-10, pascal, ruby)

    return monkeys_qtt

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

def CheckShelterDistance(firefighter, shelter):
    firefighter_pivot = CalcPivot(firefighter)
    shelter_pivot = CalcPivot(shelter)
    distance = CalcDistance(firefighter_pivot[0], firefighter_pivot[1], shelter_pivot[0], shelter_pivot[1]+50)

    if distance <= 50:
        if shelter not in firefighter.nearby_objects:
            firefighter.nearby_objects.append(shelter)
    else:
        if shelter in firefighter.nearby_objects:
            firefighter.nearby_objects.remove(shelter)

def CheckCivilianDistance(firefighter, civilians):
    for civilian in civilians:
        firefighter_pivot = CalcPivot(firefighter)
        civilian_pivot = CalcPivot(civilian)
        distance = CalcDistance(firefighter_pivot[0], firefighter_pivot[1], civilian_pivot[0], civilian_pivot[1])

        if distance <= 50:
            if civilian not in firefighter.nearby_civilians:
                if civilian.state != "rescued":
                    firefighter.nearby_civilians.append(civilian)
        else:
            if civilian in firefighter.nearby_civilians:
                firefighter.nearby_civilians.remove(civilian)

def CheckDistances(pascal, ruby, forest, shelter, civilians):
    CheckTreesDistances(pascal, forest) 
    CheckTreesDistances(ruby, forest)
    CheckShelterDistance(pascal, shelter)
    CheckShelterDistance(ruby, shelter)
    CheckCivilianDistance(pascal, civilians)
    CheckCivilianDistance(ruby, civilians)

def SpawnMonkey(forest, monkey_cooldown, monkeys_qtt, trees_qtt, trees_default_qtt):
    if monkey_cooldown.IsReady():
        if trees_default_qtt > 0 and trees_default_qtt > monkeys_qtt:
            tree_sorted = forest[randint(0,trees_qtt-1)]
            while (tree_sorted.state != "default"):
                tree_sorted = forest[randint(0,trees_qtt-1)]
            
            tree_sorted.SpawnMonkey()
            monkeys_qtt += 1
            monkey_cooldown.Reset()

    return monkeys_qtt

def SpawnCivilian(civilian_cooldown, display, civilians):
    if civilian_cooldown.IsReady():
        sorted_direction = randint(0,1)
        if sorted_direction == 0:
            direction = "right"
            x = 0
        else:
            direction = "left"
            x = WIDTH
        y = randint(0, HEIGHT-71)
        
        civilian_size = (35,71)
        new_civilian = Civilian(display, (x,y), (civilian_size[0], civilian_size[1]), direction)
        civilians.append(new_civilian)
        civilian_cooldown.Reset()

def CheckCiviliansPosition(civilians, pascal, ruby):
    for civilian in civilians:
        if civilian.x < -35 or civilian.x > WIDTH:
            if civilian in pascal.nearby_civilians:
                pascal.nearby_civilians.remove(civilian)
            if civilian in ruby.nearby_civilians:
                ruby.nearby_civilians.remove(civilian)
            civilians.remove(civilian)
            UpdateGlobalScore(-30, pascal, ruby)

def UpdateGlobalScore(points, pascal, ruby):
    pascal.score += points // 2
    ruby.score += points // 2

def ShowScore(display, pascal, ruby, font):
    pascal_score = font.render(f"Pascal: {pascal.score}", True, WHITE)
    global_score = font.render(f"{pascal.score + ruby.score}", True, WHITE)
    ruby_score = font.render(f"Ruby: {ruby.score}", True, WHITE)
    
    display.blit(pascal_score, (50, 20))
    display.blit(global_score, ((WIDTH//2 - global_score.get_width()//2), 20))
    display.blit(ruby_score, ((WIDTH - ruby_score.get_width()) - 50, 20))


def Gameplay():
    keys_pressed, trees_qtt, trees_default_qtt, fire_cooldown, monkeys_qtt, monkey_cooldown, civilians, civilian_cooldown = Start()
    shelter, pascal, ruby, forest = CreateObjects(display, trees_qtt)

    while True:
        #print(pascal.nearby_civilians)
        trees_default_qtt, monkeys_qtt = HandleEvents(keys_pressed, pascal, ruby, trees_default_qtt, monkeys_qtt)
        MoveFireFighters(keys_pressed, pascal, ruby)
        CheckDistances(pascal, ruby, forest, shelter, civilians)
        trees_default_qtt = SetFireOnTree(forest, fire_cooldown, trees_qtt, trees_default_qtt)
        monkeys_qtt = SpawnMonkey(forest, monkey_cooldown, monkeys_qtt, trees_qtt, trees_default_qtt)
        monkeys_qtt = CharTrees(forest, monkeys_qtt, pascal, ruby)
        SpawnCivilian(civilian_cooldown, display, civilians)
        CheckCiviliansPosition(civilians, pascal, ruby)

        display.fill(GREEN)
        DrawObjects(shelter, ruby, pascal, civilians, forest)
        ShowScore(display, pascal, ruby, font)

        clock.tick(60)
        pygame.display.update()

def main(game_state):
    if game_state == "menu":
        game_state = Menu(display, clock, font)
    if game_state == "gameplay":
        Gameplay()

if __name__ == "__main__":
    main(game_state)