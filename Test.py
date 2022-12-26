

class Foo:

	def __init__(self, name):

		self.name = name

	
	def someFunc(self, var):
		
		print(f"${self.name} -- {var}")


a = Foo("testy")


def doAThing(func):

	func(4)


doAThing(a.someFunc)




