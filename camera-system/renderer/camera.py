from enum import Enum


class ViewMode(Enum):
    TOP = 1
    LEFT = 2


class Camera:

    def __init__(self, screen_width=1000, screen_height=700):

        self.position = [0.0, 0.0, 0.0]

        self.zoom = 1.0

        self.view_mode = ViewMode.TOP

        self.target = None

        self.screen_width = screen_width
        self.screen_height = screen_height

        self.follow_smoothing = 0.1

    # -------------------------------------------------

    def set_view_mode(self, mode):
        self.view_mode = mode

    # -------------------------------------------------

    def follow(self, target):
        self.target = target

    # -------------------------------------------------

    def update(self):

        if self.target is None:
            return

        target_pos = self.target.get_position()

        for i in range(3):

            self.position[i] += (
                target_pos[i] - self.position[i]
            ) * self.follow_smoothing

    # -------------------------------------------------

    def zoom_in(self):
        self.zoom *= 1.1

    def zoom_out(self):
        self.zoom /= 1.1

    # -------------------------------------------------

    def pan(self, dx, dy):

        dx /= self.zoom
        dy /= self.zoom

        if self.view_mode == ViewMode.TOP:

            self.position[0] += dx
            self.position[1] += dy

        elif self.view_mode == ViewMode.LEFT:

            self.position[0] += dx
            self.position[2] += dy

    # -------------------------------------------------

    def project(self, position):

        x, y, z = position

        if self.view_mode == ViewMode.TOP:
            return x, y

        elif self.view_mode == ViewMode.LEFT:
            return x, z

        return x, y

    # -------------------------------------------------

    def world_to_screen(self, world_position):

        wx, wy = self.project(world_position)

        cx, cy = self.project(self.position)

        screen_x = (
            (wx - cx) * self.zoom
            + self.screen_width / 2
        )

        screen_y = (
            (wy - cy) * self.zoom
            + self.screen_height / 2
        )

        return int(screen_x), int(screen_y)

    # -------------------------------------------------

    def screen_to_world(self, screen_x, screen_y):

        cx, cy = self.project(self.position)

        world_x = (
            (screen_x - self.screen_width / 2)
            / self.zoom
            + cx
        )

        world_y = (
            (screen_y - self.screen_height / 2)
            / self.zoom
            + cy
        )

        if self.view_mode == ViewMode.TOP:

            return (
                world_x,
                world_y,
                self.position[2]
            )

        elif self.view_mode == ViewMode.LEFT:

            return (
                world_x,
                self.position[1],
                world_y
            )

        return world_x, world_y, 0.0