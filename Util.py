"""
	Util.py
	-------

	Stores some generic things that are useful, but don't belong anywhere else.
"""

# imports
import pygame


# copied from:
# https://stackoverflow.com/questions/2352181/how-to-use-a-dot-to-access-members-of-dictionary
# makes dict access in python, sane

class dotdict(dict):
    """dot.notation access to dictionary attributes"""
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


# copied from SO, easy rotate on center script	
def blitRotateCenter(surface, image, topleft, angle):
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
	