
class orbitalRemovalMethod(object):
    # This class holds a method of orbital removal
    def __init__(self, name, massLimit,
                 altitudeLimit, removedPerYear, cost=None):
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


def debrisRemoval(method, objects, numberOfYears, printOutput=False, duplicateObjects=True):
    import copy
    if duplicateObjects:
        objects = copy.deepcopy(objects)
    if printOutput:
        print
        print "Removal Method: " + method.name
        print "Objects in Orbit Before: " + str(len(objects))
    objectsRemoved = 0
    totalObjectsRemoved = method.removedPerYear * numberOfYears
    for debris in objects:
        if (method.withinLimits(debris.mass, debris.altitude) and
           objectsRemoved < totalObjectsRemoved):
            objects.remove(debris)
            objectsRemoved += 1
    if printOutput:
        print "Objects in Orbit After: " + str(len(objects))
    return objects
