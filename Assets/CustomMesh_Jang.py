import math

class VertexInfo:
    def __init__(self):
        self._PositionList = list()
        self._DiffusesList = list()

    def InputData(self, vertexPosition, diffuseColor):
        self._PositionList.append(vertexPosition)
        self._DiffusesList.append(diffuseColor)

    def UpdateData(self, customMesh):
        customMesh.SetPositions(self._PositionList)
        customMesh.SetDiffuses(self._DiffusesList)

    def SetData(self, idx, vertexPosition, diffuseColor):
        self._PositionList[idx] = vertexPosition
        self._DiffusesList[idx] = diffuseColor

    def SetPosition(self, idx, vertexPosition):
        self._PositionList[idx] = vertexPosition

    def SetDiffuse(self, idx, diffuseColor):
        self._DiffusesList[idx] = diffuseColor

	



class CustomMesh_Jang(Actor.Actor):
    def __init__(self):
        self._wavelength = 1
        self._aplitude_level=1
        self._pivot_point = 2
        self._move_speed_x = 1
        self._move_speed_y = 1
        self._move_speed_z = 1

        self._move_speed = Math3d.Vector3(self._move_speed_x, self._move_speed_y, self._move_speed_z)
        self._time = 0.0;

        return

    def OnCreate(self, uid):
        self.WorldContainer = GetWorldContainer()

        self.NewContainer = self.WorldContainer.AddNewChild()

        self.NewContainer.AddNewComponent("TransformGroup")
        self.CustomMesh = self.NewContainer.AddNewComponent("CustomMesh")
        
        self._World = self.WorldContainer.FindComponentByType("World")

        self.Time = 0.0;

        self.VertexList = VertexInfo()
        self.VertexList.InputData(Math3d.Vector3(-1, 0, 0), Math3d.Color(1,0,0,1))
        self.VertexList.InputData(Math3d.Vector3( 0, 0, 0), Math3d.Color(1,1,1,1))
        self.VertexList.InputData(Math3d.Vector3( 1, 0, 0), Math3d.Color(0,0,1,1))

        
        indices = list()

        #polygon
        indices.append(0)
        indices.append(1)
        indices.append(2)

        self.CustomMesh.SetPrimitiveCount(1)
        self.CustomMesh.SetIndices(indices)

        self.VertexList.UpdateData(self.CustomMesh)
        self.CustomMesh.UpdateVertexBuffer();
        return 0 

    def OnDestroy(self):
        return 0 

    def OnEnable(self):
        return 0 

    def OnDisable(self):
        return 0 

    def Update(self):
        self.Time += self._World.GetFrameElapseTime()


        self.VertexList.SetPosition(0, Math3d.Vector3(self.VertexList._PositionList[0].x + math.sin(math.pi/self._wavelength*(-(1/self._wavelength*self.Time))*self._aplitude_level), self.VertexList._PositionList[0].y, self.VertexList._PositionList[0].z))
        self.VertexList.SetPosition(1, Math3d.Vector3(self.VertexList._PositionList[1].x, self.VertexList._PositionList[1].y + math.sin(math.pi/self._wavelength*(-(1/self._wavelength*self.Time))*self._aplitude_level), self.VertexList._PositionList[1].z))
        self.VertexList.SetPosition(2, Math3d.Vector3(self.VertexList._PositionList[2].x + math.sin(math.pi/self._wavelength*(-(1/self._wavelength*self.Time))*self._aplitude_level), self.VertexList._PositionList[2].y, self.VertexList._PositionList[2].z))
        
        color = 0.5 + math.sin(self.Time)*0.5
        self.VertexList.SetDiffuse(1, Math3d.Color(color,color,color,1))


        self.VertexList.UpdateData(self.CustomMesh)

        self.CustomMesh.UpdateVertexBuffer();
        return

    def OnMessage(self, msg, number, Vector4_lparm, Vector4_wparam):
        return;


   