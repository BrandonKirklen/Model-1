#!/usr/bin/python -tt
import operator
import orbitalRemovalMethod as removal
import dataProcessing
import riskEvaluation as risk
import cost

baseCost = 290000000


def main():
    # Method Definitons
    IBS = removal.orbitalRemovalMethod("IBS", (3000, 5000), (300, 1000), 1.71, baseCost + 20000000)
    robotArmPropellant = removal.orbitalRemovalMethod("Robot Arm -- Propellant", (65, 3800), (750, 900), 5, baseCost + 10000000)
    robotArmEDT = removal.orbitalRemovalMethod("Robot Arm -- EDT", (500, 3400), (800, 1400), 1, baseCost)
    EDDE = removal.orbitalRemovalMethod("EDDE", (2, 50), (800, 1000), 357, baseCost - 30000000)
    # Data Processing
    orbitalObjects = dataProcessing.junkList("spaceobjects.csv")

    ROIlistIBS = []
    ROIlistPropellant = []
    ROIlistEDT = []
    ROIlistEDDE = []

    for i in range(1, 100):
        # Sort List
        orbitalObjects.sort(key=operator.attrgetter('weightedRisk'))
        orbitalObjects = risk.normalizeWeightedRisk(orbitalObjects)

        # Risk Analysis
        IBSresults = removal.debrisRemoval(IBS, orbitalObjects, 5)
        Propellantresults = removal.debrisRemoval(robotArmPropellant, orbitalObjects, 5)
        EDTresults = removal.debrisRemoval(robotArmEDT, orbitalObjects, 5)
        EDDEresults = removal.debrisRemoval(EDDE, orbitalObjects, 5)

        ROIlistIBS.append(cost.ROI(IBSresults, IBS))
        ROIlistPropellant.append(cost.ROI(Propellantresults, robotArmPropellant))
        ROIlistEDT.append(cost.ROI(EDTresults, robotArmEDT))
        ROIlistEDDE.append(cost.ROI(EDDEresults, EDDE))

        for debris in orbitalObjects:
            debris.scramble()
    ROIaverageIBS = sum(ROIlistIBS) / float(len(ROIlistIBS))
    ROIaveragePropellant = sum(ROIlistPropellant) / float(len(ROIlistPropellant))
    ROIaverageEDT = sum(ROIlistEDT) / float(len(ROIlistEDT))
    ROIaverageEDDE = sum(ROIlistEDDE) / float(len(ROIlistEDDE))

    print "ROI Average IBS:         " + str(ROIaverageIBS)
    print "ROI Average Propellant:  " + str(ROIaveragePropellant)
    print "ROI Average EDT:         " + str(ROIaverageEDT)
    print "ROI Average EDDE:        " + str(ROIaverageEDDE)


if __name__ == '__main__':
    main()
