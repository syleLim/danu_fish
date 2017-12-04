import math

class box_move(Actor.Actor):
	def __init__(self):
		
		self.time = 0

	def OnCreate(self, this):
		self.box = Container(this)
		self.world = GetWorldContainer().FindComponentByType("World")
		self.t = self.box.FindComponentByType("TransformGroup")
		self.pre_pos = self.t.GetPosition()
		
		return

	def Update(self):
		self.time += self.world.GetFrameElapseTime()*5 

		pos = Math3d.Vector3(math.sin(self.time) + self.pre_pos.x, self.pre_pos.y, self.pre_pos.z) 

		self.t.SetPosition(pos)
