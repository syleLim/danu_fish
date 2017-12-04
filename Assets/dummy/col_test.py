class col_test(Actor.Actor) :
	def __init__(self) :
		self.cube = Container(0)
		self.cube_a = Container(0)

		self.count = 0

	def OnCreate(self, this) :
		self.cube = Container(this)

		self.cube_trans = self.cube.GetChild(0).FindComponentByType("TransformGroup")
		self.cube_a_trans = self.cube_a.FindComponentByType("TransformGroup")

	def Update(self) :
		col = self.cube_trans.GetSumBox()
		col2 = self.cube_a_trans.GetSumBox()
		self.count +=1
		if self.count <4 : 
			print(col.OBBIntersect(col2))
