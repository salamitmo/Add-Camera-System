import pygame

from camera import Camera, ViewMode
from renderer import Renderer

from robot import Robot


pygame.init()

WIDTH = 1000
HEIGHT = 700

screen = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("Camera System")

clock = pygame.time.Clock()

font = pygame.font.SysFont(None, 28)


# =====================================================
# Objects
# =====================================================

robot = Robot()

camera = Camera(WIDTH, HEIGHT)

camera.follow(robot)

renderer = Renderer(screen, camera)


# =====================================================
# Main Loop
# =====================================================

running = True

while running:

    clock.tick(60)

    # -------------------------------------------------
    # Events
    # -------------------------------------------------

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:

            # Zoom
            if event.key == pygame.K_q:
                camera.zoom_in()

            elif event.key == pygame.K_e:
                camera.zoom_out()

            # Switch view
            elif event.key == pygame.K_TAB:

                if camera.view_mode == ViewMode.TOP:
                    camera.set_view_mode(
                        ViewMode.LEFT
                    )

                else:
                    camera.set_view_mode(
                        ViewMode.TOP
                    )

    # -------------------------------------------------
    # Keyboard Input
    # -------------------------------------------------

    keys = pygame.key.get_pressed()

    speed = 5

    # -----------------------------
    # Robot movement
    # -----------------------------

    # X axis
    if keys[pygame.K_a]:
        robot.position[0] -= speed

    if keys[pygame.K_d]:
        robot.position[0] += speed

    # Y axis
    if keys[pygame.K_w]:
        robot.position[1] -= speed

    if keys[pygame.K_s]:
        robot.position[1] += speed

    # Z axis
    if keys[pygame.K_r]:
        robot.position[2] += speed

    if keys[pygame.K_f]:
        robot.position[2] -= speed

    # -----------------------------
    # Camera panning
    # -----------------------------

    pan_speed = 10

    if keys[pygame.K_LEFT]:
        camera.pan(-pan_speed, 0)

    if keys[pygame.K_RIGHT]:
        camera.pan(pan_speed, 0)

    if keys[pygame.K_UP]:
        camera.pan(0, -pan_speed)

    if keys[pygame.K_DOWN]:
        camera.pan(0, pan_speed)

    # -------------------------------------------------
    # Update
    # -------------------------------------------------

    camera.update()

    # -------------------------------------------------
    # Render
    # -------------------------------------------------

    screen.fill((30, 30, 30))

    renderer.draw_grid()

    renderer.draw_axes()

    renderer.draw_robot(robot)

    # -------------------------------------------------
    # Debug Info
    # -------------------------------------------------

    info = (
        f"View: {camera.view_mode.name} | "
        f"Robot Position: {robot.position} | "
        f"Zoom: {camera.zoom:.2f}"
    )

    text = font.render(
        info,
        True,
        (255, 255, 255)
    )

    screen.blit(text, (20, 20))

    # -------------------------------------------------
    # Mouse Screen -> World
    # -------------------------------------------------

    mouse_x, mouse_y = pygame.mouse.get_pos()

    world_pos = camera.screen_to_world(
        mouse_x,
        mouse_y
    )

    mouse_text = font.render(
        f"Mouse World: {world_pos}",
        True,
        (255, 255, 0)
    )

    screen.blit(mouse_text, (20, 60))

    # -------------------------------------------------
    # Controls
    # -------------------------------------------------

    controls = (
        "WASD = Move XY | "
        "R/F = Move Z | "
        "Q/E = Zoom | "
        "Arrows = Pan | "
        "TAB = Switch View"
    )

    controls_text = font.render(
        controls,
        True,
        (180, 180, 180)
    )

    screen.blit(controls_text, (20, 100))

    # -------------------------------------------------

    pygame.display.flip()

pygame.quit()