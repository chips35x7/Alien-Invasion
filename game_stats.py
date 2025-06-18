import json

from pyinstaller_resource_path import resource_path

score_file = resource_path("assets\\high_score.json")

class GameStats:
    """Track statistics for alien invasion."""

    def __init__(self, ai_game):
        """Initialize statistics."""

        self.settings = ai_game.settings
        self.reset_statistics()

        # Start alien invasion in an inactive state.
        self.game_active = False # A game_active flag as an attribute to
        # GameStats to end the game when the player runs out of ships.

        # Load the previously saved high score from the high score file.
        with open(score_file) as f:
            high_score = json.load(f)

        self.high_score = high_score

    def reset_statistics(self):
        """Initialize statistics that can change during the game."""
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1