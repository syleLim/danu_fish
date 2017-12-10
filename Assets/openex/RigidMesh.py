
class CustomRigidMesh(Actor.Actor):
	def __init__(self):
	

		
		return
	def OnCreate(self, uid):
	
		self.WorldContainer = GetWorldContainer();
		##self.WorldComponent = self.WorldContainer.FindComponentByType("World")
		#con = self.WorldContainer.AddNewChild()
		#con.AddNewComponent("TransformGroup")
		#self.CloudMeshComponent = con.AddNewComponent("CloudMesh")

		#print(self.CloudMeshComponent)
		#self.CloudMeshComponent.PropCloudMesh.SetParticleSize(1.0)
		#self.CloudMeshComponent.SetParticleCount(1000)
		#self.CloudMeshComponent.SetParticlePosition(0, Math3d.Vector3(1,2,3))



		con2 = self.WorldContainer.AddNewChild()
		con2.AddNewComponent("TransformGroup")
		Sphere = con2.AddNewComponent("Sphere")
		print(type(Sphere))
		print(type(Sphere.PropRigidMesh))
		Sphere.PropRigidMesh.SetMaterial("abc")

		print(type(Sphere.PropRigidMesh))
		print(Sphere.PropRigidMesh.GetMaterial())
		#self.ContainerList = list()
		#self.WorldContainer.AddNewComponent("TransformGroup")
		#self.ContainerList.append(self.WorldContainer.LoadPrefab("$project/Assets/cubePrefab.prefab"));
		#self.ContainerList.append(self.WorldContainer.LoadPrefab("$project/Assets/cubePrefab.prefab"));
		#self.ContainerList.append(self.WorldContainer.LoadPrefab("$project/Assets/cubePrefab.prefab"));
		#self.ContainerList.append(self.WorldContainer.LoadPrefab("$project/Assets/cubePrefab.prefab"));
		#self.ContainerList.append(self.WorldContainer.LoadPrefab("$project/Assets/cubePrefab.prefab"));
		#self.ContainerList.append(self.WorldContainer.LoadPrefab("$project/Assets/cubePrefab.prefab"));

		#print(self.ContainerList)

		
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