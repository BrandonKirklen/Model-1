import riskEvaluation as risk
probabilityOfCrashDefault = 1/221.


def ROI(orbitalObjects, method, method2=None, probabilityOfCrash=probabilityOfCrashDefault):
    if method2 is not None:
        baseCost = 10000000000
        reduction = risk.reduction(orbitalObjects, probabilityOfCrash)
        investment = method.cost + method2.cost
        gain = baseCost * reduction
        return (gain - investment)/investment
    else:
        baseCost = 10000000000
        reduction = risk.reduction(orbitalObjects, probabilityOfCrash)
        investment = method.cost
        gain = baseCost * reduction
        return (gain - investment)/investment
