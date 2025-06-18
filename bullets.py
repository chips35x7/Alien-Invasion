import pygame
from pygame.sprite import Sprite


# The Bullet class inherits from Sprite, which we import from the pygame
# .sprite module. When you use sprites, you can group related elements in
# your game and act on all the grouped elements at once.

class Bullet(Sprite):
    """A class to manage bullets fired from the ship."""

    def __init__(self, ai_game):
        """Create a bullet object at ship's current position."""
        Sprite.__init__(self)

        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.bullet_color

        # Create a bullet rect at (0, 0) and then set correct position.
        self.rect = pygame.Rect(0, 0, self.settings.bullet_width,self.settings.bullet_height)
        # Here, we have created the bullet’s rect attribute. The bullet isn’t based on any
        # image, so we have to build a rect from scratch using the pygame.Rect() class.
        # This class requires the x- and y-coordinates of the top-left corner of the rect,
        # and the width and height of the rect.

        self.rect.midtop  = ai_game.ship.rect.midtop  # we set the bullet’s midtop attribute to match the ship’s
        # midtop attribute. This will make the bullet emerge from the top of the ship, making it
        # look like the bullet is fired from the ship.

        # Store the bullet's position as a decimal value
        self.y = float(self.rect.y)  # We store a decimal value for the bullet’s y-coordinate so
        # we can make fine adjustments to the bullet’s speed.

    def update(self):
        """Move the bullet up the screen."""

        # Update the decimal position of the bullet.
        self.y -= self.settings.bullet_speed
        # Update the rect position.
        self.rect.y = self.y

    def draw_bullet(self):
        """Draw the bullet to the screen."""
        pygame.draw.rect(self.screen, self.color, self.rect)