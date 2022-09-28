import pygame
import os
import math
import sys
import neat

# Map image dimensions
SCREEN_WIDTH = 473
SCREEN_HEIGHT = 473
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

TRACK = pygame.image.load(os.path.join("python/ai/img", "field.png"))

class square():
        def __init__(self, x, y, p, gamma):
            self.x = x
            self.y = y
            self.p = p
            self.gamma = gamma

s1 = (1, 1, 2, 0.4)
s2 = (1, 2, 1, 0.4)
s3 = (1, 3, 1, 0.5)
s4 = (1, 4, 3, 0.5)
s5 = (1, 5, 5, 0.5)
s6 = (2, 1, 2, 0.4)
s7 = (2, 2, 4, 0.4)
s8 = (2, 3, 6, 0.5)
s9 = (2, 4, 5, 0.5)
s10 = (2, 5, 10, 0.5)
s11 = (3, 1, 5, 0.4)
s12 = (3, 2, 10, 0.4)
s13 = (3, 3, 4, 0.5)
s14 = (3, 4, 5, 0.5)
s15 = (3, 5, 7, 0.5)
s16 = (4, 1, 2, 0.4)
s17 = (4, 2, 5, 0.4)
s18 = (4, 3, 2, 0.5)
s19 = (4, 4, 2, 0.5)
s20 = (4, 5, 1, 0.5)
s21 = (5, 1, 2, 0.4)
s22 = (5, 2, 4, 0.4)
s23 = (5, 3, 4, 0.5)
s24 = (5, 4, 4, 0.5)
s25 = (5, 5, 4, 0.5)


class Car(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # load car image and set defaults
        self.original_image = pygame.image.load(os.path.join("python/ai/img", "car.png"))
        self.image = self.original_image
        
        self.rect = self.image.get_rect(center=(10, 10))
        self.vel_vector = pygame.math.Vector2(0.8, 0)
        self.hdg = 0
        self.move = False
        self.x = 1
        self.y = 1

    
    # Update car position
    def update(self):
        self.rotate()
        self.move_position()
        self.data()
    
    # Drive forward if drive state = True by vector amount
    def move_position(self):
        if self.move:
            self.x = self.x + math.cos(self.hdg)
            self.y = self.y + math.sin(self.hdg)

    
    # Turn vehicle
    def rotate(self):
        if self.direction == 1:
            self.angle -= self.rotation_vel
            self.vel_vector.rotate_ip(self.rotation_vel)
        elif self.direction == -1:
            self.angle += self.rotation_vel
            self.vel_vector.rotate_ip(-self.rotation_vel)

        self.image = pygame.transform.rotozoom(self.original_image, self.angle, 0.1)
        self.rect = self.image.get_rect(center=self.rect.center)



    def data(self):
        input = [0, 0, 0, 0, 0]
        for i, radar in enumerate(self.radars):
            input[i] = int(radar[1])
        return input


def eval_genomes(genomes, config):
    global cars, ge, nets

    cars = []
    ge = []
    nets = []

    for genome_id, genome in genomes:
        cars.append(pygame.sprite.GroupSingle(Car()))
        ge.append(genome)
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        genome.fitness = 0


    run = True
    t = 0
    while run:
        t = t + 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Display track within window
        SCREEN.blit(TRACK, (0, 0))

        if len(cars) == 0:
            break

        for i, car in enumerate(cars):
            ge[i].fitness += 1//(0.1*t)
            
            if car.sprite.drivestate == True and car.sprite.reverse == False:
                ge[i].fitness += 0
            
            if car.sprite.marker:
                ge[i].fitness += 100
                print(f"points given to {i}")
            if not car.sprite.alive or t >= 10**3:
                remove(i)

        for i, car in enumerate(cars):
            output = nets[i].activate(car.sprite.data())
            if output[0] > 0.7 :
                car.sprite.hdg = 0
                car.sprite.move = True
            if output[1] > 0.7:
                car.sprite.hdg = 90
                car.sprite.move = True
            if output[2] > 0.7:
                car.sprite.hdg = 180
                car.sprite.move = True
            if output[3] > 0.7:
                car.sprite.hdg = 270
                car.sprite.move = True
            if output[4] > 0.7:
                car.sprite.hdg = 0
                car.sprite.move = False


        # Update
        for car in cars:
            car.draw(SCREEN)
            car.update()
        pygame.display.update()


# NEAT setup
def run(config_path):
    global pop
    config = neat.config.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_path
    )

    pop = neat.Population(config)

    pop.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    pop.add_reporter(stats)

    pop.run(eval_genomes, 50)


if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config.txt")
    run(config_path)