"""
	ParticleSystem.py
	-----------------

	This file/module will define a class for our ParticleSystem,
	which under normal circumstances I would call "Particle Manager"

	but ParticleSystem seems like a more appropriate naming scheme for this.

	Anyway, this class _manages_ the spawning / movement / life cycle / collision of particles.

	NOTE:

	This particle system will define and manage particles _for _ this _ game _ !!

	Meaning: this is not a generic game engine class, its particle names and etc is for this solution.
"""

# required for rendering etc
import pygame

# sane dictionary access
from Util import dotdict

# the particle system class
class ParticleSystem:

	# static constant particle types
	TYPES = dotdict({
		"BULLET": 0,
		"FLASH": 1,
	})

	# constructor
	def __init__(self, scene, win):
		"""Constructs the particle system

		Args:
			scene (Scene): the scene we're in
			win (Surface): the pygame window surface we render to
		"""

		# save references to our scene and render window
		self.scene = scene
		self._win = win

		# this list will contain our active particles as they're spawned and etc
		self.particles = []

		# intialize pygame stuff we'll use for particles
		self._setupPygame()


	# initialize pygame stuff we'll need for our particle system
	def _setupPygame(self):
		"""Sets up pygame related objects we'll need for the particle system, so we can tidy up the constructor
		"""

		# load the varius kinds of particle sprites we use
		self._images = [
			pygame.image.load('./img/particles/space_bullet.png'),
			pygame.image.load('./img/particles/flash.png'),
		]


	# removes particle from our array, in theory, garabage collecting it eventually
	def killParticle(self, particle):

		# see ya
		if(particle in self.particles):
			self.particles.remove(particle)

	
	# updates all particles that are spawned
	def update(self):

		# update 'em all
		for particle in self.particles:
			particle.update()


	# draws all our particles
	def draw(self):

		# draw 'em all
		for particle in self.particles:
			particle.draw()

	