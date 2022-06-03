"""
This modules houses the enemy object
"""
import pygame
import math
import threading as th
from data.bullet import*
from data.healthbar import*
import random

class Enemy:
	"""
	[__init__]
		pos: tuple
		player: object / string
		obsticles: list

	Makes an enemy at "pos", and constantly looks to see if they have a clear path to the player, by checking if the bullets would collide with something from the "obsticles" list. 
	It uses the "player" to check if the path is clear, then it will shoot towards it
	"""
	def __init__(self, pos, player, obsticles):
		self.display_surface = pygame.display.get_surface()
		self.image = pygame.image.load("images/enemy/enemy.png").convert_alpha() # convert alpha makes it so that the image is transparent
		w, h = self.image.get_size()
		self.image = pygame.transform.scale(self.image, (w*3, h*3))
		self.rect = pygame.rect.Rect(pos[0], pos[1], w+20, h+20) # making a rect that is a bit bigger than the image  
		self.pos = pos[0] + self.image.get_width() // 2, pos[1] + self.image.get_height() // 2 # changing the pos to be the middle of the image
		self.rect.center = self.pos # moving the senter of the rect to the "pos"

		self.shoot_bool = False

		self.obsticle_list = obsticles
		self.healthbar = HealthBar() # initiating the healthbar

		self.player = player # passing a reference to the player, so the enemy can interact with it
		self.shoot_delay = 0
		self.living = True
		self.health = 100
		self.angle = 0 # its current angle

		self.force = 5 # the base value for the damage of the player

		self.bullet_list = [] # making a list with all the bullets

		# used for the hurt shake
		self.hurt_animation = 0
		self.hurt_index = 0 

		self.shoot_sound = pygame.mixer.Sound("audio/enemy_shoot.mp3")
		self.shoot_sound.set_volume(0.2)

	def update(self): # this keeps track of many values and bullets etc.
		# calculate the angle between the enemy and the player
		self.myradians = math.atan2(self.player.rect.centerx-self.pos[0], self.player.rect.centery-self.pos[1])

		self.angle = math.degrees(self.myradians) - 180 # converting from radiants to degrees and flipping the gun

		# rotating the image and updating the player rect to prevent the player from getting morphed
		self.can_see_player()
		if self.shoot_bool:
			self.display_image = pygame.transform.rotate(self.image, self.angle)
			self.shoot()
		else:
			self.display_image = self.image
			

		for i in self.bullet_list: # update all the bullets in the bullet list
			i.update()

			if self.player.rect.collidepoint(i.pos): # check if the player rect collides with the bullet
				# hurt the player and remove the bullet from the drawing list
				self.player.hurt(int(self.force * random.randint(0, 4)))
				self.bullet_list.remove(i)

			for ob in self.obsticle_list: # checks if the bullet 
				if ob.rect.collidepoint(i.pos):
					self.bullet_list.remove(i)

	def hurt(self, value): # removes health if current health - hurt value is more than 0
		self.hurt_animation = True
		if self.health - value * 2 <= 0:
			self.living = False
			self.health = 100
			
		self.health -= value

	def draw(self):
		self.update()
		self.healthbar.draw(self.rect, self.health) # drawing the healthbar instance
		if self.hurt_animation:
			# this shakes the enemy a little
			self.display_surface.blit(self.display_image, (self.pos[0] - self.display_image.get_width() // 2 - (2 * math.sin(math.radians(random.randint(0, 360)))), self.pos[1] - self.display_image.get_height() // 2 - (2 * math.cos(math.radians(random.randint(0,360))))))
			if self.hurt_index >= 10:
				self.hurt_animation = False
				self.hurt_index = 0
			self.hurt_index += 1
		else:
			self.display_surface.blit(self.display_image, (self.pos[0] - self.display_image.get_width() // 2, self.pos[1] - self.display_image.get_height() // 2)) # blitting the image with the origin at the center

	def shoot(self): # if the shoot time is less
		if self.shoot_delay < 20:
			self.shoot_delay += 1
		else:
			# "spawning" one bullet for each barrel of the gun
			self.shoot_sound.play()
			self.bullet_list.append(Bullet(list(self.pos), self.myradians))
			self.bullet_list.append(Bullet(list((self.pos[0]-17, self.pos[1])), self.myradians))
			self.shoot_delay = 0

	def can_see_player_start(self): # this starts the thread for the can_see_player
		thread = th.Thread(target=self.can_see_player)
		thread.setDaemon(1) # makes it so the thread wont continute even if we close the program mid execution
		thread.start() # starts the thread
		thread.join() # uhh im not really sure abt what this does, but atleast it makes us able to get some sort of return value from the function thread


	def can_see_player(self): # places rects in the direction of the player, if the rectangles collide with a wall, shoot_bool is False and the enemy wont shoot or look at the player
		self.looking_x, self.looking_y = self.pos[0], self.pos[1]

		looking = True
		while looking:
			# move the rect towards the player
			self.looking_x = self.looking_x + (10 * math.sin(self.myradians))
			self.looking_y = self.looking_y + (10 * math.cos(self.myradians))
			rect = pygame.Rect(self.looking_x,self.looking_y, 15, 15)	

			# check for collision with the player
			if self.player.rect.colliderect(rect):
				looking = False
				self.shoot_bool = True

			else:
				for i in self.obsticle_list:
					if i.rect.colliderect(rect):
						looking = False
						self.shoot_bool = False
