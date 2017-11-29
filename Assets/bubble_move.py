import math
import random

class bubble_move(Actor.Actor):
	def __init__(self):
		#bubble setting
		self.Bubble = Container(0)
		self.bubble_child = list()

		#set_bubble position
		self.start_scale = Math3d.Vector3()
		self.start_position = Math3d.Vector3()

		#count
		self.bubble_count = 0
		self.bubble_make_count = int()
		self.bubble_life = int()
		self.is_Bubble = True

		#child_set
		self.child_life_count = list()
		self.child_life = int()
		

		return

	def OnCreate(self, this):
		self.Bubble = Container(this)
		self.start_position = self.Bubble.FindComponentByType("TransformGroup").GetPosition()


	def Update(self):
		self.bubble_count += 1

		#make bubble
		if self.bubble_count%self.bubble_make_count == 0 :
			temp = self.Bubble.AddNewChild()
			temp.AddNewComponent("TransformGroup").SetPosition(self.start_position)

			a = self.Bubble.FindComponentByType("Cube").PropRigidMesh.GetMaterial()
			temp.AddNewComponent("Cube").PropRigidMesh.SetMaterial(a)

			#print("make _ bubble")
			
			#TODO : set child charateristic
			
			#chid_life setting
			self.child_life_count.append(0)
			

		#chile_life_check
		j = len(self.child_life_count)
		i = 0
		
		#print(self.child_life_count.__str__())

		if j>0 :

			while i<j :
				self.child_life_count[i] +=1

				if self.child_life_count[i]  > self.child_life : 
					self.Bubble.DeleteChild(i)
					self.child_life_count.pop(i)
					j -= 1

			#		print("delete")

				i +=1





		#tip_move
		for i in range(self.Bubble.GetChildrenCount()) :
			bubble_tip = self.Bubble.GetChild(i)
			self.Move(bubble_tip.FindComponentByType("TransformGroup"))

		#bubble_life_check
		if self.bubble_count > self.bubble_life :
			
			return

				
	#Move_tip
	def Move(self, transform) :
		pre_pos = transform.GetPosition()

		#TODO : Moving Algorithm please write

		
		a = 1 if (random.randrange(1, 3)%2 ==1) else -1
		b = 1 if (random.randrange(1, 3)%2 ==1) else -1

		x = pre_pos.x + (random.random()/20*a)
		y = pre_pos.y + (random.random()/20+0.02)
		z = pre_pos.z + (random.random()/20*b)

		pos = Math3d.Vector3(x, y, z)

		transform.SetPosition(pos)


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