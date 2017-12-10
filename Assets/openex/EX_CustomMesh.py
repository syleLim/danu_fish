import math
# <<<  FIX ME : 122, 123, 189 line  >>>


# Vertex Buffer Input Class
class VertexInfo:
    def __init__(self, customMesh):
        self._PositionList = list()
        self._DiffusesList = list()
        self._UVList = list()
        self._Indices = list()
        self._CustomMesh = customMesh



    def UpdateData(self):
        self._CustomMesh.SetVertexCount( len(self._PositionList) )
        self._CustomMesh.SetIndices(self._Indices)


        self._PositionAttributeIdx = self._CustomMesh.GetAttributeIndex("Position")
        self._DiffusesAttributeIdx = self._CustomMesh.GetAttributeIndex("Diffuse")
        self._UVAttributeIdx = self._CustomMesh.GetAttributeIndex("UV")
        self._IndexAttributeIdx = self._CustomMesh.GetAttributeIndex("Index")
        
        # ※ Vertex Shader 에 지정된 VS_INPUT 정보에 따라 Mesh의 VertexBuffer를 동적으로 생성하므로,
        #   GetAttributeIndex의 매개변수는 VS_INPUT의 변수 이름과 일치해야함.
        for i in range(len(self._PositionList)):
            # VertexBuffer의 임의 index에 접근 및 데이터 변경 방법
            print(self._PositionList[i])

            if (self._PositionAttributeIdx != -1):
                self._CustomMesh.SetAttribute(i, self._PositionAttributeIdx, self._PositionList[i]) 
            if (self._DiffusesAttributeIdx != -1):
                self._CustomMesh.SetAttribute(i, self._DiffusesAttributeIdx, self._DiffusesList[i])
            if (self._UVAttributeIdx != -1):
                self._CustomMesh.SetAttribute(i, self._UVAttributeIdx, self._UVList[i])
            if (self._IndexAttributeIdx != -1):
                self._CustomMesh.SetAttribute(i, self._IndexAttributeIdx, float(self._Indices[i]))

            # ※ 지원하는 데이터 형식 : Float, Vector2, Vector3, Vector4
            # SetAttribute(DataType)      
            #  (Buffer Index, Attribute Name, Data)  # Slow (Safe)
            #  (Buffer Index, Attribute Index, Data)  # Fast

        self._CustomMesh.UpdateVertexBuffer();

        # 예문과 같이 for문을 돌며 전체를 갱신하지 않아도 무관하나,
        # UpdateVertexBuffer 함수가 호출되어야 정보가 갱신됨.
    def AddData(self, vertexPosition, diffuseColor, uv):
        self._PositionList.append(vertexPosition)
        self._DiffusesList.append(diffuseColor)
        self._UVList.append(uv)

    def SetData(self, idx, vertexPosition, diffuseColor, uv):
        self._PositionList[idx] = vertexPosition
        self._DiffusesList[idx] = diffuseColor
        self._UVList[idx] = uv

    def InitIndices(self, *indices):
        if (len(indices) % 3) != 0:
            return
        self._Indices.clear()
        for idx in indices:
            self._Indices.append(idx)

    def AddPolygon(self, *indices):
        if (len(indices) % 3) != 0:
            return
        for idx in indices:
            self._Indices.append(idx)

    def SetPosition(self, idx, vertexPosition):
        self._PositionList[idx] = vertexPosition

    def SetDiffuse(self, idx, diffuseColor):
        self._DiffusesList[idx] = diffuseColor

    def SetUV(self, idx, uv):
        self._UVList[idx] = uv

    def Clear(self):
        self._PositionList.clear()
        self._DiffusesList.clear()
        self._UVList.clear()
        self._Indices.clear()

    # TODO : Add Interface...




# Main Script
class EX_CustomMesh(Actor.Actor):
    def __init__(self):
        self._Time = 0.0
        self._DynamicMeshView = False
        self._Mode = 0
        


    def OnCreate(self, this):
        # for GetFrameElapseTime()
        worldContainer = GetWorldContainer()
        self.World = worldContainer.FindComponentByType("World")



        # Use Create Container
        #targetContainer = worldContainer.AddNewChild()

        # Use This Container
        targetContainer = Container(this)

        if targetContainer.FindComponentByType("TransformGroup") == None:
            targetContainer.AddNewComponent("TransformGroup")

        self.CustomMesh = targetContainer.AddNewComponent("CustomMesh")



        # Use Custom Shader
        self.CustomMesh.PropCustomMesh.SetVertexShader("/Assets/openex/CustomShader") 
        self.CustomMesh.PropCustomMesh.SetPixelShader("/Assets/openex/CustomShader")
        
        # ※ Custom Shader 파일 생성 시 주의점.
        # 1. '/'가 처음에 와야하며, 확장자를 제외한 파일명까지만 작성되어야함
        # 2. VertexShader에는 ".Vertex.hls", PixelShader에는 ".Pixel.hls" 확장자를 포함시켜야함
        #   ex) 파일 경로 : (Project)/Assets/NewShader.Vertex.hls
        #       매개 변수 : /Assets/NewShader



        # Vertex Init

        # Make Polygon
        self.DynamicMesh = VertexInfo(self.CustomMesh)

        self.DynamicMesh.AddData(Math3d.Vector3(-1,-1, 0), Math3d.Color(1, 0, 0, 1), Math3d.Vector2(0,1))    # 0
        self.DynamicMesh.AddData(Math3d.Vector3( 0, 1, 0), Math3d.Color(1, 1, 1, 1), Math3d.Vector2(0.5,0))  # 1
        self.DynamicMesh.AddData(Math3d.Vector3( 1,-1, 0), Math3d.Color(0, 0, 1, 1), Math3d.Vector2(1,1))    # 2
        
        self.DynamicMesh.AddPolygon(0,1,2)

        self.MoveVertexArray = list()
        self.MoveVertexArray.append(Math3d.Vector3(0,0,0))
        self.MoveVertexArray.append(Math3d.Vector3(0,0,0))
        self.MoveVertexArray.append(Math3d.Vector3(0,0,0))


        # Make Volum Mesh (Triangular Pyramid)
        self.StaticMesh = VertexInfo(self.CustomMesh)

        posList = list()
        posList.append(Math3d.Vector3(-1, 0, 0))        # left
        posList.append(Math3d.Vector3( 0, 0,-1.6))      # back
        posList.append(Math3d.Vector3( 1, 0, 0))        # right
        posList.append(Math3d.Vector3( 0, 1.5, -0.53))  # top

        self.StaticMesh.AddData(posList[0], Math3d.Color(1, 0, 0, 1), Math3d.Vector2(0,1))    # 0
        self.StaticMesh.AddData(posList[3], Math3d.Color(1, 0, 0, 1), Math3d.Vector2(0.5,0))  # 1
        self.StaticMesh.AddData(posList[1], Math3d.Color(1, 0, 0, 1), Math3d.Vector2(1,1))    # 2

        self.StaticMesh.AddData(posList[1], Math3d.Color(0, 1, 0, 1), Math3d.Vector2(0,1))    # 3
        self.StaticMesh.AddData(posList[3], Math3d.Color(0, 1, 0, 1), Math3d.Vector2(0.5,0))  # 4
        self.StaticMesh.AddData(posList[2], Math3d.Color(0, 1, 0, 1), Math3d.Vector2(1,1))    # 5

        self.StaticMesh.AddData(posList[3], Math3d.Color(0, 0, 1, 1), Math3d.Vector2(0.5,0))  # 6
        self.StaticMesh.AddData(posList[0], Math3d.Color(0, 0, 1, 1), Math3d.Vector2(0,1))    # 7
        self.StaticMesh.AddData(posList[2], Math3d.Color(0, 0, 1, 1), Math3d.Vector2(1,1))    # 8

        self.StaticMesh.AddData(posList[2], Math3d.Color(1, 1, 1, 1), Math3d.Vector2(0,1))    # 9
        self.StaticMesh.AddData(posList[0], Math3d.Color(1, 1, 1, 1), Math3d.Vector2(0.5,0))  # 10
        self.StaticMesh.AddData(posList[1], Math3d.Color(1, 1, 1, 1), Math3d.Vector2(1,1))    # 11
        
        self.StaticMesh.InitIndices(0,1,2, 3,4,5, 6,7,8, 9,10,11)



        # Pixel Shader cbuffer Setting
        self.Vec3Array = list()
        self.Vec3Array.append(Math3d.Vector3(0, 1, 0));
        self.Vec3Array.append(Math3d.Vector3(0, 0, 1));
        self.CustomMesh.SetUniform("Float3Array", self.Vec3Array)
        self.CustomMesh.SetUniform("Mode", self._Mode)
        self.CustomMesh.SetUniform("Color", Math3d.Vector3(0,1,0))
        self.CustomMesh.SetTexture("TextureDiffuse", "$project/Assets/openex/Texture.jpg")
        # ※ 지원하는 데이터 형식 : Int, Float, Vector2, Vector3, Vector4 ,Matrix ,list
        # SetUniform    
        # (Attribute Name, Data)
        # (Attribute Name, Data List)
        self.FPS = 0
        self.FPSTime = 0.0
    def Update(self):
        self._Time += self.World.GetFrameElapseTime()
        BWZeroOne = 0.5 + math.sin(self._Time)*0.5
        self.CustomMesh.SetUniform("ColorRate", (BWZeroOne * 0.5 + 0.25))
        if self._DynamicMeshView == True:

        #    #self.DynamicMesh.SetPosition(0, Math3d.Vector3(-1+math.sin(self._Time*1.2)*0.5,-1,0))
        #    #self.DynamicMesh.SetPosition(1, Math3d.Vector3(0,1+math.cos(self._Time*2.5)*0.5,0))
        #    #self.DynamicMesh.SetPosition(2, Math3d.Vector3(1+math.sin(self._Time)*0.5,-1,0))
            self.MoveVertexArray[0] = Math3d.Vector3(math.sin(self._Time*1.2)*0.5,0,0)
            self.MoveVertexArray[1] = Math3d.Vector3(0,math.cos(self._Time*2.5)*0.5,0)
            self.MoveVertexArray[2] = Math3d.Vector3(math.sin(self._Time*1.2)*0.5,0,0)
            self.DynamicMesh.SetDiffuse(1, Math3d.Color(BWZeroOne,BWZeroOne,BWZeroOne,1))# Tri Top Vertex Color (White <-> Black)
            self.CustomMesh.SetUniform("MoveVertex", self.MoveVertexArray)
            self.DynamicMesh.UpdateData()
        ## else: Nothing. (Static Mesh View)

        self.FPS += 1
        self.FPSTime += self.World.GetFrameElapseTime()
        if self.FPSTime > 1.0:
            print("FPS : " + str(int(float(self.FPS) / self.FPSTime)))
            self.FPS = 0
            self.FPSTime = 0.0



    def OnMessage(self, msg, number, Vector4_lparm, Vector4_wparam):
        # Dynamic Mesh View <-> Static Mesh View
        if msg == "KeyDown":
            if number == int('0x20', 16):  #VK_SPACE  
                self._DynamicMeshView = not self._DynamicMeshView

                if self._DynamicMeshView == False:
                    self.MoveVertexArray[0] = Math3d.Vector3(0,0,0)
                    self.MoveVertexArray[1] = Math3d.Vector3(0,0,0)
                    self.MoveVertexArray[2] = Math3d.Vector3(0,0,0)
            
                    self.CustomMesh.SetUniform("MoveVertex", self.MoveVertexArray)

                    self.StaticMesh.UpdateData()

            elif number == int('0x26', 16):  #VK_UP
                self._Mode += 1
                if (self._Mode > 5):
                    self._Mode = 5
                self.CustomMesh.SetUniform("Mode", self._Mode);
                print("Mode : " + str(self._Mode))

            elif number == int('0x28', 16):  #VK_DOWN
                self._Mode -= 1
                if (self._Mode < 0):
                    self._Mode = 0
                self.CustomMesh.SetUniform("Mode", self._Mode);
                print("Mode : " + str(self._Mode))
