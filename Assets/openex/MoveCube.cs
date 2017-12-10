public class MoveCube : EActor
{
    public Container CubeContainer;

    private Cube cubeComponent;

    public int OnCreate()
    {
        //cubeComponent = (Cube)CubeContainer.FindComponentByType("Cube");
        //if (cubeComponent == null)
        //{
        //    Log("cubeComponent is null", 0, 0.0);
        //    return 0;
        //}

    }

    //public void ChangeCubeTexture()
    //{
    //    if(cubeComponent != null)
    //    {
    //        cubeComponent.PropMaterial[0].SetTextureDiffuse(GetProjectPath() + "/Assets/Resource/example/1vf.png");
    //    }
        
    //}


    public override int OnMessage(string msg, int arg0, Vector4 arg1, Vector4 arg2)
    {

        
        return 0;
    }

    public override int Update()
    {


        return 0;
    }
}