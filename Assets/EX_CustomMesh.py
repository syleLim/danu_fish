import math

class VertexInfo:
    def __init__(self, customMesh):
        self._PositionList = list()
        self._DiffusesList = list()
        self._Indices = list()
        self._PrimitiveCount = 0
        self._CustomMesh = customMesh

    def UpdateData(self):
        self._CustomMesh.SetPrimitiveCount(self._PrimitiveCount)
        self._CustomMesh.SetIndices(self._Indices)
        self._CustomMesh.SetPositions(self._PositionList)
        self._CustomMesh.SetDiffuses(self._DiffusesList)
        self._CustomMesh.UpdateVertexBuffer();


    def AddData(self, vertexPosition, diffuseColor):
        self._PositionList.append(vertexPosition)
        self._DiffusesList.append(diffuseColor)

    def SetData(self, idx, vertexPosition, diffuseColor):
        self._PositionList[idx] = vertexPosition
        self._DiffusesList[idx] = diffuseColor

    def InitIndices(self, *indices):
        if (len(indices) % 3) != 0:
            return
        self._Indices.clear()
        for idx in indices:
            self._Indices.append(idx)
        self._PrimitiveCount = int(len(self._Indices) / 3)

    def AddPolygon(self, *indices):
        if (len(indices) % 3) != 0:
            return
        for idx in indices:
            self._Indices.append(idx)
        self._PrimitiveCount = int(len(self._Indices) / 3)

    def SetPosition(self, idx, vertexPosition):
        self._PositionList[idx] = vertexPosition

    def SetDiffuse(self, idx, diffuseColor):
        self._DiffusesList[idx] = diffuseColor

    def Clear(self):
        self._PositionList.clear()
        self._DiffusesList.clear()
        self._Indices.clear()
        self._PrimitiveCount = 0

    # TODO : Add Interface...



class EX_CustomMesh(Actor.Actor):
    def __init__(self):
        self._Time = 0.0
        self._DynamicMeshView = True
        


    def OnCreate(self, this):
        # for GetFrameElapseTime()
        self.WorldContainer = GetWorldContainer()
        self.World = self.WorldContainer.FindComponentByType("World")



        # Use Create Container
        #self.NewContainer = self.WorldContainer.AddNewChild()
        
        #self.NewContainer.AddNewComponent("TransformGroup")
        #self.CustomMesh = self.NewContainer.AddNewComponent("CustomMesh")



        # Use This Container
        self.ThisContainer = Container(this)

        self.ThisContainer.AddNewComponent("TransformGroup")
        self.CustomMesh = self.ThisContainer.AddNewComponent("CustomMesh")



        # Vertex Init

        # Make Polygon
        self.DynamicMesh = VertexInfo(self.CustomMesh)

        self.DynamicMesh.AddData(Math3d.Vector3(-1, 0, 0), Math3d.Color(1, 0, 0, 1)) # 0
        self.DynamicMesh.AddData(Math3d.Vector3( 0, 1, 0), Math3d.Color(1, 1, 1, 1)) # 1
        self.DynamicMesh.AddData(Math3d.Vector3( 1, 0, 0), Math3d.Color(0, 0, 1, 1)) # 2

        self.DynamicMesh.InitIndices(0,1,2)
        
        

        # Make Volum Mesh (Triangular Pyramid)
        self.StaticMesh = VertexInfo(self.CustomMesh)

        posList = list()
        posList.append(Math3d.Vector3(-1, 0, 0))        # left
        posList.append(Math3d.Vector3( 0, 0,-1.6))      # back
        posList.append(Math3d.Vector3( 1, 0, 0))        # right
        posList.append(Math3d.Vector3( 0, 1.5, -0.53))  # top

        self.StaticMesh.AddData(posList[0], Math3d.Color(1, 0, 0, 0.5)) # 0
        self.StaticMesh.AddData(posList[3], Math3d.Color(1, 0, 0, 0.5)) # 1
        self.StaticMesh.AddData(posList[1], Math3d.Color(1, 0, 0, 0.5)) # 2

        self.StaticMesh.AddData(posList[1], Math3d.Color(0, 1, 0, 0.5)) # 3
        self.StaticMesh.AddData(posList[3], Math3d.Color(0, 1, 0, 0.5)) # 4
        self.StaticMesh.AddData(posList[2], Math3d.Color(0, 1, 0, 0.5)) # 5

        self.StaticMesh.AddData(posList[3], Math3d.Color(0, 0, 1, 0.5)) # 6
        self.StaticMesh.AddData(posList[0], Math3d.Color(0, 0, 1, 0.5)) # 7
        self.StaticMesh.AddData(posList[2], Math3d.Color(0, 0, 1, 0.5)) # 8

        self.StaticMesh.AddData(posList[2], Math3d.Color(1, 1, 1, 0.5)) # 9
        self.StaticMesh.AddData(posList[0], Math3d.Color(1, 1, 1, 0.5)) # 10
        self.StaticMesh.AddData(posList[1], Math3d.Color(1, 1, 1, 0.5)) # 11
        
        self.StaticMesh.InitIndices(0,1,2, 3,4,5, 6,7,8, 9,10,11)

        

        #self.StaticMesh.AddData(posList[0], Math3d.Color(1, 0, 0, 1)) # 0
        #self.StaticMesh.AddData(posList[1], Math3d.Color(0, 1, 0, 1)) # 1
        #self.StaticMesh.AddData(posList[2], Math3d.Color(0, 0, 1, 1)) # 2
        #self.StaticMesh.AddData(posList[3], Math3d.Color(1, 1, 1, 1)) # 3

        #self.StaticMesh.InitIndices(0,3,1, 1,3,2, 3,0,2, 2,0,1)



    def Update(self):
        if self._DynamicMeshView == True:
            self._Time += self.World.GetFrameElapseTime()

            self.DynamicMesh.SetPosition(0, Math3d.Vector3(-1+math.sin(self._Time*1.2)*0.5,0,0))
            self.DynamicMesh.SetPosition(1, Math3d.Vector3(0,1+math.cos(self._Time*2.5)*0.5,0))
            self.DynamicMesh.SetPosition(2, Math3d.Vector3(1+math.sin(self._Time)*0.5,0,0))
        
            color = 0.5 + math.sin(self._Time)*0.5
            self.DynamicMesh.SetDiffuse(1, Math3d.Color(color,color,color,1))


            self.DynamicMesh.UpdateData()

        # else: Nothing. (Static Mesh View)



    def OnMessage(self, msg, number, Vector4_lparm, Vector4_wparam):
        # Dynamic Mesh View <-> Static Mesh View
        if msg == "KeyDown" and number == int('0x20', 16):  #VK_SPACE  
            self._DynamicMeshView = not self._DynamicMeshView

            if self._DynamicMeshView == False:
                self.StaticMesh.UpdateData()

