"""
	Player.py
	---------

	In this file/module we'll define the main player class that stores and handles stuff like:

	Players position
	Players Rotation
	Players animation state
	Players health
	Players amo
	Players Input, etc

"""

# for dat geometry
import math

# pygame for Vector 2 & etc
import pygame

# we gonna extend this
from WorldEntity import WorldEntity

# main player Class
class Player(WorldEntity):

	# constructor
	def __init__(self, scene, win, initialX=0, initialY=0, initialRot=0):
		"""Constructs our player character

		Args:
			scene (Scene): The games scene we're in
			win (Surface): pygame window surface we render to
			initialX (int, optional): start x position. Defaults to 0.
			initialY (int, optional): start y position. Defaults to 0.
			initialRot (int, optional): start rotate. Defaults to 0.
		"""

		# call our super constructor
		super().__init__(scene, win, initialX, initialY, initialRot)

		# set some of our player specific properties
		self._health = 100
		self._ammo = 100
		self._infAmmo = True

		# some hard coded values
		self.ROT_SPEED_IN_DEGREES = 10
		self.MOVE_SPEED = .1

		# animation settings
		self._animationWalkCycleBlend = 0

		# set up the pygame resources we'll need for our player
		self._setupPygame()


	# initialize pygame stuff we'll need for our player characater
	def _setupPygame(self):
		"""Sets up pygame related objects we'll need for the character, so we can tidy up the constructor
		"""

		# load in our player images
		self._images =  {
			"head": pygame.image.load('./img/player/char_head.png'),
			"torso": pygame.image.load('./img/player/char_torso.png'),
			"feet": pygame.image.load('./img/player/char_lower.png'),
			"gun": pygame.image.load('./img/player/space_gun.png'),			
		}

		leadOffset = 0

		# hard coded offsets for the invidual pieces
		self._headOffset = pygame.Vector2(41, 41 + leadOffset)
		self._torsoOffset = pygame.Vector2(60, 60 + leadOffset)
		self._feetOffset = pygame.Vector2(39, 39 + leadOffset)
		self._gunOffset = pygame.Vector2(19, 19 + leadOffset)


	# updates our rotation varaible (used for heading movement, and sprite rotation, etc)
	def rotate(self, direction):
		"""Rotates the player logically left (1) or right (-1), and udpates sprites

		Args:
			direction (Number): must be 1 or -1 for left or right, respecitvely
		"""

		# increase this over time, max out at 10
		if(self._animationWalkCycleBlend < 10):
			self._animationWalkCycleBlend = 10

		# adjust our rotation angle
		self.rot += (direction * self.ROT_SPEED_IN_DEGREES)

		# make sure we're in bounds in degrees
		while self.rot < 0:
			self.rot += 360

		# make sure always between 0 and 360
		self.rot = (self.rot % 360)


	# move / walk / run whatever the facing direction
	def move(self, direction):
		"""Moves (walks) the player either forward or backward

		Args:
			direction (Number): either -1 or 1 for backward / forward. Can be scalar
		"""

		# increase this over time, max out at 10
		if(self._animationWalkCycleBlend < 10):
			self._animationWalkCycleBlend = 10

		# use geometry to determine movement
		
		# convert our rotation from degrees to radians
		rotInRadians = self.rot * (math.pi/180.0)

		# get radius for movement, which is direction * our movement speed constant
		movementRadius = direction * self.MOVE_SPEED

		# make vector 2 with new heading
		newPosComponent = pygame.Vector2(math.sin(rotInRadians) * movementRadius, math.cos(rotInRadians) *movementRadius)

		# add to our position
		self.pos = self.pos + newPosComponent


	# fire gun
	def fire(self):

		# this'll do for now
		print("bang!")


	# public method called from our Scene to have the player handle input
	def checkPlayerInput(self, keysDownEvents = []):
		"""Checks input relevant to player

		Args:
			keysDownEvents (list, optional): List of key down events passed in from scene. Defaults to [].
		"""

		# while it's true we're passed in keydown events, we only care about that for firing
		# we'll use the active keys for rotation and movement
		activeKeys = pygame.key.get_pressed()

		# left/a is rotate left:
		if activeKeys[pygame.K_LEFT] or activeKeys[pygame.K_a]:
			self.rotate(1)

		# right/d is rotate right:
		if activeKeys[pygame.K_RIGHT] or activeKeys[pygame.K_d]:
			self.rotate(-1)

		# up/w is walk forward
		if activeKeys[pygame.K_UP] or activeKeys[pygame.K_w]:
			self.move(1)

		# down/s is walk backward
		if activeKeys[pygame.K_DOWN] or activeKeys[pygame.K_s]:
			self.move(-1)

		# now that we're done with the active key logic we can check if fire was pressed
		for event in keysDownEvents:
			
			# skip non key events
			if(event.type==pygame.KEYDOWN):

				# if its space, fire
				if(event.key == pygame.K_SPACE):
					self.fire()


	# copied from SO, easy rotate on center script	
	def blitRotateCenter(self, surface, image, topleft, angle):
		"""Rotates pygame image surface on center

		Args:
			surafe (Surface): target pygame surface
			image (Surface): source pygame surface image
			topleft (Tuple): top left pos tuple
			angle (Number): rotation angle
		"""

		# rotate the images
		rotated_image = pygame.transform.rotate(image, angle)
		new_rect = rotated_image.get_rect(center = image.get_rect(topleft = topleft).center)

		# new_new_rect = (new_rect[0] - (rotated_image.get_width()//2), new_rect[1] - (rotated_image.get_height()//2))

		# copy rotated image to surface
		surface.blit(rotated_image, new_rect)


	# draws player to screen
	def draw(self):

		# find where on screen we should be relative to the camera
		screenPos = self._scene.camera.getScreenPos(self.pos)
		
		# always decrease this over time, till we hit 0
		if(self._animationWalkCycleBlend > 0):
			self._animationWalkCycleBlend -= 1

		# normalize walk cycle blend value
		aniWalkCycleBlendNormalised = (self._animationWalkCycleBlend/10.0)

		# use the games time in miliseconds + 
		sineTime = pygame.time.get_ticks() * .01

		# calculate rotational offsets for feet, torso and head in degrees
		feetRotOffset = math.sin(sineTime) * 10 * aniWalkCycleBlendNormalised
		torsoRotOffset = math.sin(sineTime) * -10 * aniWalkCycleBlendNormalised
		headRotOffset = math.cos(sineTime) * 7 * aniWalkCycleBlendNormalised +(math.sin(sineTime*0.1) * 5)
		
		# we'll also always scale the torso on a mild sine curve to imply breathing
		torsoScalar = 1.0 + (math.sin(sineTime * 0.17) * 0.05)
		newTorsoOffset = self._torsoOffset * torsoScalar
		newSizeVector2 = newTorsoOffset * 2
		imgTorsoScaled = pygame.transform.scale(self._images["torso"], newSizeVector2)

		# while the gun is rotated facing the same direction as the player
		# it also needs it's own rotated X/Y offset, so lets calculate that before we draw everying else
		gunRadius = 60 * torsoScalar
		gunRotationFromPlayer = (self.rot + torsoRotOffset + 140) * (math.pi / 180)
		gunPos = screenPos + pygame.Vector2(math.sin(gunRotationFromPlayer) * gunRadius, math.cos(gunRotationFromPlayer) * gunRadius)

		# rotate bit to screen. ORDER MATTERS! bottom-to-top
		self.blitRotateCenter(self._win, self._images["feet"], screenPos-self._feetOffset, self.rot+feetRotOffset)
		self.blitRotateCenter(self._win, imgTorsoScaled, screenPos-newTorsoOffset, self.rot+torsoRotOffset)
		self.blitRotateCenter(self._win, self._images["head"], screenPos-self._headOffset, self.rot+headRotOffset)
		self.blitRotateCenter(self._win, self._images["gun"], gunPos-self._gunOffset, self.rot)
		