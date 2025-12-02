import matplotlib.pyplot as plt
import numpy as np
import math


def bottom_pression(calculationMethod, draft, hollow, rho):
    if calculationMethod == "BV":
        if draft > 0.53 * hollow:
            bottomPression = 7.5 * hollow + 3.25 * draft
        else:
            bottomPression = 17.5 * draft
    else:
        bottomPression = 9.81 * rho * draft

    return bottomPression


def wall_pression(
    calculationMethod, bottomPression, wallCalculationAltitude, rho, draft
):
    if calculationMethod == "BV":
        wallPression = max(bottomPression - 0.9 * wallCalculationAltitude, 1.25 * 10)
    else:
        wallPression = 9.81 * rho * (draft - wallCalculationAltitude)

    return wallPression


def sigma(Re, securityFactor):
    return Re * 10**6 / securityFactor


def sheet_thickness(
    stiffenerSpacing, stiffenerRange, bottomPression, sigma_adm_plating
):

    thickness = (
        math.sqrt(6 / 10)
        * stiffenerSpacing
        * math.sqrt(bottomPression * 10**3 / sigma_adm_plating)
    )

    if stiffenerRange <= 3 * stiffenerSpacing:
        correctionCoef = min(
            1.21 * math.sqrt(1 + 0.33 * (stiffenerSpacing / stiffenerRange) ** 2)
            - 0.69 * (stiffenerSpacing / stiffenerRange),
            1,
        )
    else:
        correctionCoef = 1

    thicknessMin = thickness * correctionCoef

    return thickness, thicknessMin, correctionCoef


def stiffener_calculation(
    calculationMethod,
    thicknessMin,
    stiffenerType,
    # Paramètres HP (profil du commerce - flat bar)
    flatSection=None,
    flatGY=None,
    flatInertia=None,
    flatHeight=None,
    # Paramètres MS (mécano-soudé)
    webHeight=None,
    webThickness=None,
    flangeWidth=None,
    flangeThickness=None,
):
    """
    Calcule les raidisseurs selon le type (HP ou MS)

    HP : nécessite flatSection, flatGY, flatInertia, flatHeight
    MS : nécessite webHeight, webThickness, flangeWidth, flangeThickness
    """

    # Bordé associé (commun aux deux types)
    platingThickness = thicknessMin
    platingWidth = 40 * platingThickness
    platingSection = platingThickness * platingWidth
    platingY = 0.5 * platingThickness

    if stiffenerType == "HP":
        # Vérification des paramètres HP
        if None in [flatSection, flatGY, flatInertia, flatHeight]:
            raise ValueError(
                "Pour le type HP, les paramètres flatSection, flatGY, flatInertia, flatHeight sont requis"
            )

        # Centre de gravité
        stiffenerGY = (platingSection * platingY + flatSection * flatGY) / (
            platingSection + flatSection
        )

        # Inertie autour de CG
        flatInertiaTotal = (
            flatInertia * 10**4 + flatSection * (stiffenerGY - flatGY) ** 2
        )
        platingInertia = (
            platingWidth * platingThickness**3
        ) / 12 + platingSection * (stiffenerGY - platingY) ** 2
        stiffenerInertia = platingInertia + flatInertiaTotal

        # Fibre la plus éloignée
        stiffenerMaxFiber = max(
            stiffenerGY, platingThickness + flatHeight - stiffenerGY
        )

    elif stiffenerType == "MS":
        # Vérification des paramètres MS
        if None in [webHeight, webThickness, flangeWidth, flangeThickness]:
            raise ValueError(
                "Pour le type MS, les paramètres webHeight, webThickness, flangeWidth, flangeThickness sont requis"
            )

        # Sections
        webSection = webThickness * webHeight
        flangeSection = flangeWidth * flangeThickness

        # Positions des centres (depuis le bas)
        webY = platingThickness + 0.5 * webHeight
        flangeY = platingThickness + webHeight + 0.5 * flangeThickness

        # Centre de gravité
        stiffenerGY = (
            platingSection * platingY + webSection * webY + flangeSection * flangeY
        ) / (platingSection + webSection + flangeSection)

        # Inertie autour du CG
        platingInertia = (
            platingWidth * platingThickness**3
        ) / 12 + platingSection * (stiffenerGY - platingY) ** 2
        webInertia = (webThickness * webHeight**3) / 12 + webSection * (
            stiffenerGY - webY
        ) ** 2
        flangeInertia = (flangeWidth * flangeThickness**3) / 12 + flangeSection * (
            flangeY - stiffenerGY
        ) ** 2
        stiffenerInertia = platingInertia + webInertia + flangeInertia

        # Fibre la plus éloignée
        stiffenerMaxFiber = max(
            stiffenerGY, platingThickness + webHeight + flangeThickness - stiffenerGY
        )

    else:
        raise ValueError(
            f"Type de raidisseur inconnu: {stiffenerType}. Utilisez 'HP' ou 'MS'"
        )

    # Retourner les résultats
    return {
        "stiffenerGY": stiffenerGY,
        "stiffenerInertia": stiffenerInertia,
        "stiffenerMaxFiber": stiffenerMaxFiber,
        "platingThickness": platingThickness,
    }
