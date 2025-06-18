import pygame
from pygame.sprite import Sprite

from pyinstaller_resource_path import resource_path


class Alien(Sprite):
    """A class to represent a single alien in the fleet."""

    def __init__(self, ai_game):
        """Initialize the alien and set its starting position."""
        Sprite.__init__(self)
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        # Load the alien image and set its rect attribute.
        self.image = pygame.image.load(resource_path("assets\\images\\alien.bmp"))
        self.rect = self.image.get_rect()

        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        # Store the alien's exact horizontal position.
        self.x = float(self.rect.x)

    def check_edges(self):
        """Return True if alien is at the edge of the screen."""
        screen_rect = self.screen.get_rect()

        if (self.rect.right >= screen_rect.right
                        or self.rect.left <=0):

            return True

    def update(self):
        """Move the alien to the left and right."""
        self.rect.x += self.settings.alien_speed * \
                   self.settings.fleet_direction