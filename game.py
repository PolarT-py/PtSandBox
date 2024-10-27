# Import dependencies
import json

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

        # Pre-rendered
        # Nothing here yet

    def get_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def draw(self):
        # Clear the screen
        self.screen.fill((200, 200, 200))

        # Draw the stuff
        fps_text_surface = self.fonts["upheaval_20"].render(f"fps: {round(self.pyclock.get_fps())}", True, (0, 0, 0))
        self.screen.blit(fps_text_surface, (5, 5))

        # Update the screen
        pygame.display.flip()

    def update(self):
        # Time
        self.dt = self.pyclock.tick(self.settings["fps"]) / 1000

        # Grid
        self.grid.update()


class Grid:
    def __init__(self, parent):
        self.parent = parent
        self.grid = []

    def update(self):
        print("Delta time:", self.parent.dt)
