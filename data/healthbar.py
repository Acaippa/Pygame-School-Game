"""
This modile inherits the healthbar object
"""

import pygame

class HealthBar:
	"""
	[draw]
		Player: object / string
		Health: int

	Makes a rectangle that its size is proportional to the health of the "player", and blits it above the "player"

	NOTE: The "player" can also be any other object with a rect
	"""
	def __init__(self):
		self.display_surface = pygame.display.get_surface()
		self.background = pygame.Surface((40,10))
		self.background.fill("red")
		self.rect = self.background.get_rect()
		self.w, self.h = self.background.get_size()

	def draw(self, player, health): # draws the healthbar over the rect of the "player" parameter
		# moving the healthbar to the player
		self.rect.centerx = player.centerx
		self.rect.centery = player.centery - self.h - 15
		# makes the width the same as the percentage of health left
		width = 40 / 100 * health
		foreground = pygame.Surface((width,10)) # making the green bar of the healthbar
		foreground.fill("green")
		self.display_surface.blit(self.background, self.rect)
		self.display_surface.blit(foreground, self.rect)
