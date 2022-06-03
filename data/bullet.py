"""
This module houses the bullets for the game
"""
import pygame
import math

class Bullet:
	"""
	[__init__]
		pos: tuple
		angle: int

	Creates a bullet and moves it in a certain direction at a certain speed
	"""

	def __init__(self, pos=None, angle=None): # takes a list for position and float for the radiant angle
		self.display_surface = pygame.display.get_surface() # getting the main display surface
		self.image = pygame.image.load("images/enemy/bullet.png").convert_alpha() # loading the image for the class
		w, h = self.image.get_size() # getting the size of the image
		self.image = pygame.transform.scale(self.image, (w*3, h*3)) # changing the resulution of the image, in this case just scaling it up
		self.pointing = math.degrees(angle) # converts the angle passed in as a radiant, into an angle, and storing it as pointing
		self.image = pygame.transform.rotate(self.image, self.pointing - 180)
		self.pos = pos
		self.speed = 20
		self.angle = angle

	def update(self): # this function gets called every frame
		# moves the bullet in the direction of the pointing variable
		self.pos[0] = self.pos[0] + (self.speed*math.sin(self.angle))
		self.pos[1] = self.pos[1] + (self.speed*math.cos(self.angle))

		self.display_surface.blit(self.image, self.pos) # blit the button to the main display
