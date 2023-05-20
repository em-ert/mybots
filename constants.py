import numpy

simSteps = 1000

BackLeg_Amplitude = (numpy.pi / 4)
BackLeg_Frequency = 6
BackLeg_PhaseOffset = (numpy.pi / 4)
BackLeg_TargetAngles = numpy.linspace(0, 2 * numpy.pi, simSteps)
BackLeg_TargetAngles = BackLeg_Amplitude * numpy.sin(BackLeg_Frequency * BackLeg_TargetAngles + BackLeg_PhaseOffset)

FrontLeg_Amplitude = (numpy.pi / 4)
FrontLeg_Frequency = 10
FrontLeg_PhaseOffset = 0
FrontLeg_TargetAngles = numpy.linspace(0, 2 * numpy.pi, simSteps)
FrontLeg_TargetAngles = FrontLeg_Amplitude * numpy.sin(FrontLeg_Frequency * FrontLeg_TargetAngles + FrontLeg_PhaseOffset)