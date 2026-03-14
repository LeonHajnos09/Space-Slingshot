import pygame
import math

pygame.init()

WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Space Slingshot")

PLANET_MASS = 5.97e24
SPACECRAFT_MASS = 5000
GRAVITY_CONSTANT = 6.67e-11

FPS = 60
PLANET_RADIUS = 50
SPACECRAFT_RADIUS = 5

VELOCITY_SCALE = 100
DISTANCE_SCALE = 1e6

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (40, 255, 80)


class Planet:

    def __init__(self, x, y, mass):
        self.x = x
        self.y = y
        self.mass = mass

    def draw(self):
        pygame.draw.circle(window, GREEN, (int(self.x), int(self.y)), PLANET_RADIUS)


class Spacecraft:

    def __init__(self, x, y, velocity_x, velocity_y, mass):
        self.x = x
        self.y = y
        self.velocity_x = velocity_x
        self.velocity_y = velocity_y
        self.mass = mass

    def draw(self):
        pygame.draw.circle(window, RED, (int(self.x), int(self.y)), SPACECRAFT_RADIUS)

    def update_position(self, planet):
        dx = planet.x - self.x
        dy = planet.y - self.y

        distance_pixels = math.sqrt(dx**2 + dy**2)
        distance_meters = distance_pixels * DISTANCE_SCALE

        force = GRAVITY_CONSTANT * self.mass * planet.mass / distance_meters**2
        acceleration = force / self.mass

        angle = math.atan2(dy, dx)
        acceleration_x = math.cos(angle) * acceleration
        acceleration_y = math.sin(angle) * acceleration

        self.velocity_x += acceleration_x
        self.velocity_y += acceleration_y

        self.x += self.velocity_x
        self.y += self.velocity_y


def create_spacecraft(start_position, mouse_position):
    start_x, start_y = start_position
    mouse_x, mouse_y = mouse_position

    velocity_x = (mouse_x - start_x) / VELOCITY_SCALE
    velocity_y = (mouse_y - start_y) / VELOCITY_SCALE

    return Spacecraft(start_x, start_y, -velocity_x, -velocity_y, SPACECRAFT_MASS)


def main():
    running = True
    clock = pygame.time.Clock()

    planet = Planet(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2, PLANET_MASS)
    spacecrafts = []
    launch_position = None

    while running:
        clock.tick(FPS)
        mouse_position = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if launch_position:
                    spacecraft = create_spacecraft(launch_position, mouse_position)
                    spacecrafts.append(spacecraft)
                    launch_position = None
                else:
                    launch_position = mouse_position

        window.fill(BLACK)

        if launch_position:
            pygame.draw.line(window, WHITE, launch_position, mouse_position, 2)
            pygame.draw.circle(window, RED, launch_position, SPACECRAFT_RADIUS)

        for spacecraft in spacecrafts[:]:
            spacecraft.draw()
            spacecraft.update_position(planet)

            off_screen = spacecraft.x < 0 or spacecraft.x > WINDOW_WIDTH or spacecraft.y < 0 or spacecraft.y > WINDOW_HEIGHT
            collided = math.sqrt((spacecraft.x - planet.x)**2 + (spacecraft.y - planet.y)**2) < PLANET_RADIUS

            if off_screen or collided:
                spacecrafts.remove(spacecraft)

        planet.draw()
        pygame.display.update()

    pygame.quit()


main()
