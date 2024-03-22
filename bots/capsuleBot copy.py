import math
import pyrosim.pyrosim as pyrosim

class CAPSULE_BOT:
    def __init__(self):
        self.root = "Torso"
        self.joints = []
        self.links = []
        self.Define_Body()

    def Define_Body(self):
        # Upper Joints
        self.joints.append(JOINT(name="Torso_FrontLeg", parent="Torso", child="FrontLeg"))
        self.joints.append(JOINT(name="Torso_BackLeg", parent="Torso", child="BackLeg"))
        self.joints.append(JOINT(name="Torso_LeftLeg", parent="Torso", child="LeftLeg"))
        self.joints.append(JOINT(name="Torso_RightLeg", parent="Torso", child="RightLeg"))

        # Upper Links
        self.links.append("FrontLeg")
        self.links.append("BackLeg")
        self.links.append("LeftLeg")
        self.links.append("RightLeg")

        # Lower Joints
        self.joints.append(JOINT(name="FrontLeg_FrontLower", parent="FrontLeg", child="FrontLower"))
        self.joints.append(JOINT(name="BackLeg_BackLower", parent="BackLeg", child="BackLower"))
        self.joints.append(JOINT(name="LeftLeg_LeftLower", parent="LeftLeg", child="LeftLower"))
        self.joints.append(JOINT(name="RightLeg_RightLower", parent="RightLeg", child="RightLower"))

        # Lower Links
        self.links.append("FrontLower")
        self.links.append("BackLower")
        self.links.append("LeftLower")
        self.links.append("RightLower")

    def Create_Body(self, start_x, start_y, start_z):
        pyrosim.Start_URDF("body.urdf")

        pyrosim.Send_Cube(name="Torso", pos=[start_x, start_y, start_z], size=[1,1,1])

        # Front leg
        pyrosim.Send_Joint(
            name=self.joints[0].name, 
            parent=self.joints[0].parent, 
            child=self.joints[0].child, 
            type="revolute", 
            position=[start_x, start_y+0.5, start_z], 
            jointAxis="1 0 1")
        pyrosim.Send_Capsule(
            name="FrontLeg", 
            pos=[0, 0.5, 0], 
            size=[0.2, 1],
            rpy=[0,(math.pi/2),(math.pi/2)])
        pyrosim.Send_Joint(
            name=self.joints[4].name, 
            parent=self.joints[4].parent, 
            child=self.joints[4].child, 
            type="revolute", 
            position=[0, 1, 0], 
            jointAxis="1 0 1")
        pyrosim.Send_Capsule(
            name="FrontLower", 
            pos=[0, 0, -0.5], 
            size=[0.2, 1])

        # Back leg
        pyrosim.Send_Joint(
            name=self.joints[1].name, 
            parent=self.joints[1].parent, 
            child=self.joints[1].child, 
            type="revolute", 
            position=[start_x, start_y-0.5, start_z], 
            jointAxis="1 0 1")
        pyrosim.Send_Capsule(
            name="BackLeg", 
            pos=[0, -0.5, 0],
            size=[0.2, 1],
            rpy=[0,(math.pi/2),(math.pi/2)])
        pyrosim.Send_Joint(
            name=self.joints[5].name, 
            parent=self.joints[5].parent, 
            child=self.joints[5].child, 
            type="revolute", 
            position=[0, -1, 0], 
            jointAxis="1 0 1")
        pyrosim.Send_Capsule(
            name="BackLower", 
            pos=[0, 0, -0.5], 
            size=[0.2, 1])

        # Left leg
        pyrosim.Send_Joint(
            name=self.joints[2].name, 
            parent=self.joints[2].parent, 
            child=self.joints[2].child, 
            type="revolute",
            position=[start_x-0.5, start_y, start_z], 
            jointAxis="0 1 1")
        pyrosim.Send_Capsule(
            name="LeftLeg", 
            pos=[-0.5, 0, 0], 
            size=[0.2, 1],
            rpy=[0,(math.pi/2),0])
        pyrosim.Send_Joint(
            name=self.joints[6].name, 
            parent=self.joints[6].parent, 
            child=self.joints[6].child, 
            type="revolute", 
            position=[-1, 0, 0], 
            jointAxis="0 1 1")
        pyrosim.Send_Capsule(
            name="LeftLower", 
            pos=[0, 0, -0.5], 
            size=[0.2, 1])

        # Right leg
        pyrosim.Send_Joint(
            name=self.joints[3].name, 
            parent=self.joints[3].parent, 
            child=self.joints[3].child, 
            type="revolute", 
            position=[start_x+0.5, start_y, start_z], 
            jointAxis="0 1 1")
        pyrosim.Send_Capsule(
            name="RightLeg", 
            pos=[0.5, 0, 0], 
            size=[0.2, 1],
            rpy=[0,(math.pi/2),0])
        pyrosim.Send_Joint(
            name=self.joints[7].name, 
            parent=self.joints[7].parent, 
            child=self.joints[7].child, 
            type="revolute", 
            position=[1, 0, 0], 
            jointAxis="0 1 1")
        pyrosim.Send_Capsule(
            name="RightLower", 
            pos=[0, 0, -0.5],
            size=[0.2, 1])
        
        pyrosim.End()

class JOINT:
    def __init__(self, name, parent, child):
        self.name = name
        self.parent = parent
        self.child = child