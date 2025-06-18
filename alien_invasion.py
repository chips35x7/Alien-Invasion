"""Alien Invasion Overview"""

# In Alien Invasion, the player controls a rocket ship that appears
# at the bottom center of the screen. The player can move the ship
# right and left using the arrow keys and shoot bullets using the
# spacebar. When the game begins, a fleet of aliens fills the sky
# and moves across and down the screen. The player shoots and
# destroys the aliens. If the player shoots all the aliens, a new fleet
# appears that moves faster than the previous fleet. If any alien hits
# the player’s ship or reaches the bottom of the screen, the player
# loses a ship. If the player loses three ships, the game ends.

import sys
from time import sleep

import pygame

from settings import Settings # We import the Settings class into the main program file.
from ship import Ship
from bullets import Bullet
from alien import Alien
from game_stats import GameStats
from button import Button
from scoreboard import ScoreBoard


class AlienInvasion:
    """Overall class to manage game assets and behaviour."""

    def __init__(self):
        """Initialize the game and create game resources."""
        pygame.init()  # This initializes the background settings that Pygame needs to work properly.

        self.settings = Settings() # We instantiate the Settings class and assign it to self.settings.

        # self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        # self.settings.screen_width = self.screen.get_rect().width
        # self.settings.screen_height = self.screen.get_rect().height
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))  # This creates a display window on which we'll draw all the
        # games graphical elements. The argument (1280, 720) is a tuple that defines the dimensions of
        # the game window, which will be 1280 pixels wide by 720 pixels high.
        pygame.display.set_caption("Alien Invasion")

        # Create an instance to store game statistics,
        # and create a scoreboard.
        self.stats = GameStats(self)
        self.sb = ScoreBoard(self)

        self.ship = Ship(self) # We import Ship and then make an instance of Ship after the screen
        # has been created u. The call to Ship() requires one argument, an instance
        # of AlienInvasion. The self argument here refers to the current instance of
        # AlienInvasion. This is the parameter that gives Ship access to the game’s
        # resources, such as the screen object. We assign this Ship instance to
        # self.ship.

        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()

        self.play_button = Button(self, "Play Game")

    def run_game(self):  #The game is controlled by the run_game() method.
        """Start the main loop for the game"""
        while True:  # This method contains a while loop that runs continually.
            self._check_events()

            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()

            self._update_screen()

    def _check_events(self):
        """Responding to a Keypress"""
        # Whenever the player presses a key, that keypress is registered in Pygame as
        # an event. Each event is picked up by the pygame.event.get() method. We need
        # to specify in our _check_events() method what kind of events we want the
        # game to check for. Each keypress is registered as a KEYDOWN event.
        # When Pygame detects a KEYDOWN event, we need to check whether the
        # key that was pressed is one that triggers a certain action. For example, if the
        # player presses the right arrow key, we want to increase the ship’s rect.x value
        # to move the ship to the right.

        for event in pygame.event.get():  # The while loop contains an event loop and code that manages screen
            # updates. An event is an action that the user performs while playing the game, such as pressing
            # a key or moving the mouse.
            if event.type == pygame.QUIT:  # To access the events that Pygame detects, we’ll use the pygame.event
                # .get() function. This function returns a list of events that have taken place
                # since the last time this function was called. Any keyboard or mouse event
                # will cause this for loop to run. Inside the loop, we’ll write a series of if
                # statements to detect and respond to specific events. For example, when the
                # player clicks the game window’s close button, a pygame.QUIT event is detected
                sys.exit()  # and we call sys.exit() to exit the game.

            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_play_button(self, mouse_pos):
        """Start a new game when the player clicks the play button."""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            # Reset the game settings.
            self.settings.initialize_dynamic_settings()

            # Reset the game statistics.
            self.stats.reset_statistics()
            self.stats.game_active = True
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()

            #  Get rid of any remaining aliens and bullets.
            self.aliens.empty()
            self.bullets.empty()

            # Create a new fleet and center the ship.
            self._create_fleet()
            self.ship.center_ship()

            # Hide the mouse cursor.
            pygame.mouse.set_visible(False)

    def _check_keydown_events(self,event):
        """Respond to key-presses."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self,event):
        """Respond to key-releases"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _ship_hit(self):
        """Respond to the ship being hit by an alien."""

        if self.stats.ships_left > 0:
            # Decrement ships left, and update the scoreboard.
            self.stats.ships_left -= 1
            self.sb.prep_ships()

            # Get rid of any remaining aliens and bullets.
            self.aliens.empty()
            self.bullets.empty()

            # Create a new fleet and center the ship.
            self._create_fleet()
            self.ship.center_ship()

            # Pause to allow the player to regroup.
            sleep(2)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def check_aliens_bottom(self):
        """Check if any aliens have reached the bottom of the screen."""
        screen_rect = self.screen.get_rect()

        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                # Treat this the same way as when a ship gets hit.
                self._ship_hit()
                break

    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group."""

        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):

        self.bullets.update()

        # Get rid of bullets that have disappeared.
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        """Respond to bullet-alien collisions."""
        # Remove any bullets and aliens that have collided.

        # Check for bullets that have hit aliens.
        # If so, get rid of the bullet and the alien.
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True
        )
        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()

        if not self.aliens:
            # Destroy existing bullets and create a new fleet.
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()


            # Increase the level.
            self.stats.level += 1
            self.sb.prep_level()

    def _update_aliens(self):
        """
        Check if fleet is at an edge,
        then update the positions of all aliens in the fleet.
        """
        self._check_fleet_edges()
        self.aliens.update()

        # Look for alien-ship collisions.
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        # Look for aliens that have hit the bottom of the screen.
        self.check_aliens_bottom()

    def _create_fleet(self):
        """Create the fleet of aliens."""

        # Create an alien and find the number of aliens in a row.
        # Note: Spacing between each alien is equal to one alien width.
        # Note: The margin is also equal to one alien width.
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2*alien_width)
        number_of_aliens_x = available_space_x // (2*alien_width)

        # Determine the number of rows of aliens that fit on the screen.
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height -
                             (3  *  alien_height) - ship_height)
        number_of_rows = available_space_y // (2 * alien_height)

        # Create a full fleet of aliens.
        for row_number in range(number_of_rows):
            for alien_number in range(number_of_aliens_x):
                # Create an alien and place it in the row.
               self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number , row_number):
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien_x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien_x
        alien.rect.y = alien_height + 2 * alien_height * row_number
        self.aliens.add(alien)

    def _check_fleet_edges(self):
        """Respond appropriately if any aliens have reached an edge."""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Drop the entire fleet and change the fleet's direction."""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _update_screen(self):
        # Redraw the screen during each pass through the loop.
        self.screen.fill(
            self.settings.background_color)  # We fill the screen with the background color using the fill()
        # method, which acts on a surface and takes only one argument: a color.

        self.ship.blitme()  # After filling the background, we draw the ship on the screen by calling
        # ship.blitme(), so the ship appears on top of the background.

        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)

        # Draw score and game information.
        self.sb.show_game_statistics()

        if not self.stats.game_active:
            # Display the play button.
            self.play_button.draw_button()

        # Make the most recently drawn screen visible.
        pygame.display.flip()  # The call to pygame.display.flip() tells Pygame to make the most
        # recently drawn screen visible. In this case, it simply draws an empty screen
        # on each pass through the while loop, erasing the old screen so only the new
        # screen is visible. When we move the game elements around, pygame.display.flip()
        # continually updates the display to show the new positions of game
        # elements and hides the old ones, creating the illusion of smooth movement.


if __name__ == "__main__":
    # Make a game instance and run the game.
    ai = (AlienInvasion())  # We then create an instance of the game, and then call the run_game() method.
    ai.run_game()