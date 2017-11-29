import numpy
import math

class vertex():
	def __init__(self, custom_object):
		self._init_local_pos = list()
		self._local_pos = list()
		self._Postions = list()
		self._Color = list()
		self._object = custom_object

	def UdateObject(self):

		last_position = list()

		for i in len(self._Postions) :
			last_position.append(self._Postions[i]+(self._local_pos[i]-self._init_local_pos))

		self._object.SetPositions(last_position)
		self._object.SetDiffuses(self._Color)


	def Set_ver_Position(self, idx,  vector3_pos):
		self._Postions[idx] = vector3_pos

	def Set_local_Postion(self, lo_pos_changed):
		self._local_pos = lo_pos_changed


	def Insert_ver_pos(self, vector3_pos):
		self._Postions.append(vector3_pos)
		self._init_local_pos.append(vector3_pos)
		self._local_pos.append(vector3_pos)

	def SetColor(self, vector4_col):
		self._Color[idx] = vector4_col

	def InsertColor(self, vector4_col):
		self._Color.append(vector4_col)


class fish_move(Actor.Actor):
	def __init__(self):
		self._test1 = int
		self._wavelength = int(0)


		self._aplitude_level = int(0)
		self._pivot_point = int(0)
		self._move_speed_x = int(0)
		self._move_speed_y = int(0)
		self._move_speed_z = int(0)

		self._move_speed = Math3d.Vector3(_move_speed_x, _move_speed_y, _move_speed_z)
		self._time = 0.0;

		return

	def OnCreate(self, this):
		
		#TODO : Object setting
		self.container = GetWorldContainer()
		self.World = self.container.FindComponentByType("World")

		self.ThisContainer = Container(this)

		self.ThisContainer.AddNewComponent("TransformGourp")
		self.CustomMesh = self.ThisContainer.AddNewComponent("CustomMesh")
		self.position = vertex(self.CustomMesh)



		#dumy data_setup
		self.position.insert_ver_pos(Math3d.Vector3(0,0,0))
		self.position.insert_ver_pos(Math3d.Vector3(1,0,0))
		self.position.insert_ver_pos(Math3d.Vector3(2,0,0))
		self.position.insert_ver_pos(Math3d.Vector3(3,0,0))

		self.position.InsertColor(Math3d.Color(1,1,1,1))
		self.position.InsertColor(Math3d.Color(1,1,1,1))
		self.position.InsertColor(Math3d.Color(1,1,1,1))
		self.position.InsertColor(Math3d.Color(1,1,1,1))


	def Update(self):
	
		Fish_wave()
		
		self.position.UpdateObject()


	def Fish_wave(self):
		#TOTO : main time lenth
		self._time += self.container.GetFrameElapseTime()

		pivot_pos = self.position._local_pos[self._pivot_point]
		front_pos = self.position._local_pos[:self._pivot_point-1]
		back_pos = self.position._local_pos[self._pivot_point:]

		lo_front_pos = list()
		lo_back_pos = list()

		#pivot = (0,0,0)
		for pos in front_pos :
			lo_front_pos.append(pivot_pos-pos)
		front_pos.clear()

		for pos in back_pos :
			lo_back_pos.append(pos-pivot_pos)
		back_pos.clear()

		amplitude = self._aplitude_level*(len(front_pos)+1)
		change_front_pos = list()

		for pos in lo_front_pos :
			amplitude -= self._aplitude_level

			# f(x, t) = A * sin (2pi / (wavelenth * (wavelength*(x(pivot = 0 )-time * frequency))
			change_front_pos.append(pos+math.sin(math.pi/self._wavelength*(-(1/self._wavelength*self._time))*amplitude))

		amplitude = 0
		change_back_pos = list()

		for pos in lo_back_pos :
			amplitude += self._aplitude_level
			
			# f(x, t) = A * sin (2pi / (wavelenth * (wavelength*(x(pivot = 0 )-time * frequency))
			change_back_pos.append(pos+math.sin(math.pi/self._wavelength*(-(1/self._wavelength*self._time))*amplitude))


		for pos in change_front_pos :
			front_pos.append(pivot_pos-pos)

		for pos in change_back_pos :
			back_pos.append(pos+pivot_pos)


		self.position.Set_local_Postion(front_pos + pivot_pos + back_pos) 


	def Fish_move(self):
		pass

	def OnDestroy(self):

		return 0

	def OnEnable(self):

		return 0

	def OnEnable(self):

		return 0

	def OnDisable(self):

		return 0



	def OnMessage(self, msg, number, Vertor4_lparm, Vector4_wparm):
		return




