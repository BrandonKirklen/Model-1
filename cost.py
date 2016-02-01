import riskEvaluation as risk


def ROI(orbitalObjects, method, method2=None):
    if method2 is not None:
        baseCost = 10000000000
        reduction = risk.reduction(orbitalObjects)
        investment = method.cost + method2.cost
        gain = baseCost * reduction
        return (gain - investment)/investment
    else:
        baseCost = 10000000000
        reduction = risk.reduction(orbitalObjects)
        investment = method.cost
        gain = baseCost * reduction
        return (gain - investment)/investment
