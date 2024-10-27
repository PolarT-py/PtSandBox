# Import dependencies
import json
import os

# Import pygame
import pygame
pygame.init()


class SandBox:
    # Attributes
    fonts = {
        "grapple_24": pygame.font.Font("fonts/grapple/grapple.ttf", 24),
        "upheaval_20": pygame.font.Font("fonts/upheaval/upheavtt.ttf", 20),
    }
    with open("settings.json", "r") as f:
        settings = json.load(f)

    def __init__(self):
        # Pygame stuff
        self.screen = pygame.display.set_mode(self.settings["res"])
        pygame.display.set_caption(self.settings["title"])
        self.pyclock = pygame.time.Clock()

        # Other stuff
        self.running = True
        self.dt = 0.1

        # Children
        self.grid = Grid(self)

        # Pre-set
        self.tile_dictionary = {
            0: (255, 255, 255),      # air
            1: (226, 185, 83),       # sand
            2: (103, 167, 245)       # water
        }

    def get_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def draw(self):
        # Clear the screen
        self.screen.fill((200, 200, 200))

        # Draw FPS
        fps_text_surface = self.fonts["upheaval_20"].render(
            f"fps: {round(self.pyclock.get_fps())}", True, (0, 0, 0)).convert_alpha()
        self.screen.blit(fps_text_surface, (5, 5))

        # Draw grid
        self.grid.draw()

        # Update the screen
        pygame.display.flip()

    def update(self):
        # Time
        # self.dt = self.pyclock.tick(self.settings["fps"]) / 1000
        self.dt = self.pyclock.tick(60) / 1000

        # Grid
        self.grid.update()


class Grid:
    def __init__(self, parent):
        self.parent = parent
        self.size = [100, 100]
        self.tile_size = 10
        self.grid_line_width = 1
        self.rect = pygame.rect.Rect((100, 100, self.size[0] * self.tile_size, self.size[1] * self.tile_size))
        self.tile_map = [[Air(self, (j, i)) for j in range(self.size[0])] for i in range(self.size[1])]
        self.tile_map[10][10] = Sand(self, (10, 10))

    def draw(self):
        # Draw rectangle background
        pygame.draw.rect(self.parent.screen, (150, 150, 150), self.rect, 0)

        # Draw tiles
        for x in range(self.size[0]):
            for y in range(self.size[1]):
                pygame.draw.rect(self.parent.screen, self.parent.tile_dictionary[self.tile_map[y][x].id],
                                 (x * self.tile_size + self.rect.x, y * self.tile_size + self.rect.y,
                                  self.tile_size, self.tile_size))

        # Draw grid                 (+1 is to draw the very last line)
        for i in range(self.size[0] + 1):
            pygame.draw.line(self.parent.screen,
                             (0, 0, 0),
                             (self.rect.x + i * self.tile_size, self.rect.y),
                             (self.rect.x + i * self.tile_size, self.rect.y + self.tile_size * self.size[1]),
                             self.grid_line_width)
        for i in range(self.size[1] + 1):
            pygame.draw.line(self.parent.screen,
                             (0, 0, 0),
                             (self.rect.x, self.rect.y + i * self.tile_size),
                             (self.rect.x + self.tile_size * self.size[0], self.rect.y + i * self.tile_size),
                             self.grid_line_width)

    def tile_request(self, tile, request, data, data2=None):
        if request == "move":
            tile.x += data[0]
            tile.y += data[1]

            print(tile.x, tile.y)

            self.tile_map[tile.y][tile.x] = data2(self, (tile.x, tile.y))
            self.tile_map[tile.y + data[1]][tile.x + data[0]] = tile

    def update(self):
        # Update tiles
        for x in range(self.size[0]):
            for y in range(self.size[1]):
                self.tile_map[y][x].update()


class Tile:
    def __init__(self, parent, pos):
        self.parent = parent
        self.id = -1
        self.x = pos[0]
        self.y = pos[1]

    def update(self):
        pass


class Air(Tile):
    def __init__(self, parent, pos):
        super().__init__(parent, pos)
        self.id = 0


class Sand(Tile):
    def __init__(self, parent, pos):
        super().__init__(parent, pos)
        self.id = 1

    def update(self):
        self.parent.tile_request(self, "move", (0, -1), Air)
