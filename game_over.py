import pygame

class GameOver:
    """A class to display the game over message."""

    def __init__(self, ai_game):

        self.screen =  ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings

        # Configure settings for the text.
        self.text_color = (255, 0, 0)
        self.font = pygame.font.SysFont(None, 60, True)

        # Display a Game Over! message.
        self.game_over = "Game Over!"
        self.prep_game_over()

    def prep_game_over(self):
        """Display the game over message."""
        game_over = self.game_over
        self.game_over_image = self.font.render(game_over, True,
                        self.text_color, self.settings.background_color)

        # Set the position of the message.
        self.game_over_rect = self.game_over_image.get_rect()
        self.game_over_rect.center = self.screen_rect.center

    def display_game_over(self):
        self.screen.blit(self.game_over_image, self.game_over_rect)