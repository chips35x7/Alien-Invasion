import pygame.font

class Button:

    def __init__(self, ai_game, msg):
        """Initialize button attributes."""
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()

        # Set dimensions and properties of the button.
        self.width, self.height = (200, 50)
        self.button_color = (255, 251, 42)
        self.text_color = (255, 0, 0)
        self.font = pygame.font.SysFont(None, 48, True)

        # Build the buttons rect object and center it.
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        # The button message needs to be prepped only once.
        self._prep_msg(msg)

    def _prep_msg(self, msg):
        """Turn msg into a rendered image and center text on the button"""
        self.msg_image = self.font.render(msg, True,
                          self.text_color, self.button_color)

        # Get the rect attribute of msg_image.
        self.msg_image_rect = self.msg_image.get_rect()

        # Center msg_image on the button.
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        # Draw blank button and then draw the message.
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)