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
    for h in range (5):
        for i in range(10):
            width_temp = width * (0.9**i)
            length_temp = length * (0.9**i)
            height_temp = height * (0.9**i)
            pyrosim.Send_Cube(name="Box_"+str(i) , pos=[x, y, .5+i], size=[width_temp, length_temp, height_temp])
        y += 1  
    x += 1
    y = -2

pyrosim.End()