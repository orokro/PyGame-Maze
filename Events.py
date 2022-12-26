"""
	Events.py
	---------

	Suuuper simple system to collect callbacks in named lists & fires them arbitraitly.

	This file/module provides two classes:

	One for event contains, called EventsEvent,

	and the main Event system object, called Events.

"""

# containeer for events
class EventsEvent:

	# constructor
	def __init__(self):
		"""Constructs the EventEvent, which is a container to hold/add/remove call back functions
		"""
		
		# abitrary counter for indexing events as they're added
		self.listenerCoutner = 0

		# array to add listeners to
		self.listeners = []

	
	# adds a listener callback to this event
	def add_listener(self, callback):
		"""Adds a listerner function callback refernce to our array of listener callbacks

		Args:
			callback (function): call back to call when event is fired

		Returns:
			Number: the unique ID added to this listener, so we can remove it via ID later on
		"""

		# increment our count for a unique ID:
		self.listenerCoutner += 1
		newID = self.listenerCoutner

		# make new basic dict for event
		eventInfo = {
			"id": newID,
			"func": callback,
		}

		# add it to our list of listeners
		self.listeners.append(eventInfo)

		# return the ID of this listener, incase we want to remove it via ID later
		return eventInfo["id"]


	# fires the event, i.e. calls all our listeners with paramers
	def fire(self, *params):
		"""Fires all the callbacks we have in our array, with whatever arbitrary params are passed into fire(...)
		"""

		# loop over all our callbacks and pass the exact same parameters we got in, to them
		for listener in self.listeners:
			
			# call listener with identical params
			listener["func"](*params)


	# removes a listern so it doesn't get called in the future
	def remove_listener(self, listenerToRemove):
		"""Removes a listener from this event, so it wont get called in the future

		Args:
			listenerToRemove (Number|function): EITHER the ID number of the listener, or the function reference itself

		Returns:
			function|False: returns either the call back removed, or False if none found
		"""

		# there's probably some pythonic way to do this, but for simplicity, gonna use a good ol' fashion for loop
		for listener in self.listeners:

			# check if the id matches or the func matches:
			if(listener["id"]==listenerToRemove or listener["func"]==listenerToRemove):

				# remove this listener from the list
				self.listeners.remove(listener)

				# return just the function in case called wants ref of removed item,
				return listener["func"]


		# if nothing was found, return false isntead
		return False


# main events class that we'll use to instantiate things
class Events:

	# constrcutor
	def __init__(self, eventsList = None):

		# handle optional mutable parameter
		eventsList = eventsList or []

		# add all events created on construction
		self.add_events(eventsList)


	# add many events at once
	def add_events(self, eventsList = None):
		"""Adds multiple events via array. Reuses our add_event method

		Args:
			eventsList (List, optional): List of event names to add. Defaults to None.
		"""

		# handle optional mutable parameter
		eventsList = eventsList or []

		# loop over events list and create event events for all of the strings
		for eventName in eventsList:

			# reuse our add event method
			self.add_event(eventName)


	# adds a named event to ourself as an attr
	def add_event(self, eventName):
		"""Adds named event to ourself

		Args:
			eventName (str): name of event
		"""

		# create a new EventsEvnt object
		newEvent = EventsEvent()

		# set it as an attribute of ourself, with the eventName passed in as the event
		setattr(self, eventName, newEvent)


	# simple helper method to see if we have an event with a given name
	def has_event(self, eventName):

		# has attribute?
		if(hasattr(self, eventName) is False):
			return False

		# return if type matches, since we have the attr
		return isinstance(getattr(self, eventName), EventsEvent)
