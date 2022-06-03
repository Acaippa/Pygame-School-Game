import pygame

class MainMenu: # The start menu of the game
	def __init__(self):
		pygame.display.set_mode((1300, 700)) # change the size of the window
		self.display_surface = pygame.display.get_surface()
		self.screen_dimentions = self.display_surface.get_size()
		self.middlex = self.screen_dimentions[0] // 2
		self.own_surface = pygame.Surface(self.screen_dimentions)
		self.title_font = pygame.font.SysFont('Sans-Bold', 120)

		self.background = pygame.image.load("images/menu/background.png")
		self.background = pygame.transform.scale(self.background, self.screen_dimentions)
		self.own_surface.blit(self.background, (0, 0))

		self.play_button = Button("Play", (self.middlex, 250), self.own_surface)

		self.quit_button = Button("Quit", (self.middlex, 400), self.own_surface)

		self.title = self.title_font.render("Title of the game", True, "#ffffff")
		self.own_surface.blit(self.title, (self.middlex - self.title.get_rect().width // 2, 40)) # placing the text in the center of the screen, and subtracting half of its own length

		
	def run(self):
		self.display_surface.blit(self.own_surface, (0, 0))
		self.play_button.draw()
		self.quit_button.draw()

class GameOverMenu:
	def __init__(self, player, won):

		if won:
			self.won = "You Won!"
		else:
			self.won = "You Lost!"

		self.init = True # used for updating the score variable in the run function

		self.display_surface = pygame.display.get_surface()
		self.screen_dimentions = self.display_surface.get_size() # get the size of the screen()
		self.title_font = pygame.font.SysFont("Sans", 50)
		self.smaller_font = pygame.font.SysFont("Sans", 30)
		self.player = player

		# here i make my own surface to blit all my things to, then i blit that surface to the display surface
		self.own_surface = pygame.Surface((400, 600))
		self.own_surface_dimentions = self.own_surface.get_size()
		self.own_surface.fill((50, 50, 50))

		# making the title and blitting it
		self.title = self.title_font.render("Game Over", True, "#ffffff")
		self.own_surface.blit(self.title, (self.own_surface_dimentions[0] // 2 - self.title.get_size()[0] // 2, 20))

		# making the <hr> tag again and blittint it 
		self.split_rect = pygame.Rect(0, 130, 300, 1)
		self.split_rect.centerx = self.own_surface_dimentions[0] // 2

		# making the text saying wether or not you won the game
		self.you_won = self.smaller_font.render(self.won, True, "#ffffff")
		self.own_surface.blit(self.you_won, (self.own_surface_dimentions[0] // 2 - self.you_won.get_size()[0] // 2, 80))
		
		pygame.draw.rect(self.own_surface, "#ffffff", self.split_rect)

		# making all the buttons at the bottom
		self.replay_button = Button("Replay", (570, 500), self.display_surface, (0,0,0))
	
		self.quit_button = Button("Quit", (760, 500), self.display_surface, (0,0,0))

	def run(self):

		if self.init: # this only happens once 
			self.score_text = self.smaller_font.render(f"Score: {self.player.score}", True, "#ffffff")
			self.own_surface.blit(self.score_text, (20, 160))
			self.init = False
	
		# blits my own durface, then draws the buttons 
		self.display_surface.blit(self.own_surface, (self.screen_dimentions[0] // 2 - 200, 20))
		self.replay_button.draw()
		self.quit_button.draw()


class Button: # a clickable button (pygame doesnt have inbuilt buttons i think, so i made my own)
	def __init__(self, text, pos, surface, color=(50,50,50)):
		self.display_surface = surface
		self.font = pygame.font.SysFont("Sans", 40)
		self.rendered_font = self.font.render(text, True, "#ffffff")
		self.pos = pos
		self.color = color
		self.clicked = False
		self.active = False # this variable will be used to check if the button is clicked

		self.rect = self.rendered_font.get_rect(center=pos)


		# adding the padding of the button
		self.background_rect = pygame.Rect(self.rect)
		self.background_rect.width += 30
		self.background_rect.x -= 15
		self.background_rect.height += 10
		self.background_rect.y -= 5


	def draw(self):
		print(self.display_surface)
		pygame.draw.rect(self.display_surface, self.color, self.background_rect, 0, 10)
		self.display_surface.blit(self.rendered_font, self.rect)

		# checks if the button was clicked
		if self.rect.collidepoint(pygame.mouse.get_pos()) and self.clicked == False:
			if pygame.mouse.get_pressed()[0]:
				self.clicked = True

		# makes it so that the "active" variable is set to True only when the mousebutton is lifted
		if pygame.mouse.get_pressed()[0] != True and self.clicked == True and self.rect.collidepoint(pygame.mouse.get_pos()):
			self.clicked = False
			self.active = True

