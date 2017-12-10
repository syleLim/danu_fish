import math

class CharacterController(Actor.Actor):
    def __init__(self):
        self.Camera = Container(0) #인스펙터 노출
        self.ClothContainer = Container(0)

        self._Time = 0.0
        self.currentAngle = 0.0
        return

    def OnCreate(self, this):
        # for GetFrameElapseTime()
        self.WorldContainer = GetWorldContainer()
        self.World = self.WorldContainer.FindComponentByType("World")

        self.CameraTransform = self.Camera.FindComponentByType("TransformGroup")

        # Use This Container
        self.ThisContainer = Container(this)
        self.SphereTransform = self.ThisContainer.FindComponentByType("TransformGroup")

        #self.ClothScript = self.ClothContainer.FindComponentByType("ScriptComponent")
        #self.ClothComponent = ClothScript.GetActor()
        #ClothComponent.AddSphere(self.ThisContainer)
        return

    def Update(self):
        self._Time += self.World.GetFrameElapseTime()
        

        return

    def CameraLookAt(self):
        dir = self.SphereTransform.GetDirection()
        SpherePos = self.SphereTransform.GetPosition()
        self.CameraTransform.SetRotation(Math3d.Quaternion.RotationAxis(self.SphereTransform.GetUp(), self.currentAngle))
        CameraOffset = SpherePos + (dir * 12.0)
        CameraOffset.y = 4.0

        self.CameraTransform.LookAt(CameraOffset, SpherePos, Math3d.Vector3(0, 1, 0))
        return


    def OnMessage(self, msg, number, Vector4_lparm, Vector4_wparam):
        if msg == "KeyDown" and number == int('0x20', 16):  #VK_SPACE
            self.CameraLookAt()
            print(self.ThisContainer.FindComponentByType("TransformGroup").GetPosition())

        if msg == "KeyDown" and number == int('0x57', 16): # w
            currentPosition = self.CameraTransform.GetPosition()
            self.CameraTransform.SetPosition(currentPosition+Math3d.Vector3(0,0,1))

        if msg == "KeyDown" and number == int('0x41', 16): # a
            currentRotation = self.CameraTransform.GetRotation()
            currentRotation.y = currentRotation.y - (0.2 * self.World.GetFrameElapseTime())
            if(currentRotation.y < -2*math.pi):
                currentRotation.y = 0
            self.CameraTransform.SetRotation(currentRotation)

        if msg == "KeyDown" and number == int('0x53', 16): # s
            currentPosition = self.CameraTransform.GetPosition()
            self.CameraTransform.SetPosition(currentPosition+Math3d.Vector3(0,0,-1))

        if msg == "KeyDown" and number == int('0x44', 16): # d
            currentRotation = self.CameraTransform.GetRotation()
            currentRotation.y = currentRotation.y + (0.2 * self.World.GetFrameElapseTime())
            if(currentRotation.y > 2*math.pi):
                currentRotation.y = 0
            self.CameraTransform.SetRotation(currentRotation)



        if msg == "KeyDown" and number == int('0x26', 16): # 위
            Transform = self.ThisContainer.FindComponentByType("TransformGroup")
            CurrentPos = Transform.GetPosition()
            CurrentPos.z = CurrentPos.z + 0.5
            Transform.SetPosition(CurrentPos)
        if msg == "KeyDown" and number == int('0x28', 16): # 아래
            Transform = self.ThisContainer.FindComponentByType("TransformGroup")
            CurrentPos = Transform.GetPosition()
            CurrentPos.z = CurrentPos.z - 0.5
            Transform.SetPosition(CurrentPos)
        if msg == "KeyDown" and number == int('0x25', 16): # 왼
            Transform = self.ThisContainer.FindComponentByType("TransformGroup")
            CurrentPos = Transform.GetPosition()
            CurrentPos.x = CurrentPos.x - 0.5
            Transform.SetPosition(CurrentPos)
        if msg == "KeyDown" and number == int('0x27', 16): # 오
            Transform = self.ThisContainer.FindComponentByType("TransformGroup")
            CurrentPos = Transform.GetPosition()
            CurrentPos.x = CurrentPos.x + 0.5
            Transform.SetPosition(CurrentPos)

        if msg == "KeyDown" and number == int('0x31', 16): # 1
            ClothScript = self.ClothContainer.FindComponentByType("ScriptComponent")
        if msg == "KeyDown" and number == int('0x32', 16): # 2
            ScriptComponent = self.ClothContainer.FindComponentByType("ScriptComponent")
            #ClothComponent = ScriptComponent.GetActor()
            #ClothComponent.SendMsg()
        if msg == "KeyDown" and number == int('0x33', 16): # 3
            i = 1
        if msg == "KeyDown" and number == int('0x34', 16): # 4
            i = 1