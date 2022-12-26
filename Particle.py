"""
	Particle.py
	-----------

	This file/module hosts the Particle class that our Particle System spawns & manages
"""

# yup
import pygame
from Util import blit_rotate_center, blit_rotate_center_blend

# we're gonna extend this
from WorldEntity import WorldEntity

# the particle class
class Particle(WorldEntity):

	# static automatic ID counter
	particleIdCounter = 0

	# constructor
	def __init__(
			self, 
			scene,
			win,
			system,
			image,
			initialX = 0,
			initialY = 0,
			initialRot = 0,
			initialSpeed = 10,
			cycleCount = 1,
			cycleLengthInMS = 1000,
			killWhenOOB = True, 
			onComplete = None,
			customUpdate = None,
			customCollision = None,
			onCollide = None):
		
		# give ourself a unique ID for this particle
		Particle.particleIdCounter += 1
		self.id = Particle.particleIdCounter

		# should we kill with out of bounds of the screen?
		# use with caution! combined with cycleCount = 0,
		# could end up with long running / infinte particles out in the void
		self.killWhenOOB = killWhenOOB

		# save reference to our system & use it's 
		# call our super constructor
		super().__init__(scene, win, initialX, initialY, initialRot)

		# keep reference to our particle system we belong to
		self._system = system

		# keep reference of which image we should use for drawing ourself
		self._img = image

		# default blend mode, which can be set externally
		self._blendMode = 0 #ygame.BLEND_ADD

		# save speed
		self.speed = initialSpeed

		# save our cycle count and cyle time length
		# NOTE: for our purposes, cycles will have a time length, and a normalized time from 0-1
		# We can use multiple "cycles" to do things like bouncing or repeitions, etc
		# note: 0 = inifinite
		self._cycleCount = cycleCount
		self._cycleLengthInMS = cycleLengthInMS

		# these are functions / function-referencs thatwill be used for extending particle behavior outside this class
		self._onComplete = onComplete
		self._customUpdate = customUpdate
		self._onCollide = onCollide
		self._customCollision = customCollision

		# during our construction, let's save the time elapses do we can use delta time later
		self._timeAtCreation = pygame.time.get_ticks()


	# public way to set / update cycle settings after creation
	def set_cycle_settings(self, cycleCount=0, cycleLengthInMS = 1000):
		"""Set / update our cycle settings externally

		Args:
			cycleCount (int, optional): how many times particle should "loop". Defaults to 0.
			cycleLengthInMS (int, optional): cycle length in MS. Or... "time units". Defaults to 1000.
		"""

		# udpate our settings
		self._cycleCount = cycleCount
		self._cycleLengthInMS = cycleLengthInMS


	# set our render blend mode
	def set_blend_mode(self, blendMode):
		"""Sets the blend mode for pygame to draw our sprint

		Args:
			blendMode (Nummber): one of pygames blend mode constants
		"""

		# update our render blend modes
		self._blendMode = blendMode


	# function to update particle, move it, rotate it, whatever	
	def update(self):

		# regardless if we use a custom update function (see comment block below) we still gotta do time schizz
		
		# get the time now, and the deltatime since the particle spawned
		timeNow = pygame.time.get_ticks()
		deltaTime = timeNow - self._timeAtCreation

		# compute how many cycles we've done:
		currentCycleNumber = deltaTime // self._cycleLengthInMS

		# if we have inifite cycles, nothing else to do here, but other wise, see if we are done
		if self._cycleCount!=0 and currentCycleNumber>self._cycleCount:

			# rip
			self.kill();
			return

		# get the time in our current cycle
		currentCycleTime = deltaTime % self._cycleLengthInMS

		# normalise it between 0.0 - 1.0
		currentCycleTimeNormalised = (currentCycleTime / self._cycleLengthInMS)

		"""
			Right, so, because I'm probably over-engineering this, our particle system will have
			some special logic here.

			Basically, IF "customUpdate" was passed in, we should call that for custom update logic.

			IF that function returns 'True' we should still do the default updates as well

			IF that function returns 'False' then we don't needd any more update logic.
		"""

		# check if have an customUpdate funciton:
		if self._customUpdate is not None and callable(self._customUpdate):
			
			# call our custom function and capture it's return status
			# note that we pass in reference to ourself and cycle time settings
			updateResult = self._customUpdate(self, currentCycleTimeNormalised, currentCycleTime, currentCycleNumber)

			# like the comment block says above, if we get False as a response, we're done here
			# so lets GTFO
			if updateResult is False:
				return

		# ----------------------------------------------

		# if we got this far, we either already ran custom logic, or we didnt have any.
		# whatever, doesn't matter
		# below this line is whatever the regular logic would have been anyway

		# basically move the partle in the direction its facing, is all we're gonnda do for now
		self.default_move()

		# if we have custom collision, call it our - other wise, only collision is OOB
		if self._customCollision is not None and callable(self._customCollision):

			# call custom collision routine
			col = self._customCollision(self)

			# if col is not none, then it's a dictionary with collision results.
			# so just forward it our event
			if col is not None:

				# if we have the evnet
				if self._onCollide is not None and callable(self._onCollide):

					# call it with collision results
					self._onCollide(self, col)

		# if we have kill on OoB enabled, check if we should kill ourself
		if self.killWhenOOB is True:

			# are we OoB (out of bounds)
			isOoB = self._scene.camera.is_off_screen(self.pos, 100)

			# if out of bounds, see ya
			if isOoB is True:
				self.kill()

		

	# this kills the particle
	def kill(self):
		"""Remove our self
		"""

		# tell our particle system to remove us
		self._system.kill_particle(self)
	

	# draw ourself
	def draw(self):

		# calclate particle postion
		imageCenter = pygame.Vector2(self._img.get_width()/2, self._img.get_height()/2)
		screenPos = self._system.cam.get_screen_pos(self.pos) - imageCenter

		# draw the particle		
		blit_rotate_center_blend(self._win, self._img, screenPos, self.rot, self._blendMode)

