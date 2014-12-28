#!/usr/bin/env python

from pygamehelper import *
from pygame import *
from pygame.locals import *
from vec2d import *
from random import uniform, randrange


def gravity(a, b, r):
    G = 6.67 * (10 ** -11)
    g = (G * a * b) / (r ** 2)
    return g


class Planet:
    def __init__(self, x, y, m):
        self.pos = vec2d(x, y)
        self.mass = m
        self.vel = vec2d(0, 0)
        self.color = (randrange(100, 150),
                      randrange(100, 255),
                      randrange(100, 255))

    def update(self):
        self.pos += self.vel

    def draw(self, screen):
        pygame.draw.circle(screen, self.color,
                           (int(self.pos[0]), int(self.pos[1])),
                           int(self.mass / 0.2))


class Star:
    def __init__(self, x, y):
        self.pos = vec2d(x, y)
        self.mass = uniform(2.0, 2.4)
        self.color = (randrange(200, 255),
                      randrange(150, 220),
                      randrange(130, 180))

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, self.pos, int(self.mass / 0.2))


class Planets(PygameHelper):
    def __init__(self):
        self.w, self.h = 800, 600
        PygameHelper.__init__(self, size=(self.w, self.h))

        self.planets = []
        count = input('Number of planets: ')
        for i in range(count):
            p = Planet(randrange(0, self.w), randrange(0, self.h),
                       uniform(0.8, 1.2))
            self.planets.append(p)

        self.stars = []

    def mouseUp(self, pos):
        s = Star(pos[0], pos[1])
        self.stars.append(s)

    def mouseUp2(self, pos):
        pos = vec2d(pos)
        for s in self.stars:
            maxdist = (s.mass / 0.2)
            dist = pos - s.pos
            if dist.length <= maxdist:
                self.stars.remove(s)

    def update(self):
        for p in self.planets:
            for s in self.stars:
                d = s.pos - p.pos
                g = gravity(p.mass * (10 ** 5), s.mass * (10 ** 7.25), d.length)
                d.length = g
                p.vel += d
                nxt = p.pos + p.vel
                maxdist = (p.mass / 0.2) + (s.mass / 0.2)
                dist = s.pos - nxt
                if dist.length < maxdist:
                    dist.length = p.vel.length
                    p.vel -= dist

            if p.pos[0] < 0 or p.pos[0] > self.w:
                p.pos[0] = 0 if p.pos[0] < 0 else self.w
                p.vel[0] = -p.vel[0]

            if p.pos[1] < 0 or p.pos[1] > self.h:
                p.pos[1] = 0 if p.pos[1] < 0 else self.h
                p.vel[1] = -p.vel[1]

            p.update()

    def draw(self):
        self.screen.fill((0, 0, 0))

        for p in self.planets:
            p.draw(self.screen)

        for s in self.stars:
            s.draw(self.screen)

        pygame.display.flip()


a = Planets()
a.mainLoop(60)
