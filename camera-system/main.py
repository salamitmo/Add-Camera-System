import pygame
import sys

pygame.init()

WIDTH, HEIGHT = 1000, 700
WORLD_W, WORLD_H = 2200, 1600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flexible Camera Demo")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 26)

WHITE = (245, 245, 245)
BLACK = (20, 20, 20)
GREEN = (70, 180, 90)
RED = (220, 60, 60)
BLUE = (60, 120, 220)
YELLOW = (240, 220, 70)
GRAY = (180, 180, 180)

follow = True

class Camera:
    def __init__(self, width, height):
        self.x = 0
        self.y = 0
        self.zoom = 1.0
        self.width = width
        self.height = height
        self.follow_target = None
        self.mode = "top"

    def world_to_screen(self, pos):
        return ((pos[0] - self.x) * self.zoom, (pos[1] - self.y) * self.zoom)

    def screen_to_world(self, pos):
        return (pos[0] / self.zoom + self.x, pos[1] / self.zoom + self.y)

    def apply(self, rect):
        return pygame.Rect(
            (rect.x - self.x) * self.zoom,
            (rect.y - self.y) * self.zoom,
            rect.width * self.zoom,
            rect.height * self.zoom
        )

    def update(self, follow_enabled):
        if follow_enabled and self.follow_target:
            cx = self.follow_target.x + self.follow_target.width / 2
            cy = self.follow_target.y + self.follow_target.height / 2
            self.x = cx - self.width / (2 * self.zoom)
            self.y = cy - self.height / (2 * self.zoom)

        self.x = max(0, min(self.x, WORLD_W - self.width / self.zoom))
        self.y = max(0, min(self.y, WORLD_H - self.height / self.zoom))

class Robot:
    def __init__(self, x, y, color, speed=4):
        self.x = x
        self.y = y
        self.width = 40
        self.height = 40
        self.color = color
        self.speed = speed

    @property
    def rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def update(self, keys):
        if keys[pygame.K_LEFT]:
            self.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.x += self.speed
        if keys[pygame.K_UP]:
            self.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.y += self.speed

        self.x = max(0, min(self.x, WORLD_W - self.width))
        self.y = max(0, min(self.y, WORLD_H - self.height))

camera = Camera(WIDTH, HEIGHT)
robot = Robot(300, 300, GREEN)
target = Robot(600, 800, RED, speed=0)
marker = Robot(900, 500, BLUE, speed=0)
camera.follow_target = robot

def draw_grid(surface, cam):
    step = 80
    for x in range(0, WORLD_W + 1, step):
        sx1, sy1 = cam.world_to_screen((x, 0))
        sx2, sy2 = cam.world_to_screen((x, WORLD_H))
        pygame.draw.line(surface, (230, 230, 230), (sx1, sy1), (sx2, sy2), 1)

    for y in range(0, WORLD_H + 1, step):
        sx1, sy1 = cam.world_to_screen((0, y))
        sx2, sy2 = cam.world_to_screen((WORLD_W, y))
        pygame.draw.line(surface, (230, 230, 230), (sx1, sy1), (sx2, sy2), 1)

def draw_top_view(surface, cam):
    pygame.draw.rect(surface, BLACK, cam.apply(pygame.Rect(0, 0, WORLD_W, WORLD_H)), 2)
    pygame.draw.rect(surface, GREEN, cam.apply(robot.rect))
    pygame.draw.rect(surface, RED, cam.apply(target.rect))
    pygame.draw.rect(surface, BLUE, cam.apply(marker.rect))

    rx, ry = cam.world_to_screen((robot.x + robot.width / 2, robot.y + robot.height / 2))
    tx, ty = cam.world_to_screen((target.x + target.width / 2, target.y + target.height / 2))
    mx, my = cam.world_to_screen((marker.x + marker.width / 2, marker.y + marker.height / 2))

    pygame.draw.circle(surface, YELLOW, (int(rx), int(ry)), max(3, int(5 * cam.zoom)))
    pygame.draw.circle(surface, (255, 255, 255), (int(rx), int(ry)), 2)
    pygame.draw.circle(surface, BLUE, (int(tx), int(ty)), max(3, int(6 * cam.zoom)))
    pygame.draw.circle(surface, (255, 255, 255), (int(tx), int(ty)), 2)

    pygame.draw.circle(surface, (0, 0, 255), (int(mx), int(my)), 15)
    pygame.draw.circle(surface, (255, 255, 255), (int(mx), int(my)), 5)

def draw_left_view(surface, cam):
    base_y = HEIGHT - 150
    ground_h = 110

    pygame.draw.rect(surface, GRAY, (0, base_y, WIDTH, ground_h))
    pygame.draw.line(surface, BLACK, (0, base_y), (WIDTH, base_y), 3)

    robot_x = 120
    target_x = 260
    marker_x = 390

    pygame.draw.rect(surface, GREEN, (robot_x, base_y - 90, 60, 90))
    pygame.draw.rect(surface, RED, (target_x, base_y - 60, 45, 60))
    pygame.draw.rect(surface, BLUE, (marker_x, base_y - 50, 40, 50))

    pygame.draw.line(surface, BLACK, (robot_x + 30, base_y - 90), (robot_x + 30, base_y), 2)
    pygame.draw.line(surface, BLACK, (target_x + 22, base_y - 60), (target_x + 22, base_y), 2)
    pygame.draw.line(surface, BLACK, (marker_x + 20, base_y - 50), (marker_x + 20, base_y), 2)

    pygame.draw.circle(surface, (0, 0, 255), (marker_x + 20, base_y - 80), 10)

def draw_world(surface, cam, follow_enabled):
    surface.fill(WHITE)
    draw_grid(surface, cam)

    if cam.mode == "top":
        draw_top_view(surface, cam)
    else:
        draw_left_view(surface, cam)

    marker_world = (marker.x, marker.y)
    marker_screen = cam.world_to_screen(marker_world)

    info = [
        f"Mode: {cam.mode}",
        f"Follow: {follow_enabled}",
        f"Zoom: {cam.zoom:.2f}",
        f"Camera x: {cam.x:.1f}",
        f"Camera y: {cam.y:.1f}",
        f"Marker world: ({marker_world[0]:.1f}, {marker_world[1]:.1f})",
        f"Marker screen: ({marker_screen[0]:.1f}, {marker_screen[1]:.1f})",
        "Arrows: move robot",
        "I/J/K/L: move marker",
        "1: top view | 2: left view",
        "F: follow toggle",
        "W/S: zoom in/out"
    ]

    for i, line in enumerate(info):
        txt = font.render(line, True, BLACK)
        surface.blit(txt, (12, 12 + i * 24))

running = True

while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_f:
                follow = not follow
                print("Follow:", follow)
            elif event.key == pygame.K_w:
                camera.zoom = min(2.5, camera.zoom + 0.1)
            elif event.key == pygame.K_s:
                camera.zoom = max(0.4, camera.zoom - 0.1)
            elif event.key == pygame.K_1:
                camera.mode = "top"
            elif event.key == pygame.K_2:
                camera.mode = "left"

    keys = pygame.key.get_pressed()
    robot.update(keys)

    if keys[pygame.K_i]:
        marker.y -= 4
    if keys[pygame.K_k]:
        marker.y += 4
    if keys[pygame.K_j]:
        marker.x -= 4
    if keys[pygame.K_l]:
        marker.x += 4

    marker.x = max(0, min(marker.x, WORLD_W - marker.width))
    marker.y = max(0, min(marker.y, WORLD_H - marker.height))

    camera.update(follow)

    draw_world(screen, camera, follow)
    pygame.display.flip()

pygame.quit()
sys.exit()