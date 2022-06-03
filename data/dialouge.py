"""
This module houses the dialoge logic
"""
import pygame

class Dialouge:
	"""
	This object is responsible for creating dialogs throughout the game

	[draw_for_some_time]
		time: int
		
		This function blits the text until the "index" variable has reached the "time" value 
	"""
	def __init__(self):
		self.display_surface = pygame.display.get_surface()
		self.font = pygame.font.SysFont("Sans", 30) # loading the font for this dialouge
		self.pos = (1200//2, self.display_surface.get_height() - 80) # changing the position to the middle of the screen, and adding some padding from the bottom
		self.text = '' # this variable gets changed in the module that creates an instance of this object

	def draw(self): # draws the text on the screen with the text "text"
		self.rendered_font = self.font.render(self.text, True, '#ffffff')
		self.rect = self.rendered_font.get_rect(topleft=self.pos)
		# making the background rectangle a bit wider than the text and moving it back to center it
		self.rect.width += 20
		self.rect.x -= 10

		if self.text != '': # checks if "text" is empty to prevent there from being an empty rectangle on the screen with no text
			pygame.draw.rect(self.display_surface, (0,0,0), self.rect)
		self.display_surface.blit(self.rendered_font, self.pos)

	def draw_for_some_time(self, time): # blits the text until the "index" is the same as the "time" parameter
		index = 0
		if index <= time:
			self.rendered_font = self.font.render(self.text, True, '#ffffff')
			self.rect = self.rendered_font.get_rect(topleft=self.pos)
			self.rect.width += 20
			self.rect.x -= 10

			
			if self.text != '':
				pygame.draw.rect(self.display_surface, (0,0,0), self.rect)
			self.display_surface.blit(self.rendered_font, self.pos)
			index += 1
		