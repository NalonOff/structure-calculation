



def bottom_pression(calculationMethod, draft, hollow, rho) :
    if calculationMethod == "BV" :
        if draft > 0.53 * hollow:
            bottomPression = 7.5 * hollow + 3.25 * draft
        else:
            bottomPression = 17.5 * draft
    else:
        bottomPression = 9.81 * rho * draft

    return bottomPression

def wall_pression(calculationMethod, bottomPression, wallCalculationAltitude, rho, draft):
    if calculationMethod == "BV" :
        wallPression = max(bottomPression - 0.9 * wallCalculationAltitude, 1.25 * 10)
    else:
        wallPression = 9.81 * rho * (draft - wallCalculationAltitude)

    return wallPression

