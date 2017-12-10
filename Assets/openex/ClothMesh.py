import math

class VertexInfo: #Cloth 옷감 전체
    def __init__(self, customMesh):
        self.numParticleWidth = int()
        self.numParticleHeight = int()
        self._Movable = list()
        #self._MassList = list()
        self.PositionList = list()
        self._OldPositionList = list()
        self._Acceleration = list()
        self._Accumulated_normal = list()
        self._DiffusesList = list()
        self.Constraints = list()
        
        self._Indices = list()
        self._PrimitiveCount = 0
        self._CustomMesh = customMesh
        return

    def UpdateData(self):
        self._CustomMesh.SetPrimitiveCount(self._PrimitiveCount)
        self._CustomMesh.SetIndices(self._Indices)
        self._CustomMesh.SetPositions(self.PositionList)
        self._CustomMesh.SetDiffuses(self._DiffusesList)

        self._CustomMesh.UpdateVertexBuffer();

    def GetIndexByMatrix(self, x, y):
        return y * self.numParticleWidth + x

    def InitIndices(self, indices):
        self._Indices.clear()
        for tri in indices:
            for idx in tri:
                self._Indices.append(idx)
        self._PrimitiveCount = int(len(self._Indices))

    def InitCloth(self):
        width = 8.00
        height = 8.00
        numParticleWidth = 16
        numParticleHeight = 16

        self.numParticleWidth = numParticleWidth
        self.numParticleHeight = numParticleHeight

        self._Movable = [True] * (numParticleWidth * numParticleHeight)
        #self._MassList = [1] * (numParticleWidth * numParticleHeight)
        self.PositionList = [Math3d.Vector3(0,0,0)] * (numParticleWidth * numParticleHeight)
        self._OldPositionList = [Math3d.Vector3(0,0,0)] * (numParticleWidth * numParticleHeight)
        self._Acceleration = [Math3d.Vector3(0,0,0)] * (numParticleWidth * numParticleHeight)
        self._Accumulated_normal = [Math3d.Vector3(0,0,0)] * (numParticleWidth * numParticleHeight)
        self._DiffusesList = []

        self.ClothColor = Math3d.Color(1, 1, 1, 1)

		# 파티클 생성
        for x in range(numParticleWidth):
            for y in range(numParticleHeight):
                pos = Math3d.Vector3(width * (x/numParticleWidth), -height * (y/numParticleHeight), 0)
                idx = y*numParticleWidth+x # insert particle in column x at y'th row
                self.PositionList[idx] = pos
                self._OldPositionList[idx] = pos
                self._DiffusesList.append(self.ClothColor)

		# Constraints: Connecting immediate neighbor particles with constraints (distance 1 and sqrt(2) in the grid)
        for x in range(numParticleWidth):
            for y in range(numParticleHeight):
                if (x<numParticleWidth-1):
                    c = Constraint()
                    c.SetConstraint(self, self.GetIndexByMatrix(x,y), self.GetIndexByMatrix(x+1,y))
                    self.Constraints.append(c)
                if (y<numParticleHeight-1):
                    c = Constraint()
                    c.SetConstraint(self, self.GetIndexByMatrix(x,y), self.GetIndexByMatrix(x,y+1))
                    self.Constraints.append(c)
                if (x<numParticleWidth-1 and y<numParticleHeight-1):
                    c = Constraint()
                    c.SetConstraint(self, self.GetIndexByMatrix(x,y), self.GetIndexByMatrix(x+1,y+1))
                    self.Constraints.append(c)
                if (x<numParticleWidth-1 and y<numParticleHeight-1):
                    c = Constraint()
                    c.SetConstraint(self, self.GetIndexByMatrix(x+1,y), self.GetIndexByMatrix(x,y+1))
                    self.Constraints.append(c)
		# Constraints: Connecting secondary neighbors with constraints (distance 2 and sqrt(4) in the grid)
        for x in range(numParticleWidth):
            for y in range(numParticleHeight):
                if (x<numParticleWidth-2):
                    c = Constraint()
                    c.SetConstraint(self, self.GetIndexByMatrix(x,y), self.GetIndexByMatrix(x+2,y))
                    self.Constraints.append(c)
                if (y<numParticleHeight-2):
                    c = Constraint()
                    c.SetConstraint(self, self.GetIndexByMatrix(x,y), self.GetIndexByMatrix(x,y+2))
                    self.Constraints.append(c)
                if (x<numParticleWidth-2 and y<numParticleHeight-2):
                    c = Constraint()
                    c.SetConstraint(self, self.GetIndexByMatrix(x,y), self.GetIndexByMatrix(x+2,y+2))
                    self.Constraints.append(c)
                if (x<numParticleWidth-2 and y<numParticleHeight-2):
                    c = Constraint()
                    c.SetConstraint(self, self.GetIndexByMatrix(x+2,y), self.GetIndexByMatrix(x,y+2))
                    self.Constraints.append(c)
        
        #Triangle
        tri = list()
        for x  in range(numParticleWidth-1):
            for y  in range(numParticleHeight-1):
                tri.append([self.GetIndexByMatrix(x+1,y), self.GetIndexByMatrix(x,y), self.GetIndexByMatrix(x,y+1)])
                tri.append([self.GetIndexByMatrix(x+1,y+1), self.GetIndexByMatrix(x+1,y), self.GetIndexByMatrix(x,y+1)])
        
        self.InitIndices(tri)

		# 왼쪽 최상단 2개, 오른쪽 최상단 2개 고정
        self.MakeUnmovable(self.GetIndexByMatrix(0, 0))
        self.MakeUnmovable(self.GetIndexByMatrix(1, 0))
        self.MakeUnmovable(self.GetIndexByMatrix(numParticleWidth-1 ,0))
        self.MakeUnmovable(self.GetIndexByMatrix(numParticleWidth-2 ,0))
        return

    def SetPosition(self, idx, vertexPosition):
        self.PositionList[idx] = vertexPosition

    def SetDiffuse(self, idx, diffuseColor):
        self._DiffusesList[idx] = diffuseColor

    def AddForce(self, f):
        for idx in range(len(self.PositionList)):
            self._Acceleration[idx] = self._Acceleration[idx] + f #/self._MassList[idx] 중량은 다 1로 고정하는 것으로 계산량 줄이기

    def TimeStep(self):
        DAMPING = 0.03
        TIME_STEPSIZE2 = 0.5*0.5
        CONSTRAINT_ITERATIONS = 4

        for i in range(CONSTRAINT_ITERATIONS):
            for constraint in self.Constraints:
                constraint.SatisfyConstraint(self)

        for idx in range(len(self.PositionList)):
            if(self._Movable[idx]):
                temp = self.PositionList[idx]
                self.PositionList[idx] = self.PositionList[idx] + (self.PositionList[idx]-self._OldPositionList[idx])*(1.0 - DAMPING) + self._Acceleration[idx] * TIME_STEPSIZE2
                self.PositionList[idx] = self.PositionList[idx] + self._Acceleration[idx] * TIME_STEPSIZE2
                self._OldPositionList[idx] = temp
                self._Acceleration[idx] = Math3d.Vector3(0,0,0) # acceleration is reset since it HAS been translated into a change in position (and implicitely into velocity)	
        
        return

    def CollisionCheck(self, sphereContainerList):
        if len(sphereContainerList) != 0:
            for idx in range(len(self.PositionList)):
                for sphere in sphereContainerList:
                    sphereTransform = sphere.FindComponentByType("TransformGroup")
                    sphereComponent = sphere.FindComponentByType("Sphere")
                    v = self.PositionList[idx] - sphereTransform.GetPosition()
                    l = v.Length()
                    radius = 1.000
                    normal = self.Normalize(v, l)
                    offset = normal * (radius - l)
                    if l < radius: # collision condition
                        self.OffsetPos(idx, offset); # project the particle to the surface of the sphere
                        break
    
    def Normalize(self, v, l):
        return Math3d.Vector3(v.x/l, v.y/l, v.z/l)

    def OffsetPos(self, idx, v):
        if(self._Movable[idx]):
            self.PositionList[idx] = self.PositionList[idx] + v
        return

    def MakeUnmovable(self, idx):
        self._Movable[idx] = False
        return

class Constraint:
    def __init__(self):
        self.restDistance = 0.000 #인스펙터 노출
        self.Idx_p1 = 0
        self.Idx_p2 = 0
        return

    def SetConstraint(self, vertexInfo, idx_p1, idx_p2):
        self.Idx_p1 = idx_p1
        self.Idx_p2 = idx_p2
        v3 = vertexInfo.PositionList[idx_p1] - vertexInfo.PositionList[idx_p2]
        self.restDistance = v3.Length()

    def SatisfyConstraint(self, vertexInfo):
        p1_to_p2 = vertexInfo.PositionList[self.Idx_p2] - vertexInfo.PositionList[self.Idx_p1] # vector from p1 to p2
        current_distance = p1_to_p2.Length() # current distance between p1 and p2

        correctionVector = p1_to_p2 *(1 - self.restDistance/current_distance) # The offset vector that could moves p1 into a distance of rest_distance to p2
        correctionVectorHalf = correctionVector * 0.5 # Lets make it half that length, so that we can move BOTH p1 and p2.
        

        vertexInfo.OffsetPos(self.Idx_p1, correctionVectorHalf)  # correctionVectorHalf is pointing from p1 to p2, so the length should move p1 half the length needed to satisfy the constraint.
        vertexInfo.OffsetPos(self.Idx_p2, correctionVectorHalf * -1)  # we must move p2 the negative direction of correctionVectorHalf since it points from p2 to p1, and not p1 to p2.	
        
        return

class ClothMesh(Actor.Actor):
    def __init__(self):
        self.Camera = Container(0) #인스펙터 노출
        self._TIME_STEPSIZE2 = 0.5*0.5
        self.Sphere1 = Container(1)
        self.Sphere2 = Container(2)

        self.SphereList = list()
        return

    def SendMsg(self):
        print("asdasdasdasdsadasddas")
        return

    def OnCreate(self, this):
        self.WorldContainer = GetWorldContainer()
        self.World = self.WorldContainer.FindComponentByType("World")

        self.CameraTransform = self.Camera.FindComponentByType("TransformGroup")

        self.ThisContainer = Container(this)
        self.ThisContainer.AddNewComponent("TransformGroup")
        self.CustomMesh = self.ThisContainer.AddNewComponent("CustomMesh")

        self.DynamicMesh = VertexInfo(self.CustomMesh)
        self.DynamicMesh.InitCloth()

        self.SphereList.append(self.Sphere1)
        self.SphereList.append(self.Sphere2)

        return 0 

    def OnDestroy(self):
        return 0 

    def OnEnable(self):
        return 0 

    def OnDisable(self):
        return 0 

    def Update(self):
        self.DynamicMesh.AddForce(Math3d.Vector3(0,-0.2,0)*self._TIME_STEPSIZE2)
        self.DynamicMesh.TimeStep()
        self.DynamicMesh.CollisionCheck(self.SphereList)
        self.DynamicMesh.UpdateData()
        return

    def OnMessage(self, msg, number, Vector4_lparm, Vector4_wparam):
        if msg == "KeyDown":
            print(number)

        if msg == "KeyDown" and number == int('0x20', 16):  # SPACE
            i = 1

        if msg == "KeyDown" and number == int('0x57', 16): # w
            print(self.DynamicMesh.PositionList[self.DynamicMesh.GetIndexByMatrix(8,8)])

        if msg == "KeyDown" and number == int('0x5A', 16): # z
            self.DynamicMesh.AddForce(Math3d.Vector3(-1,0,0))

        if msg == "KeyDown" and number == int('0x58', 16): # x
            i = 1
        if msg == "KeyDown" and number == int('0x43', 16): # c
            i = 1