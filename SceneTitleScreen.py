"""
	SceneTitleScreen.py
	-------------------

	This file/module provides the scene to house our Title screen logic.

	The class we export will extend the Scene base-class.
"""

# we're gonna use pygame for our rendering, etc
import pygame

# import Scene since we finna use that
from Scene import Scene

# Title screen scene
class TitleScreen(Scene):

	# constructor
	def __init__(self, game, win):
		"""Builds TitleScreen scene

		Args:
			game (MazeGame): reference to our main game isntance
			win (Surface): pygame surface for rendering
		"""
		# we'll hard code title in this file, we dont need to pass it in
		super().__init__(game, win, "Title Screen")

		# well load our just the picture for the title screen here, in this scene
		self._images = {
			"bg": pygame.image.load('./img/TitleScreen_BG.png')
		}

	# method called when we enter this scene
	def sceneEnter(self):
		"""Called when we enter this scene
		"""

		# do super stuffs, if any
		super().sceneEnter()

		# for debug and whatnot
		print(f"Doing title screen business...")


	# method called when we exit this scene
	def sceneExit(self):
		"""Called when we exit this scene
		"""

		# do super stuffs, if any
		super().sceneExit()

		# for debug and whatnot
		print(f"Title Screen says buh-bye")


	# method for doing update logic on this scene
	def update(self):
		"""Update logic method
		"""

		# do super stuffs, if any
		super().update()

		pass


	# method for rendering scene
	def render(self):
		"""Render method for pygame schizz
		"""

		# do super stuffs, if any
		super().render()

		# draw our background of the title screen
		self._win.blit(self._images["bg"], (0, 0))
		
		# update the display
		pygame.display.update()
