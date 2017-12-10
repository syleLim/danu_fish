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
        self.count = 0;



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
            #print(self._PositionList[i])
            
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
        print(self._PositionList[1])

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

    def InitIndices(self, indices):
        
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

class custom_flow(Actor.Actor):
    def __init__(self):
        self._Time = 0.0
        self._Mode = 1
    

    def OnCreate(self, this):
        worldContainer = GetWorldContainer()
        self.World = worldContainer.FindComponentByType("World")

        targetContainer = Container(this)

        if targetContainer.FindComponentByType("TransformGroup") == None:
            targetContainer.AddNewComponent("TransformGroup")

        self.CustomMesh = targetContainer.AddNewComponent("CustomMesh")

        self.CustomMesh.PropCustomMesh.SetVertexShader("/Assets/openex/CustomShader") 
        self.CustomMesh.PropCustomMesh.SetPixelShader("/Assets/openex/CustomShader")        

        self.waterMesh = VertexInfo(self.CustomMesh)

        self.posList = list()
        
        self.col = 60
        self.row = 60
        
        i = -1
        j = -1


        for x in range(0, self.col*self.row) :
            i +=1

            if i%self.col == 0 :
                j +=1
                i = 0
            
            self.posList.append(Math3d.Vector3(i/5, 0, j/5))

        print(len(self.posList))
        

        i = -1

        for x in range(0, (self.col-1)*(self.row-1)) :
            i +=1
            if (i+1)%self.col == 0 :
                i +=1

            self.waterMesh.AddData(self.posList[i], Math3d.Color(0, 0, 1, 0.5), Math3d.Vector2(0,1))
            self.waterMesh.AddData(self.posList[i+1], Math3d.Color(0, 0, 1, 0.3), Math3d.Vector2(0.5,0))
            self.waterMesh.AddData(self.posList[i+self.col+1], Math3d.Color(0, 0, 1, 0.2), Math3d.Vector2(1,1))

            #print(str(x)+" :"+posList[i].__str__()+" : "+posList[i+1].__str__()+":"+posList[i+col].__str__())

        i= -1

        for x in range(0, (self.col-1)*(self.row-1)) :
            i +=1
            if (i+1)%self.col == 0:
                i +=1

            self.waterMesh.AddData(self.posList[i], Math3d.Color(0, 0, 1, 0.3), Math3d.Vector2(0,1))
            self.waterMesh.AddData(self.posList[i+self.col], Math3d.Color(0, 0, 1, 0.5), Math3d.Vector2(0.5,0))
            self.waterMesh.AddData(self.posList[i+self.col+1], Math3d.Color(0, 0, 1, 0.2), Math3d.Vector2(1,1))

            #print(str(x)+" :"+posList[i].__str__()+" : "+posList[i+col].__str__()+":"+posList[i+col+1].__str__())

        temp_index = list();

        for i in range(0, 6*(self.col-1)*(self.row-1)) :
            temp_index.append(i)

        self.waterMesh.InitIndices(temp_index)

        #print(temp_index)
        
        self.Vec3Array = list()
        self.Vec3Array.append(Math3d.Vector3(0, 1, 0));
        self.Vec3Array.append(Math3d.Vector3(0, 0, 1));
        self.CustomMesh.SetUniform("Float3Array", self.Vec3Array)
        self.CustomMesh.SetUniform("Mode", self._Mode)
        self.CustomMesh.SetUniform("Color", Math3d.Vector3(0,0,1))
        #self.CustomMesh.SetTexture("TextureDiffuse", "$project/Assets/water_1.jpg")
        #self.CustomMesh.SetTexture("TextureNormal", "$project/Assets/water_no_1.jpg")
        
        self.MoveVertexArray = list()
        for i in range(0, 6*(self.col-1)*(self.row-1)) :
            self.MoveVertexArray.append(Math3d.Vector3(0,0,0))    
    

    def Update(self) :

        self._Time += self.World.GetFrameElapseTime()
        BWZeroOne = 0.5 + math.sin(self._Time)*0.5
        self.CustomMesh.SetUniform("ColorRate", (BWZeroOne * 0.5 + 0.25))

        for i in range(len(self.posList)) :
            if i%2 == 0 :
                self.posList[i] += Math3d.Vector3(0, math.sin(self._Time*2)*0.01 ,0)
            else : 
                self.posList[i] += Math3d.Vector3(0, math.cos(self._Time*2)*0.01 ,0)


        i = -1

        for x in range(0, (self.col-1)*(self.row-1)) :
            i +=1
            if (i+1)%self.col == 0 :
                i +=1

            self.waterMesh.SetData(3*x, self.posList[i], Math3d.Color(0, 0, 1, 0.3), Math3d.Vector2(0,1))
            self.waterMesh.SetData(3*x+1, self.posList[i+1], Math3d.Color(0, 0, 1, 0.2), Math3d.Vector2(0.5,0))
            self.waterMesh.SetData(3*x+2, self.posList[i+self.col+1], Math3d.Color(0, 0, 1, 0.5), Math3d.Vector2(1,1))


        i= -1

        for x in range((self.col-1)*(self.row-1), 2*(self.col-1)*(self.row-1)) :
            i +=1
            if (i+1)%self.col == 0:
                i +=1

            self.waterMesh.SetData(3*x, self.posList[i], Math3d.Color(0, 0, 1, 0.5), Math3d.Vector2(0,1))
            self.waterMesh.SetData(3*x+1, self.posList[i+self.col], Math3d.Color(0, 0, 1, 0.2), Math3d.Vector2(0.5,0))
            self.waterMesh.SetData(3*x+2, self.posList[i+self.col+1], Math3d.Color(0, 0, 1, 0.3), Math3d.Vector2(1,1))



#        for i in range(0, 6*(col-1)*(row-1)) :
#            print(i)
#            if i%2 == 0 :
#                self.MoveVertexArray[i] = Math3d.Vector3(0, math.sin(self._Time) ,0)
#            else :
#                self.MoveVertexArray[i] = Math3d.Vector3(0, math.cos(self._Time) ,0)
            

        self.waterMesh.SetDiffuse(1, Math3d.Color(BWZeroOne,BWZeroOne,BWZeroOne,1))
        #self.CustomMesh.SetUniform("MoveVertex", self.MoveVertexArray)
        

        self.waterMesh.UpdateData()

   
        
