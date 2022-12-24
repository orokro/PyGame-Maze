"""
	WorldEntity.py
	--------------

	I may be prematurely optimizing and/or overengineering here, but hear me out:

	All the things in our main GameScene will probably need co-ordinates on screen, maybe rotation as well.

	They'll probably all want a reference tot he scene and a reference to the window.

	So lets make a base class here for world entities, just 'cause
"""

# for vector maffs
import pygame

# Basis for one screen things in the main game scene (not for TitleScreen or Ending Screen... yet)
class WorldEntity:

	# cosntructor
	def __init__(self, scene, win, x=0, y=0, rot=0, w=10, h=10):
		"""Constructor for WorldEntity class that will store mostly positional data common to onscreen things

		Args:
			scene (Scene): Scene we belong to
			win (Surface): pygame surface we render to for the window
			x (int, optional): x pos. Defaults to 0.
			y (int, optional): y pos. Defaults to 0.
			rot (int, optional): rotate. Defaults to 0.
			w (int, optional): width. Defaults to 10.
			h (int, optional): height. Defaults to 10.
		"""

		# save scene and window arguments
		self._scene = scene
		self._win = win

		# save positional and dimensional data
		self.pos = pygame.Vector2(x, y)
		self.rot = rot
		self.width = w
		self.height = h

