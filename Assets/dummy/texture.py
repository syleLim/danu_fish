class texture(Actor.Actor) :
	def __init__(self) :
		self.roof = Container(0)

	def OnCreate(self, this) :
		self.roof = Container(this)
		self.roof_cube = self.roof.FindComponentByType("Cube")
		self.i = 1
		self.count = 0


	def Update(self) :
		self.count +=1

		if self.count%10 != 0 :
			return

		self.i += 1

		if self.i >10 :
			self.i = 1


		self.roof_cube.PropMaterial.SetTextureDiffuse("$project/Assets/water_"+str(self.i)+".jpg")
		self.roof_cube.PropMaterial.SetTextureNormal("project/Assets/water_"+str(self.i)+"_no.jpg`")

