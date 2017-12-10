
class MoveCube(Actor.Actor):
	def __init__(self):
	
		return
	def OnCreate(self, uid):
		self.WorldContainer = GetWorldContainer();



		newContainer = self.WorldContainer.AddNewChild()
		newContainer.AddNewComponent("TransformGroup")
		RigidMesh = newContainer.AddNewComponent("RigidMesh")


		


		
		return 0 
	def OnDestroy(self):
	    return 0 
	def OnEnable(self):
	    return 0 
	def OnDisable(self):
	    return 0 
	def Update(self):
	    return
	
	def OnMessage(self, msg, number, Vector4_lparm, Vector4_wparam):
			#con.AddNewComponent("TransformGroup")
			#print(self.WorldComponent.GetFrameElapseTime())
		return