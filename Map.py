"""
	Map.py
	------

	This file/module provides a class for rendering an image as a big'ol map.

	Loads an image and uses the colors of the map as "tiles"

	This will be what we use to render the main game background.

	Because we are using this for the map, this will also be responsible for wall collision (roughly)

"""

# for dat geometry
from email.iterators import typed_subpart_iterator
import math
from turtle import left

# pygame for Vector 2 & etc
import pygame

# main map class
class Map:

	# static constants for tiles
	WALL = 0
	GROUND = 1
	DARK = 2

	# for now our title size will be constant
	TILE_SIZE = 128


	# constructor
	def __init__(self, scene, win):	
		"""Constructs the map

		Args:
			scene (Scene): the scene were built in
			win (Surface): pygam window surface we render to
		"""

		# safe reference to the scene we live in & render window
		self._scene = scene
		self._win = win

		# initialize the pygome stuff we'll need (like image tiles, etc)
		self._setupPygame()

		# None until a map is loaded, after, reference to pygame image surface
		self._mapImage = None


	# initialize pygame stuff in this method to  declutter constructor
	def _setupPygame(self):
		"""Sets up pygame related objects we'll need for the map renderer, so we can tidy up the constructor
		"""

		# load the varius kinds of tiles we use, this time instead of named, we'll use indicies cuz y not
		self._images = [
			pygame.image.load('./img/map/tiles_beeg_stones.png'),
			pygame.image.load('./img/map/tiles_smol_stones.png'),
			pygame.image.load('./img/map/tiles_dark_stone.png'),
		]


	# public method to load a maze png to use as our map
	def loadMap(self, pathToMapImage):

		# load the map image:
		self._mapImage = pygame.image.load(pathToMapImage)


	# checks our loaded map image for a pixel
	def getTileAtPixelPos(self, pos):

		# get x/y depending if a pygameVector2 was passed in, or a tuple
		x = int(pos.x) if isinstance(pos, pygame.Vector2) else int(pos[0])
		y = int(pos.y) if isinstance(pos, pygame.Vector2) else int(pos[1])
		
		# if map image is not define return ground (at least would be able to walk around infinately)
		if(self._mapImage==None):
			return Map.DARK

		# make sure the position is in bounds of our image:
		if(
			x < 0
			or x >= self._mapImage.get_width()
			or y < 0
			or y >= self._mapImage.get_height()):

			# if its out of bounds (OoB), we return solid wall
			return Map.DARK
		
		# otherwise, check the color. For now, we'll just yse the R channel:
		pixelRGB = tuple(self._mapImage.get_at((x, y)))
		redChannel = pixelRGB[0]

		# if it's less than, say 10, we'll assume its black (aka wall)
		if(redChannel < 10):
			return Map.WALL
		elif(redChannel>= 10):
			return Map.GROUND
			

	# draws a tile at a specifc pos
	def drawTile(self, tileType, pos):

		# get tile image to draw from our list
		tileImg = self._images[tileType]

		# blit at point:
		self._win.blit(tileImg, tuple(pos))


	# draws the map based on the current camera positon (and maybe zoom someday)
	def drawMap(self):

		# if we don't have a map loaded yet, gtfo
		if self._mapImage==None:
			return

		# math

		"""
			NOTE: previously we used a different co-ordinate system for the camera / "world"

			However, I decided just to use pixels as the universal coordinate because:
			1) this project is not srs bsns
			2) collision wasn't working and debugging in PX is easier
			3) 8)

			So what we have to do is get the top-left of the camera, convert it to pixels in the map
			then using the width and height of the camera figure out which tiles would be on screen
			
			Note that this math depends on tile-size.

			For now our tiles are 128x128 px, so we'll use that
			Someday this comment may need to be updated if we go with dynamic tile sizes at a later date
		"""

		# for ease of coding, get local copy of camera
		cam = self._scene.camera

		# get the camera's top/left/width/height
		bounds = cam.getCameraBounds()

		# decompose object for easier reading after
		topPx = int(bounds["topLeft"].y)
		leftPx = int(bounds["topLeft"].x)
		RightPx = bounds["bottomRight"].x
		bottomPx = bounds["bottomRight"].y
		width = bounds["width"]
		height = bounds["height"]
		
		# how many tiles could fit on the screen?
		widthInTiles = width // Map.TILE_SIZE
		heightInTiles = height // Map.TILE_SIZE

		# add extra tiles so we can "overscan" whilst scrolling
		widthInTiles += 1
		heightInTiles += 1

		# what is the top left tile of the camera?
		topLeftTileX = leftPx // Map.TILE_SIZE
		topLeftTileY = topPx // Map.TILE_SIZE

		# lastly, the camera can be scrolled to some fractional amount of a tile
		# (i.e. 64, 64 would be halfway through tile, if tiles are 128x128, etc)
		# so we need to calculate the scroll-offset for rendering tiles.
		# done with modulo!
		cameraOffset = pygame.Vector2(
			(-(leftPx % Map.TILE_SIZE)),
		 	(-(topPx % Map.TILE_SIZE))			
		)

		# loop to draw tiles on x / y ranges
		for x in range(0, widthInTiles):
			for y in range(0, heightInTiles):

				# calculate the position we should sample on the map-image:
				samplePos = (topLeftTileX + x, topLeftTileY + y)

				# check our pixel map and figure out which tile should render for this x/y position
				tile = self.getTileAtPixelPos(samplePos)

				# get the screen position this tile should be drawn at:
				tileScreenPos = cameraOffset.copy()
				tileScreenPos.x += (x * Map.TILE_SIZE)
				tileScreenPos.y += (y * Map.TILE_SIZE)

				# draw the tile
				self.drawTile(tile, tileScreenPos)
				