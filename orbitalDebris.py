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
        # risk
        self.risk = risk(self.velocity, self.crossSectionalArea)
        # Mass weighted Colision risk
        self.weightedRisk = self.risk * self.mass


# Used to determine the risk of colision
def risk(velocity, area):
    return velocity * area


# Randomly assigns a mass to an object
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


# Uses object mass to assign an appropriate cross sectional area
def crossSectionalArea(mass):
    if mass <= 65:
        return random.uniform(0.2, 0.7)
    elif mass >= 125 and mass <= 990:
        return random.uniform(1, 3.8)
    elif mass >= 1000 and mass <= 4000:
        return random.triangular(5.3, 11, 8)
    else:
        return 0


# Uses Vis-Viva equation to find approx velocity
def orbitalVelocity(currentDistance):
    gravitationalConstant = (6.67408 * 10**-11) * 1/(1000**3)
    massEarth = 5.972 * pow(10, 24)
    radiusEarth = 6378.1370
    return (math.sqrt(gravitationalConstant * massEarth *
            1 / (currentDistance + radiusEarth)))


def test(got, expected):
    if got == expected:
        prefix = ' OK '
    else:
        prefix = '  X '
    print '%s got: %s expected: %s' % (prefix, repr(got), repr(expected))


def tester():
    print "Orbital Velocity Test:"
    print test(orbitalDebris.orbitalVelocity(384400), 1.009928142899429)
    print test(orbitalDebris.orbitalVelocity(867), 7.41706871529025)
    print

    print "Mass Test"
    print orbitalDebris.mass()
    print

    print "Cross Sectional Area Test"
    print orbitalDebris.crossSectionalArea(60)
    print orbitalDebris.crossSectionalArea(150)
    print orbitalDebris.crossSectionalArea(2000)
