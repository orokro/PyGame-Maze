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

# gonna need this for collision
from Map import Map

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
		self.ROT_SPEED_IN_DEGREES = 5
		self.MOVE_SPEED = 4

		# animation settings
		self._animationWalkCycleBlend = 0

		# set up the pygame resources we'll need for our player
		self._setup_pygame()

		# keep track of coillision points for debug
		self.colPoints = []


	# initialize pygame stuff we'll need for our player characater
	def _setup_pygame(self):
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


	# our animation timer for walk cycle is set on (max)
	def _enable_walk_cycle_animation(self):
		"""Sets our walk cycle variable to max, whenever there's keyboard input
		"""

		# set to max, it will drain after keys are let go. max out at 10
		if self._animationWalkCycleBlend < 10:
			self._animationWalkCycleBlend = 10


	# updates our rotation varaible (used for heading movement, and sprite rotation, etc)
	def rotate(self, direction):
		"""Rotates the player logically left (1) or right (-1)

		Args:
			direction (Number): must be 1 or -1 for left or right, respecitvely
		"""

		# sets our walk cycle animation to max
		self._enable_walk_cycle_animation()

		# adjust our rotation angle
		self.rot += (direction * self.ROT_SPEED_IN_DEGREES)

		# make sure we're in bounds in degrees
		while self.rot < 0:
			self.rot += 360

		# make sure always between 0 and 360
		self.rot = (self.rot % 360)


	# move / walk / run whatever the facing direction
	def move(self, direction, strafe=False):
		"""Moves (walks) the player either forward or backward

		Args:
			direction (Number): either -1 or 1 for backward / forward. Can be scalar
			strafe (bool, optional): set true to move perpendicular (add bonus 90 degrees)
		"""

		# sets our walk cycle animation to max
		self._enable_walk_cycle_animation()

		# ternary for straf modifier
		strafeModifierAngle = 90 if (strafe is True) else 0

		# use geometry to determine movement
		
		# convert our rotation from degrees to radians
		rotInRadians = (self.rot + strafeModifierAngle) * (math.pi/180.0)

		# get radius for movement, which is direction * our movement speed constant
		movementRadius = direction * self.MOVE_SPEED

		# make vector 2 with new heading
		newPosComponent = pygame.Vector2(math.sin(rotInRadians) * movementRadius, math.cos(rotInRadians) * movementRadius)

		# add to our position and get temporary new position
		newPos = self.pos - newPosComponent

		# collision check pos
		self.pos = self._check_wall_collision(self.pos, newPos)

		# print(self.pos)

	
	# checks cardinal directions around player to see if he touched a wall and revert old coodinate if so
	def _check_wall_collision(self, oldPos, newPos):
		"""Checks if player collided with a wall tile. This collision will be separate from enemey / particles, etc

		Args:
			oldPos (Vector2): original position of player before we attempted to move
			newPos (Vector2): the new position we're attempting to move into

		Returns:
			Vector2: the position after adjusted for potential collisions with walls
		"""

		# get temporary local reference to map for easier readability
		map = self._scene.map

		# we will use px and py as "push x" and "push y"
		# we wll push by the delta, but if delta is 0 we'll use a constant
		# the reason we do this:
		# if we use the delta in movement, we'll just push the player back to where they started,
		# which will visually look like a perfect collision.
		# however, if the delta is 0, the collider can get stuck in the wall and wont "push" the player out
		# so instead we'll used a hard coded value incase no delta. This will push the player out, opposite
		# the direction of the collision point
		dx = abs(int(newPos.x) - int(oldPos.x))
		dy = abs(int(newPos.y) - int(oldPos.y))
		px = dx if (dx!=0) else 10
		py = dy if (dy!=0) else 10

		# radius to use for collision around the player
		colisionRadius = 24

		# if either of these are not ground, reset x pos

		# check just a bit left of the player	
		left = newPos + pygame.Vector2(-colisionRadius, 0)
		if map.get_tile_at_pixel_pos(left) != Map.GROUND:
			self.colPoints.append(left.copy())
			newPos.x += px

		# check just right of the player
		right = newPos + pygame.Vector2( colisionRadius, 0)
		if map.get_tile_at_pixel_pos(right) != Map.GROUND:
			self.colPoints.append(right.copy())
			newPos.x -= px

		# if either of these are not ground, reset y pos

		# check just above the player
		top = newPos + pygame.Vector2(0, -colisionRadius)
		if map.get_tile_at_pixel_pos(top) != Map.GROUND:
			self.colPoints.append(top.copy())
			newPos.y += py

		# check just below the player
		bottom = newPos + pygame.Vector2(0,  colisionRadius)
		if map.get_tile_at_pixel_pos(bottom) != Map.GROUND:
			self.colPoints.append(bottom.copy())
			newPos.y -= py

		# return adjusted pos
		return newPos


	# strafe, like move but p e r p e n d i c u l a r
	def strafe(self, direction):
		"""Strafes the player (i.e. perpendicular movement to facing direction)

		Args:
			direction (Number): either -1 or 1 for strafing left/right, respectivelky
		"""

		# just call our move function with bonus parameter
		self.move(direction, True)


	# fire gun
	def fire(self):
		"""Code goes here for firing the gun
		"""

		# this'll do for now
		print("bang!")


	# public method called from our Scene to have the player handle input
	def check_player_input(self, keysDownEvents = None):
		"""Checks input relevant to player

		Args:
			keysDownEvents (list, optional): List of key down events passed in from scene. Defaults to [].
		"""

		# handle optional paramter with or ternary b/c using mutable default has sPoWoKy side effects in Pyland
		keysDownEvents = keysDownEvents or []

		# while it's true we're passed in keydown events, we only care about that for firing
		# we'll use the active keys for rotation and movement
		activeKeys = pygame.key.get_pressed()

		# if shift is not held, we rotate (as opposed to strafe)
		if activeKeys[pygame.K_LSHIFT] is False and activeKeys[pygame.K_RSHIFT] is False:

			# left/a is rotate left:
			if activeKeys[pygame.K_LEFT] or activeKeys[pygame.K_a]:
				self.rotate(1)

			# right/d is rotate right:
			if activeKeys[pygame.K_RIGHT] or activeKeys[pygame.K_d]:
				self.rotate(-1)

		# otherwise, one of the shifts was held, so maybe strafe instead:
		else:

			# left/a is strafe left:
			if activeKeys[pygame.K_LEFT] or activeKeys[pygame.K_a]:
				self.strafe(1)

			# right/d is strafe right:
			if activeKeys[pygame.K_RIGHT] or activeKeys[pygame.K_d]:
				self.strafe(-1)
			

		# up/w is walk forward
		if activeKeys[pygame.K_UP] or activeKeys[pygame.K_w]:
			self.move(1)

		# down/s is walk backward
		if activeKeys[pygame.K_DOWN] or activeKeys[pygame.K_s]:
			self.move(-1)

		# now that we're done with the active key logic we can check if fire was pressed
		for event in keysDownEvents:
			
			# skip non key events
			if event.type==pygame.KEYDOWN:

				# if its space, fire
				if event.key == pygame.K_SPACE:
					self.fire()


	# copied from SO, easy rotate on center script	
	def blit_rotate_center(self, surface, image, topleft, angle):
		"""Rotates pygame image surface on center

		Args:
			surface (Surface): target pygame surface
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


	# debug function to show collisions as red dots
	def draw_collisions(self):
		"""Draws collisions with walls as red dots
		"""

		# loop over our list of colision point vectors & draw 'em on screen as red circles
		for colPoint in self.colPoints:
			sp = self._scene.camera.get_screen_pos(colPoint)
			pygame.draw.circle(self._win, (255,0,0), (int(sp[0]), int(sp[1])), 5)

		# reset array of colisions till next frame
		self.colPoints = []


	# draws player to screen
	def draw(self):
		"""Draws the player's character on screen, with animations and all.
		"""

		# find where on screen we should be relative to the camera
		screenPos = self._scene.camera.get_screen_pos(self.pos)
		
		# always decrease this over time, till we hit 0
		if self._animationWalkCycleBlend > 0:
			self._animationWalkCycleBlend -= 1

		# normalize walk cycle blend value
		# this will result in a float between 1.0 and 0.0 (which decreses towards 0 over time)
		# used to blend walking rotations in
		aniWalkCycleBlendNormalised = (self._animationWalkCycleBlend/10.0)

		# use the games time in miliseconds as basis for input to a sine curve eq
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
		# (this is because the gun is its own sprite in the players hand, so its X/Y is the hand-pos)
		gunRadius = 60 * torsoScalar
		gunRotationFromPlayer = (self.rot + torsoRotOffset + 140) * (math.pi / 180)
		gunPos = screenPos + pygame.Vector2(math.sin(gunRotationFromPlayer) * gunRadius, math.cos(gunRotationFromPlayer) * gunRadius)

		# rotate bit to screen. ORDER MATTERS! bottom-to-top
		self.blit_rotate_center(self._win, self._images["feet"], screenPos-self._feetOffset, self.rot+feetRotOffset)
		self.blit_rotate_center(self._win, imgTorsoScaled, screenPos-newTorsoOffset, self.rot+torsoRotOffset)
		self.blit_rotate_center(self._win, self._images["head"], screenPos-self._headOffset, self.rot+headRotOffset)
		self.blit_rotate_center(self._win, self._images["gun"], gunPos-self._gunOffset, self.rot)

		self.draw_collisions()
		