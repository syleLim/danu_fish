import math
import random

class fish_moving(Actor.Actor):
	def __init__(self):
		#Object => Head
		self.Fish_ob = Container(0)
		
		#ChildObject => Fish body
		self.Fish_Head = Container(0)
		self.Fish_Pivot = Container(0)
		self.Fish_Back_1 = Container(0)
		self.Fish_Back_2 = Container(0)

		#start_time
		self._time = 0

		#Speed =>go ahead speed
		self.fish_speed = 0.06;
		self.direction = Math3d.Vector3(0, 0, 0)

		#turn_move
		self.is_Turn = False
		self.turn_speed = 0.1
		self.turn_degree = 10;
		self.turn_direction = Math3d.Vector3()
		self.turn_divide_euler = Math3d.Vector3()
		self.d = None
		self.turn_count = 0
		self.wall_check = int()
		self.Wall_x_1 = Container(0)
		self.Wall_x_2 = Container(0)
		self.Wall_z_1 = Container(0)
		self.Wall_z_2 = Container(0)
		self.ground_up = Container(0)
		self.ground_down = Container(0)
		self.ground_check = int()

		#turn_label
		self.is_wall_turn = False
		self.is_ob_turn = False
		self.is_ground_turn = False

		#change_speed
		self.fish_first_speed = 0.06
		self.is_speed_up = False
		self.is_speed_down = False
		self.speed_count = 0
		self.speed_factor = 0.02

		#set Oculus
		self.Oculus_right_Container = Container(0)
		self.Oculus_left_Container = Container(0)
		self.is_inter_action = True
		self.pre_hand_pos = Math3d.Vector3()
		self.is_hand_move = None
		self.is_ob_hand_length = int()
		
		return



	def OnCreate(self, this):
		self.World = GetWorldContainer().FindComponentByType("World")
		self.is_hand_move = 0.5
		
		if 1 == random.randrange(0, 2) :
			a = -1
		else : 
			a = 1
		if 1 == random.randrange(0, 2) :
			b = -1
		else : 
			b = 1
		if 1 == random.randrange(0, 2) :
			c = -1
		else : 
			c = 1

		self.direction  = self.Nor(Math3d.Vector3(a*random.random(), b*random.random(), c*random.random()))

		self.Fish_ob = Container(this)
		self.Fish_Head_2 = self.Fish_ob.GetChild(0)
		self.Fish_Head_1 = self.Fish_ob.GetChild(1)
		self.Fish_Pivot = self.Fish_ob.GetChild(2)
		self.Fish_Back_1 = self.Fish_ob.GetChild(3)
		self.Fish_Back_2 = self.Fish_ob.GetChild(4)
		self.Fish_Back_3 = self.Fish_ob.GetChild(5)
		self.Fish_Back_4 = self.Fish_ob.GetChild(6)
		self.Fish_Back_5 = self.Fish_ob.GetChild(7)


		self.Fish_ob_transform = self.Fish_ob.FindComponentByType("TransformGroup")
		
		self.Fish_Head_2_transform = self.Fish_Head_2.FindComponentByType("TransformGroup")
		self.Fish_Head_1_transform = self.Fish_Head_1.FindComponentByType("TransformGroup")
		self.Fish_Pivot_transform = self.Fish_Pivot.FindComponentByType("TransformGroup")
		self.Fish_Back_1_transform = self.Fish_Back_1.FindComponentByType("TransformGroup")
		self.Fish_Back_2_transform = self.Fish_Back_2.FindComponentByType("TransformGroup")
		self.Fish_Back_3_transform = self.Fish_Back_3.FindComponentByType("TransformGroup")
		self.Fish_Back_4_transform = self.Fish_Back_4.FindComponentByType("TransformGroup")
		self.Fish_Back_5_transform = self.Fish_Back_5.FindComponentByType("TransformGroup")


		self.Fish_Head_2_transform.SetScale(Math3d.Vector3(0.33, 0.33, 0.33))
		self.Fish_Head_1_transform.SetScale(Math3d.Vector3(0.37, 0.37, 0.37))
		self.Fish_Pivot_transform.SetScale(Math3d.Vector3(0.4, 0.4, 0.4))
		self.Fish_Back_1_transform.SetScale(Math3d.Vector3(0.38, 0.38, 0.38))
		self.Fish_Back_2_transform.SetScale(Math3d.Vector3(0.35, 0.35, 0.35))
		self.Fish_Back_3_transform.SetScale(Math3d.Vector3(0.31, 0.31, 0.31))
		self.Fish_Back_4_transform.SetScale(Math3d.Vector3(0.28, 0.28, 0.28))
		self.Fish_Back_5_transform.SetScale(Math3d.Vector3(0.27, 0.27, 0.27))


		#oculus Script save
		self.oculus_right_hand_pos = self.Oculus_right_Container.FindComponentByType("TransformGroup")
		self.oculus_left_hand_pos = self.Oculus_left_Container.FindComponentByType("TransformGroup")
		self.pre_hand_pos_right = self.oculus_right_hand_pos.GetPosition()
		self.pre_hand_pos_left = self.oculus_left_hand_pos.GetPosition()
		self.hand_count = 0

		#first in data
		self.pre_rot = self.Fish_ob_transform.GetRotation()

		#trun_wall
		self.wall_x = [self.Wall_x_1.FindComponentByType("TransformGroup").GetPosition().x, self.Wall_x_2.FindComponentByType("TransformGroup").GetPosition().x]
		self.wall_z = [self.Wall_z_1.FindComponentByType("TransformGroup").GetPosition().z, self.Wall_z_2.FindComponentByType("TransformGroup").GetPosition().z]
		self.ground_y = [self.ground_up.FindComponentByType("TransformGroup").GetPosition().y, self.ground_down.FindComponentByType("TransformGroup").GetPosition().y]



	def Update(self):
		
		if self.hand_count%10 == 0 :
			self.pre_hand_pos_right = self.oculus_right_hand_pos.GetPosition()
			self.pre_hand_pos_left = self.oculus_left_hand_pos.GetPosition()
		
		self.hand_count +=1


		if self.is_speed_up :
			self.Go_fast()

		if self.is_speed_down :
			self.Go_slow()

		

		self.check_out(self.Fish_ob_transform)

		self.Check_hand(self.oculus_right_hand_pos, self.pre_hand_pos_right)
		self.Check_hand(self.oculus_left_hand_pos, self.pre_hand_pos_left)

		#error _ wall active -> check_hand is no work
		self.Check_Wall(self.wall_x, 'x')
		self.Check_Wall(self.wall_z, 'z')
		self.Check_ground(self.ground_y)


		#print(self.is_Turn)
		
		if self.is_Turn :
			if self.direction == self.turn_direction :
				self.turn_count = 0
				self.is_Turn = False
				self.is_ground_turn = False
				self.is_wall_turn = False
				self.is_ob_turn = False
			else :
				self.Fish_turn(self.turn_degree)

				if self.turn_count >200 :
					self.turn_count = 0
					self.is_Turn = False
					self.is_ground_turn = False
					self.is_wall_turn = False
					self.is_ob_turn = False					
		else :
			self.Fish_go_ahead(self.fish_speed, self.direction)



	def Fish_go_ahead(self, speed, direction):
		#print(self.fish_speed)
		self._time += self.World.GetFrameElapseTime()*self.fish_speed*60

		pre_position = self.Fish_ob_transform.GetPosition()

		#anytime initialize
		if direction.Length() == 0 :
			pass
		else :
			direction = self.Nor(direction)	
		

		#Stardard position
		pre_position_head_2 =  Math3d.Vector4(1.5, 0, 0, 0)
		pre_position_head_1 =  Math3d.Vector4(0.75, 0, 0, 0)
		pre_position_pivot = Math3d.Vector4(0, 0, 0, 0)
		pre_position_back_1 = Math3d.Vector4(-0.75, 0, 0, 0)
		pre_position_back_2 = Math3d.Vector4(-1.5, 0, 0, 0)
		pre_position_back_3 = Math3d.Vector4(-2.25, 0, 0, 0)
		pre_position_back_4 = Math3d.Vector4(-3, 0, 0, 0)
		pre_position_back_5 = Math3d.Vector4(-3.75, 0, 0, 0)

		
		#local moveing algorithm
		#Set angle(20, 40), transform matrix
		transform_1 = Math3d.Matrix(1,0,0,0.75,0, 1, 0, 0, 0, 0, 1,0, 0,0,0,1)
		rotate_head_2 = Math3d.Matrix(math.cos(math.pi*(math.sin(self._time)*(-10)/180)), 0, math.sin(math.pi*(math.sin(self._time)*(-10)/180)), 0, 0,1,0,0, -math.sin(math.pi*(math.sin(self._time)*(-10)/180)), 0, math.cos(math.pi*(math.sin(self._time)*(-15)/180)), 0, 0,0,0,1)
		re_transform_1 = Math3d.Matrix(1,0,0, -0.75, 0, 1, 0, 0, 0, 0, 1,0, 0,0,0,1)

		rotate_head_1 = Math3d.Matrix(math.cos(math.pi*(math.sin(self._time)*(-7.5)/180)), 0, math.sin(math.pi*(math.sin(self._time)*(-7.5)/180)), 0, 0,1,0,0, -math.sin(math.pi*(math.sin(self._time)*(-7.5)/180)), 0, math.cos(math.pi*(math.sin(self._time)*(-7.5)/180)), 0, 0,0,0,1)

		rotate_1 = Math3d.Matrix(math.cos(math.pi*(math.sin(self._time)*7.5/180)), 0, math.sin(math.pi*(math.sin(self._time)*7.5/180)), 0, 0,1,0,0, -math.sin(math.pi*(math.sin(self._time)*7.5/180)), 0, math.cos(math.pi*(math.sin(self._time)*7.5/180)), 0, 0,0,0,1)

		transform_2 = Math3d.Matrix(1,0,0,-0.75,0, 1, 0, 0, 0, 0, 1,0, 0,0,0,1)
		rotate_2 = Math3d.Matrix(math.cos(math.pi*(math.sin(self._time)*12/180)), 0, math.sin(math.pi*(math.sin(self._time)*12/180)), 0,0,1,0,0, -math.sin(math.pi*(math.sin(self._time)*12/180)), 0, math.cos(math.pi*(math.sin(self._time)*12/180)), 0, 0,0,0,1 )
		re_transform_2 = Math3d.Matrix(1,0,0, 0.75, 0, 1, 0, 0, 0, 0, 1,0, 0,0,0,1)

		transform_3 = Math3d.Matrix(1,0,0,-0.75,0, 1, 0, 0, 0, 0, 1,0, 0,0,0,1)
		rotate_3 = Math3d.Matrix(math.cos(math.pi*(math.sin(self._time)*18/180)), 0, math.sin(math.pi*(math.sin(self._time)*18/180)), 0,0,1,0,0, -math.sin(math.pi*(math.sin(self._time)*18/180)), 0, math.cos(math.pi*(math.sin(self._time)*18/180)), 0, 0,0,0,1 )
		re_transform_3 = Math3d.Matrix(1,0,0, 0.75, 0, 1, 0, 0, 0, 0, 1,0, 0,0,0,1)

		transform_4 = Math3d.Matrix(1,0,0,-0.75,0, 1, 0, 0, 0, 0, 1,0, 0,0,0,1)
		rotate_4 = Math3d.Matrix(math.cos(math.pi*(math.sin(self._time)*24/180)), 0, math.sin(math.pi*(math.sin(self._time)*24/180)), 0,0,1,0,0, -math.sin(math.pi*(math.sin(self._time)*24/180)), 0, math.cos(math.pi*(math.sin(self._time)*24/180)), 0, 0,0,0,1 )
		re_transform_4 = Math3d.Matrix(1,0,0, 0.75, 0, 1, 0, 0, 0, 0, 1,0, 0,0,0,1)		

		transform_5 = Math3d.Matrix(1,0,0,-0.75,0, 1, 0, 0, 0, 0, 1,0, 0,0,0,1)
		rotate_5 = Math3d.Matrix(math.cos(math.pi*(math.sin(self._time)*30/180)), 0, math.sin(math.pi*(math.sin(self._time)*30/180)), 0,0,1,0,0, -math.sin(math.pi*(math.sin(self._time)*30/180)), 0, math.cos(math.pi*(math.sin(self._time)*30/180)), 0, 0,0,0,1 )
		re_transform_5 = Math3d.Matrix(1,0,0, 0.75, 0, 1, 0, 0, 0, 0, 1,0, 0,0,0,1)		

		#rotate_euler
		temp = self.MatrixCal(re_transform_2, self.MatrixCal(rotate_head_2, self.MatrixCal(transform_2, pre_position_head_2)))
		next_postion_head_2 = Math3d.Vector3(temp.x, temp.y, temp.z)

		temp = self.MatrixCal(rotate_head_1, pre_position_head_1)
		next_postion_head_1 = Math3d.Vector3(temp.x, temp.y, temp.z)
		
		next_postion_pivot = Math3d.Vector3(pre_position_pivot.x, pre_position_pivot.y, pre_position_pivot.z )
		
		temp = self.MatrixCal(rotate_1, pre_position_back_1)
		next_postion_back_1 = Math3d.Vector3(temp.x, temp.y, temp.z)
		
		temp = self.MatrixCal(re_transform_2, self.MatrixCal(rotate_2, self.MatrixCal(transform_2, pre_position_back_2)))
		next_postion_back_2 = Math3d.Vector3(temp.x, temp.y, temp.z)

		temp = self.MatrixCal(re_transform_3, self.MatrixCal(rotate_3, self.MatrixCal(transform_3, pre_position_back_3)))
		next_postion_back_3 = Math3d.Vector3(temp.x, temp.y, temp.z)

		temp = self.MatrixCal(re_transform_4, self.MatrixCal(rotate_4, self.MatrixCal(transform_4, pre_position_back_4)))
		next_postion_back_4 = Math3d.Vector3(temp.x, temp.y, temp.z)

		temp = self.MatrixCal(re_transform_5, self.MatrixCal(rotate_5, self.MatrixCal(transform_5, pre_position_back_5)))
		next_postion_back_5 = Math3d.Vector3(temp.x, temp.y, temp.z)
		
		self.Fish_Head_2_transform.SetLocalPosition(next_postion_head_2)
		self.Fish_Head_1_transform.SetLocalPosition(next_postion_head_1)
		self.Fish_Pivot_transform.SetLocalPosition(next_postion_pivot)
		self.Fish_Back_1_transform.SetLocalPosition(next_postion_back_1)
		self.Fish_Back_2_transform.SetLocalPosition(next_postion_back_2)
		self.Fish_Back_3_transform.SetLocalPosition(next_postion_back_3)
		self.Fish_Back_4_transform.SetLocalPosition(next_postion_back_4)
		self.Fish_Back_5_transform.SetLocalPosition(next_postion_back_5)

		#TODO : Local Rotation Phase - not work/ some strange
		
		quat_head_2 = Math3d.Quaternion().EulerToQuaternionFloat(Math3d.Vector3(0, math.pi*(math.sin(self._time)*(-13)/180), 0))
		quat_head_1 = Math3d.Quaternion().EulerToQuaternionFloat(Math3d.Vector3(0, math.pi*(math.sin(self._time)*(-7)/180), 0))
		quat_back_1 = Math3d.Quaternion().EulerToQuaternionFloat(Math3d.Vector3(0, math.pi*(math.sin(self._time)*(7)/180), 0))
		quat_back_2 = Math3d.Quaternion().EulerToQuaternionFloat(Math3d.Vector3(0, math.pi*(math.sin(self._time)*(13)/180), 0))
		quat_back_3 = Math3d.Quaternion().EulerToQuaternionFloat(Math3d.Vector3(0, math.pi*(math.sin(self._time)*(22)/180), 0))
		quat_back_4 = Math3d.Quaternion().EulerToQuaternionFloat(Math3d.Vector3(0, math.pi*(math.sin(self._time)*(36)/180), 0))
		quat_back_5 = Math3d.Quaternion().EulerToQuaternionFloat(Math3d.Vector3(0, math.pi*(math.sin(self._time)*(52)/180), 0))
		

		self.Fish_Head_2_transform.SetLocalRotation(quat_head_2)
		self.Fish_Head_1_transform.SetLocalRotation(quat_head_1)
		self.Fish_Back_1_transform.SetLocalRotation(quat_back_1)
		self.Fish_Back_2_transform.SetLocalRotation(quat_back_2)
		self.Fish_Back_3_transform.SetLocalRotation(quat_back_3)
		self.Fish_Back_4_transform.SetLocalRotation(quat_back_4)
		self.Fish_Back_5_transform.SetLocalRotation(quat_back_5)
		

		#moving algorithm
		pre_axis = Math3d.Vector3(1, 0, 0)
		q = self.CalQuaternion(pre_axis, direction)

		angle_y = None
		angle_z = None

		if (direction.x*direction.x + direction.z*direction.z) != 0:
			angle_z = math.atan(direction.y/math.sqrt(direction.x*direction.x + direction.z*direction.z))
		else :
			if direction.y>0 :
				angle_z = math.pi/2
			else :
				angle_z = - math.pi/2
		
		if direction.x == 0 :
			if direction.z>0 :
				angle_y = - math.pi/2
			elif direction.z == 0 :
				angle_y = 0
			else :
				angle_y = math.pi/2
		else :
			angle_y = math.atan(direction.z/direction.x)

		#q_ = Math3d.Quaternion().EulerToQuaternionFloat(Math3d.Vector3(0, 0, angle_z))
		#q__ = Math3d.Quaternion().EulerToQuaternionFloat(Math3d.Vector3(0, angle_y, 0))
		#q___ = q__*q_*self.pre_rot*Math3d.Quaternion(-q_.x, -q_.y, -q_.z, q_.w)*Math3d.Quaternion(-q__.x, -q__.y, -q__.z, q__.w)

		
		#rot_z = Math3d.Matrix(math.cos(angle_z), -math.sin(angle_z), 0,0,math.sin(angle_z), math.cos(angle_z), 0, 0, 0, 0, 1, 0, 0, 0, 0, 1)
		#rot_y = Math3d.Matrix(math.cos(angle_y), 0, math.sin(angle_y), 0, 0, 1, 0, 0, -math.sin(angle_y), 0, math.cos(angle_y), 0, 0, 0, 0, 1)

		#q =	Math3d.Quaternion().EulerToQuaternionFloat(Math3d.Vector3(0, angle_y, angle_z))
		
		next_position = pre_position + (direction*speed)

		
		#print(q___.__str__())
		#print(self.Fish_ob_transform.GetRotation())

		self.Fish_ob_transform.SetPosition(next_position)


		x = q
		y = Math3d.Quaternion.QuaternionToEulerDegreeFloat(x)
		y.x = 0
		z = Math3d.Quaternion.EulerDegreeToQuaternionFloat(y)
		self.Fish_ob_transform.SetRotation(z)
	


	def Fish_turn(self, degree):

		self._time += self.World.GetFrameElapseTime()*50*self.fish_speed

		pre_position = self.Fish_ob_transform.GetPosition()

		#Stardard position
		pre_position_head_2 =  Math3d.Vector4(1.5, 0, 0, 0)
		pre_position_head_1 =  Math3d.Vector4(0.75, 0, 0, 0)
		pre_position_pivot = Math3d.Vector4(0, 0, 0, 0)
		pre_position_back_1 = Math3d.Vector4(-0.75, 0, 0, 0)
		pre_position_back_2 = Math3d.Vector4(-1.5, 0, 0, 0)
		pre_position_back_3 = Math3d.Vector4(-2.25, 0, 0, 0)
		pre_position_back_4 = Math3d.Vector4(-3, 0, 0, 0)
		pre_position_back_5 = Math3d.Vector4(-3.75, 0, 0, 0)

		#rotate matrix
		#local moveing algorithm
		#Set angle(20, 40), transform matrix
		transform_1 = Math3d.Matrix(1,0,0,0.75,0, 1, 0, 0, 0, 0, 1,0, 0,0,0,1)
		rotate_head_2 = Math3d.Matrix(math.cos(math.pi*(math.sin(self._time)*(-15)/180)), 0, math.sin(math.pi*(math.sin(self._time)*(-15)/180)), 0, 0,1,0,0, -math.sin(math.pi*(math.sin(self._time)*(-15)/180)), 0, math.cos(math.pi*(math.sin(self._time)*(-15)/180)), 0, 0,0,0,1)
		re_transform_1 = Math3d.Matrix(1,0,0, -0.75, 0, 1, 0, 0, 0, 0, 1,0, 0,0,0,1)

		rotate_head_1 = Math3d.Matrix(math.cos(math.pi*(math.sin(self._time)*(-7.5)/180)), 0, math.sin(math.pi*(math.sin(self._time)*(-7.5)/180)), 0, 0,1,0,0, -math.sin(math.pi*(math.sin(self._time)*(-7.5)/180)), 0, math.cos(math.pi*(math.sin(self._time)*(-7.5)/180)), 0, 0,0,0,1)

		rotate_1 = Math3d.Matrix(math.cos(math.pi*(math.sin(self._time)*7.5/180)), 0, math.sin(math.pi*(math.sin(self._time)*7.5/180)), 0, 0,1,0,0, -math.sin(math.pi*(math.sin(self._time)*7.5/180)), 0, math.cos(math.pi*(math.sin(self._time)*7.5/180)), 0, 0,0,0,1)

		transform_2 = Math3d.Matrix(1,0,0,-0.75,0, 1, 0, 0, 0, 0, 1,0, 0,0,0,1)
		rotate_2 = Math3d.Matrix(math.cos(math.pi*(math.sin(self._time)*12/180)), 0, math.sin(math.pi*(math.sin(self._time)*12/180)), 0,0,1,0,0, -math.sin(math.pi*(math.sin(self._time)*12/180)), 0, math.cos(math.pi*(math.sin(self._time)*12/180)), 0, 0,0,0,1 )
		re_transform_2 = Math3d.Matrix(1,0,0, 0.75, 0, 1, 0, 0, 0, 0, 1,0, 0,0,0,1)

		transform_3 = Math3d.Matrix(1,0,0,-0.75,0, 1, 0, 0, 0, 0, 1,0, 0,0,0,1)
		rotate_3 = Math3d.Matrix(math.cos(math.pi*(math.sin(self._time)*18/180)), 0, math.sin(math.pi*(math.sin(self._time)*18/180)), 0,0,1,0,0, -math.sin(math.pi*(math.sin(self._time)*18/180)), 0, math.cos(math.pi*(math.sin(self._time)*18/180)), 0, 0,0,0,1 )
		re_transform_3 = Math3d.Matrix(1,0,0, 0.75, 0, 1, 0, 0, 0, 0, 1,0, 0,0,0,1)

		transform_4 = Math3d.Matrix(1,0,0,-0.75,0, 1, 0, 0, 0, 0, 1,0, 0,0,0,1)
		rotate_4 = Math3d.Matrix(math.cos(math.pi*(math.sin(self._time)*24/180)), 0, math.sin(math.pi*(math.sin(self._time)*24/180)), 0,0,1,0,0, -math.sin(math.pi*(math.sin(self._time)*24/180)), 0, math.cos(math.pi*(math.sin(self._time)*24/180)), 0, 0,0,0,1 )
		re_transform_4 = Math3d.Matrix(1,0,0, 0.75, 0, 1, 0, 0, 0, 0, 1,0, 0,0,0,1)		

		transform_5 = Math3d.Matrix(1,0,0,-0.75,0, 1, 0, 0, 0, 0, 1,0, 0,0,0,1)
		rotate_5 = Math3d.Matrix(math.cos(math.pi*(math.sin(self._time)*30/180)), 0, math.sin(math.pi*(math.sin(self._time)*30/180)), 0,0,1,0,0, -math.sin(math.pi*(math.sin(self._time)*30/180)), 0, math.cos(math.pi*(math.sin(self._time)*30/180)), 0, 0,0,0,1 )
		re_transform_5 = Math3d.Matrix(1,0,0, 0.75, 0, 1, 0, 0, 0, 0, 1,0, 0,0,0,1)		


		#rotate_euler
		temp = self.MatrixCal(re_transform_2, self.MatrixCal(rotate_head_2, self.MatrixCal(transform_2, pre_position_head_2)))
		next_postion_head_2 = Math3d.Vector3(temp.x, temp.y, temp.z)

		temp = self.MatrixCal(rotate_head_1, pre_position_head_1)
		next_postion_head_1 = Math3d.Vector3(temp.x, temp.y, temp.z)
		
		next_postion_pivot = Math3d.Vector3(pre_position_pivot.x, pre_position_pivot.y, pre_position_pivot.z )
		
		temp = self.MatrixCal(rotate_1, pre_position_back_1)
		next_postion_back_1 = Math3d.Vector3(temp.x, temp.y, temp.z)
		
		temp = self.MatrixCal(re_transform_2, self.MatrixCal(rotate_2, self.MatrixCal(transform_2, pre_position_back_2)))
		next_postion_back_2 = Math3d.Vector3(temp.x, temp.y, temp.z)

		temp = self.MatrixCal(re_transform_3, self.MatrixCal(rotate_3, self.MatrixCal(transform_3, pre_position_back_3)))
		next_postion_back_3 = Math3d.Vector3(temp.x, temp.y, temp.z)

		temp = self.MatrixCal(re_transform_4, self.MatrixCal(rotate_4, self.MatrixCal(transform_4, pre_position_back_4)))
		next_postion_back_4 = Math3d.Vector3(temp.x, temp.y, temp.z)

		temp = self.MatrixCal(re_transform_5, self.MatrixCal(rotate_5, self.MatrixCal(transform_5, pre_position_back_5)))
		next_postion_back_5 = Math3d.Vector3(temp.x, temp.y, temp.z)
		

		self.Fish_Head_2_transform.SetLocalPosition(next_postion_head_2)
		self.Fish_Head_1_transform.SetLocalPosition(next_postion_head_1)
		self.Fish_Pivot_transform.SetLocalPosition(next_postion_pivot)
		self.Fish_Back_1_transform.SetLocalPosition(next_postion_back_1)
		self.Fish_Back_2_transform.SetLocalPosition(next_postion_back_2)
		self.Fish_Back_3_transform.SetLocalPosition(next_postion_back_3)
		self.Fish_Back_4_transform.SetLocalPosition(next_postion_back_4)
		self.Fish_Back_5_transform.SetLocalPosition(next_postion_back_5)


		quat_head_2 = Math3d.Quaternion().EulerToQuaternionFloat(Math3d.Vector3(0, math.pi*(math.sin(self._time)*(-13)/180), 0))
		quat_head_1 = Math3d.Quaternion().EulerToQuaternionFloat(Math3d.Vector3(0, math.pi*(math.sin(self._time)*(-7)/180), 0))
		quat_back_1 = Math3d.Quaternion().EulerToQuaternionFloat(Math3d.Vector3(0, math.pi*(math.sin(self._time)*(7)/180), 0))
		quat_back_2 = Math3d.Quaternion().EulerToQuaternionFloat(Math3d.Vector3(0, math.pi*(math.sin(self._time)*(13)/180), 0))
		quat_back_3 = Math3d.Quaternion().EulerToQuaternionFloat(Math3d.Vector3(0, math.pi*(math.sin(self._time)*(22)/180), 0))
		quat_back_4 = Math3d.Quaternion().EulerToQuaternionFloat(Math3d.Vector3(0, math.pi*(math.sin(self._time)*(36)/180), 0))
		quat_back_5 = Math3d.Quaternion().EulerToQuaternionFloat(Math3d.Vector3(0, math.pi*(math.sin(self._time)*(52)/180), 0))
		

		self.Fish_Head_2_transform.SetLocalRotation(quat_head_2)
		self.Fish_Head_1_transform.SetLocalRotation(quat_head_1)
		self.Fish_Back_1_transform.SetLocalRotation(quat_back_1)
		self.Fish_Back_2_transform.SetLocalRotation(quat_back_2)
		self.Fish_Back_3_transform.SetLocalRotation(quat_back_3)
		self.Fish_Back_4_transform.SetLocalRotation(quat_back_4)
		self.Fish_Back_5_transform.SetLocalRotation(quat_back_5)


		#moving postion _set1
		#self.pre_direction  = self.direction

		#self.direction = self.turn_direction

		#q = self.CalQuaternion(self.pre_direction, self.direction)

		#next_position = pre_position + (self.direction*self.fish_speed)

		#TODO : Rotate angle setting
		

		#moving position_set2
		#obj <- Rotate and turn by axis
		self.direction +=  self.d

		q = self.CalQuaternion(Math3d.Vector3(1, 0, 0), self.direction)

		next_position = pre_position + (self.Nor(self.direction)*self.fish_speed)
	
		#set position to axis point and play and ----

		
		self.Fish_ob_transform.SetPosition(next_position)

		x = q
		y = Math3d.Quaternion.QuaternionToEulerDegreeFloat(x)
		y.x = 0
		z = Math3d.Quaternion.EulerDegreeToQuaternionFloat(y)
		self.Fish_ob_transform.SetRotation(z)

		self.turn_count +=1


	def Check_ground(self, ground_y) :

		if self.is_ground_turn :
			return

		ob_pos = self.Fish_ob_transform.GetPosition()

		for i in ground_y :
			if abs(ob_pos.y - i) < self.ground_check :
				if self.direction.y == 0 :
					if abs(self.direction.x) > abs(self.direction.z) :
						if self.direction.z >= 0 :
							self.turn_direction = self.Nor(Math3d.Vector3(self.direction.x, -self.direction.y, self.direction.z-0.3))
						else :
							self.turn_direction = self.Nor(Math3d.Vector3(self.direction.x, -self.direction.y, self.direction.z+0.3))
					else : 	
						if self.direction.x >= 0 :
							self.turn_direction = self.Nor(Math3d.Vector3(self.direction.x-0.3, -self.direction.y, self.direction.z))
						else :
							self.turn_direction = self.Nor(Math3d.Vector3(self.direction.x+0.3, -self.direction.y, self.direction.z))
				else :
					self.turn_direction = self.Nor(Math3d.Vector3(self.direction.x, -self.direction.y, self.direction.z))

				self.pre_direction = self.direction
				self.d = (self.turn_direction - self.pre_direction)/50
				self.is_wall_turn = False
				self.turn_count = 0
				self.is_ground_turn = True
				self.is_Turn = True


	def Check_Wall(self, wall_pos_axis, label) :

		if self.is_wall_turn :
			return

		ob_pos = self.Fish_ob_transform.GetPosition()

		if label == 'x' :
			for i in wall_pos_axis :
				if abs(ob_pos.x - i) < self.wall_check :
					if self.direction.z == 0 :
						self.turn_direction  = self.Nor(Math3d.Vector3(-self.direction.x, self.direction.y, self.direction.z+0.3))
					else :
						self.turn_direction = self.Nor(Math3d.Vector3(-self.direction.x, self.direction.y, self.direction.z))
					
					self.pre_direction = self.direction
					self.d = (self.turn_direction - self.pre_direction)/70
					
					self.is_wall_turn = True
					self.turn_count = 0
					self.is_ground_turn = False
					self.is_Turn = True
					

		if label == 'z' :
			for i in wall_pos_axis :
				if abs(ob_pos.z - i) < self.wall_check :
					if self.direction.z == 0 :
						self.turn_direction  = self.Nor(Math3d.Vector3(self.direction.x+0.3, self.direction.y, -self.direction.z))
					else :
						self.turn_direction = self.Nor(Math3d.Vector3(self.direction.x, self.direction.y, -self.direction.z))
					
					self.pre_direction = self.direction
					self.d = (self.turn_direction - self.pre_direction)/70
					
					self.is_wall_turn = True
					self.is_ground_turn = False
					self.turn_count = 0
					self.is_Turn = True



	def Check_hand(self, ouclus_tranform, pre_pos):

		hand_pos = ouclus_tranform.GetPosition()
		ob_pos = self.Fish_ob_transform.GetPosition()

		if (hand_pos - ob_pos).Length() > self.is_ob_hand_length :
			return

		if (hand_pos-pre_pos).Length() < self.is_hand_move :
			#self.pre_hand_pos = hand_pos

			return
		
		else :
			var = (hand_pos-pre_pos).Length()

			if self.is_speed_up == False and self.is_speed_down == False:
				self.speed_factor = 0.01/var
				self.is_speed_up = True


			#self.pre_hand_pos = hand_pos
			self.turn_direction = (ob_pos - (hand_pos+pre_pos)/2)
			self.turn_direction = self.Nor(self.turn_direction)
			
			self.pre_direction = self.direction
			self.d = (self.turn_direction - self.pre_direction)/20
			
			self.is_wall_turn = False
			self.is_ground_turn = False
			self.turn_count = 0
			self.is_Turn = True

			return


	def Go_fast (self) :
		#print("fast")
		#print(self.fish_speed)
		self.speed_count +=1

		if self.speed_count > 30 :
			self.speed_count = 0
			self.is_speed_up = False
			self.is_speed_down = True
		#	print("fast_end")

			return

		self.fish_speed += self.speed_factor/self.speed_count


		


	def Go_slow(self) :
		#print("slow")
		#print(self.fish_speed)
		self.speed_count +=1

		if self.fish_speed < 0.06 :
			self.fish_speed = 0.06
			self.speed_count = 0
			self.is_speed_down = False
		#	print("slow_end")

			return

		self.fish_speed -= self.speed_factor/self.speed_count




	def OnDestroy(self):

		return 0

	def OnEnable(self):

		return 0

	def OnDisable(self):

		return 0


	def OnMessage(self, msg, number, Vector4_lparm, Vector4_wparm):

		return 0


	#angry make			
	def Nor(self, v) :
		l = v.Length()

		v = Math3d.Vector3(v.x/l, v.y/l, v.z/l)
		return v 


	def CalQuaternion(self, pre_axis, p) :
		q = None

		angle_cos = Math3d.Vector3.Dot(pre_axis, p)/(pre_axis.Length()*p.Length())
		angle = math.acos(angle_cos)
		
		u = Math3d.Vector3.Cross(pre_axis, p)
		u_len = u.Length()

		if(u_len == 0) :
			if p.x == -pre_axis.x :
				q = Math3d.Quaternion.EulerDegreeToQuaternionFloat(Math3d.Vector3(0, 180, 0))
			else :
				q = Math3d.Quaternion(0,0,0,0)
		else :
			u_ = self.Nor(u)

			temp = math.sin(angle/2)*u_

			q = Math3d.Quaternion(temp.x, temp.y, temp.z, math.cos(angle/2))

		return q


	def MatrixCal(self, Mat, Vec4):
		a=0.0
		m = list()
		Vec = [Vec4.x, Vec4.y, Vec4.z, Vec4.w]


		for i in range(4):
			for j in range(4):
				a+=Mat.m[i][j]*Vec[j]

			m.append(a)
			a = 0.0
		b = Math3d.Vector4(m[0], m[1], m[2], m[3])
		return b


	def check_out(self, ob_transform) :
		ob_pos = ob_transform.GetPosition()

		if random.randrange(1,3)%2 == 0 :
				a = -1
		else :
				a = 1
		
		if random.randrange(1,3)%2 == 0 :
				b = -1
		else :
				b = 1

		if 35 < abs(ob_pos.x) or 35 < abs(ob_pos.z) :

			ob_pos = Math3d.Vector3(0,0,0)
			self.direction = self.Nor(Math3d.Vector3(random.random()*a+a, random.random(), random.random()*b+b))
			self.Fish_ob_transform.SetPosition(ob_pos)


		if 33 < ob_pos.y or ob_pos.y < -11:
			ob_pos = Math3d.Vector3(0,0,0)
			self.direction = self.Nor(Math3d.Vector3(random.random()*a+a, random.random(), random.random()*b+b))
			self.Fish_ob_transform.SetPosition(ob_pos)
			self.is_Turn = False
			self.is_ground_turn = False
			self.is_wall_turn = False
			self.is_ob_turn = False
	

			
				