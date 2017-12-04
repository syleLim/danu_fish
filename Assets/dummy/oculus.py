class oculus(Actor.Actor):
        def __init__(self):
		self.head = Container(0)
		self.rightHand = Container(0)
		self.leftHand = Container(0)

		self.tick = 0

		#for_bubble
		self.left_pre_pos = Math3d.Vector3()
		self.right_pre_pos = Math3d.Vector3()

		self.bubble_make_len = float()
		

	def OnCreate(self, this):
		#set transform
		self.head_transform = self.Head.FindComponentByType("TransformGroup")
		self.rightHand_transform = self.rightHand.FindComponentByType("TransformGroup")
		self.leftHand_transform = self.leftHand.FindComponentByType("TransformGroup")

		#set up camera
		self.head_camera = self.Head.FindComponentByType("Camera")

	def Update(self):
		#head setting
		hmd_status = DeviceInput.GetHMDStatus("Oculus")
		hmd_rot = DeviceInput.GetHMDOrientation("Oculus", False)
		hmd_pos = DeviceInput.GetHMDPosition("Oculus", False)
		input_time = DeviceInput.GetInputTime("Oculus")
                button_info = DeviceInput.GetInputInfo("Oculus", 0)
                touch_info = DeviceInput.GetInputInfo("Oculus", 1)
                controller_type = DeviceInput.GetControllerType("Oculus")

                #hand setting
                self.left_pos = None
                self.right_pos = None

                #using with hand
                cam_position = head_transform.GetPosition()


                # 0 = left 1 = right
                for i in range(0, 2):
                        hand = i+1

                        hand_status = DeviceInput.GetHandStatus("Oculus", hand)

                        if(hand_status > 0):
                                hand_rot = DeviceInput.GetHandOrientation("Oculus", hand)
                                hand_pos = DeviceInput.GetHandPosition("Oculus", hand)

        		      #I don`t konw what they are below
                        hand_trigger = DeviceInput.GetTrigger("Oculus", hand, False, 0)
                        index_trigger = DeviceInput.GetTrigger("Oculus", hand, False, 1)
                        t_stick = DeviceInput.GetThumbStick("Oculus", hand, False);

                        if i == 0:
                	left_pos = hand_pos
                	print("Left : "+str(hand_pos))
                else :
                	right_pos = hand_pos
                	print("Right : "str(hand_pos))

                #Maybe hand position is based on cam_position
                n_pos = cam_position + hand_pos
                n_rot = hand_rot

                if hand == 1:
                	if self.leftHand_transform != None:
                		self.leftHand_transform.PropTransform.SetPosition(n_pos)
                		self.leftHand_transform.PropTransform.SetRotation(n_rot)
                elif hand == 2:
                	if self.rightHand_transform !=None:
                		self.rightHand_transform.PropTransform.SetPosition(n_pos)
                		self.rightHand_transform.PropTransform.SetPosition(n_rot)



                #make bubble check
                if hand == 1:
                	if (n_pos - self.left_pre_pos).Length() > self.bubble_make_len :
                		#TODO : Create Object( (n_pos+left_pre_pos)/2 -> bubble ) # or Move Position Bubble
                	left_pre_pos = n_pos
                
                elif hand ==2:
                	if (n_pos - self.right_pre_pos).Length() > self.bubble_make_len :
                		#TODO : Create Object( (n_pos+right_pre_pos)/2 -> bubble ) # or Move Position Bubble
                	right_pre_pos = n_pos

                

        







