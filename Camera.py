"""
	Camera.py
	---------

	This file/module provides a class that acts as a logical camera.

	Note, that I say 'logical camera' because this camera does not actually render anything!

	(That will all be handled in our GameScreen.render() method)

	Rather, this class will just store the X/Y location in the game world we should be rendering.

	Also, possibly prodive some function for Zoom, Rotate, or Lerp-Pan down the road.

	So, in otherwords, this handles the logic around the games "camera", not actually rendering.
"""

# pygame for Vector 2 & etc
import pygame

# we gonna extend this
from WorldEntity import WorldEntity

# main Camera cass
class Camera(WorldEntity):

	# constructor
	def __init__(self, scene, win, initialX=0, initialY=0):
		"""Constructs the Camera object

		Args:
			scene (Scene): the game's scene we're in
			win (Surface): the pygame render surface for our window
		"""

		# call super, we can ignore all params for now
		super().__init__(scene, win, initialX, initialY)

		# for now our window is non-resizable
		# and TBH idk if pygame supports that
		# and TBevenmoreH idk if I wanna support that
		# so lets just get stuff out of the way
		self._winW = self._win.get_width()
		self._winH = self._win.get_height()

		# center of screen is half W/H
		self._center = pygame.Vector2(self._winW // 2, self._winH // 2)

		# world scale
		# we'll say some arbitary pixel amount is 1 world coordinate, e.g. 100 pixels = 1 unit
		self.worldScale = 128

		# not sure if I plan on supporting this, but ill leave it here just in case
		# how much we are zooming
		self.zoom = 1
	

	# public method to update camera position in game co-ordinates
	def moveTo(self, newPos):
		"""public method to update camera position in game coordinates

		Args:
			newPos (Vector2): new pos, as pygame Vector2
		"""

		# update our position
		self.pos = newPos

	
	# helper function to get screen coordinates of a tuple from our camera position
	def getScreenPos(self, pos):
		"""Gets where on screen an object should be in pixels, from it's position relative to the camera in world coordinates

		Args:
			pos (Vector2): pygame Vector2 in game coordinates

		Returns:
			Vector2: pygame Vector2 tuple in screen position pixels
		"""

		# our pos will be a tuple in game world coordinates
		# however, instead of the top-left of the screen, we'll assume the center of the camera is 0,0

		# so with that in mind, figure out where the position is relative to center of camera in world scale
		posRelativeToCamera = self.pos - pos

		# convert to pixels:
		posRelativeToCameraInPixels = posRelativeToCamera * self.worldScale

		# add to center of screen to get final screen coordinates
		return self.center + posRelativeToCameraInPixels

		# add to center of screen to get final screen coordinates
		return (self._center.x + posRelativeToCameraInPixels[0], self._center.y + posRelativeToCameraInPixels[1])



	# helper function to get the bounds of the camera
	def getCameraBounds(self):
		"""Gets the top/bottom/left/right postion of the camera in world units

		Returns:
			dict: a dictionary with top/bottom/left/right values
		"""

		return {
			"top": self.pos.y - (self._center.y / 128),
			"bottom": self.pos.y + (self._center.y / 128),
			"left": self.pos.x - (self._center.x / 128),
			"right": self.pos.x + (self._center.x / 128),
		}

	@property
	def center(self):
		return self._center