import math

class Ocul(Actor.Actor) :
	def __init__(self) :
		self.head = Container(0)
		self.right_hand = Container(0)
		self.left_hand = Container(0)

		self.tick = 0


		#for editor
		self.is_ocul = False
		self.is_hand_move = False
		self.hand_move_count = 0
		self._time = 0


	def OnCreate(self, this) :
		

		#set transform
		self.head_transform = self.head.FindComponentByType("TransformGroup")
		self.right_hand_transform = self.right_hand.FindComponentByType("TransformGroup")
		self.left_hand_transform = self.left_hand.FindComponentByType("TransformGroup")
		self.head_camera = self.head.FindComponentByType("Camera")

		#for editor
		self.World = GetWorldContainer().FindComponentByType("World")
		self.pre_pos = self.right_hand_transform.GetPosition()


	def Update(self) :
		self._time += self.World.GetFrameElapseTime()*5

		if self.is_ocul == False :
			if self.is_hand_move :
				self.right_hand_transform.SetLocalPosition(self.pre_pos + Math3d.Vector3(0, 0, math.sin(self._time)))

				self.hand_move_count +=1

				if self.hand_move_count > 200 :
					self.hand_move_count = 0
					self.is_hand_move = False


			return


		self.tick +=1

		if(self.tick <= 250) :
			return

		cam_Position = self.head_transform.GetPosition()

		hmd_status = DeviceInput.GetHMDStatus("Oculus")
		hed_rotation = DeviceInput.GetHMDOrientation("Oculus", False)
		hmd_position = DeviceInput.GetHMDPosition("Oculus", False)
		input_time = DeviceInput.GetInputTime("Oculus")
		button_info = DeviceInput.GetInputInfo("Oculus", 0)
		touch_info = DeviceInput.GetInputInfo("Oculus", 1)
		controller_type = DeviceInput.GetControllerType("Oculus")

		self.left_hand_pos = None
		self.right_hand_pos = None

		for i in range(0, 2) :
			hand = i+1

			handStatus = DeviceInput.GetHandStatus("Oculus", hand)

			if handStatus > 0 :
				hand_rotation = DeviceInput.GetHandOrientation("Oculus", hand)
				hand_position = DeviceInput.GetHandPosition("Oculus", hand)
				hand_trigger = DeviceInput.GetTrigger("Oculus", hand, False, 0)
				index_trigger = DeviceInput.GetTrigger("Oculus", hand, False, 1)
				t_stick = DeviceInput.GetThumbStick("Oculus", hand, False)

				if i == 0 :
					left_hand_pos = hand_position
				else :
					right_hand_pos = hand_position


				nPos = cam_Position + hand_position
				nRot = hand_rotation

				if hand == 1 :
					if self.left_hand_transform != None :
						self.left_hand_transform.SetPosition(nPos)
						self.left_hand_transform.SetRotation(nRot)
				elif hand == 2 :
					if self.right_hand_transform != None :
						self.right_hand_transform.SetPosition(nPos)
						self.right_hand_transform.SetRotation(nRot)



				# for button
				btnYCheck = buttonInfo & DeviceInput.ovrButton_Y
				btnXCheck = buttonInfo & DeviceInput.ovrButton_X
				btnBCheck = buttonInfo & DeviceInput.ovrButton_B
				btnACheck = buttonInfo & DeviceInput.ovrButton_A

				if btnYCheck > 0:
					DeviceInput.SetVibration("Oculus", 1, 0.5, 0.5)

				if btnXCheck > 0:
					DeviceInput.SetVibration("Oculus", 1, 0, 0)

				if btnBCheck > 0:
					DeviceInput.SetVibration("Oculus", 2, 0.5, 0.5)
                
				if btnACheck > 0:
					DeviceInput.SetVibration("Oculus", 2, 0, 0)

		#i don`t know why it is
		hLength = (right_hand_pos - left_hand_pos).Length()

	def OnMessage(self, msg, number, Vector4_lparm, Vector4_wparam):
		
		if msg == "KeyDown" and number == 37 :
			self.head_transform.Rotate(-1,0,0)

		elif msg == "KeyDown" and number == 39 :
			self.head_transform.Rotate(1,0,0)

		elif msg == "KeyDown" and number == 38 :
			self.head_transform.Rotate(0,1,0)

		elif msg == "KeyDown" and number == 40 :
			self.head_transform.Rotate(0,-1,0)

		elif msg == "KeyDown" and number == 32 :
			self.is_hand_move = True

		elif msg == "KeyDown" and number == 68 :
			self.right_hand_transform.SetPosition(self.right_hand_transform.GetPosition()+Math3d.Vector3(0.05, 0, 0))

		elif msg == "KeyDown" and number == 65 :
			self.right_hand_transform.SetPosition(self.right_hand_transform.GetPosition()+Math3d.Vector3(-0.05, 0, 0))

		elif msg == "KeyDown" and number == 87 :
			self.right_hand_transform.SetPosition(self.right_hand_transform.GetPosition()+Math3d.Vector3(0, 0, 0.05))

		elif msg == "KeyDown" and number == 83 :
			self.right_hand_transform.SetPosition(self.right_hand_transform.GetPosition()+Math3d.Vector3(0, 0, -0.05))
		
		elif msg == "KeyDown" and number == 71 :
			self.head_transform.SetPosition(self.head_transform.GetPosition()+Math3d.Vector3(0.05, 0, 0))
		
		elif msg == "KeyDown" and number == 84 :
			self.head_transform.SetPosition(self.head_transform.GetPosition()+Math3d.Vector3(-0.05, 0, 0))

		elif msg == "KeyDown" and number == 72 :
			self.head_transform.SetPosition(self.head_transform.GetPosition()+Math3d.Vector3(0, 0, 0.05))

		elif msg == "KeyDown" and number == 70 :
			self.head_transform.SetPosition(self.head_transform.GetPosition()+Math3d.Vector3(0, 0, -0.05))




			