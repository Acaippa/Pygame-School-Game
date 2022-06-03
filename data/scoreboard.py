"""
This module houses the scoreboard object
"""

import pygame

class ScoreBoard:
	def __init__(self, background, player, enemies):
		self.display_surface = pygame.display.get_surface()
		self.background_rect = background
		self.rect = pygame.Rect(1200, 0, 600, 300)
		self.dimentions = self.rect.width, self.rect.height # get the dimentions of the rect and store it in a tuple
		self.font = pygame.font.SysFont('Sans', 40)
		self.smaller_font = pygame.font.SysFont('Sans', 20)
		self.player = player
		self.enemies = enemies

		self.surface = pygame.Surface((300,600))
		self.surface_dimentions = self.surface.get_rect().width, self.surface.get_rect().height
		self.surface.fill((40,40,40))

	def draw(self): # updates all its values and draws it on the screen
		self.update()

		self.surface.blit(self.score_font, (self.dimentions[1] // 2 - self.score_font_dimentions[0] // 2 ,20)) # place the text in the middle of the scoreboard
		self.surface.blit(self.split, (10, 80))
		self.surface.blit(self.enemies_left, (10, 100))
		self.display_surface.blit(self.surface, self.rect)

	def update(self):
		self.score = f"Score: {self.player.score}"

		self.split = pygame.Surface((self.surface_dimentions[0] - 20, 2)) # same as the <hr> tag in html
		self.split.fill('white') # colors the hr

		# render the amount of enemies left
		self.enemies_left = self.smaller_font.render(f"Enemies left: {len(self.enemies)}", True, "#ffffff")

		self.score_font = self.font.render(self.score, True, "#ffffff")
		self.score_font_dimentions = self.score_font.get_rect().width, self.score_font.get_rect().height
