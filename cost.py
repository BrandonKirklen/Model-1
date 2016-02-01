import riskEvaluation as risk


def ROI(orbitalObjects, method):
    baseCost = 10000000000
    reduction = risk.reduction(orbitalObjects)
    investment = method.cost
    gain = baseCost * reduction
    return (gain - investment)/investment
