"""
	MazeGame.py
	-----------

	This is the main game class to create our Game object.

	This is high level and only handles the highest level things, like scene creation and juggling, etc
"""

# we're gonna use pygame for our rendering, etc
import pygame

# main Game class
class MazeGame:

	# constructor
	def __init__(self):

		# welcome msg for debug and etc
		print("Starting MazeGame...")

		# our resolution, hard coded here for meow
		self.resolution = (900, 650)

		# set up pygame lib to create a window and etc
		self.win = self.setupPyGame()

		# true until user quits or w/e
		self.run = True

		# start main loop
		self.mainLoop()


	# set up pygame
	def setupPyGame(self):

		# create our window surface for rendering, with our hard-coded resolution, and our hard coded window title
		win = pygame.display.set_mode(self.resolution)
		pygame.display.set_caption("Monster Maze v0.00001 - Bg Greg")

		# return dat win
		return win

	
	# check if pygame's windows events includes a quit message, if so, set run false so we can gracefully quit
	def checkWindowEventsForQuitMessage(self):

		# loop over current stack of pygame events
		for event in pygame.event.get():

			# check if it's a quit-type message:
			if event.type == pygame.QUIT:

				# game no longer running
				self.run = False

		
	# our logical main-loop
	def mainLoop(self):

		# loop until this boolean is false, or we break the while
		while(self.run):

			# check to see if we should keep running:
			self.checkWindowEventsForQuitMessage()

		# shut down cleanly after main loop quits
		pygame.quit()
