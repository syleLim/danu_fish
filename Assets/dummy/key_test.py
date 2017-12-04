class key_test(Actor.Actor) :
	def __init__(self) :
		self.container = Container(0)

	def OnCreate(self, this) :
		self.container = Container(this)

	def OnMessage(self, msg, number, Vector4_lparm, Vector4_wparam):
		print(msg)
		print(number)