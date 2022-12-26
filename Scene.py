"""
	Scene.py
	--------

	This file/module provides the Scene class, which will be a Base-class
	for the various Scenes in our project.

	This Scene abstraction is unique to this project, and not part of pygame or anything.

	NOTE:

	This class is use more like an Interface than a base-class,

	but we'll do some debug prints on some of methods, so not _just_ an Interface, etc.
"""

# the Scene base class
class Scene:

	# constructor
	def __init__(self, game, win, name):
		"""Builds the Scene base class

		Args:
			game (MazeGame): reference to our main game instance
			win (Surface): the pygame surface we will render to
			name (Str): logical name of this scene
		"""

		# save reference to the main game we're part of & the surface for rendering
		self._game = game
		self._win = win

		# save the name we were given, leave as public cuz we'll probably want that later
		self.name = name


	# method called when we enter this scene
	def scene_enter(self):
		"""Called when we enter this scene (the scene that extends this base class)

		   Main purpose is to be overloaded by child class
		"""

		# for debug and whatnot
		print(f"Now entering scene: \"{self.name}\"")


	# method called when we exit this scene
	def scene_exit(self):
		"""Called when we exit this scene (the scene that extends this base class)

		   Main purpose is to be overloaded by child class
		"""

		# for debug and whatnot
		print(f"Now exiting scene: \"{self.name}\"")


	# method for doing update logic on this scene
	def update(self):
		"""Update logic method

		   Main purpose is to be overloaded by child class
		"""
		pass


	# method for rendering scene
	def render(self):
		"""Render method for pygame schizz

		   Main purpose is to be overloaded by child class
		"""
		pass
