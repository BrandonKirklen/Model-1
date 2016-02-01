#!/usr/bin/python -tt
import operator
import orbitalRemovalMethod as removal
import dataProcessing
import riskEvaluation as risk


def main():
    # Method Definitons
    IBS = removal.orbitalRemovalMethod("IBS", (3000, 5000), (300, 1000), 1.71)
    robotArmPropellant = removal.orbitalRemovalMethod("Robot Arm -- Propellant", (65, 3800), (750, 900), 5)
    robotArmEDT = removal.orbitalRemovalMethod("Robot Arm -- EDT", (500, 3400), (800, 1400), 1)
    EDDE = removal.orbitalRemovalMethod("EDDE", (2, 50), (800, 1000), 357)
    # Data Processing
    orbitalObjects = dataProcessing.junkList("spaceobjects.csv")
    orbitalObjects.sort(key=operator.attrgetter('weightedRisk'))
    orbitalObjects = risk.normalizeWeightedRisk(orbitalObjects)

    # Risk Analysis
    print 1/141.
    IBSresults = removal.debrisRemoval(IBS, orbitalObjects, 5, True)
    print risk.reductionFactor(IBSresults)
    Propellantresults = removal.debrisRemoval(robotArmPropellant, orbitalObjects, 5, True)
    print risk.reductionFactor(Propellantresults)
    EDTresults = removal.debrisRemoval(robotArmEDT, orbitalObjects, 5, True)
    print risk.reductionFactor(EDTresults)
    EDDEresults = removal.debrisRemoval(EDDE, orbitalObjects, 5, True)
    print risk.reductionFactor(EDDEresults)


if __name__ == '__main__':
    main()
