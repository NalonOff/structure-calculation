import matplotlib.pyplot as plt
import numpy as np
import math

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

def sigma(Re, secutityFactor):
    return Re * 10**6 / secutityFactor

def sheet_thickness(lisseSpacing, lisseRange, bottomPression, sigma_adm_tole):

    thickness = math.sqrt(6/10) * lisseSpacing * math.sqrt(bottomPression * 10**3 / sigma_adm_tole)

    if lisseRange <= 3 * lisseSpacing:
        correctionCoef = min(1.21 * math.sqrt(1 + 0.33 * (lisseSpacing / lisseRange)**2) - 0.69 * (lisseSpacing / lisseRange), 1)
    else:
        correctionCoef = 1

    thicknessMin = thickness * correctionCoef

    return thickness, thicknessMin, correctionCoef

