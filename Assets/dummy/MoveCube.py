class MoveCube(Actor.Actor):
    def __init__(self):
        self.CubeContainer = Container(0)  #Container
        self.test1 = Container          # type
        self.intData = int                # type
        self.intData2 = int(0)            # int
        return
    def OnCreate(self, uid):
        self.CubeComponent = self.CubeContainer.FindComponentByType("Cube")
        self.CubeTransComponent = self.CubeContainer.FindComponentByType("TransformGroup")
        self.CubeComponent.PropMaterial.SetTextureDiffuse("$project/Assets/1vf.png")
        self.CubeTransComponent.SetPosition(Math3d.Vector3(0,1,0))
        
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
        return;


   