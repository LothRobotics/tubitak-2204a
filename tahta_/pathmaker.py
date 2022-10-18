import pygame as pg
import sys

# For creating test maps easiy in pygame and then exporting them to test pathfinder.py


SC_SIZE = SW,SH = (800,500)
HSW,HSH = SW//2,SH//2


def drawcircle(surf,pos,camerapos):
    pg.draw.circle(surf,"blue",(pos[0]-camerapos[0],pos[1]-camerapos[1]),5)

def drawrect(surf,rect,camerapos):
    pg.draw.rect(surf,"red",(rect[0]-camerapos[0],rect[1]-camerapos[1],rect[2],rect[3]),3)

class MapManager: #TODO: Save mappos and map as numpy arrays
    def __init__(self,app) -> None:
        self.app = app
        self.map = []
        # data structure: 
        # self.map will contain neighbours of the nodes, which will be converted before being sent to pathfinder.py
        # while self.posmap is just for visualization of the map, and is not something that pathfinder.py needs
        # Usage:
        # Firstly create all the points, then click 'C' and it will go into connecting mode, in connecting mode you can 
        # connect different nodes together to make them neightbours
        self.posmap = []
        self.x = 0
        self.y = 0
        self.mode = "add/remove"
        self.delrectw = 70 
        self.delrect = pg.rect.Rect(self.x+HSW-(self.delrectw//2),self.y+HSH-(self.delrectw//2),self.delrectw,self.delrectw)
        self.chosen1st = None
        self.chosen2nd = None

    def update(self,dt):
        keys =  pg.key.get_pressed()
        movx = 0
        movy = 0
        if keys[pg.K_a] or keys[pg.K_LEFT]:
            movx -= 1
        if keys[pg.K_d] or keys[pg.K_RIGHT]:
            movx += 1
        if keys[pg.K_w] or keys[pg.K_UP]:
            movy -= 1
        if keys[pg.K_s] or keys[pg.K_DOWN]:
            movy += 1

        self.x += movx * dt
        self.y += movy * dt
        self.delrect.x = self.x+HSW-(self.delrectw//2)
        self.delrect.y = self.y+HSH-(self.delrectw//2)

    def draw(self,surf):
        for node in self.posmap:
            drawcircle(surf,node["pos"],(self.x,self.y))
        drawrect(surf,self.delrect,(self.x,self.y))

    def add(self):
        pointamount = len(self.map)

        self.map.append([])
        #self.map.append([0 for x in range(pointamount)])
        self.posmap.append({"pos":[self.x+HSW,self.y+HSH]})

        print(self.map)

    def remove(self):
        i = 0
        for node in self.posmap:
            if self.delrect.collidepoint(node["pos"]):
                self.posmap.pop(i)
                self.map.pop(i)
                break
            i += 1

    def choosefirst(self): #TODO: Make connection mode
        pass

class App:
    def __init__(self) -> None:
        self.screen = pg.display.set_mode(SC_SIZE)
        self.clock = pg.time.Clock()
        self.dt = 1

    def draw(self):
        self.mapmanager.draw(self.screen)

    def update(self):
        pg.display.set_caption(str(self.clock.get_fps()))
        
        self.mapmanager.update(self.dt*0.3)

    def start_app(self):
        self.mapmanager = MapManager(self)

    def run(self):
        self.start_app()

        while True:
            self.dt = self.clock.tick(60)
            self.screen.fill("black")


            for event in pg.event.get():
                if event.type == pg.QUIT:
                    sys.exit()
                if event.type == pg.MOUSEBUTTONDOWN:
                    if self.mapmanager.mode == "add/remove":
                        if pg.mouse.get_pressed()[0]:
                            self.mapmanager.add()
                        if pg.mouse.get_pressed()[2]:
                            self.mapmanager.remove()
                

            self.update()
            self.draw()

            pg.display.update()

if __name__ == '__main__':
    app = App()
    app.run()