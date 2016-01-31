#!/usr/bin/python -tt
import math
import copy
import operator
import orbitalDebris
import orbitalRemovalMethod as removal
import dataProcessing


# Uses Vis-Viva equation to find approx velocity
def orbitalVelocity(currentDistance):
    gravitationalConstant = (6.67408 * 10**-11) * 1/(1000**3)
    massEarth = 5.972 * pow(10, 24)
    radiusEarth = 6378.1370
    return (math.sqrt(gravitationalConstant * massEarth *
            1 / (currentDistance + radiusEarth)))


# Finds the total risk for a list of orbital objects
def sumOfRisk(orbitalObjects):
    risk = 0
    for debris in orbitalObjects:
        risk += debris.weightedRisk
    return risk


def normalizeWeightedRisk(orbitalObjects):
    totalWeight = 0
    for debris in orbitalObjects:
        totalWeight += debris.weightedRisk
    for debris in orbitalObjects:
        debris.weightedRisk = debris.weightedRisk / totalWeight
    return orbitalObjects


# Likelyhood of crash for given mission
def missionRisk(orbitalObjects):
    probabilityOfCrash = .5
    return (sumOfRisk(orbitalObjects) * probabilityOfCrash)


def test(got, expected):
    if got == expected:
        prefix = ' OK '
    else:
        prefix = '  X '
    print '%s got: %s expected: %s' % (prefix, repr(got), repr(expected))


def tester():
    print "Orbital Velocity Test:"
    print test(orbitalVelocity(384400), 1.009928142899429)
    print test(orbitalVelocity(867), 7.41706871529025)
    print

    print "Mass Test"
    print orbitalDebris.mass()
    print

    print "Cross Sectional Area Test"
    print orbitalDebris.crossSectionalArea(60)
    print orbitalDebris.crossSectionalArea(150)
    print orbitalDebris.crossSectionalArea(2000)


def main():
    # Method Definitons
    IBS = removal.orbitalRemovalMethod("IBS", (3000, 5000), (300, 1000), 1.71)
    robotArmPropellant = removal.orbitalRemovalMethod("Robot Arm -- Propellant", (65, 3800), (750, 900), 5)
    robotArmEDT = removal.orbitalRemovalMethod("Robot Arm -- EDT", (500, 3400), (800, 1400), 1)
    EDDE = removal.orbitalRemovalMethod("EDDE", (2, 50), (800, 1000), 357)
    # Data Processing
    orbitalObjects = dataProcessing.junkList("spaceobjects.csv")
    orbitalObjects.sort(key=operator.attrgetter('weightedRisk'))
    orbitalObjects = normalizeWeightedRisk(orbitalObjects)

    IBSresults = removal.debrisRemoval(IBS, orbitalObjects, 5, True)
    print missionRisk(IBSresults)
    Propellantresults = removal.debrisRemoval(robotArmPropellant, orbitalObjects, 5, True)
    print missionRisk(Propellantresults)
    EDTresults = removal.debrisRemoval(robotArmEDT, orbitalObjects, 5, True)
    print missionRisk(EDTresults)
    EDDEresults = removal.debrisRemoval(EDDE, orbitalObjects, 5, True)
    print missionRisk(EDDEresults)
    # for debris in orbitalObjects:
    #     print debris.altitude


if __name__ == '__main__':
    main()
