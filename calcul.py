# Calcul de structure des navires (par calcul direct)
import matplotlib.pyplot as plt
import numpy as np
import math

# Fonction
    # Pressions
        # Méthode BV
def pression_fond(MC,C,Te) :
    if MC == "BV" :
        if Te > 0.53*C :
            P_fond = 7.5*C+3.25*Te
        else:
            P_fond = 17.5*Te
    else:
        P_fond = 9.81*rho*Te
    return P_fond

def pression_muraille(MC,P_fond,z):
    if MC == "BV" :
        P_muraille = max(P_fond -0.9*z, 1.25*10)
    else:
        P_muraille = 9.81*rho*(Te-z)
    return P_muraille


Portee_varangue = float(input("Portée des varangues (m) : "))
Spacing_varangue = float(input("Espacement des varangues (m) : "))
Re_varangue = float(input("Re des varangues (MPa) : Re varangue = "))

Portee_lisse = Spacing_varangue
Spacing_lisse = float(input("Espacement des lisses (m) : "))
Re_lisse = float(input("Re des lisses (MPa) : Re lisse = "))
print()

Re_tole = float(input("Re du bordé (MPa) : Re borde = "))
print()

FS = float(input("Facteur de sécurité global : FS = "))

sigma_adm_tole = Re_tole*10**6/FS
sigma_adm_lisse = Re_lisse*10**6/FS
sigma_adm_varangue = Re_varangue*10**6/FS


    # Définition de la coque
x_coque =[-B/2, -B/2, 0, B/2, B/2]
y_coque = [C, math.tan(math.radians(alpha))*B*0.5, 0, math.tan(math.radians(alpha))*B*0.5, C]

    # Définition de la flottaison
x_flottaison =[-B/2-0.1*B, B/2+0.1*B]
y_flottaison = [Te, Te]

# Calcul de la presion
P_fond = pression_fond(MC, C, Te)
P_muraille = pression_muraille(MC, P_fond, z)

print("\n > Les pressions considérées sont : Pfond =",round(P_fond,3), "kN/m², et Pmuraille =",round(P_muraille,3), " kN/m²")

# Calcul de pression pour représentation graphique
def graphics_pressions(Te, C, P_fond, MC, y_coque):
    c_red = 0.025
    z1 = max(Te,min(C,(P_fond-12.5)/0.9))
    if MC == "BV" :
        p1 = c_red*pression_muraille(MC,P_fond,y_coque[0])
        p2 = c_red*pression_muraille(MC,P_fond,z1)
    else :
        p1 = 0
        p2 = 0
    p3 = c_red*pression_muraille(MC,P_fond,y_coque[1])
    p4 = c_red*P_fond

    return p1,p2,p3,p4

# Calcul de l'épaisseur de tôle
def sheet_thickness(Spacing_lisse, Portee_lisse, P_fond, sigma_adm_tole):
    t = math.sqrt(6/10)*Spacing_lisse*math.sqrt(P_fond*10**3/sigma_adm_tole)
    if Portee_lisse <= 3*Spacing_lisse :
        Ccorrection = min(1.21*math.sqrt(1+0.33*(Spacing_lisse/Portee_lisse)**2)-0.69*(Spacing_lisse/Portee_lisse), 1)
    else:
        Ccorrection = 1

    tmini = t*Ccorrection
    return t, tmini, Ccorrection

toleEpaisseur = sheet_thickness(Spacing_lisse, Portee_varangue, P_fond, sigma_adm_tole)

print("\n > L'épaisseur du bordé est calculée à",round(toleEpaisseur[0]*10**3,1), "mm et est corrigée à", round(toleEpaisseur[1]*10**3,1), "mm (coeff de correction de ", round(toleEpaisseur[2],3),") \n")

# Calcul des lisses
def lisses_calculation(MC, tmini, type_lisse):
    type_lisse = input("type de lisse ? HP [HP] ou mécano-soudés [MS]: ")
    if type_lisse not in ["HP", "MS"]:
        raise ValueError("ERREUR : le profile doit être 'HP' ou 'MS' ! \n")

    # Bordé associé
    ep_borde = tmini
    l_borde_lisse = 40 * ep_borde
    A_borde = ep_borde * l_borde_lisse
    y_borde = 0.5 * ep_borde

    #recuperer dans un svg les profiles et les mettres dans une biblio

    if type_lisse == "HP" :
        # Profils HP du commerce (h,Section,yg,I)
            #S_plat, yg_plat en fait parti, I_plat

            # Cente de gravité
        yg_lisse = (A_borde * y_borde + S_plat * yg_plat) / (A_borde + S_plat)

            # Inertie aytour de CG
        I_HP = I_plat*10**4 + S_plat * (yg_lisse - yg_plat)**2
        I_borde = (l_borde_lisse * ep_borde**3) / 12 + A_borde * (yg_lisse - y_borde)**2
        I_lisse = I_borde + I_HP

            # Fibe la plus éloignée
        v_lisse = max(yg_lisse, ep_borde + h_plat - yg_lisse)
    else :
    # Mécano-soudées
        # Dimensions (a laisser, l'utilisateur le rentre)
        h_ame_lisse = float(input("hauteur âme des lisses (mm) : "))
        e_ame_lisse = float(input("épaisseur âme des lisses (mm) : "))
        l_semelle_lisse = float(input("longueur semelle des lisses (mm) : "))
        e_semelle_lisse = float(input("épaisseur semelle des lisses (mm) : "))

            # Aires
        A_ame = e_ame_lisse * h_ame_lisse
        A_semelle = l_semelle_lisse * e_semelle_lisse

            # Positions des centres (depuis le bas)
        y_ame = ep_borde + 0.5 * h_ame_lisse
        y_semelle = ep_borde + h_ame_lisse + 0.5 * e_semelle_lisse

            # Cente de gravité
        yg_lisse = (A_borde * y_borde + A_ame * y_ame + A_semelle * y_semelle) / (A_borde + A_ame + A_semelle)

            # Inertie autour du CG
        I_borde = (l_borde_lisse * ep_borde**3) / 12 + A_borde * (yg_lisse - y_borde)**2
        I_ame = (e_ame_lisse * h_ame_lisse**3) / 12 + A_ame * (yg_lisse - y_ame)**2
        I_semelle = (l_semelle_lisse * e_semelle_lisse**3) / 12 + A_semelle * (y_semelle - yg_lisse)**2
        I_lisse = I_borde + I_ame + I_semelle

            # Fibe la plus éloignée
        v_lisse = max(yg_lisse, ep_borde + h_ame_lisse + e_semelle_lisse - yg_lisse)

# Contraintes
def contraintes_lisse_calculation(P_fond, Spacing_lisse, Portee_lisse, sigma_adm_lisse, I_lisse,v_lisse):
    mfz_lisse = (P_fond*10**3*Spacing_lisse*Portee_lisse**2)/12
    wmini_lisse = (mfz_lisse/sigma_adm_lisse)*10**6
    w_calcul_lisse = (I_lisse/v_lisse)*10**-3

    return mfz_lisse, wmini_lisse, w_calcul_lisse

print("\n > Le module minimum des lisses est de", round(contraintes_lisse_calculation(P_fond, Spacing_lisse, Portee_lisse, sigma_adm_lisse, I_lisse, v_lisse)[1],1),"cm3, et le module calculé est de", round(w_calcul_lisse,1), "cm3 \n")

# Calcul des varangues
def varangues_calculations(tmini,Portee_varangue,Spacing_varangue):
    h_ame_varangue = float(input("hauteur âme des varangues (mm) : "))
    e_ame_varangue = float(input("épaisseur âme des varangues (mm) : "))
    l_semelle_varangue = float(input("longueur semelle des varangues (mm) : "))
    e_semelle_varangue = float(input("épaisseur semelle des varangues (mm) : "))
    # Mécano-soudées
    # Dimensions
    ep_borde = tmini
    l_borde_varangue = min(0.2*Portee_varangue, Spacing_varangue)

    # Aires
    A_borde = ep_borde * l_borde_varangue
    A_ame = e_ame_varangue * h_ame_varangue
    A_semelle = l_semelle_varangue * e_semelle_varangue

        # Positions des centres (depuis le bas)
    y_borde = 0.5 * ep_borde
    y_ame = ep_borde + 0.5 * h_ame_varangue
    y_semelle = ep_borde + h_ame_varangue + 0.5 * e_semelle_varangue

        # Centre de gravité
    yg_varangue = (A_borde * y_borde + A_ame * y_ame + A_semelle * y_semelle) / (A_borde + A_ame + A_semelle)

        # Inertie autour du CG
    I_borde = (l_borde_varangue * ep_borde**3) / 12 + A_borde * (yg_varangue - y_borde)**2
    I_ame = (e_ame_varangue * h_ame_varangue**3) / 12 + A_ame * (yg_varangue - y_ame)**2
    I_semelle = (l_semelle_varangue * e_semelle_varangue**3) / 12 + A_semelle * (y_semelle - yg_varangue)**2
    I_varangue = I_borde + I_ame + I_semelle

        # Fibre la plus éloignée
    v_varangue = max(yg_varangue, ep_borde + h_ame_varangue + e_semelle_varangue - yg_varangue)

        # Contraintes
    mfz_varangue = (P_fond*10**3*Spacing_varangue*Portee_varangue**2)/12
    wmini_varangue = (mfz_varangue/sigma_adm_varangue)*10**6
    w_calcul_varangue = (I_varangue/v_varangue)*10**-3

    return mfz_varangue, wmini_varangue, w_calcul_varangue

print("> Le module minimum des varangues est de", round(varangues_calculations[1],1),"cm3, et le module calculé est de", round(varangues_calculations[2],1), "cm3")


'''


# GRAPHIQUE 1 : REPRESENTATION DE LA STRUCTURE
    # Définition de l'origine
x0 = 0
y0 = 0

    # Définition de la tôle
Ltole = 2*Spacing_varangue
ltole = Portee_varangue

    # Définition des points
        #Tôle
x1_tole = x0
x2_tole = x0+Ltole
y1_tole = y0
y2_tole = y0+Portee_varangue
x_tole =[x1_tole, x2_tole, x2_tole, x1_tole, x1_tole]
y_tole = [y1_tole, y1_tole, y2_tole, y2_tole, y1_tole]
        #Varangue
x1_varangue = x0+0.5*Spacing_varangue
x2_varangue = x1_varangue+Spacing_varangue
y1_varangue = y0
y2_varangue = y1_varangue+Portee_varangue

x_varangue = [x1_varangue, x1_varangue, x2_varangue, x2_varangue]
y_varangue = [y1_varangue, y1_varangue+Portee_varangue , y1_varangue+Portee_varangue , y1_varangue]
        #Lisse
tab_y_lisse = np.arange(y0, ltole, Spacing_lisse)

motif_x = [x1_tole, x2_tole, x2_tole, x1_tole]
x_lisse = motif_x * len(tab_y_lisse)

y_lisse = np.repeat(np.arange(len(tab_y_lisse)) * Spacing_lisse, 2)
x_lisse = x_lisse[:len(y_lisse)]

    # Tracé du Rendu de la structure
plt.figure(1)
plt.plot(x_varangue, y_varangue, label='Varangues', color = 'red', linewidth = 2)
plt.plot(x_lisse,y_lisse, label='Lisses',color = 'green', linewidth = 2)
plt.plot(x_tole, y_tole, label='Tôle',color = 'blue', linewidth = 2)

plt.title("Représentation de la structure")
plt.xlabel("Axe X (m)")
plt.ylabel("Axe Y (m)")
plt.legend(loc='lower left')
plt.grid(True)


# GRAPHIQUE 2 : REPRESENTATION HYDROSTATIQUE
    # Définition de l'origine
x0 = 0
y0 = x0

    # Tracé des forces hydro
plt.figure(2)

x_pression_muraille_b = [x_coque[0], x_coque[0]-p1, x_coque[0]-p2, x_coque[0]-p3, x_coque[0]-p4, x_coque[1]]
y_pression_muraille_b = [y_coque[0], y_coque[0], z1, Te, y_coque[1], y_coque[1]]
x_pression_fond_b = [x_coque[1], x_coque[1]-p3*math.sin(math.radians(alpha)), x_coque[2]-p3*math.sin(math.radians(alpha)), x_coque[2]]
y_pression_fond_b = [y_coque[1], y_coque[1]-p3*math.cos(math.radians(alpha)), y_coque[2]-p3*math.cos(math.radians(alpha)), y_coque[2]]

x_pression_muraille_t = [-x for x in x_pression_muraille_b]
y_pression_muraille_t = y_pression_muraille_b
x_pression_fond_t = [-x for x in x_pression_fond_b]
y_pression_fond_t = y_pression_fond_b

plt.plot(x_pression_muraille_b, y_pression_muraille_b, label='Pression hydrostatique', color ='black', linewidth = 2)
plt.plot(x_pression_fond_b, y_pression_fond_b, color ='black', linewidth = 2)
plt.plot(x_pression_muraille_t, y_pression_muraille_t, color ='black', linewidth = 2)
plt.plot(x_pression_fond_t, y_pression_fond_t, color ='black', linewidth = 2)

    # Tracé de la coque
plt.plot(x_coque, y_coque, label='Coque', color = 'red', linewidth = 2)
plt.plot(x_flottaison,y_flottaison, label='DWL',color = 'blue', linewidth = 2)

plt.title("Représentation des pressions hydrostatiques")
plt.xlabel("OH(m)")
plt.ylabel("CL (m)")
plt.legend(loc='upper center')
plt.grid(True)


# GRAPHIQUE 3 : REPRESENTATION DES RAIDISSEURS
    # Définition des points
x0 = 0
y0 = 0
        # Varangues
x1_tole_varangue = -1*l_borde_varangue*10**3
x2_tole_varangue = l_borde_varangue*10**3
y1_tole_varangue = y0
y2_tole_varangue = y0+tmini*10**3
x_tole_varangue =[x1_tole_varangue, x2_tole_varangue, x2_tole_varangue, x1_tole_varangue, x1_tole_varangue]
y_tole_varangue = [y1_tole_varangue, y1_tole_varangue, y2_tole_varangue, y2_tole_varangue, y1_tole_varangue]

x1_ame_varangue = x0-0.5*e_ame_varangue
x2_ame_varangue = x0+0.5*e_ame_varangue
y1_ame_varangue = y2_tole_varangue
y2_ame_varangue = y1_ame_varangue+h_ame_varangue
x_ame_varangue =[x1_ame_varangue, x2_ame_varangue, x2_ame_varangue, x1_ame_varangue, x1_ame_varangue]
y_ame_varangue = [y1_ame_varangue, y1_ame_varangue, y2_ame_varangue, y2_ame_varangue, y1_ame_varangue]

x1_semelle_varangue = x0-0.5*l_semelle_varangue
x2_semelle_varangue = x0+0.5*l_semelle_varangue
y1_semelle_varangue = y2_ame_varangue
y2_semelle_varangue = y1_semelle_varangue+e_semelle_varangue
x_semelle_varangue =[x1_semelle_varangue, x2_semelle_varangue, x2_semelle_varangue, x1_semelle_varangue, x1_semelle_varangue]
y_semelle_varangue = [y1_semelle_varangue, y1_semelle_varangue, y2_semelle_varangue, y2_semelle_varangue, y1_semelle_varangue]

        # lisses
if type_lisse == "MS" :
    x1_tole_lisse = -1*l_borde_lisse*10**3
    x2_tole_lisse = l_borde_lisse*10**3
    y1_tole_lisse = y0
    y2_tole_lisse = y0+tmini*10**3
    x_tole_lisse =[x1_tole_lisse, x2_tole_lisse, x2_tole_lisse, x1_tole_lisse, x1_tole_lisse]
    y_tole_lisse = [y1_tole_lisse, y1_tole_lisse, y2_tole_lisse, y2_tole_lisse, y1_tole_lisse]

    x1_ame_lisse = x0-0.5*e_ame_lisse
    x2_ame_lisse = x0+0.5*e_ame_lisse
    y1_ame_lisse = y2_tole_lisse
    y2_ame_lisse = y1_ame_lisse+h_ame_lisse
    x_ame_lisse =[x1_ame_lisse, x2_ame_lisse, x2_ame_lisse, x1_ame_lisse, x1_ame_lisse]
    y_ame_lisse = [y1_ame_lisse, y1_ame_lisse, y2_ame_lisse, y2_ame_lisse, y1_ame_lisse]

    x1_semelle_lisse = x0-0.5*l_semelle_lisse
    x2_semelle_lisse = x0+0.5*l_semelle_lisse
    y1_semelle_lisse = y2_ame_lisse
    y2_semelle_lisse = y1_semelle_lisse+e_semelle_lisse
    x_semelle_lisse =[x1_semelle_lisse, x2_semelle_lisse, x2_semelle_lisse, x1_semelle_lisse, x1_semelle_lisse]
    y_semelle_lisse = [y1_semelle_lisse, y1_semelle_lisse, y2_semelle_lisse, y2_semelle_lisse, y1_semelle_lisse]

fig3, (ax1, ax2) = plt.subplots(2, sharex=True, sharey=True)

ax1.plot(x_ame_varangue, y_ame_varangue, label="Âme : "+str(int(h_ame_varangue))+"x "+str(int(e_ame_varangue)), color = 'blue', linewidth = 2)
ax1.plot(x_semelle_varangue,y_semelle_varangue, label='Semelle : '+str(int(l_semelle_varangue))+"x "+str(int(e_semelle_varangue)),color = 'blue', linewidth = 2)
ax1.plot(x_tole_varangue, y_tole_varangue, label='Tôle ep. '+str(round(tmini*10**3,1))+" mm",color = 'red', linewidth = 2)
ax1.set_title("Echantillonnage des varangues")
ax1.set_xlabel("Axe Y (mm)")
ax1.set_ylabel("Axe Z (mm)")
ax1.legend(loc='lower right')
ax1.grid(True)

if type_lisse == "MS" :
    ax2.plot(x_ame_lisse, y_ame_lisse, label='Âme'+str(int(h_ame_lisse))+"x "+str(int(e_ame_lisse)), color = 'blue', linewidth = 2)
    ax2.plot(x_semelle_lisse,y_semelle_lisse, label='Semelle : '+str(int(l_semelle_lisse))+"x "+str(int(e_semelle_lisse)),color = 'blue', linewidth = 2)
    ax2.plot(x_tole_lisse, y_tole_lisse, label='Tôle ep.'+str(round(tmini*10**3,1))+" mm",color = 'red', linewidth = 2)
    ax2.set_title("Echantillonnage des lisses")
    ax2.set_xlabel("Axe Y (mm)")
    ax2.set_ylabel("Axe Z (mm)")
    ax2.legend(loc='upper right')
    ax2.grid(True)

for ax in (ax1, ax2):
    ax.set_aspect('equal', adjustable='box')
    ax.autoscale()

x_min = min(ax1.get_xlim()[0], ax2.get_xlim()[0])
x_max = max(ax1.get_xlim()[1], ax2.get_xlim()[1])

ax1.set_xlim(x_min, x_max)
ax2.set_xlim(x_min, x_max)

plt.tight_layout()

plt.show()

'''
