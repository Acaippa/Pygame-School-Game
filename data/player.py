"""
This module houses the player
"""

import pygame
from data.healthbar import*
from data.bullet import*
import random


class Player:
	"""
	
	Blits the player at the "pos", then takes inputs for moving the player and checks for collision with the "obsticles" list

	[__init__]
		pos: tuple
		obsticles: list
		enemies: list

	[hurt]
		value: int

	[collide]
		direction: list / vector2
	"""
	def __init__(self, pos, obsticles, enemies):
		self.image = pygame.image.load("images/player/player.png")
		self.w, self.h = self.image.get_size()
		self.image = pygame.transform.scale(self.image, (self.w*2, self.h*2))
		self.rect = self.image.get_rect()
		self.display_surface = pygame.display.get_surface()
		self.pos = pos
		self.rect[0], self.rect[1] = self.pos
		self.shoot_sound = pygame.mixer.Sound("audio/shoot.mp3") #loading the sound
		
		self.direction = pygame.math.Vector2() # creating a 2d vector to move the player [xVel, yVel]
		
		self.healthbar = HealthBar()

		self.obsticle_list = obsticles
		self.enemy_list = enemies
		self.bullet_list = []

		self.shoot_time = 5 # time delay_index for shooting
		self.shoot_delay_index = 0
		self.speed = 4
		self.force = 10
		self.health = 100
		self.living = True
		self.score = 0
		self.has_key = False

		self.action = 0 #changes to 1 if the key E is pressed

		self.inventory = [] # a list for managing item pickups and the items effetcs
		
	def input(self): # move the character based on keyboard input
		keys = pygame.key.get_pressed()
		if keys[pygame.K_d]: # right
			self.direction.x = 1
		elif keys[pygame.K_a]: # left
			self.direction.x = -1
		else:
			# resets the vector if noe keys are pressed
			self.direction.x = 0

		if keys[pygame.K_w]: # up
			self.direction.y = -1
		elif keys[pygame.K_s]: # down
			self.direction.y = 1
		else:
			# resets the vector if noe keys are pressed
			self.direction.y = 0

		if keys[pygame.K_e]:
			self.action = 1
		else:
			self.action = 0

		if pygame.mouse.get_pressed()[0]: #check if the user clicks the left mouse button
			self.shoot()

		self.move()

	def move(self):
		if self.direction.magnitude() != 0:
			self.direction = self.direction.normalize()

		# adding the players "speed" onto the relevant part of its vector
		self.rect.x += self.direction.x * self.speed
		self.collide("horizontal")
		self.rect.y += self.direction.y * self.speed
		self.collide("vertical")
		self.pos = self.rect

	def hurt(self, value): # the hurties for the player
		if self.health - value * 2 <= 0:
			self.living = False
			self.health = 0
		else:
			self.health -= value

	def collide(self, direction): # checks if the player is colliding with one of the walls, if so it "glues" the player to the wall in that direction instead of moving through it
		if direction == "vertical":
			for i in self.obsticle_list:
				if self.rect.colliderect(i.rect):
					if self.direction.y < 0: #beveger seg opp
						self.rect.top = i.rect.bottom
					if self.direction.y > 0: # beveger seg ned
						self.rect.bottom = i.rect.top

		if direction == "horizontal":
			for i in self.obsticle_list:
				if self.rect.colliderect(i.rect):
					if self.direction.x < 0: #beveger seg opp
						self.rect.left = i.rect.right # setting the player rect left side to the obsticle rect right side
					if self.direction.x > 0: # beveger seg ned
						self.rect.right = i.rect.left


	def update(self):
		self.healthbar.draw(self.rect, self.health)
		self.input()

		# caps the health at 100
		if self.health > 100:
			self.health = 100

		self.display_surface.blit(self.image, self.rect)

		# shoot only if enough time has passed since the last shot
		if self.shoot_delay_index < self.shoot_time:
			self.shoot_delay_index += 1

		for i in self.bullet_list:
			i.update()
			# checks if the bullets from the player has hit a wall, if so delete it
			for ob in self.obsticle_list:
				if ob.rect.colliderect(i.pos):
					try: # i had some errors here, where it sometimes would throw an error, so i just took the wasy way out
						self.bullet_list.remove(i)
					except: 
						pass
			# checks if the bullets from the player hits an enemy, if so hurt it with a random amount and remove the button
			for en in self.enemy_list:
				if en.rect.colliderect(i.pos):
					try:
						en.hurt(self.force * random.randint(0,3))
						self.score += 10
						self.bullet_list.remove(i)
					except Exception as e: 
						print(e)

		# checks the inventory if the player has the key
		for i in self.inventory:
			if i == "key":
				self.has_key = True


	def shoot(self): # gets the angle of the player to the mouse and shoots a bullet in that direction, and also rotates it in that direction
		if self.shoot_delay_index >= self.shoot_time:
			mouse_pos = pygame.mouse.get_pos()
			# get the angle between the player and the mouse
			self.myradians = math.atan2(mouse_pos[0] - self.rect.x, mouse_pos[1] - self.rect.y)

			self.bullet_list.append(Bullet(list(self.rect), self.myradians))
			self.shoot_sound.set_volume(0.5) # play the shoot sound if the player shoots
			self.shoot_sound.play()
			self.shoot_delay_index = 0

