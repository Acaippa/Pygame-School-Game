"""
This is the main tile object
"""

import pygame

class Tile():
	"""
	[__init__]
		pos: tuple
		path: string

	Blits the image at the path at the pos
	"""
	def __init__(self, pos, path): # loads the image from the path and blits it in the position
		self.display_surface = pygame.display.get_surface()
		self.window_width, self.window_height = self.display_surface.get_size()
		self.image = pygame.image.load(path).convert_alpha()
		self.pos = pos
		w, h = self.image.get_size()
		self.image = pygame.transform.scale(self.image, (w*3, h*3))
		self.rect = self.image.get_rect(topleft=pos)
		self.rect.height -= 15
		self.rect.y += 15
		self.rect.width -= 15
		self.rect.x += 7

	def draw(self):
		self.display_surface.blit(self.image, (self.pos[0], self.pos[1]))