"""
	WorldEntity.py
	--------------

	I may be prematurely optimizing and/or overengineering here, but hear me out:

	All the things in our main GameScene will probably need co-ordinates on screen, maybe rotation as well.

	They'll probably all want a reference tot he scene and a reference to the window.

	So lets make a base class here for world entities, just 'cause
"""

# for misc maffs
import math

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

		# speed (might not be used by all subclasses)
		self.speed = 1

	
	# moves ourself by our self-defined variables
	def default_move(self):
		"""Basically, a light weight wrapper for moveByAngleAndMagnitute to use our self props
		"""

		# call our gernci move by angle/magnitude method with our self params
		self.move_by_angle_and_magnitude(self.rot, self.speed)


	# helper function for angle sin/cos movement
	def move_by_angle_and_magnitude(self, angle, magnitude, returnInsteadOfApply = False):
		"""Moves our pos by an Angle (in degrees) and by some magnitute

		Args:
			angle (Number): angle to move towards
			magnitude (Number): radius in world pixels
			returnInsteadOfApply (bool, optional): Set true to return movement x/y instead of applying immediately. Defaults to False.

		Returns:
			Vector2: either, our old pos, OR the movement compoinent
		"""

		# convert to radians
		angleInRadians = angle * (math.pi/180.0)

		# compute new position component as Vector2
		moveComponent = pygame.Vector2(math.sin(angleInRadians) * magnitude, math.cos(angleInRadians) * magnitude)

		# if we're asked to return the compoent, isntead of applying, do so now
		if(returnInsteadOfApply==True):
			return moveComponent

		# save old position
		oldPos = self.pos.copy()

		# update our position with this component
		self.pos -= moveComponent

		# return the old position
		return oldPos

