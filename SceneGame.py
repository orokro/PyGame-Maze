"""
	SceneGame.py
	------------

	This file/module provides the scene to house our main gameplay screen logic.

	The class we export will extend the Scene base-class.
"""

# we're gonna use pygame for our rendering, etc
import pygame

# import Scene since we finna use that
from Scene import Scene

# import our camera class
from Camera import Camera

# Game screen scene, extends Scene
class GameScreen(Scene):

	# constructor
	def __init__(self, game, win):
		"""Builds GameScreen scene

		Args:
			game (MazeGame): reference to our main game isntance
			win (Surface): pygame surface for rendering
		"""

		# make our camera we'll use for moving around our world
		self._cam = Camera(self, win)

		# we'll hard code title in this file, we dont need to pass it in
		super().__init__(game, win, "Game Play Screen")


	# method called when we enter this scene
	def sceneEnter(self):
		"""Called when we enter this scene
		"""

		# do super stuffs, if any
		super().sceneEnter()

		# for debug and whatnot
		print(f"Doing game play screen business...")


	# method called when we exit this scene
	def sceneExit(self):
		"""Called when we exit this scene
		"""

		# do super stuffs, if any
		super().sceneExit()

		# for debug and whatnot
		print(f"Game play scene says buh-bye")


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
		self._win.fill((0, 0, 0))
		
		# update the display
		pygame.display.update()
