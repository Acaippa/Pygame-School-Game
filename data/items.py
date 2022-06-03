"""
This module houses all of the item objects
It inhertits from the "items" object
"""

import pygame
from data.tile import*
import math
import random

class Item(Tile): # create an item object and inherit the attributes and functions of the tile object
	"""
	[__init__]
		Pos: tuple
		Path: string
		Player: object / string
		Id: string

	This object takes in the parameters listed and changes the players attributes according to the id of the item
	"""

	def __init__(self, pos, path, player, id):	
			super().__init__(pos, path) # initiates the object this object inhertited from, thus making this an extension of it
			self.player	= player # getting the player of the game
			w, h = self.image.get_size()
			self.image = pygame.transform.scale(self.image, (w*2, h*2))

			self.id = id
			self.picked_up = False
			self.angle = random.randint(0,360)

			# makes the item spawn in random radius from the thing that dropped it
			self.pos = (self.pos[0] + (30*math.sin(self.angle)), self.pos[1] + (30*math.cos(self.angle)))
			self.rect = self.image.get_rect(topleft=self.pos)


	def update(self): # checks if the item is picked up, and depending on the if of the item, it will have different outcomes
		if self.player.rect.colliderect(self.rect):
			if self.id == "key":
				self.player.inventory.append(self.id)
				self.picked_up = True

			if self.id == 'health':
				self.player.health += 20
				self.picked_up = True
		self.draw()
