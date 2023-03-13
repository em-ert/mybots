import pyrosim.pyrosim as pyrosim

pyrosim.Start_SDF("boxes.sdf")
width = 1
length = 1
height = 1
x = -2
y = -2
#pyrosim.Send_Cube(name="Box", pos=[0, 0, 0.5], size=[width, length, height])
#pyrosim.Send_Cube(name="Box2", pos=[1, 0, 1.5], size=[width, length, height])

for g in range (5):
    x += 1
    y = -2
    for h in range (5):
        y += 1
        width = 1
        height = 1
        length = 1
        for i in range(10):
            width = width*0.9
            length = length * 0.9
            height = height * 0.9
            pyrosim.Send_Cube(name="Box_"+str(i) , pos=[x, y, .5+i], size=[width, length, height])


pyrosim.End()