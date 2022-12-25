"""
	MazeGame.py
	-----------

	This is the main game class to create our Game object.

	This is high level and only handles the highest level things, like scene creation and juggling, etc
"""

# we're gonna use pygame for our rendering, etc
import pygame

# import the scene stuff we'll need
from SceneManager import SceneManager
from SceneTitleScreen import TitleScreen
from SceneGame import GameScreen
from SceneEnd import EndScreen

# for lazy hacks on debug keys
import time

# main Game class
class MazeGame:

	# constructor
	def __init__(self):
		"""Constructor for the MazeGame
		"""

		# welcome msg for debug and etc
		print("Starting MazeGame...")

		# our resolution, hard coded here for meow
		self._resolution = (900, 650)

		# our target FPS, hard coded here for meow
		self._targetFPS = 60

		# set up pygame lib to create a window and etc
		self._win = self._setupPyGame()

		# create a scene manager for us to juggle the main sceens (title, game, ending)
		self._sceneMgr = SceneManager(self)

		# build our scenes
		self._setupScenes()

		# for debug: skip to game screen (past title screen)
		self._sceneMgr.switchScene(1)

		# true until user quits or w/e
		self._run = True

		# start main loop
		self._mainLoop()


	# set up pygame
	def _setupPyGame(self):
		"""Simple method to encapsulate the pygame init schizz

		Returns:
			Surface: the pygame window surface for rendering
		"""

		# create our window surface for rendering, with our hard-coded resolution, and our hard coded window title
		win = pygame.display.set_mode(self._resolution)
		pygame.display.set_caption("Monster Maze v0.00001 - Bg Greg")

		# create a clock so we can use pygames framerate timing logic
		self._pygameClock = pygame.time.Clock()

		# return dat win
		return win


	# instantiate our scenes
	def _setupScenes(self):
		"""Constructes the scenes for our game and adds them to our scene manager
		"""

		# construct our 3 main scenes, even though we'll only use one-at-a-time
		self._sceneMgr.addScene(
			TitleScreen(self, self._win)
		)
		self._sceneMgr.addScene(
			GameScreen(self, self._win)
		)
		self._sceneMgr.addScene(
			EndScreen(self, self._win)
		)


	# check if pygame's windows events includes a quit message, if so, set run false so we can gracefully quit
	def _checkWindowEventsForQuitMessage(self):
		"""Loops over pygame events checking for a quit/exit message
		"""

		# loop over current stack of pygame events
		for event in pygame.event.get():

			# check if it's a quit-type message:
			if event.type == pygame.QUIT:

				# game should quit
				self.quitGame()

		
	# debug key input
	def _debugInput(self):
		"""Checks some keys and does debug functions if detected
		"""

		# get current keys
		keys = pygame.key.get_pressed()

		# switch scenes via keypressed
		if(keys[pygame.K_1]):
			self._sceneMgr.switchScene(0)	
		if(keys[pygame.K_2]):
			self._sceneMgr.switchScene(1)
		if(keys[pygame.K_3]):
			self._sceneMgr.switchScene(2)

		# quit
		if(keys[pygame.K_q]):
			self.quitGame()


	# public method to let the game be quit
	def quitGame(self):
		"""Sets game to quit on next iteration of main loop
		"""

		# set our loop condition variable false
		self._run = False


	# goes from title scene to main game scene
	def startGame(self):
		"""Setes scene to game scecne
		"""

		# simply tell our scene manager to goto scene index 1
		self._sceneMgr.switchScene(1)


	# our logical main-loop
	def _mainLoop(self):
		"""Main game loop
		"""

		# loop until this boolean is false, or we break the while
		while(self._run):

			# we'll lock/target our hardcoded FPS
			# (FYI pygame clocks will automatically sleep the amount required to target a FPS)
			self._pygameClock.tick(self._targetFPS)

			# at a top level, handle some debug input
			# (other scenes will handle input just for that scene)
			self._debugInput()

			# get our current screen, then call update and render on it
			scene = self._sceneMgr.currentScene

			# if we have a current scene
			if(scene!=None):

				# update scene logic
				scene.update()

				# render scene
				scene.render()

			# check to see if we should keep running:
			self._checkWindowEventsForQuitMessage()

		# shut down cleanly after main loop quits
		pygame.quit()
