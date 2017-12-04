import math

class collide_coral(Actor.Actor):
	def __init__(self) :
		self.coral = Container(0)
		self.coral_0 = Container(0)
		self.coral_1 = Container(0)
		self.coral_2 = Container(0)
		self.coral_3 = Container(0)
		self.coral_4 = Container(0)
		self.coral_5 = Container(0)
		self.coral_6 = Container(0)
		self.coral_7 = Container(0)

		self.coral_tansform_list = list()

		self.right_hand = Container(0)
		self.left_hand = Container(0)

		#flag
		self.is_touch = False
		self.is_first_touch = True
		self.touch_ob = None
		self.is_reback = False
		self.re_touch_ob = None
		self.is_coral_up = False
		self.is_coral_down = False
		self.coral_list_up = []
		self.coral_list_down = []

		#distance flag
		self.effect_distance = 0.5
		self.local_pos_var = 0.5
		self.local_scale=0.5


		#for hand and rotate
		self.pre_hand = Math3d.Vector3()
		self.coral_num = None
		self.last_p = Math3d.Quaternion()
		self.last_up_p = [ None, None, None, None, None, None, None, None ]
		self.last_down_p = [ None, None, None, None, None, None, None, None ]



	def OnCreate(self, this) :
		self.coral = Container(this)
		self.coral_tansform = self.coral.FindComponentByType("TransformGroup")
		self.coral_pos = self.coral_tansform.GetPosition()

		self.coral_0_tansform = self.coral.GetChild(0).FindComponentByType("TransformGroup")
		self.coral_1_tansform = self.coral.GetChild(1).FindComponentByType("TransformGroup")
		self.coral_2_tansform = self.coral.GetChild(2).FindComponentByType("TransformGroup")
		self.coral_3_tansform = self.coral.GetChild(3).FindComponentByType("TransformGroup")
		self.coral_4_tansform = self.coral.GetChild(4).FindComponentByType("TransformGroup")
		self.coral_5_tansform = self.coral.GetChild(5).FindComponentByType("TransformGroup")
		self.coral_6_tansform = self.coral.GetChild(6).FindComponentByType("TransformGroup")
		self.coral_7_tansform = self.coral.GetChild(7).FindComponentByType("TransformGroup")

		self.coral_tansform_list.append(self.coral_0_tansform)
		self.coral_tansform_list.append(self.coral_1_tansform)
		self.coral_tansform_list.append(self.coral_2_tansform)
		self.coral_tansform_list.append(self.coral_3_tansform)
		self.coral_tansform_list.append(self.coral_4_tansform)
		self.coral_tansform_list.append(self.coral_5_tansform)
		self.coral_tansform_list.append(self.coral_6_tansform)
		self.coral_tansform_list.append(self.coral_7_tansform)

		for i in range(len(self.coral_tansform_list)) :
			self.coral_tansform_list[i].SetLocalPosition(Math3d.Vector3(0, self.local_pos_var*i, 0))
			self.coral_tansform_list[i].SetScale(Math3d.Vector3(self.local_scale, self.local_scale, self.local_scale))

		self.right_hand_transform = self.right_hand.FindComponentByType("TransformGroup")
		self.left_hand_transform = self.left_hand.FindComponentByType("TransformGroup")

		
	def Update(self) :


		if self.is_reback :
			#print("re_back_worl")
			temp = (Math3d.Vector3(0, self.coral_num*self.local_pos_var, 0))

			d = (temp - self.last_p)/100

			self.re_touch_ob.SetLocalPosition(self.Nor(self.re_touch_ob.GetLocalPosition()+d)*self.coral_num*self.local_pos_var)

			#print(self.re_touch_ob.GetLocalPosition().__str__())


			temp_1 = [ None, None, None, None, None, None, None, None ]
			if self.is_coral_up :
				for i in range(len(self.coral_list_up)) :
					temp_1[i] = (Math3d.Vector3(0, (self.coral_num+1+i)*self.local_pos_var, 0))
					d = (temp_1[i] - self.last_up_p[i])/100
					self.coral_list_up[i].SetLocalPosition(self.Nor(self.coral_list_up[i].GetLocalPosition()+d)*(self.coral_num+i+1)*self.local_pos_var)

			temp_2 = [ None, None, None, None, None, None, None, None ]
			if self.is_coral_down :
				for i in range(len(self.coral_list_down)) :
					if i == 0 :
						continue

					temp_2[i] = (Math3d.Vector3(0, i*self.local_pos_var, 0))
					d = (temp_2[i] - self.last_down_p[i])/100

					
					self.coral_list_down[i].SetLocalPosition(self.Nor(self.coral_list_down[i].GetLocalPosition()+d)*i*self.local_pos_var)
			
			print((self.re_touch_ob.GetLocalPosition() - temp).Length())
			if (self.re_touch_ob.GetLocalPosition() - temp).Length() < 0.01 :
				print("re_back_ending")
				self.re_touch_ob.SetLocalPosition(temp)

				if self.is_coral_up :
					for i in range(len(self.coral_list_up)) :
						self.coral_list_up[i].SetLocalPosition(temp_1[i])

				if self.is_coral_down :
					for i in range(len(self.coral_list_down)) :
						self.coral_list_down[i].SetLocalPosition(temp_2[i])


				self.is_reback = False
				self.is_touch = False
				self.re_touch_ob = None
				self.coral_num = None
				self.is_first_touch = True

			return

		for i in range(0, len(self.coral_tansform_list)) :
			temp = self.right_hand_transform.GetPosition()
			if (self.coral_tansform_list[i].GetPosition() - temp).Length() < self.effect_distance :
				#print("why??")
				if self.is_first_touch == True :
					#print("why??2")
					self.pre_hand = temp +Math3d.Vector3(0.01, 0, 0)
					self.is_first_touch = False
					self.is_touch = True
					self.is_reback = False

				self.touch_ob = self.coral_tansform_list[i]
				self.coral_num = i
				break

			else :
				self.touch_ob = None
					
		

		if self.touch_ob == None :
			#self.coral_tansform = 0

			self.Check_out()
			return


		#for head
		q = self.CalQuaternion(self.Nor(self.pre_hand - self.coral_pos), self.Nor(self.right_hand_transform.GetPosition()-self.coral_pos)) 
		p = Math3d.Quaternion(0, self.coral_num*self.local_pos_var, 0,  0)
		p_ = self.Q(q ,self.Q(p, Math3d.Quaternion(-q.x, -q.y, -q.z, q.w)))
		self.last_p = Math3d.Vector3(p_.x, p_.y, p_.z)
		#print("wor")
		
		self.touch_ob.SetLocalPosition(Math3d.Vector3(p_.x, p_.y, p_.z))
		self.re_touch_ob = self.touch_ob

		#for other`s
		self.coral_list_up = self.coral_tansform_list[self.coral_num+1:]
		self.coral_list_down = self.coral_tansform_list[0:self.coral_num]

		if self.coral_list_up == [] :
			self.is_coral_up = False
		else :
			self.is_coral_up = True

		if self.coral_list_down == [] :
			self.is_coral_down = False
		else :
			self.is_coral_down = True

		

		if self.is_coral_up :
			for i in range(0, len(self.coral_list_up)) :

				tranform_up = Math3d.Matrix(1,0,0,(self.coral_num+i)*self.local_pos_var,  0,1,0,0,  0,0,1,0,  0,0,0,1)
				re_transform_up = Math3d.Matrix(1,0,0,(-self.coral_num-i)*self.local_pos_var,  0,1,0,0,  0,0,1,0,  0,0,0,1)

				p = Math3d.Quaternion(0, (self.coral_num+i+1)*self.local_pos_var, 0, 0)

				q_ = self.CalQuaternion(self.Nor(self.pre_hand - self.coral_pos), self.Nor(((i+1)*(self.right_hand_transform.GetPosition()-self.coral_pos) + (len(self.coral_list_up)-i)*(self.pre_hand - self.coral_pos))/(len(self.coral_list_up)+1)))

				x = self.MatrixCal( tranform_up ,p)
				y = self.Q(q_, self.Q(x, Math3d.Quaternion(-q_.x, -q_.y, -q_.z, q_.w)))
				z = self.MatrixCal( re_transform_up, y)

				p__ = self.Q(q, self.Q(z ,Math3d.Quaternion(-q.x, -q.y, -q.z, q.w)))

				self.coral_list_up[i].SetLocalPosition(Math3d.Vector3(p__.x, p__.y, p__.z))
				self.last_up_p[i] = self.coral_list_up[i].GetLocalPosition()




		#have _ to _change
		if self.is_coral_down :
			for i in range(0, len(self.coral_list_down)) :

				if i == 0 :
					continue

				tranform_down = Math3d.Matrix(1,0,0,(i-1)*self.local_pos_var,  0,1,0,0,  0,0,1,0,  0,0,0,1)
				re_transform_down = Math3d.Matrix(1,0,0,(-i+1)*self.local_pos_var,  0,1,0,0,  0,0,1,0,  0,0,0,1)

				p = Math3d.Quaternion(0, i*self.local_pos_var, 0, 0)

				q_ = self.CalQuaternion(self.Nor(self.right_hand_transform.GetPosition() - self.coral_pos), self.Nor((i*(self.right_hand_transform.GetPosition() - self.coral_pos)+(self.coral_num-i)*(self.pre_hand - self.coral_pos))/self.coral_num))

				x = self.MatrixCal( tranform_down ,p)
				y = self.Q(q_, self.Q(x, Math3d.Quaternion(-q_.x, -q_.y, -q_.z, q_.w)))
				z = self.MatrixCal( re_transform_down, y)

				p_ = self.Q(q, self.Q(z ,Math3d.Quaternion(-q.x, -q.y, -q.z, q.w)))
				self.coral_list_down[i].SetLocalPosition(Math3d.Vector3(p_.x, p_.y, p_.z))
				self.last_down_p[i] = self.coral_list_down[i].GetLocalPosition()

		#if self.is_coral_down :
		#	for i in range(0, len(coral_list_down)) :
		#		p = Math3d.Quaternion(0, (self.coral_num-1), 0, 0)
		#		q_ = 


			



			
	def Check_out(self) :
		
		if self.is_touch :
			#print("Check_out_work_2")
			self.is_touch = False
			self.is_reback = True



	def CalQuaternion(self, pre_axis, p) :
		q = None

		angle_cos = Math3d.Vector3.Dot(pre_axis, p)/(pre_axis.Length()*p.Length())
		print(angle_cos)
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

	def Nor(self, v) :
		l = v.Length()

		v = Math3d.Vector3(v.x/l, v.y/l, v.z/l)
		return v 

	def Q(self, p, q) :

		p_ = Math3d.Quaternion(p.x*q.w+p.y*q.z-p.z*q.y+p.w*q.x, -p.x*q.z+p.y*q.w+p.z*q.x+p.w*q.y, p.x*q.y-p.y*q.x+p.z*q.w+p.w*q.z, -p.x*q.x-p.y*q.y-p.z*q.z+p.w*q.w)
		return p_

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


