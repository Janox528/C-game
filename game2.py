import pygame
import random
import sys
from tkinter import *
from tkinter import messagebox


if not pygame.font: print('Fehler pygame.font Modul konnte nicht geladen werden!')
if not pygame.mixer: print('Fehler pygame.mixer Modul konnte nicht geladen werden!')

pygame.font.init()

class Button():
    def __init__(self,x,y,sizeX,sizeY,msg):
        self.x = x
        self.y = y
        self.sizeY = sizeY
        self.sizeX = sizeX
        self.msg = msg
    def draw(self,screen):
        pygame.draw.rect(screen, (0, 0, 255), [self.x, self.y, self.sizeX, self.sizeY])
    def getMsg(self):
        return self.msg
    def getX(self):
        return self.x
    def getY(self):
        return self.y
    def getSizeX(self):
        return self.sizeX
    def getSizeY(self):
        return self.sizeY
        
        
class Interface():
    buttonlist = []
    def __init__(self,name):
        self.name =  name
    def createButton(self,x,y,sizeX,sizeY,msg):
        self.buttonlist.append(Button(x,y,sizeX,sizeY,msg))
    def deleteAllButtons(self):
        self.buttonList = []
    def checkButtonHit(self,pos):
        for b in self.buttonlist:
            if pos[0] > b.getX()-b.getSizeX() and pos[0] < b.getX()+b.getSizeX()and pos[1] > b.getY()-b.getSizeY() and pos[1] < b.getY()+b.getSizeY():
                return b.getMsg()
        return "No Button here"
    def draw(self,screen):
        for b in self.buttonlist:
            b.draw(screen)

class Game_Object():
    def __init__(self,x,y,sizeX,sizeY):
        self.x = x
        self.y = y
        self.sizeY = sizeY
        self.sizeX = sizeX
    def getX(self):
        return self.x
    def getY(self):
        return self.y
    def getSizeX(self):
        return self.sizeX
    def getSizeY(self):
        return self.sizeY


class Obstacle(Game_Object):
    def draw(self,screen):
        pygame.draw.rect(screen, (255, 0, 0), [self.x, self.y, self.sizeX, self.sizeY])
    def checkObstacleHit(self,pos):
        return self.getX() <= pos[0]+50 and pos[0] <= self.getX() + self.getSizeX() and self.getY() <= pos[1]+50 and pos[1] <= self.getY() + self.getSizeY()

class Goal(Game_Object):
    def draw(self,screen):
        pygame.draw.rect(screen, (0, 255, 0), [self.x, self.y, self.sizeX, self.sizeY],3)
    def checkGoalHit(self,pos):
        return self.getX() <= pos[0]+50 and pos[0] <= self.getX() + self.getSizeX() and self.getY() <= pos[1]+50 and pos[1] <= self.getY() + self.getSizeY()

class Player(Game_Object):

    def __init__(self,x,y,sizeX,sizeY,image):
        self.x = x
        self.y = y
        self.sizeY = sizeY
        self.sizeX = sizeX
        self.image = pygame.image.load(image)
        self.image = pygame.transform.scale(self.image, (50, 50))

        self.lastpressed = "U"
        self.speed = 10

    def move(self,direction):
        if direction == "U":
            self.y -= self.speed
        if direction == "D":
            self.y += self.speed
        if direction == "L":
            self.x -= self.speed
        if direction == "R":
            self.x += self.speed

    def getpos(self):
        return [self.getX(),self.getY()]

    def setpos(self,x,y):
        self.x = x
        self.y = y

    def setimage(self,image):
        self.image = pygame.image.load(image)
        self.image = pygame.transform.scale(self.image, (50, 50))

    def increment_speed(self,val):
        if 0 <= self.speed + val and self.speed + val <= 50:
            self.speed += val


class Bullet(Game_Object):
    def __init__(self,x,y,sizeX,sizeY,direction,image):
        self.x = x
        self.y = y
        self.sizeY = sizeY
        self.sizeX = sizeX
        self.direction = "U"
        self.image = pygame.image.load(image)
        self.image = pygame.transform.scale(self.image, (50, 50))
    def move(self):
        if self.direction == "U":
            self.y -= 10
        if self.direction == "D":
            self.y += 10
        if self.direction == "L":
            self.x -= 10
        if self.direction == "R":
            self.x += 10
    def getpos(self):
        return [self.getX(),self.getY()]
    def draw(self,screen):
        if self.direction == "U":
            screen.blit(pygame.transform.rotate(self.image,0),self.getpos())
        if self.direction == "D":
            screen.blit(pygame.transform.rotate(self.image,180),self.getpos())
        if self.direction == "L":
            screen.blit(pygame.transform.rotate(self.image,90),self.getpos())
        if self.direction == "R":
            screen.blit(pygame.transform.rotate(self.image,270),self.getpos())

    





class Station(Game_Object):
    def draw(self,screen):
        pygame.draw.rect(screen, (0, 0, 255), [self.x, self.y, self.sizeX, self.sizeY],3)
    def checkStationHit(self,pos):
        return self.getX() <= pos[0]+50 and pos[0] <= self.getX() + self.getSizeX() and self.getY() <= pos[1]+50 and pos[1] <= self.getY() + self.getSizeY()
        
    
class Level():
    instances = 0

    def __init__(self,obstacles,goals,stations):
        Level.instances += 1
        self.obstacles = obstacles
        self.goals = goals
        self.stations = stations

class Game():
    def __init__(self,level):
        self.level = level
        self.level_count = len(self.level)
        self.current_level = 0






def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))

    #song = pygame.mixer.music.load('sources/t2i.xm')
    #pygame.mixer.music.play(-1)
    
    
    interface =  Interface("default")
    interface.createButton(30,30,20,20,"You clicked Button No.1")
    interface.createButton(60,30,20,20,"You clicked Button No.2")

    font = pygame.font.SysFont("arial", 50)
    
    player = Player(0,550,50,50,'sources/toilpap.png')

    font = pygame.font.SysFont("comicsansms", 52)


    #level 1
    o1 = Obstacle(375,0,50,300)
    o2 = Obstacle(375,380,50,300)
    g1 = Goal(650,150,70,70)

    s1 = Station(100,100,100,100)

    level1 = Level([o1,o2],[g1],[s1])



    #level 2
    o4 = Obstacle(100,100,50,500)
    o5 = Obstacle(300,0,50,500)
    o6 = Obstacle(500,100,50,500)
    g2 = Goal(700,500,70,70)

    level2 = Level([o4,o5,o6],[g2],[])

    #level3
    o7 = Obstacle(375,0,50,300)
    o8 = Obstacle(375,380,50,300)
    o9 = Obstacle(100,100,100,100)
    g3 = Goal(650,150,70,70)
    
    level3 = Level([o7,o8,o9],[g3],[])

    game = Game([level1,level2,level3])

    text = font.render("Level " + str(game.current_level+1), True, (0, 128, 0))
    text_speed = font.render("Speed " + str(player.speed), True, (255,165,0))


 
    pygame.mouse.set_visible(1)
    pygame.key.set_repeat(1, 30)
 
    clock = pygame.time.Clock()
 

    hintergrundfarbe = (120,120, 120)
    screen.fill(hintergrundfarbe)

    bullet_exists = False

    
    running = True
    while running:
        clock.tick(60)


        ev = pygame.event.get()

        
        
        for event in ev:
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    posMouse = (pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1])
                    if interface.checkButtonHit(posMouse) == "You clicked Button No.1":
                        pygame.event.post(pygame.event.Event(pygame.QUIT))
                        running = False
                        pygame.quit()
                        sys.exit()
                    if interface.checkButtonHit(posMouse) == "You clicked Button No.2":
                        print("Hilfe: Bewegen mit Pfeiltasten blablabla...")
                    
                    
                if event.button == 3:
                    pass
                    #rechtsklick
                
                


            if event.type == pygame.KEYDOWN:
                
                if event.key == pygame.K_ESCAPE:
                    pygame.event.post(pygame.event.Event(pygame.QUIT))
                    running = False
                    pygame.quit()
                    sys.exit()

                if event.key == pygame.K_u:
                    player.increment_speed(1)
                    text_speed = font.render("Speed " + str(player.speed), True, (255,165,0))

                if event.key == pygame.K_d:
                    player.increment_speed(-1)
                    text_speed = font.render("Speed " + str(player.speed), True, (255,165,0))

                if event.key == pygame.K_f:
                    if player.lastpressed == "L" and not bullet_exists:
                        bullet = Bullet(player.getX(),player.getY()+int(player.getSizeY()/2),10,10,"L",'sources/fireball.png')
                    if player.lastpressed == "R" and not bullet_exists:
                        bullet = Bullet(player.getX()+player.getSizeX(),player.getY()+int(player.getSizeY()/2),10,10,"R",'sources/fireball.png')
                    if player.lastpressed == "U" and not bullet_exists:
                        bullet = Bullet(player.getX(),player.getY()+int(player.getSizeY()/2),10,10,"U",'sources/fireball.png')
                    if player.lastpressed == "D" and not bullet_exists:
                        bullet = Bullet(player.getX()+int(player.getSizeX()/2),player.getY()+int(player.getSizeY()/2),10,10,"D",'sources/fireball.png')
                    bullet_exists = True

                
                print(player.getpos())
                if event.key == pygame.K_LEFT:
                    if player.getX() - player.speed >= 0:
                        player.move("L")
                        player.lastpressed = "L"
                    else:
                        player.x = 0
                if event.key == pygame.K_RIGHT:
                    if player.getX() + player.speed <= 750:
                        player.move("R")
                        player.lastpressed = "R"
                    else:
                        player.x = 700
                if event.key == pygame.K_UP:
                    if player.getY() - player.speed >= 0:
                        player.move("U")
                        player.lastpressed = "U"
                    else:
                        player.y = 0
                if event.key == pygame.K_DOWN:
                    if player.getY() + player.speed <= 550:
                        player.move("D")
                        player.lastpressed = "D"
                    else:
                        player.y = 550

                    
                    
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_r:
                    pass


            for g in game.level[game.current_level].goals:
                if g.checkGoalHit(player.getpos()):
                    print("gewonnen")
                    if game.current_level == game.level_count - 1:
                        game.current_level = 0
                    else:
                        game.current_level += 1
                    player.setpos(0,500)


            for o in game.level[game.current_level].obstacles:
                if o.checkObstacleHit(player.getpos()):
                    print("verloren")
                    Tk().wm_withdraw()
                    messagebox.showinfo('Info','Du hast verloren')
                    pygame.event.post(pygame.event.Event(pygame.QUIT))
                    running = False
                    pygame.quit()
                    sys.exit()


            for s in game.level[game.current_level].stations:
                if s.checkStationHit(player.getpos()):
                    player.setimage('sources/spag.png')
                    song = pygame.mixer.music.load('sources/roi.ogg')
                    pygame.mixer.music.play(-1)
                    

            screen.fill(hintergrundfarbe)


            #draw player
            if player.lastpressed == "U":
                screen.blit(pygame.transform.rotate(player.image,0),player.getpos())
            if player.lastpressed == "D":
                screen.blit(pygame.transform.rotate(player.image,180),player.getpos())
            if player.lastpressed == "L":
                screen.blit(pygame.transform.rotate(player.image,90),player.getpos())
            if player.lastpressed == "R":
                screen.blit(pygame.transform.rotate(player.image,270),player.getpos())



            #draw bullets
            if bullet_exists:
                bullet.draw(screen)
                bullet.move()

            
            




            for o in game.level[game.current_level].obstacles:
                o.draw(screen)
                
            for g in game.level[game.current_level].goals:
                g.draw(screen)

            for s in game.level[game.current_level].stations:
                s.draw(screen)


            screen.blit(text,(620 - text.get_width() // 2, 40 - text.get_height() // 2))

            
            screen.blit(text_speed,(620 - text_speed.get_width() // 2, 100 - text_speed.get_height() // 2))

                
            interface.draw(screen)
 
 
        # Inhalt von screen anzeigen.
        pygame.display.flip()
 
 
if __name__ == '__main__':
    main()
