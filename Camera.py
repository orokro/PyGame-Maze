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

# main Camera cass
class Camera:

	# constructor
	def __init__(self, scene, win):
		"""Constructs the Camera objec

		Args:
			scene (Scene): the game's scene we're in
			win (Surface): the pygame render surface for our window
		"""

		# save reference to the scene we're in
		# (We probably don't need to go all the way up to game reference)
		self._scene = scene

		# also save the window we're rendering in.
		# NOTE: we COULD technically just access scene._win, but it's private and exposing it seems weird
		self._win = win

		# for now our window is non-resizable
		# and TBH idk if pygame supports that
		# and TBevenmoreH idk if I wanna support that
		# so lets just get stuff out of the way
		self._winW = win.get_width()
		self._winH = win.get_height()

		# center of screen is half W/H
		self._centerX = self._winW // 2
		self._centerY = self._winH // 2

		# for debug
		# print(f'Screen Center: {self._centerX}, {self._centerY}')

		# initial pos for now
		self.x = 0
		self.y = 0

		# world scale
		# we'll say some arbitary pixel amount is 1 world coordinate, e.g. 100 pixels = 1 unit
		self._worldScale = 100

		# not sure if I plan on supporting this, but ill leave it here just in case
		# how much we are zooming
		self.zoom = 1
	

	# public method to update camera position in game co-ordinates
	def moveTo(self, x, y):
		"""public method to update camera position in game coordinates

		Args:
			x (Number): x pos of camera in game world
			y (Number): y pos of camera in game world
		"""

		# update our position
		self.x = x
		self.y = y

	
	# helper function to get screen coordinates of a tuple from our camera position
	def getScreenPos(self, pos):
		"""Gets where on screen an object should be in pixels, from it's position relative to the camera in world coordinates

		Args:
			pos (Tuple): (X, Y) tuple position

		Returns:
			Typle: (X, Y) tuple in screen position pixels
		"""

		# our pos will be a tuple in game world coordinates
		# however, instead of the top-left of the screen, we'll assume the center of the camera is 0,0

		# so with that in mind, figure out where the position is relative to center of camera in world scale
		posRelativeToCamera = (self.x - pos[0], self.y - pos[1])

		# convert to pixels:
		posRelativeToCameraInPixels = (posRelativeToCamera[0] * self._worldScale, posRelativeToCamera[1] * self._worldScale)

		# add to center of screen to get final screen coordinates
		return (self._centerX + posRelativeToCameraInPixels[0], self._centerY + posRelativeToCameraInPixels[1])
