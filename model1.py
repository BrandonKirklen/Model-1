#!/usr/bin/python -tt
import math
import random


class orbitalDebris(object):
    def __init__(self, ID, name, period=None, inclination=None, apogee=None,
                 perigee=None):
        # Information from CSV file
        self.ID = str(ID)
        self.name = str(name)
        self.period = float(period)
        self.inclination = float(inclination)
        self.apogee = float(apogee)
        self.perigee = float(perigee)
        # Calculated Values
        radiusEarth = 6378.1370
        self.altitude = (apogee + perigee) / 2
        # radius is height above center of earth gravity
        self.radius = self.altitude + radiusEarth
        # Uses the period to calculate the velocity
        self.velocity = (((1440/self.period) * 2 * math.pi * self.radius) /
                         (24*60*60))
        # Randomly Choses a mass
        self.mass = mass()
        # Uses that mass to pick a cross sectional area that matches
        self.crossSectionalArea = crossSectionalArea(self.mass)
        # Probability
        self.probability = probability(self.velocity, self.crossSectionalArea)
        # Mass weighted Colision Probability
        self.weightedProbability = self.probability * self.mass


class orbitalRemovalMethod(object):
    def __init__(self, name, massLimit,
                 altitudeLimit, removedPerYear, cost=0):
        self.name = name
        self.massLimit = massLimit
        self.altitudeLimit = altitudeLimit
        self.removedPerYear = removedPerYear
        self.cost = cost

    def withinLimits(self, mass, altitude):
        withinAltitude = (altitude >= self.altitudeLimit[0] and
                          altitude <= self.altitudeLimit[1])
        withinMass = (mass >= self.massLimit[0] and
                      mass <= self.massLimit[1])
        return (withinAltitude and withinMass)


def orbitalVelocity(currentDistance):
    gravitationalConstant = (6.67408 * 10**-11) * 1/(1000**3)
    massEarth = 5.972 * pow(10, 24)
    radiusEarth = 6378.1370
    return (math.sqrt(gravitationalConstant * massEarth *
            1 / (currentDistance + radiusEarth)))


def mass():
    regime = random.randint(1, 3)
    if regime == 1:
        return random.uniform(1, 65)
    elif regime == 2:
        return random.uniform(125, 990)
    elif regime == 3:
        return random.uniform(1000, 4000)
    else:
        return 0


def crossSectionalArea(mass):
    if mass <= 65:
        return random.uniform(0.2, 0.7)
    elif mass >= 125 and mass <= 990:
        return random.uniform(1, 3.8)
    elif mass >= 1000 and mass <= 4000:
        return random.triangular(5.3, 11, 8)
    else:
        return 0


def probability(velocity, area):
    return velocity * area


def junkList(fileName):
    orbitalObjects = []
    import csv                      # imports the csv module
    f = open(fileName, 'rU')        # opens the csv file
    try:
        reader = csv.reader(f, dialect=csv.excel_tab, delimiter=',')
        parsed = ((row[0], row[1], float(row[2]), float(row[3]), int(row[4]),
                   int(row[5])) for row in reader)
        for row in parsed:          # iterates the rows of the file in orders
            if "DEB" not in row[1]:
                orbitalObjects.append(orbitalDebris(row[0], row[1], row[2],
                                                    row[3], row[4], row[5]))
    finally:
        f.close()      # closing
    return orbitalObjects


def normalizeWeightedProbability(orbitalObjects):
    totalWeight = 0
    for debris in orbitalObjects:
        totalWeight += debris.weightedProbability
    for debris in orbitalObjects:
        debris.weightedProbability = debris.weightedProbability / totalWeight
    return orbitalObjects


def debrisRemoval(method, orbitalObjects, numberOfYears):
    objectsRemoved = 0
    totalObjectsRemoved = method.removedPerYear * numberOfYears
    for debris in orbitalObjects:
        if method.withinLimits(debris.mass, debris.altitude) and objectsRemoved < totalObjectsRemoved:
            orbitalObjects.remove(debris)
            objectsRemoved += 1
    return orbitalObjects


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
    print mass()
    print

    print "Cross Sectional Area Test"
    print crossSectionalArea(60)
    print crossSectionalArea(150)
    print crossSectionalArea(2000)


def main():
    # tester()
    # Method Definitons
    IBS = orbitalRemovalMethod("IBS", (3000, 5000), (300, 1000), 1.71)
    robotArmPropellant = orbitalRemovalMethod("Robot Arm -- Propellant", (65, 3800), (750, 900), 5)
    robotArmEDT = orbitalRemovalMethod("Robot Arm -- EDT", (500, 3400), (800, 1400), 1)
    EDDE = orbitalRemovalMethod("EDDE", (2, 50), (800, 1000), 357)
    orbitalObjects = junkList("spaceobjects.csv")
    import operator
    orbitalObjects.sort(key=operator.attrgetter('weightedProbability'))
    orbitalObjects = normalizeWeightedProbability(orbitalObjects)
    # for debris in orbitalObjects:
    #     print "Mass: " + str(debris.mass)
    print len(orbitalObjects)
    debrisRemoval(EDDE, orbitalObjects, 5)
    print len(orbitalObjects)
    # for debris in orbitalObjects:
    #     print "Mass: " + str(debris.mass)

if __name__ == '__main__':
    main()
