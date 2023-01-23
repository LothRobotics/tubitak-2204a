import pygame as pg
import sys
import pymunk
from pathfinder import PathFinder
import json
import random
import time

from copy import deepcopy

SC_SIZE = (800, 600)
GRAVITY = (0, 0)

space = pymunk.Space()
space.gravity = GRAVITY

# static = static
# dynamic = a barrel that can be rolled
# kinematic = player

# inertia = resistance to movement


ROOM_TYPE_COLORS = {"classroom": "blue",
                    "exit": "red",
                    "stair": "green",
                    "other": "yellow"}

EVACUATE_TIME = 2.4  # 0.001, 6
# NEW_EVACUATE_TIME = 0.001
STUDENT_SPEED = 0.15

STUDENT_TOO_CLOSE_RADIUS = 15

STUDENT_RADIUS = 6

# size, pos, radius
WALLS = [

    ]


def drawcircle(surf, pos, col, camerapos):
    pg.draw.circle(surf, col, (pos[0]-camerapos[0], pos[1]-camerapos[1]), 9)


def drawrect(surf, rect, camerapos):
    pg.draw.rect(surf, "red", (rect[0]-camerapos[0],
                 rect[1]-camerapos[1], rect[2], rect[3]), 3)


def drawline(surf, p1, p2, color, camerapos):
    pg.draw.line(surf, color, (p1[0]-camerapos[0], p1[1] -
                 camerapos[1]), (p2[0]-camerapos[0], p2[1]-camerapos[1]), 4)


class Student:  # Dynamic Ball
    def __init__(self, classroom, position, route, app,  radius=80, speed=4.5):
        self.radius = radius
        self.app = app
        self.classroom = classroom
        # mass and inertia
        self.body = pymunk.Body(1, 100, body_type=pymunk.Body.DYNAMIC)
        self.body.position = position  # (SC_SIZE[0]//2, 0)
        self.shape = pymunk.Circle(self.body, self.radius)
        self.speed = speed
        # the parent of the shape
        space.add(self.body, self.shape)
        self.hasreacheddestination = False
        self.route = deepcopy(route)
        self.canmove = False

    def check_next_point(self):
        if self.hasreacheddestination is False:
            node_to_go = self.route[0]
            point = self.app.mapmanager.posmap[node_to_go]  # point pos
            dist = pg.Vector2(self.body.position[0] - point[0],
                              self.body.position[1] - point[1])
            if dist.length() < 10 + self.radius:
                self.route.remove(node_to_go)
                if len(self.route) == 0:
                    print("Reached destination")
                    self.hasreacheddestination = True
                    # self.app.stuff.remove(self)  # this isnt a good way to delete it
                    # nvm actually it should not delete it
                print("Went to the next node")

    def draw(self, window):
        pg.draw.circle(window, (245, 66, 191), self.body.position, self.radius)

    def determine_speed(self):
        foundclose = False
        for thing in self.app.stuff:
            dist = pg.math.Vector2(thing.body.position[0] - self.body.position[0],
                                   thing.body.position[1] - self.body.position[1])
            if dist.length() < STUDENT_TOO_CLOSE_RADIUS and thing.classroom != self.classroom:
                foundclose = True

        if foundclose:
            return self.speed*0.3
        else:
            return self.speed

    def update(self, dt):
        if self.hasreacheddestination is True:
            return
        else:
            if self.canmove:
                self.check_next_point()
                if self.hasreacheddestination is False:
                    node_to_go = self.route[0]
                    point = self.app.mapmanager.posmap[node_to_go]

                    dist = pg.Vector2(self.body.position[0] - point[0],
                                      self.body.position[1] - point[1])
                    if dist.length() != 0:
                        dist = dist.normalize()

                    direction = [-dist.x, -dist.y]

                    speed = self.determine_speed()

                    vel = [direction[0]*speed*dt,
                           direction[1]*speed*dt]
                    self.body.velocity = vel
            else:
                pass

class StaticRect:
    def __init__(self, size, position, radius):
        self.radius = radius
        # mass and inertia
        self.body = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.body.position = [position[0]-size[0]//2, position[1]-size[1]//2]
        self.shape = pymunk.Poly.create_box(self.body, size, radius)
        self.size = size
        #         the parent of the shape
        space.add(self.body, self.shape)
        # self.rectangle_shape = pymunk.Poly(space.static_body, [(10,10),(20,10),(20,15),(10,15)])

    def draw(self, window):
        # SEKILLER NEDEN HALFWIDTH VE HALFHEIGHT KADAR SOLA KACIYOR YA
        # yukarıda yazığım şey olduğundan draw fonksiyonunu değiştirdim
        pg.draw.rect(window, "black",
                     [self.body.position[0]-(self.size[0]//2),
                      self.body.position[1]-(self.size[1]//2),
                      self.size[0], self.size[1]], self.radius)

    def update(self, dt):
        pass


class MapManager:
    def __init__(self):
        self.map = []
        self.posmap = []
        self.typemap = {}

    def load_map(self):
        with open("testmap.json", "r") as file:
            data = json.load(file)
        self.posmap = []

        for index, position in enumerate(data["posmap"]):
            position = position
            self.posmap.append((int(position[0]), int(position[1])))

        self.typemap = {}
        for id, val in enumerate(data["typemap"].values()):
            # key is actually just the node id but in string
            self.typemap[id] = val

        self.map = []
        for neighbors in data["map"]:
            self.map.append(neighbors)
        print("Loaded map")

    def roomtype_draw(self, surf):
        i = 0
        for node in self.posmap:
            color = ROOM_TYPE_COLORS[self.typemap[i]]
            drawcircle(surf, node, color, (0, 0))
            if len(self.map[i]) != 0:
                for neighbourid in self.map[i]:
                    drawline(
                        surf, self.posmap[i], self.posmap[neighbourid],
                        "green", (0, 0))
            #surf.blit(self.app.font.render(str(i), False, (240, 240, 240)),
            #          (node[0]-self.x, node[1]-self.y))
            i += 1

    def draw(self, surf):
        self.roomtype_draw(surf)
        #surf.blit(self.app.font.render(
        #    "Count:  "+str(len(self.posmap)), False, "white"), (250, 0))


class System:
    def __init__(self, class_student_thing, routes, app):
        self.cla_stu = class_student_thing
        self.app = app
        self.routes = deepcopy(routes)
        print("self.routes", self.routes)

        self.times = {}
        self.classes = []
        print("\n\n\n\n")
        print(class_student_thing)
        for _class, students in self.cla_stu.items():
            print(_class, students)
            self.times[_class] = None
            self.classes.append(_class)

        self.starttime = time.time()
        self.time = time.time()
        self.wrote = False

        print(f"classes: {self.classes}")



    def update(self, dt):
        self.time = time.time()

        elapsed_time = self.time - self.starttime

        num_of_classes_to_evacuate = 1 + (elapsed_time // EVACUATE_TIME)
        print(f"num_of_classes_to_evacuate: {num_of_classes_to_evacuate}")

        for id in range(int(num_of_classes_to_evacuate)):
            if id < len(self.classes):
                self.evacuate_class(self.classes[id])

        # times of classroom exiting
        for _class, students in self.cla_stu.items():
            all_exited = True
            for student in students:
                if student.hasreacheddestination != True:
                    all_exited = False

            if all_exited and self.times[_class] is None:
                self.times[_class] = elapsed_time

        done = True
        for t in self.times.values():
            if t is None:
                done = False

        if done and self.wrote is False:
            with open(f"simulation_results{EVACUATE_TIME}.json", "w") as file:
                json.dump(self.times, file, indent=4)
                print("wrote the simulation_results")
                self.wrote = True
                sys.exit()
                # self.app.setup()


    def evacuate_class(self, class_id):
        for student in self.cla_stu[class_id]:
            student.canmove = True
        print(f"Gave evacuate command to class: {class_id}")


class Game:
    def __init__(self):
        self.window = pg.display.set_mode(SC_SIZE)
        self.clock = pg.time.Clock()

    def draw(self):
        self.window.fill("grey")

        self.mapmanager.draw(self.window)
        for thing in self.stuff:
            thing.draw(self.window)

        pg.display.update()

    def update(self):
        mpos = pg.mouse.get_pos()
        self.system.update(self.dt)
        for thing in self.stuff:
            dist = pg.Vector2(thing.body.position[0]-mpos[0],
                              thing.body.position[1]-mpos[1])
            if dist.length() != 0:
                velocity = dist.normalize()
                velocity = [-velocity.x*self.dt, -velocity.y*self.dt]
            else:
                velocity = [0, 0]
            thing.update(self.dt)

        space.step(1/50)

    def spawn_students(self, amount):
        self.routes = self.pathfinder.calculate_escape_routes()
        print("routes:", self.routes)
        clasrooms = []
        for index, node in enumerate(self.mapmanager.typemap.values()):
            if node == "classroom":
                clasrooms.append(index)
                self.class_student_thing[index] = []
        print(f"classrooms: {clasrooms}")

        for i in range(amount):
            classroom = random.choice(clasrooms)
            class_pos = self.mapmanager.posmap[classroom]
            offsetx = random.randint(-20, 20)
            offsety = random.randint(-20, 20)
            position = [class_pos[0] + offsetx, class_pos[1] + offsety]

            student = Student(classroom, position, self.routes[classroom],
                              self, radius=STUDENT_RADIUS)
            self.stuff.append(student)

            # print(f"""self.class_student_thing::::
            # {self.class_student_thing}\n classroom: {classroom}""")

            self.class_student_thing[classroom].append(student)

    def setup(self):
        self.stuff = []
        for size, pos, radius in WALLS:
            self.stuff.append(StaticRect(size, pos, radius))
        self.mapmanager = MapManager()
        self.mapmanager.load_map()
        self.pathfinder = PathFinder()
        self.pathfinder.loadMap("testmap.json")
        self.class_student_thing = {}
        self.spawn_students(50)

        print(f"class_student_thing: {self.class_student_thing}")
        self.system = System(self.class_student_thing, self.routes, self)

    def run(self):
        self.setup()
        while True:
            self.dt = self.clock.tick(60)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    sys.exit()

            self.draw()
            self.update()


if __name__ == "__main__":
    app = Game()
    app.run()
