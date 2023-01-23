import pygame as pg
import sys
import json
from pathfinder import PathFinder

# For creating test maps easiy in pygame and then exporting them to test pathfinder.py

# MODES
# add/remove : make the points in this mode
# connect    : Put the connections in between here
# room_type  : give types to rooms

# KEYS
# WASD : move
# F4 key: Save the map
# F2 key: Load map
# F1 key: Test the algorithm

# ADD_REMOVE
# lmb : add a point
# rmb : delete a point
# C key: open connect mode

# CONNECT
# lmb : choose the first point
# rmb : choose the second point
# E key : connect the two chosen points
# Delete key: delete the connection between two chosen points
# T key: open room_type mode

# ROOM_TYPE
# lmb : classroom
# rmb : exit
# o : other rooms(such as corridors)
# g : make stairs

SC_SIZE = SW, SH = (800, 600)
HSW, HSH = SW//2, SH//2

pg.font.init()

ROOM_TYPE_COLORS = {"classroom": "blue",
                    "exit": "red",
                    "stair": "green",
                    "other": "yellow"}


# Why did I create seperate functions for this bruh
def drawcircle(surf, pos, col, camerapos):
    pg.draw.circle(surf, col, (pos[0]-camerapos[0], pos[1]-camerapos[1]), 9)


def drawrect(surf, rect, camerapos):
    pg.draw.rect(surf, "red", (rect[0]-camerapos[0],
                 rect[1]-camerapos[1], rect[2], rect[3]), 3)


def drawline(surf, p1, p2, color, camerapos):
    pg.draw.line(surf, color, (p1[0]-camerapos[0], p1[1] -
                 camerapos[1]), (p2[0]-camerapos[0], p2[1]-camerapos[1]), 4)


class MapManager:
    def __init__(self, app) -> None:
        self.app = app
        self.map = []
        self.posmap = []
        self.typemap = {}
        # data structure:
        # Map will contain neighbours of the nodes, which will be converted before being sent to pathfinder.py
        # Posmap is for visualization of the map and isnt used by the algorithm
        self.x = 0
        self.y = 0
        self.mode = "add/remove"
        self.delrectw = 50
        self.delrect = pg.rect.Rect(
            self.x+HSW-(self.delrectw//2), self.y+HSH-(self.delrectw//2), self.delrectw, self.delrectw)
        self.chosen1st = None
        self.chosen2nd = None
        self.speed = 0.8

    def update(self, dt):
        keys = pg.key.get_pressed()
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

        self.x += movx * dt * self.speed
        self.y += movy * dt * self.speed
        self.delrect.x = self.x+HSW-(self.delrectw//2)
        self.delrect.y = self.y+HSH-(self.delrectw//2)

    def connected_draw(self, surf):
        i = 0
        for node in self.posmap:
            drawcircle(surf, node, "blue", (self.x, self.y))
            if len(self.map[i]) != 0:
                for neighbourid in self.map[i]:
                    drawline(
                        surf, node,
                        self.posmap[neighbourid], "white", (self.x, self.y))
            surf.blit(self.app.font.render(str(i), False, (240, 240, 240)),
                      (node[0]-self.x, node[1]-self.y))
            i += 1

    def roomtype_draw(self, surf):
        i = 0
        for node in self.posmap:
            col = ROOM_TYPE_COLORS[self.typemap[i]]
            drawcircle(surf, node, col, (self.x, self.y))
            if len(self.map[i]) != 0:
                for neighbourid in self.map[i]:
                    drawline(
                        surf, self.posmap[i], self.posmap[neighbourid],
                        "white", (self.x, self.y))
            surf.blit(self.app.font.render(str(i), False, (240, 240, 240)),
                      (node[0]-self.x, node[1]-self.y))
            i += 1

    def draw(self, surf):
        drawcircle(surf, (SC_SIZE[0]//2, SC_SIZE[1]//2), "grey", (self.x, self.y))

        drawcircle(surf, (0+40, 0+40), "grey", (self.x, self.y))
        drawcircle(surf, (SC_SIZE[0]-40, 0+40), "grey", (self.x, self.y))
        drawcircle(surf, (0+40, SC_SIZE[1]-40), "grey", (self.x, self.y))
        drawcircle(surf, (SC_SIZE[0]-40, SC_SIZE[1]-40), "grey", (self.x, self.y))
        if self.mode != "room_type":
            self.connected_draw(surf)
        else:
            self.roomtype_draw(surf)
        drawrect(surf, self.delrect, (self.x, self.y))

        surf.blit(self.app.font.render(self.mode, False, "white"), (0, 0))

        surf.blit(self.app.font.render(
            "Count:  "+str(len(self.posmap)), False, "white"), (250, 0))

        surf.blit(self.app.font.render(
            "1ST:  "+str(self.chosen1st), False, "white"), (0, 50))
        surf.blit(self.app.font.render(
            "2ND:  "+str(self.chosen2nd), False, "white"), (0, 100))

    def add(self):
        self.map.append([])
        self.posmap.append([self.x + HSW, self.y + HSH])

    def remove(self):
        i = 0
        for node in self.posmap:
            if self.delrect.collidepoint(node):
                self.posmap.pop(i)
                self.map.pop(i)
                break
            i += 1

    def connect(self):
        if self.chosen1st is not None and self.chosen2nd is not None:

            # if it already doesnt have a connection
            if self.map[self.chosen1st].__contains__(self.chosen2nd) is False and self.map[self.chosen2nd].__contains__(self.chosen1st) is False:
                self.map[self.chosen1st].append(self.chosen2nd)
                self.map[self.chosen2nd].append(self.chosen1st)

            else:
                print("already has a connection")

            self.chosen1st = None
            self.chosen2nd = None

    def unconnect(self):
        print("unconnect")
        if self.chosen1st is not None and self.chosen2nd is not None:
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
            if self.delrect.collidepoint(node):
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
            if self.delrect.collidepoint(node):
                self.chosen2nd = i
                if self.chosen2nd != self.chosen1st:
                    pass
                else:
                    self.chosen1st = None
                break
            i += 1
        print(f"1st is {self.chosen1st} \t 2nd is: {self.chosen2nd}")

    def make_classroom(self):
        i = 0
        for node in self.posmap:
            if self.delrect.collidepoint(node):
                self.typemap[i] = "classroom"
                print(f"Made node id:{i} a classroom")
                break
            i += 1

    def make_exit(self):
        i = 0
        for node in self.posmap:
            if self.delrect.collidepoint(node):
                self.typemap[i] = "exit"
                print(f"Made node id:{i} an exit")
                break
            i += 1

    def make_otherroom(self):
        i = 0
        for node in self.posmap:
            if self.delrect.collidepoint(node):
                self.typemap[i] = "other"
                print(f"Made node id:{i} an other room")
                break
            i += 1

    def make_stair(self):
        for i, node in enumerate(self.posmap):
            if self.delrect.collidepoint(node):
                self.typemap[i] = "stair"
                print(f"Made node id:{i} a stair")
                break

    def make_all_otherroom(self):
        if len(self.typemap) == 0:
            i = 0
            for node in self.posmap:
                self.typemap[i] = "other"
                i += 1
        print("Made all rooms other room")

    def convert(self):
        """Converts the map data to be used in pathfinder.py"""
        # self.map içerisinde her noktanın neighbor listesindeki değerler komşu noktanın id'si olduğundan dolayı direkten bunu sort
        # edip daha sonra da 0 olmayan(yani connection olmayan) noktaların hepsini 1 yapabiliriz
        exportmap = {"posmap": self.posmap,
                     "typemap": self.typemap,
                     "map": self.map}

        return exportmap

    def export(self):
        with open("testmap.json", "w") as file:
            data = json.dumps(self.convert(), indent=4)
            file.write(data)
            print("Saved Map")

    def load_map(self):
        with open("testmap.json", "r") as file:
            data = json.load(file)
        self.posmap = []
        index = 0
        for position in data["posmap"]:
            position = position
            self.posmap.append((int(position[0]), int(position[1])))
            index += 1

        self.typemap = {}
        for id, val in enumerate(data["typemap"].values()):
            # key is actually just the node id but in string
            self.typemap[id] = val

        self.map = []
        for neighbors in data["map"]:
            self.map.append(neighbors)

        print("Loaded map")


class App:
    def __init__(self) -> None:
        self.screen = pg.display.set_mode(SC_SIZE)
        self.clock = pg.time.Clock()
        self.dt = 1
        self.font = pg.font.Font(pg.font.get_default_font(), 24)

    def draw(self):
        self.mapmanager.draw(self.screen)

    def update(self):
        pg.display.set_caption(str(self.clock.get_fps())[:2])

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
                    elif self.mapmanager.mode == "connect":
                        if pg.mouse.get_pressed()[0]:
                            self.mapmanager.choosefirst()
                        if pg.mouse.get_pressed()[2]:
                            self.mapmanager.choosesecond()
                    elif self.mapmanager.mode == "room_type":
                        if pg.mouse.get_pressed()[0]:
                            self.mapmanager.make_classroom()
                        if pg.mouse.get_pressed()[2]:
                            self.mapmanager.make_exit()
                if event.type == pg.KEYDOWN:
                    if self.mapmanager.mode == "add/remove":
                        if event.key == pg.K_c:
                            self.mapmanager.startconnecting()
                    elif self.mapmanager.mode == "connect":
                        if event.key == pg.K_DELETE or event.key == pg.KSCAN_DELETE or event.key == pg.K_BACKSPACE:
                            self.mapmanager.unconnect()
                        if event.key == pg.K_e:
                            self.mapmanager.connect()
                        if event.key == pg.K_t:
                            self.mapmanager.mode = "room_type"
                            self.mapmanager.make_all_otherroom()
                    elif self.mapmanager.mode == "room_type":
                        if event.key == pg.K_o:
                            self.mapmanager.make_otherroom()
                        if event.key == pg.K_g:
                            self.mapmanager.make_stair()
                    if event.key == pg.K_F4:
                        self.mapmanager.export()
                    if event.key == pg.K_F2:
                        self.mapmanager.load_map()

            self.update()
            self.draw()

            pg.display.update()


if __name__ == '__main__':
    app = App()
    app.run()
