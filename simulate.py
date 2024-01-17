import pybullet as p
import time

# Create a physicsClient object and draw the results to a GUI
physicsClient = p.connect(p.GUI)
p.configureDebugVisualizer(p.COV_ENABLE_GUI,0)

for i in range(1000):
    # Step the physics simulation then sleep for 1/60th of a second
    p.stepSimulation()
    time.sleep(0.00166)
    # Print the value of the for loop to the console
    print (i)

# Disconnect
p.disconnect()
