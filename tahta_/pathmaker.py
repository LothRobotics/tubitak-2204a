import pygame as pg
import sys,json

# For creating test maps easiy in pygame and then exporting them to test pathfinder.py

#modes : 
# add/remove : make the points in this mode
# connect    : Put the connections in between here

# Keys: 
# WASD : move

# add_remove: 
# lmb : add a point
# rmb : delete a point
# C key: open connect mode

# connect:
# lmb : choose the first point 
# rmb : choose the second point
# middle mouse button: connect the two chosen points 
# Delete key: delete the connection between two chosen points
# F4 key: Save the map 

SC_SIZE = SW,SH = (800,500)
HSW,HSH = SW//2,SH//2

pg.font.init()

def drawcircle(surf,pos,camerapos):
    pg.draw.circle(surf,"blue",(pos[0]-camerapos[0],pos[1]-camerapos[1]),5)

def drawrect(surf,rect,camerapos):
    pg.draw.rect(surf,"red",(rect[0]-camerapos[0],rect[1]-camerapos[1],rect[2],rect[3]),3)

def drawline(surf,p1,p2,color,camerapos):
    pg.draw.line(surf,color,(p1[0]-camerapos[0],p1[1]-camerapos[1]),(p2[0]-camerapos[0],p2[1]-camerapos[1]),4)

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
        i = 0
        for node in self.posmap:
            drawcircle(surf,node["pos"],(self.x,self.y))
            surf.blit(self.app.font.render(str(i+1),False,"white"),(node["pos"][0]-self.x,node["pos"][1]-self.y))
            if len(self.map[i]) != 0:
                for neighbourid in self.map[i]:
                    drawline(surf,self.posmap[i]["pos"],self.posmap[neighbourid]["pos"],"green",(self.x,self.y))
            i += 1
        drawrect(surf,self.delrect,(self.x,self.y))

        if self.mode == "connect":
            surf.blit(self.app.font.render("Connect",False,"white"),(0,0))
        else:
            surf.blit(self.app.font.render("Add/remove",False,"white"),(0,0))
        
        surf.blit(self.app.font.render("Count:  "+str(len(self.posmap)),False,"white"),(250,0))

        surf.blit(self.app.font.render("1ST:  "+str(self.chosen1st),False,"white"),(0,50))
        surf.blit(self.app.font.render("2ND:  "+str(self.chosen2nd),False,"white"),(0,100))

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

    def connect(self):
        if self.chosen1st != None and self.chosen2nd != None:
            
            # if it already doesnt have a connection
            if self.map[self.chosen1st].__contains__(self.chosen2nd) == False and self.map[self.chosen2nd].__contains__(self.chosen1st) == False : 
                self.map[self.chosen1st].append(self.chosen2nd)
                self.map[self.chosen2nd].append(self.chosen1st)
                
            else:
                print("already has a connection")
            
            self.chosen1st = None
            self.chosen2nd = None
    
    def unconnect(self):
        print("unconnect")
        if self.chosen1st != None and self.chosen2nd != None:
            try:
                self.map[self.chosen1st].remove(self.chosen2nd)

                self.map[self.chosen2nd].remove(self.chosen1st)
            except ValueError:
                print("no connections found")

            self.chosen1st = None
            self.chosen2nd = None

    def startconnecting(self):
        self.mode = "connect"

    def choosefirst(self):
        i = 0
        for node in self.posmap:
            if self.delrect.collidepoint(node["pos"]):
                self.chosen1st = i
                if self.chosen1st != self.chosen2nd:
                    pass
                else:
                    self.chosen2nd = None
                break
            i += 1
        print(f"1st is {self.chosen1st} \t 2nd is: {self.chosen2nd}")
    
    def choosesecond(self):
        i = 0
        for node in self.posmap:
            if self.delrect.collidepoint(node["pos"]):
                self.chosen2nd = i
                if self.chosen2nd != self.chosen1st:
                    pass
                else:
                    self.chosen1st = None
                break
            i += 1
        print(f"1st is {self.chosen1st} \t 2nd is: {self.chosen2nd}")

    def convert(self):
        """Converts the map data to be used in pathfinder.py"""
        # self.map içerisinde her noktanın neighbor listesindeki değerler komşu noktanın id'si olduğundan dolayı direkten bunu sort
        # edip daha sonra da 0 olmayan(yani connection olmayan) noktaların hepsini 1 yapabiliriz 
        emptylist = [[] for node in self.map]
        wanted_count = len(self.posmap)
        x = 0
        
        print(self.map)
        newmap = []
        for node in self.map:
            newlist = []
            for i in range(len(self.map)):
                if node.__contains__(i):
                    newlist.append(1)
                else:
                    newlist.append(0)
            newmap.append(newlist)

        return newmap

        # for node in self.map:
        #     current_n_count = len(node)
        #     #print(f"sorted neihgbour list of {i} looks like: {sorted(node)}")
        #     sortedlist = sorted(node)

        #     for i in range(wanted_count):
        #         if sortedlist.__contains__(i):
        #             for t in sortedlist: # there should be a better way to do this
        #                 if t == i:
        #                     sortedlist[t] = 1 #"VAR"
        #         else:
        #             sortedlist.insert(i,0) #None
        #     emptylist[x] = sortedlist
        #     x += 1
        # return emptylist

    def export(self):
        with open("testmap.json","w") as file:
            data = json.dumps(self.convert())
            file.write(data)
            print("Saved Map")

class App:
    def __init__(self) -> None:
        self.screen = pg.display.set_mode(SC_SIZE)
        self.clock = pg.time.Clock()
        self.dt = 1
        self.font = pg.font.Font(pg.font.get_default_font(),24)

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
                    if self.mapmanager.mode == "connect":
                        if pg.mouse.get_pressed()[0]:
                            self.mapmanager.choosefirst()
                        if pg.mouse.get_pressed()[1]:
                            self.mapmanager.connect()
                        if pg.mouse.get_pressed()[2]:
                            self.mapmanager.choosesecond()
                if event.type == pg.KEYDOWN:
                    if self.mapmanager.mode == "add/remove":
                        if event.key == pg.K_c:
                            self.mapmanager.startconnecting()
                    elif self.mapmanager.mode == "connect":
                        if event.key == pg.K_DELETE or event.key == pg.KSCAN_DELETE or event.key == pg.K_BACKSPACE :
                            self.mapmanager.unconnect() 
                    if event.key == pg.K_F4:
                        self.mapmanager.export()

            self.update()
            self.draw()

            pg.display.update()

if __name__ == '__main__':
    app = App()
    app.run()