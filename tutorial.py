import pygame
import time
import random
pygame.init()

WIDTH,HEIGHT = 800,600

win = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Sharmeen Fireworks!")

FPS = 60

COLOURS = [
    (255, 0, 0),
    (0, 255, 0),
    (0, 0, 255),
    (0, 255, 255),
    (255, 165, 0),
    (255, 255, 255),
    (230, 230, 250),
    (255, 192, 203)
]

class Projectile:
    pass

class Fireworks:
    RADIUS = 10
    MAX_PROJECTILE = 50
    MIN_PROJECTILE = 25
    PROJECTILE_VEL = 4

    def __init__(self, x, y, y_vel, explode_height, colour):
        self.x = x
        self.y = y
        self.y_vel = y_vel
        self.explode_height = explode_height
        self.colour = colour
        self.projectiles = []
        self.exploded = False

    def explode(self):
        self.exploded = True

    def move(self, max_width, max_height):
        if not self.exploded:
            self.y += self.y_vel
            if self.y <= self.explode_height:
                self.explode()      

    def draw(self, win):
        if not self.exploded:
            pygame.draw.circle(win, self.colour, (self.x, self.y), self.RADIUS)
            for projectile in self.projectiles:
                projectile.draw(win)       

class Launcher:
    WIDTH = 20
    HEIGHT= 20
    COLOUR = 'grey'

    def __init__(self,x,y,frequency):
        self.x = x
        self.y = y
        self.frequency = frequency    #millisec
        self.start_time = time.time()
        self.fireworks = []

    def draw(self, win):
        pygame.draw.rect(win, self.COLOUR, (self.x, self.y, self.WIDTH, self.HEIGHT))
        for firework in self.fireworks:
            firework.draw(win)


    def launch(self):
        colour = random.choice(COLOURS)
        explode_height = random.randrange( 50, 400)
        firework = Fireworks(self.x + self.WIDTH/2,self.y, -5, explode_height, colour)
        self.fireworks.append(firework)

    def loop(self, max_width, max_height):
        current_time = time.time()
        time_elapsed = current_time - self.start_time

        if time_elapsed * 1000 >= self.frequency:
            self.start_time = current_time
            self.launch()

        fireworks_to_remove = []
        for firework in self.fireworks:
            firework.move(max_width, max_height)
            if firework.exploded and len(firework.projectiles) == 0:
                fireworks_to_remove.append(firework) 

        for firework in fireworks_to_remove:
            self.fireworks.remove(firework)


def draw(Launchers):
    win.fill('black')

    for launcher in Launchers:
        launcher.draw(win)

    pygame.display.update()

def main():
    run = True
    clock = pygame.time.Clock()

    launchers = [Launcher(100, HEIGHT - Launcher.HEIGHT, 3000)]

    while run :
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        for launcher in launchers:
            launcher.loop(WIDTH,HEIGHT)

        draw(launchers)

    pygame.quit()
    quit()        

if __name__ == '__main__':
    main()            
