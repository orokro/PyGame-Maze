"""
	MapRenderer.py
	--------------

	This file/module provides a class for rendering an image as a big'ol map.

	Loads an image and uses the colors of the map as "tiles"

	This will be what we use to render the main game background.

	Because we are using this for the map, this will also be responsible for wall collision (roughly)

"""

# for dat geometry
from email.iterators import typed_subpart_iterator
import math

# pygame for Vector 2 & etc
import pygame

# main map renderer class
class MapRenderer:

	# static constants for tiles
	WALL = 0
	GROUND = 1
	DARK = 2	

	# constructor
	def __init__(self, scene, win):	
		"""Constructs the map renderer

		Args:
			scene (Scene): the scene were built in
			win (Surface): pygam window surface we render to
		"""

		# safe reference to the scene we live in & render window
		self._scene = scene
		self._win = win

		# initialize the pygome stuff we'll need (like image tiles, etc)
		self._setupPygame()

		# None until a map is loaded
		self._mapImage = None


	# initialize pygame stuff in this method to  declutter constructor
	def _setupPygame(self):
		"""Sets up pygame related objects we'll need for the map renderer, so we can tidy up the constructor
		"""

		# load the two kinds of tiles we use, this time instead of named, we'll use indicies cuz y not
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

		# if map image is not define return ground (at least would be able to walk around infinately)
		if(self._mapImage==None):
			return MapRenderer.DARK

		# make sure the position is in bounds of our image:
		if(
			pos.x < 0
			or pos.x >= self._mapImage.get_width()
			or pos.y < 0
			or pos.y >= self._mapImage.get_height()):

			# if its out of bounds (OoB), we return solid wall
			return MapRenderer.DARK

		# invert to picture coordinations
		# pos.x = self._mapImage.get_width() - pos.x
		# pos.y = self._mapImage.get_height() - pos.y
		
		# otherwise, check the color. For now, we'll just yse the R channel:
		pixelRGB = tuple(self._mapImage.get_at((int(pos.x), int(pos.y))))
		redChannel = pixelRGB[0]

		# if it's less than, say 10, we'll assume its black (aka wall)
		if(redChannel < 10):
			return MapRenderer.WALL
		elif(redChannel>= 10):
			return MapRenderer.GROUND
			

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
			Right, so - game / camera use world units, which right now are 128 pixels in size.

			Incidentally, that's also the size of our map tiles. Huh, fancy that.

			So in the image file we loaded, each pixel is 1 tile, where black pixels = walls and white pixels = land

			So to render the map, we need to convert the camera's position into map pixels

			Then loop to draw the tiles
		"""

		# for ease of coding, get local copy of camera
		cam = self._scene.camera

		# how many files fit on screen?
		screenWidthInTiles = self._win.get_width() // cam.worldScale
		screenHeightInTiles = self._win.get_height() // cam.worldScale
		
		# get the half screen size
		halfScreenWidthInTiles = (screenWidthInTiles // 2)
		halfScreenHeightInTiles = (screenHeightInTiles // 2)

		# "overscan" to fit more on the map
		rangeWidth = halfScreenWidthInTiles + 4
		hangeHeight = halfScreenHeightInTiles + 4

		# determine the range we should loop for on both axies:
		xRange = range(-rangeWidth, rangeWidth)
		yRange = range(-hangeHeight, hangeHeight)
		
		# get the camera fractional offset
		cameraFrac = pygame.Vector2( math.modf(cam.pos.x)[0] * cam.worldScale, math.modf(cam.pos.y)[0] * cam.worldScale)

		# loop to draw tiles on x / y ranges
		for x in xRange:
			for y in yRange:

				# get tile at this position:
				tilePos = pygame.Vector2(int(cam.pos.x) - x, int(cam.pos.y) - y)
				tile = self.getTileAtPixelPos(tilePos)

				# for debug
				# if(x==0 and y==0):
					# print(cam.pos)
					# continue

				# draw center tile will be when the range is in the middle
				centerTilePos = cam.center - (pygame.Vector2(cam.worldScale, cam.worldScale) // 2)

				# adjust tile pos by current x/y (center would be 0, 0 in middle)
				pixelPos = centerTilePos + (pygame.Vector2(x, y) * cam.worldScale) + cameraFrac

				# draw the tile
				self.drawTile(tile, pixelPos)
				


	


