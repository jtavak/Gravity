import math
import sys
import pygame

G = 10

pygame.init()

fps = 60
fpsClock = pygame.time.Clock()

width, height = 1280, 720
screen = pygame.display.set_mode((width, height))


class Planet:
    def __init__(self, x, y, mass, vx, vy):
        self.x = x
        self.y = y
        self.mass = mass
        self.radius = (math.log(self.mass, 10) + 1) * 5
        self.vx = vx
        self.vy = vy
        self.ax = 0
        self.ay = 0

    def add_force(self, fx, fy):
        self.ax += fx/self.mass
        self.ay += fy/self.mass

    def update(self):
        self.vx += self.ax
        self.vy += self.ay
        self.x += self.vx
        self.y += self.vy
        self.ax = 0
        self.ay = 0

    def draw(self, scr, translation_x, translation_y):
        pygame.draw.circle(scr, (255, 255, 255), (self.x + translation_x, height - self.y - translation_y), self.radius)


planets = [Planet(501, 400, 100, 0, 0), Planet(500, 450, 1, 4, 0), Planet(499, 500, 1, 3, 0),
           Planet(502, 600, 1, 2, 0)]
# planets = [Planet(700, 400, 100, -2, -2), Planet(600, 401, 100, -2, 2), Planet(650, 200, 100, 2, 0)]

translation_x, translation_y = 0, 0

while True:
    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                for planet in planets:
                    translation_x += 25
            if event.key == pygame.K_RIGHT:
                for planet in planets:
                    translation_x -= 25
            if event.key == pygame.K_DOWN:
                for planet in planets:
                    translation_y += 25
            if event.key == pygame.K_UP:
                for planet in planets:
                    translation_y -= 25

    for planet1 in planets:
        for planet2 in planets:
            if planet1 != planet2:
                x_distance = planet2.x - planet1.x
                y_distance = planet2.y - planet1.y
                distance = math.hypot(x_distance, y_distance)
                gravity = (G * planet1.mass * planet2.mass)/distance**2
                theta = math.atan(y_distance / x_distance)

                if x_distance < 0:
                    ang = theta + math.pi
                else:
                    ang = theta

                gravity_x = gravity * math.cos(ang)
                gravity_y = gravity * math.sin(ang)
                planet1.add_force(gravity_x, gravity_y)

    for planet1 in planets:
        planet1.update()
        planet1.draw(screen, translation_x, translation_y)

    pygame.display.flip()
    fpsClock.tick(fps)
