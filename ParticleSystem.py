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

# uhh yea, ParticleSystem definately gonna want some Particle
from Particle import Particle

# the particle system class
class ParticleSystem:

	# static constant particle types
	TYPES = dotdict({
		"BULLET": 0,
		"FLASH": 1,
		"POOF": 2,
	})

	# constructor
	def __init__(self, scene, win):
		"""Constructs the particle system

		Args:
			scene (Scene): the scene we're in
			win (Surface): the pygame window surface we render to
		"""

		# save references to our scene and render window
		self._scene = scene
		self._win = win

		# break out camera cuz our particles will need it for rendering
		self.cam = self._scene.camera

		# this list will contain our active particles as they're spawned and etc
		self.particles = []

		# intialize pygame stuff we'll use for particles
		self._setup_pygame()


	# initialize pygame stuff we'll need for our particle system
	def _setup_pygame(self):
		"""Sets up pygame related objects we'll need for the particle system, so we can tidy up the constructor
		"""

		# load the varius kinds of particle sprites we use
		self._images = [
			pygame.image.load('./img/particles/space_bullet.png'),
			pygame.image.load('./img/particles/flash.png'),
			pygame.image.load('./img/particles/poof.png'),
		]


	# removes particle from our array, in theory, garabage collecting it eventually
	def kill_particle(self, particle):
		"""Removes a particle from our list of particles

		Args:
			particle (Particle): the particle to remove
		"""

		# see ya
		if particle in self.particles:
			self.particles.remove(particle)

		# for debug
		# print(f"Active Particles: {len(self.particles)}")
	

	# updates all particles that are spawned
	def update(self):
		"""Basically just calls update on all the parctles spawned and in our particles[] list
		"""

		# update 'em all
		for particle in self.particles:
			particle.update()


	# draws all our particles
	def draw(self):
		"""Basically just calls draw() on all the particles spawned in our particles[] list
		"""

		# draw 'em all
		for particle in self.particles:
			particle.draw()

	
	# spawns particles
	def spawn_particle(self, type, pos, angle, speed,
			onComplete = None,
			customUpdate = None,
			customCollision = None,
			onCollide = None):

		"""Spawns a new particle

		Args:
			type (Number): the ty pe tto spawn
			pos (Vector2): postion to spawn in
			angle (Number): angle to move in degrees
			speed (Number): how quick should move per update

		Returns:
			Paricle: the newly instiated particle
		"""

		# get image via type
		particleImage = self._images[type]

		# spawn the particle
		newParticle = Particle(
			self._scene,
			self._win,
			self,
			particleImage,
			int(pos.x),
			int(pos.y),
			angle,
			speed,
			0,
			1000,
			True,
			onComplete,
			customUpdate,
			customCollision,
			onCollide)

		# particle exists, just add it to our list
		self.particles.append(newParticle)

		# return reference to the new particle, for extra customization
		return newParticle
