
class orbitalRemovalMethod(object):
    # This class holds a method of orbital removal
    def __init__(self, name, massLimit,
                 altitudeLimit, removedPerYear, cost=0):
        self.name = name
        self.massLimit = massLimit
        self.altitudeLimit = altitudeLimit
        self.removedPerYear = removedPerYear
        self.cost = cost

    # this function returns a bool that says if this method can remove an object
    # given the mass and altitude

    def withinLimits(self, mass, altitude):
        withinAltitude = (altitude >= self.altitudeLimit[0] and
                          altitude <= self.altitudeLimit[1])
        withinMass = (mass >= self.massLimit[0] and
                      mass <= self.massLimit[1])
        return (withinAltitude and withinMass)
