#!/usr/bin/python -tt
import operator
import orbitalRemovalMethod as removal
import dataProcessing
import riskEvaluation as risk
import cost

# baseCost = 290000000


def main():
    costIter = iter([10000000, 100000000, 290000000/2, 290000000, 290000000*2, 1000000000])
    # Base ROI Lists
    ROIlistIBS = []
    ROIlistPropellant = []
    ROIlistEDT = []
    ROIlistEDDE = []
    for baseCost in costIter:
        # Method Definitons
        IBS = removal.orbitalRemovalMethod("IBS", (3000, 5000), (300, 1000), 1.71, baseCost + 0.06896551724*baseCost)
        robotArmPropellant = removal.orbitalRemovalMethod("Robot Arm -- Propellant", (65, 3800), (750, 900), 5, baseCost + 0.03448275862*baseCost)
        robotArmEDT = removal.orbitalRemovalMethod("Robot Arm -- EDT", (500, 3400), (800, 1400), 1, baseCost)
        EDDE = removal.orbitalRemovalMethod("EDDE", (2, 50), (800, 1000), 357, baseCost - 0.1034482759*baseCost)
        # Data Processing
        orbitalObjects = dataProcessing.junkList("spaceobjects.csv")

        # Sort List
        orbitalObjects.sort(key=operator.attrgetter('weightedRisk'))
        orbitalObjects = risk.normalizeWeightedRisk(orbitalObjects)
        orbitalObjects.reverse()

        years = 5
        IBSresults = removal.debrisRemoval(IBS, orbitalObjects, years)
        Propellantresults = removal.debrisRemoval(robotArmPropellant, orbitalObjects, years)
        EDTresults = removal.debrisRemoval(robotArmEDT, orbitalObjects, years)
        EDDEresults = removal.debrisRemoval(EDDE, orbitalObjects, years)

        ROIlistIBS.append(cost.ROI(IBSresults, IBS))
        ROIlistPropellant.append(cost.ROI(Propellantresults, robotArmPropellant))
        ROIlistEDT.append(cost.ROI(EDTresults, robotArmEDT))
        ROIlistEDDE.append(cost.ROI(EDDEresults, EDDE))

    print ROIlistIBS
    print ROIlistPropellant
    print ROIlistEDT
    print ROIlistEDDE

    # ROIaverageIBS = np.mean(ROIlistIBS)
    # ROIaveragePropellant = np.mean(ROIlistPropellant)
    # ROIaverageEDT = np.mean(ROIlistEDT)
    # ROIaverageEDDE = np.mean(ROIlistEDDE)

    # MissionRiskIBS = np.mean(MissionRisklistIBS)
    # MissionRiskPropellant = np.mean(MissionRisklistPropellant)
    # MissionRiskEDT = np.mean(MissionRisklistEDT)
    # MissionRiskEDDE = np.mean(MissionRisklistEDDE)

    # print "ROI Average IBS:         " + str(ROIaverageIBS) + " Mission Risk: " + str(MissionRiskIBS)
    # print "ROI Average Propellant:  " + str(ROIaveragePropellant) + " Mission Risk: " + str(MissionRiskPropellant)
    # print "ROI Average EDT:         " + str(ROIaverageEDT) + " Mission Risk: " + str(MissionRiskEDT)
    # print "ROI Average EDDE:        " + str(ROIaverageEDDE) + " Mission Risk: " + str(MissionRiskEDDE)


if __name__ == '__main__':
    main()
