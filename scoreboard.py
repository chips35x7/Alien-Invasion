import json

import pygame.font
from pygame.sprite import Group

from ship import Ship

from pyinstaller_resource_path import resource_path

score_file = resource_path("assets\\high_score.json")

class ScoreBoard:
    """A class to report scoring information."""

    def __init__(self, ai_game):
        """Initialize score-keeping attributes."""
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats

        # Font settings for scoring information.
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)

        # Prepare the initial score images.
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ships()

    def prep_score(self):
        """Turn the score into a rendered image."""
        rounded_score = round(self.stats.score, -1)
        score_str = "SCORE  "+'{:,}'.format(rounded_score)
        self.score_image = self.font.render(score_str, True,
                    self.text_color, self.settings.background_color)

        # Display the score at the top right of the screen.
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def prep_high_score(self):
        """Turn the high score into a rendered image."""
        high_score = round(self.stats.high_score, -1)
        high_score_str = "HIGH SCORE   "+"{:,}".format(high_score)
        self.high_score_image = self.font.render(high_score_str, True,
                            self.text_color, self.settings.background_color)

        # Center the high score at the top of the screen.
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.midtop = self.screen_rect.midtop

    def check_high_score(self):
        """Check to see if there's a new high score."""
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.prep_high_score()

            with open(score_file, "w") as f:
                json.dump(self.stats.high_score, f)

    def prep_level(self):
        """Turn the level into a rendered image."""
        level_str = 'LVL  '+ str(self.stats.level)
        self.level_image = self.font.render(level_str, True,
                    self.text_color, self.settings.background_color)

        # Position the level just below the score.
        self.level_rect = self.level_image.get_rect()
        self.level_rect.y = self.score_rect.y + 50
        self.level_rect.right = self.screen_rect.right - 20

    def prep_ships(self):
        """Show how many ships are left."""
        self.ships = Group()

        for ship_number in range(self.stats.ships_left):
            ship = Ship(self.ai_game)
            ship.rect.x = ship_number * ship.rect.width
            ship.rect.y = 0
            self.ships.add(ship)

    def show_game_statistics(self):
        """Draw scores, level and ships to the screen."""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.ships.draw(self.screen)
