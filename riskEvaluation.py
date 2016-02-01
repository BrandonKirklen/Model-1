probabilityOfCrash = 1/221.


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
    return (sumOfRisk(orbitalObjects) * probabilityOfCrash)


def reduction(orbitalObjects):
    return (probabilityOfCrash - missionRisk(orbitalObjects))


def reductionFactor(orbitalObjects):
    return (probabilityOfCrash - missionRisk(orbitalObjects))/probabilityOfCrash
