import pygame
from pygame.sprite import Sprite

from pyinstaller_resource_path import resource_path

# Pygame is efficient because it lets you treat all game elements like rectangles (rects), even if they’re not exactly shaped like rectangles.
# Treating an element as a rectangle is efficient because rectangles are simple geometric shapes. When Pygame needs to figure out whether two
# game elements have collided, for example, it can do this more quickly if it treats each object as a rectangle. This approach usually works well
# enough that no one playing the game will notice that we’re not working with the exact shape of each game element. We’ll treat the ship and the
# screen as rectangles in this class.

# We import the pygame module before defining the class. The __init__()
# method of Ship takes two parameters: the self reference and a reference to
# the current instance of the AlienInvasion class. This will give Ship access to
# all the game resources defined in AlienInvasion.

# When you’re working with a rect object, you can use the x- and y-coordinates of the top, bottom, left, and right edges of the rectangle,
# as well as the center, to place the object. You can set any of these values to establish the current position of the rect. When you’re
# centering a game element, work with the center, centerx, or centery attributes of a rect. When you’re working at an edge of the screen,
# work with the top, bottom, left, or right attributes. There are also attributes that combine these properties, such as midbottom, midtop,
# midleft, and midright. When you’re adjusting the horizontal or vertical placement of the rect, you can just use the x and y attributes,
# which are the x- and y-coordinates of its top-left corner. These attributes spare you from having to do calculations that game developers
# formerly had to do manually, and you’ll use them often.
# Note: In Pygame, the origin (0, 0) is at the top-left corner of the screen, and coordinates
# increase as you go down and to the right. On a 1200 by 800 screen, the origin is
# at the top-left corner, and the bottom-right corner has the coordinates (1200, 800).
# These coordinates refer to the game window, not the physical screen.


class Ship(Sprite):
    """A class to manage the ship."""
    def __init__(self, ai_game):
        """Initialize the ship and set its starting position."""
        Sprite.__init__(self)
        self.screen = ai_game.screen # We assign the screen to an attribute of Ship, so we can access it easily in all the methods in this class.
        # At we access the screen’s rect attribute using the get_rect() method and assign it to self.screen_rect. Doing so allows us to place the
        # ship in the correct location on the screen.
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()

        # Load the ship image and get its rect.
        self.image = pygame.image.load(resource_path("assets\\images\\ship.bmp"))# To load the image, we call pygame.image.load() w and give it the location of our ship
        # image. This function returns a surface representing the ship, which we assign to self.image. When the image is loaded, we call
        # get_rect() to access the ship surface’s rect attribute so we can later use it to place the ship.
        self.rect = self.image.get_rect()

        # Start each new ship at the bottom center of the screen.
        self.rect.midbottom = self.screen_rect.midbottom # We’ll position the ship at the bottom center of the screen. To do so,
        # make the value of self.rect.midbottom match the midbottom attribute of the
        # screen’s rect. Pygame uses these rect attributes to position the ship
        # image so it’s centered horizontally and aligned with the bottom of the
        # screen.

        # Store a decimal value for the ship's horizontal position.
        self.x = float(self.rect.x)

        # Movement flag
        self.moving_right = False # We add a self.moving_right attribute in the __init__() method and set it
        # to False initially.
        self.moving_left = False

    def update(self):
        """Update the ship's position based on the movement flag."""
        if self.moving_right and self.rect.right < self.screen_rect.right: # we add update(), which moves the ship right if the
            self.x += self.settings.ship_speed # flag is True. The update() method will be called through an instance of
        # Ship, so it’s not considered a helper method.
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed

        # Update the rect object from self.x
        self.rect.x = self.x

    def blitme(self):
        """Draw the ship at its current position."""
        self.screen.blit(self.image, self.rect)  # Here, we have define the blitme() method, which draws the image to the
        # screen at the position specified by self.rect.

    def center_ship(self):
        """Center the ship on the screen."""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)