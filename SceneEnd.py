"""
	SceneEnding.py
	--------------

	This file/module provides the scene to house our main gameover / end screen logic.

	The class we export will extend the Scene base-class.
"""

# we're gonna use pygame for our rendering, etc
import pygame

# import Scene since we finna use that
from Scene import Scene

# Game screen scene, extends Scene
class EndScreen(Scene):

	# constructor
	def __init__(self, game, win):
		"""Builds EndScreen scene

		Args:
			game (MazeGame): reference to our main game isntance
			win (Surface): pygame surface for rendering
		"""
		# we'll hard code title in this file, we dont need to pass it in
		super().__init__(game, win, "Ending Screen")


	# method called when we enter this scene
	def scene_enter(self):
		"""Called when we enter this scene
		"""

		# do super stuffs, if any
		super().scene_enter()

		# for debug and whatnot
		print(f"Doing ending screen business...")


	# method called when we exit this scene
	def scene_exit(self):
		"""Called when we exit this scene
		"""

		# do super stuffs, if any
		super().scene_exit()

		# for debug and whatnot
		print(f"Ending scene says buh-bye")


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
		self._win.fill((255, 255, 255))
		
		# update the display
		pygame.display.update()
