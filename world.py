import pybullet as p


class WORLD:
    def __init__(self):
        self.planeId = p.loadURDF("plane.urdf")
        self.objects = p.loadSDF("world.sdf")
        self.numObjects = len(self.objects)

    def Get_Link_Position(self, linkID):
        posAndOrientation = p.getBasePositionAndOrientation(self.objects[linkID])
        position = posAndOrientation[0]
        return position

    def Get_Link_Orientation(self, linkID):
        posAndOrientation = p.getBasePositionAndOrientation(self.objects[linkID])
        orientation = posAndOrientation[1]
        return orientation