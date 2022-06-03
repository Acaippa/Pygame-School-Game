"""
This module is responsible for controlling what should be displayed on the screen
"""

import pygame
from data.level import Level
from data.menu.menu_ import*

screen = pygame.display.set_mode((1500, 600))
pygame.display.set_caption("Skattespill")

game = True
game_state = "Main_menu"

def start(): # initiates all the level objects. Its also used as a reset function
	global main_level
	global main_menu
	global game_over_menu_win
	global game_over_menu_lose

	main_level = Level()
	main_menu = MainMenu()
	game_over_menu_win = GameOverMenu(main_level.player, True)
	game_over_menu_lose = GameOverMenu(main_level.player, False)

start()

"""
[SOME NOTES]
the game cane be a bit laggy at times, due to the player detection thing not being optimized

there are some modules you will need to install in order for this to work:

threading
math (maybe)

"""
clock = pygame.time.Clock() # pygame clokc module used to regulate the framerate

while game: # main gameloop
	for event in pygame.event.get(): # loop through all of the pygame events and check if the close window variable is true. if so, break the loop
		if event.type == pygame.QUIT:
			game = False

	screen.fill('black') # i fill the screen black to clear it, and prepare it to draw the new frame on it

	# according to the current game state, the game loop runs different games and or menus
	if game_state == "Main_menu":
		main_menu.run()

		if main_menu.play_button.active: # checks if the button in the menu is clicked
			game_state = "game"

		if main_menu.quit_button.active: # quit if the quit button is placed
			break

	if game_state == "game":
		main_level.run(clock.get_fps()) # passing in the fps to blit it on the surface during gameplay
		if main_level.game == False:
			if main_level.won:
				game_state = "game_over_win"
			else:
				game_state = "game_over_lose"

	if game_state == "game_over_win":
		main_level.idle()
		game_over_menu_win.run()

		if game_over_menu_win.replay_button.active:
			start()
			game_state = 'game'

		if game_over_menu_win.quit_button.active:
			start()
			game_state = 'Main_menu'

	if game_state == "game_over_lose":
		main_level.idle()
		game_over_menu_lose.run()

		if game_over_menu_lose.replay_button.active:
			start()
			game_state = 'game'

		if game_over_menu_lose.quit_button.active:
			start()
			game_state = 'Main_menu'


	pygame.display.flip() # update the pygame display
	clock.tick(60) # cap the framerate as 60 fps

pygame.quit() # when we break out of the game loop, this is the next line that executes.
