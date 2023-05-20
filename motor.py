class MOTOR:
    def __init__(self, jointName):
        self.jointName = jointName
        self.values = numpy.zeros(c.simSteps)
        Prepare_To_Act()

    def Prepare_To_Act(self):
        self.amplitude = c.BackLeg_Amplitude
        self.frequency = c.BackLeg_Frequency
        self.offset = c.BackLeg_PhaseOffset
        self.motorValuespyrosim.Set_Motor_For_Joint(
            bodyIndex=robotId,
            jointName=b'Torso_BackLeg',
            controlMode=p.POSITION_CONTROL,
            targetPosition=c.BackLeg_TargetAngles[i],
            maxForce=8)
        pyrosim.Set_Motor_For_Joint(
            bodyIndex=robotId,
            jointName=b'Torso_FrontLeg',
            controlMode=p.POSITION_CONTROL,
            targetPosition=c.FrontLeg_TargetAngles[i],
            maxForce=8)