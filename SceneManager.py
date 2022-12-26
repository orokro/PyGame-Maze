"""
	SceneManager.py
	---------------

	This file/modulue will provide a class that let's us manage
	our loaded Scene objects.

	Scenes are defined in Scene.py - this is not a pygame specific thing.

	Scene.py will be a base-class for the individual scenes we may make:
		- Title Screen Scene
		- Gameplay Scene
		- Game Over Scene
"""

# import Scene since we finna use that
from Scene import Scene

# the main Scene Manager class:
class SceneManager:

	# constructor:
	def __init__(self, game):
		"""Builds the SceneManager

		Args:
			game (MazeGame): reference to our main game object
		"""

		# keep reference to the game that instantiated us
		self._game = game

		# empty list of scenes we'll manager
		self._scenes = []

		# our current scene, which is non until we pick one
		self._currentScene = None
	

	# adds a scene for us to manage, returns the index
	def add_scene(self, scene):
		"""Adds a scene to this SceneManager to manage

		Args:
			scene (Scene): the scecen to add

		Returns:
			Number: the index of the added scene
		"""

		# append to our list of scenes
		self._scenes.append(scene)

		# if we dont have a scene yet, add the first one we find
		if self._currentScene is None:
			self.switch_scene(scene)

		# the new length -1 is it's index
		return (len(self._scenes) - 1)
	

	# lets user switch scene
	def switch_scene(self, sceneOrSceneIndex):
		"""Switches the scene

		Args:
			sceneOrSceneIndex (Number|Scene): Either a number (for index), or a reference to a previously instantiated scene

		Returns:
			None|Scene: either None, or whatever the previous scene was
		"""

		# if our arg is of type int, we'll treat it as an index and convert the var to a reference to the scene with that index
		scene = self._scenes[sceneOrSceneIndex] if isinstance(sceneOrSceneIndex, int) else sceneOrSceneIndex
			
		# if our scene is already this scene, just gtfo
		if self._currentScene is scene:
			return scene;

		# call "exit" on our current scene, which is now the old scene
		oldScene = self._currentScene
		if oldScene!=None:
			oldScene.scene_exit()

		# replace current scene with the chosen one
		self._currentScene = scene

		# call enter method on current scene
		self._currentScene.scene_enter()

		# Just for fun, return the old scene incase caller wants it
		return oldScene


	# getter function to explose w/e the current scene is
	@property
	def current_scene(self):
		"""Simple helper getter to expose our current scene

		Returns:
			None/Scene: either None, or w/e the current sceneis
		"""

		# just return whatever the current scene is
		return self._currentScene

	