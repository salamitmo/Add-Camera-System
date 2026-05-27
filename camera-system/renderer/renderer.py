import pygame


class Renderer:

    def __init__(self, screen, camera):

        self.screen = screen
        self.camera = camera

    # -------------------------------------------------

    def draw_grid(self):

        for x in range(-1000, 1001, 100):

            start = self.camera.world_to_screen(
                (x, -1000, 0)
            )

            end = self.camera.world_to_screen(
                (x, 1000, 0)
            )

            pygame.draw.line(
                self.screen,
                (50, 50, 50),
                start,
                end
            )

        for y in range(-1000, 1001, 100):

            start = self.camera.world_to_screen(
                (-1000, y, 0)
            )

            end = self.camera.world_to_screen(
                (1000, y, 0)
            )

            pygame.draw.line(
                self.screen,
                (50, 50, 50),
                start,
                end
            )

    # -------------------------------------------------

    def draw_axes(self):

        # X axis
        pygame.draw.line(
            self.screen,
            (255, 0, 0),
            self.camera.world_to_screen(
                (-1000, 0, 0)
            ),
            self.camera.world_to_screen(
                (1000, 0, 0)
            ),
            3
        )

        # Y axis
        pygame.draw.line(
            self.screen,
            (0, 255, 0),
            self.camera.world_to_screen(
                (0, -1000, 0)
            ),
            self.camera.world_to_screen(
                (0, 1000, 0)
            ),
            3
        )

    # -------------------------------------------------

    def draw_robot(self, robot):

        position = self.camera.world_to_screen(
            robot.get_position()
        )

        pygame.draw.circle(
            self.screen,
            (0, 255, 255),
            position,
            20
        )