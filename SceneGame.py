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

# crucial: require the player /s
from Player import Player

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
		self.camera = Camera(self, win)

		# make a new player object
		self.player = Player(self, win, 100, 100, 0)

		# move camera to player:
		self.camera.moveTo(self.player.pos)

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

		# get all the events that happened so we can pass to to things that might care
		# NOTE: 1) this will clear the stack of events
		# NOTE: 2) havnt each object loop over them is stupid, will need better event dispatch later
		recentEvents = pygame.event.get(pygame.KEYDOWN)

		# update our player:
		self.player.checkPlayerInput(recentEvents)

		# move camera to player:
		# self.camera.moveTo(self.player.pos)


	# method for rendering scene
	def render(self):
		"""Render method for pygame schizz
		"""

		# do super stuffs, if any
		super().render()

		# draw our background of the title screen
		self._win.fill((0, 0, 0))

		# draw our player
		self.player.draw()

		# update the display
		pygame.display.update()

