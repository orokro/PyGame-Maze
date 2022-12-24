"""
	SceneTitleScreen.py
	-------------------

	This file/module provides the scene to house our Title screen logic.

	The class we export will extend the Scene base-class.

	NOTE:

	Currently the options selection is a bit crude. Only two options,
	no support for pages (like if we wanted a settings page later), etc.

	Works for now, however.
"""

# we're gonna use pygame for our rendering, etc
import pygame

# import Scene since we finna use that
from Scene import Scene

# enums for cleanliness
from enum import Enum

# for dat sin curve. mmm nice
import math

# Title screen scene, extends Scene
class TitleScreen(Scene):

	# static enum for title screen option integers
	Options = Enum('Options', ["START", "QUIT"])

	# constructor
	def __init__(self, game, win):
		"""Builds TitleScreen scene

		Args:
			game (MazeGame): reference to our main game isntance
			win (Surface): pygame surface for rendering
		"""
		# we'll hard code title in this file, we dont need to pass it in
		super().__init__(game, win, "Title Screen")

		# hard coded font size for menu text
		self._menuTextFontSize = 50

		# we will have two options on the title screen, this is the current one
		self._selectedOption = TitleScreen.Options.START

		# we will use this a 
		# set up pygame stuff we'll need for this scene
		self._setupPygame()


	# moves pygame related stuff out of constructor
	def _setupPygame(self):
		"""Initilizes the pygame objects we'll need for this scene
		"""

		# well load our just the picture for the title screen here, in this scene
		self._images = {
			"bg": pygame.image.load('./img/TitleScreen_BG.png')
		}

		# some reusable color tuples
		self._colors = {
			"white": (255, 255, 255),
			"green": (0, 255, 0)
		}

		# inint font support (can be called more than once)
		pygame.font.init()

		# set up our font and some rendered text
		self._font = pygame.font.Font("./fonts/framd.ttf", self._menuTextFontSize)

		# make sure we render our text surfaces at least once on init, etc
		self._renderOptionText()

		# we'll save the initial canvas sizes of both of 'em so we can animate them in render later
		self._txtStartInitialSize = (self._txtStart.get_width(), self._txtStart.get_height())
		self._txtQuitInitialSize = (self._txtQuit.get_width(), self._txtQuit.get_height())
		
		
	# renders the option text with updated colors whenever the options change, or on init
	def _renderOptionText(self):
		"""Renders text surfaces for our "START" and "QUIT" options
		"""

		# pick our two colors
		startColor = self._colors["green"] if self._selectedOption==TitleScreen.Options.START else self._colors["white"]
		quitColor = self._colors["white"] if self._selectedOption==TitleScreen.Options.START else self._colors["green"]
		
		# create two "surfacecs" for drawing "START" and "QUIT"
		self._txtStart = self._font.render("START", True, startColor)
		self._txtQuit = self._font.render("QUIT", True, quitColor)


	# method called when we enter this scene
	def sceneEnter(self):
		"""Called when we enter this scene
		"""

		# do super stuffs, if any
		super().sceneEnter()

		# for debug and whatnot
		print(f"Doing title screen business...")

		# make sure we always enter this scene with the first option selected...
		self._selectedOption = TitleScreen.Options.START


	# method called when we exit this scene
	def sceneExit(self):
		"""Called when we exit this scene
		"""

		# do super stuffs, if any
		super().sceneExit()

		# for debug and whatnot
		print(f"Title Screen says buh-bye")


	# handles keyboard input for the title screen
	def _checkKeys(self):
		"""Checks keyboard keydown events so we can select options, etc
		"""

		# via pygame lib, get list of key down events
		keyDownEventsThisFrame = pygame.event.get(pygame.KEYDOWN)

		# loop over keys down
		for event in keyDownEventsThisFrame:

			# check if key was up or down, since we only have two options we can just toggle the option
			# actually, any of the arrow keys TBH
			if (
				event.key==pygame.K_UP 
				or event.key==pygame.K_DOWN
				or event.key==pygame.K_LEFT
				or event.key==pygame.K_RIGHT):

				# simple ternary toggle
				self._selectedOption = TitleScreen.Options.QUIT if (self._selectedOption==TitleScreen.Options.START) else TitleScreen.Options.START

				# re-render text, so colors are fresh
				self._renderOptionText()

			# if enter/return was pressed, do whatever option we have currently selected
			if(event.key==pygame.K_RETURN or event.key==pygame.K_KP_ENTER):

				# just call our select option method with whatever one we currently have in our class
				self._selectOption(self._selectedOption)


	# selets one of t he options on the title screen
	def _selectOption(self, option):
		"""Selets one of the title screen options & does the correct corresponding action

		Args:
			option (TitleScreen.Option): The enum for which option to pick & act on
		"""
		
		# handle corresponding option
		if(option==TitleScreen.Options.START):
			self._game.startGame()
		
		elif(option==TitleScreen.Options.QUIT):
			self._game.quitGame()
		

	# method for doing update logic on this scene
	def update(self):
		"""Update logic method
		"""

		# do super stuffs, if any
		super().update()

		# check keys for up, down, and enter
		self._checkKeys()


	# fugly function to scale the currenty selected text on a sine curve. mmmm B O U N C Y mmm
	def _scaleTextOnOnSineCurve(self):
		"""Scales both our txtStart and txtQuit based on which is selected, on a nice sine curve

		Returns:
			Dictionary: a dict containing both images for rendering
		"""
		# use sine curve with time elapsed as theta, to get some fraction to multiply by
		timeElapsed = pygame.time.get_ticks() * 0.01
		scaleAmountFloat = 1.0 + (math.sin(timeElapsed) * 0.15)
		if(self._selectedOption==TitleScreen.Options.START):

			# return just start scaled
			newSize = (self._txtStartInitialSize[0]*scaleAmountFloat, self._txtStartInitialSize[1] * scaleAmountFloat )
			return {
				"txtStart": pygame.transform.scale(self._txtStart, newSize),
				"txtQuit": self._txtQuit
			}

		else:

			# return just end scaled
			newSize = (self._txtQuitInitialSize[0]*scaleAmountFloat, self._txtQuitInitialSize[1] * scaleAmountFloat )
			return {
				"txtStart": self._txtStart,
				"txtQuit": pygame.transform.scale(self._txtQuit, newSize)
			}


	# method for rendering scene
	def render(self):
		"""Render method for pygame schizz
		"""

		# do super stuffs, if any
		super().render()

		# get local copy of win for easier code writing
		win = self._win

		# draw our background of the title screen
		win.blit(self._images["bg"], (0, 0))

		# get approrpriately scaled texts
		scaledTexts = self._scaleTextOnOnSineCurve()

		# copy text to screen, centered on a point
		txtStart = scaledTexts["txtStart"]
		startPos = ((win.get_width() // 3) - (txtStart.get_width() // 2), 550 - (txtStart.get_height() // 2))
		win.blit(txtStart, startPos)

		txtQuit = scaledTexts["txtQuit"]
		quitPos = ((win.get_width() // 3) * 2 - (txtQuit.get_width() // 2), 550 - (txtQuit.get_height() // 2))
		win.blit(txtQuit, quitPos)
		
		# update the display
		pygame.display.update()
