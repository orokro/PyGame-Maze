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

# our various scene objects and systems
from ParticleSystem import ParticleSystem
from Camera import Camera
from Map import Map
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
		self.player = Player(self, win, 512, 396, 0)

		# create our particle system so we can spawn particles & udpate em & etc
		self.particles = ParticleSystem(self, win)

		# move camera to player:
		self.camera.move_to(self.player.pos)

		# create new map renderer & load level one map
		self.map = Map(self, win)
		self.map.load_map('./levels/level_02/map.png')

		# we'll hard code title in this file, we dont need to pass it in
		super().__init__(game, win, "Game Play Screen")

		# subscribe to various events we might care about
		self.subscribe_events()


	# set up event handlers for any objects we care to listen to
	def subscribe_events(self):
		"""Some objects may fire events. Well subcribe to most or all of them here, for tidyness sake
		"""

		# player has event for firing...
		self.player.events.onFire.add_listener(self.shoot)


	# event handler for when player fires his gun
	def shoot(self, player):
		"""Handle event when player fires his gun

		Args:
			player (Player): the player that fired
		"""

		# collect our variables
		pType = ParticleSystem.TYPES.BULLET
		pos = self.player.handPos
		angle = self.player.rot
		speed = 10

		self.particles.spawn_particle(pType, pos, angle, speed)


	# method called when we enter this scene
	def scene_enter(self):
		"""Called when we enter this scene
		"""

		# do super stuffs, if any
		super().scene_enter()

		# for debug and whatnot
		print(f"Doing game play screen business...")


	# method called when we exit this scene
	def scene_exit(self):
		"""Called when we exit this scene
		"""

		# do super stuffs, if any
		super().scene_exit()

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
		self.player.check_player_input(recentEvents)

		# update our particles
		self.particles.update()

		# move camera to player:
		self.camera.move_to(self.player.pos)


	# method for rendering scene
	def render(self):
		"""Render method for pygame schizz
		"""

		# do super stuffs, if any
		super().render()

		# draw our background of the title screen
		self._win.fill((0, 0, 0))

		# draw map before player & other stuff on top
		self.map.draw_map()

		# draw our player
		self.player.draw()

		# draw our particles
		self.particles.draw()
				
		# update the display
		pygame.display.update()

