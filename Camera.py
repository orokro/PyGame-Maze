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
			scene (Scene): The game's scene we're in
			win (Surface): the pygame render surfacec for our window
			initialX (int, optional): x start position. Defaults to 0.
			initialY (int, optional): y start position. Defaults to 0.
		"""

		# call super, we can ignore all params for now
		super().__init__(scene, win, initialX, initialY)

		# for now our window is non-resizable
		# and TBH idk if pygame supports that
		# and TBevenmoreH idk if I wanna support that
		# so lets just get stuff out of the way & cache the size once
		self._winW = self._win.get_width()
		self._winH = self._win.get_height()

		# center of screen is half W/H
		self._center = pygame.Vector2(self._winW // 2, self._winH // 2)

		# not sure if I plan on supporting this, but ill leave it here just in case
		# how much we are zooming
		self.zoom = 1
	

	# public method to update camera position to some pixels
	def moveTo(self, newPos):
		"""public method to update camera position in game pixel coordinates

		Args:
			newPos (Vector2): new pos, as pygame Vector2
		"""

		# update our position
		self.pos = newPos


	# helper function to get screen coordinates of a vector2 from our camera position
	def getScreenPos(self, pos):
		"""Gets where on screen an object should be in pixels, from it's position relative to the camera in world coordinates

		Args:
			pos (Vector2): pygame Vector2 in game coordinates

		Returns:
			Vector2: pygame Vector2 tuple in screen position pixels
		"""

		# we want to think of our x/y position as the center of the screen, so we should subtract
		# center to get what would be the top-left pixel of the window:
		windowTopLeft = self.topLeftInPixels

		# now we should get the vector from top left TO object pos
		# tip-minus-tail:
		screenPos = pos-windowTopLeft

		# add to center of screen to get final screen coordinates
		return screenPos


	# gets the top left of the camera in screen/world pixels
	# (well, screen is always 0,0, but where is that top left in the world?)
	@property
	def topLeftInPixels(self):
		"""Gets the cameras top-left corner in world pixels

		Returns:
			Vector2: the world pos of the top left of the camera
		"""

		# ez-pz
		return (self.pos - self.center)
	

	# gets the bottom of the camera in screen/world pixels
	# (well, screen is always w,h, but where is that bottom right in the world?)
	@property
	def bottomRightInPixels(self):
		"""Gets the camerasbottom-right corner in world pixels

		Returns:
			Vector2: the world pos of the bottom-right of the camera
		"""

		# ez-pz
		return (self.pos + self.center)
	

	# helper function to get the bounds of the camera
	def getCameraBounds(self):
		"""Gets the top/bottom/left/right postion of the camera in world units

		Returns:
			dict: a dictionary with top/bottom/left/right values
		"""

		return {
			"topLeft": self.topLeftInPixels,
			"bottomRight": self.bottomRightInPixels,
			"width": self._winW,
			"height": self._winH,
		}


	@property
	def center(self):
		return self._center
