import json
import os

FICHIER_JSON = "profiles.json"


def charger_profiles():
    """Charge les profils depuis le fichier JSON"""
    if not os.path.exists(FICHIER_JSON):
        return {}

    try:
        with open(FICHIER_JSON, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"Erreur lors du chargement: {e}")
        return {}


def sauvegarder_profiles(profiles):
    """Sauvegarde les profils dans le fichier JSON"""
    try:
        with open(FICHIER_JSON, "w", encoding="utf-8") as f:
            json.dump(profiles, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"Erreur lors de la sauvegarde: {e}")
        return False


def demander_nombre(message):
    """Demande un nombre avec gestion d'erreur"""
    while True:
        try:
            valeur = input(message).strip()
            if not valeur:
                print("Erreur: La valeur ne peut pas être vide")
                continue
            return float(valeur)
        except ValueError:
            print("Erreur: Veuillez entrer un nombre valide")


def ajouter_profile():
    """Ajoute un nouveau profil"""
    print("\n=== Ajout d'un profil ===\n")

    # Charger les profils existants
    profiles = charger_profiles()

    # Demander le nom
    while True:
        nom = input("Nom du profil: ").strip()
        if nom:
            break
        print("Erreur: Le nom ne peut pas être vide")

    # Vérifier les doublons
    nom_upper = nom.upper()
    if nom_upper in profiles:
        print(f"\nAttention: Le profil '{nom}' existe déjà!")
        print(f"Valeurs actuelles: {profiles[nom_upper]}")
        reponse = input("Remplacer? (o/n): ").strip().lower()
        if reponse != "o":
            print("Annulé")
            return

    # Demander les valeurs
    hauteur = demander_nombre("Hauteur (mm): ")
    section = demander_nombre("Section (mm²): ")
    inertie = demander_nombre("Inertie (mm⁴): ")
    centre_gravite = demander_nombre("Centre de gravité (mm): ")

    # Sauvegarder
    profiles[nom_upper] = {
        "hauteur": hauteur,
        "section": section,
        "inertie": inertie,
        "centre_gravite": centre_gravite,
    }

    if sauvegarder_profiles(profiles):
        print(f"\nSuccès: Profil '{nom}' ajouté!")
        print(f"Total: {len(profiles)} profil(s)")
    else:
        print("\nErreur: Échec de la sauvegarde")


def obtenir_profile(nom):
    """Récupère un profil par son nom"""
    profiles = charger_profiles()
    return profiles.get(nom.upper())


def lister_profiles():
    """Liste tous les noms de profils"""
    profiles = charger_profiles()
    return list(profiles.keys())


def afficher_profiles():
    """Affiche tous les profils existants"""
    profiles = charger_profiles()

    if not profiles:
        print("\nAucun profil enregistré")
        return

    print(f"\n=== Liste des profils ({len(profiles)}) ===\n")
    for nom, data in sorted(profiles.items()):
        print(f"Profil: {nom}")
        print(f"  Hauteur: {data['hauteur']} mm")
        print(f"  Section: {data['section']} cm²")
        print(f"  Inertie: {data['inertie']} cm⁴")
        print(f"  Centre de gravité: {data['centre_gravite']} mm")
        print()


def supprimer_profile():
    """Supprime un profil existant"""
    profiles = charger_profiles()

    if not profiles:
        print("\nAucun profil à supprimer")
        return

    print("\n=== Suppression d'un profil ===\n")
    print("Profils disponibles:")
    for nom in sorted(profiles.keys()):
        print(f"  - {nom}")

    nom = input("\nNom du profil à supprimer: ").strip()
    nom_upper = nom.upper()

    if nom_upper not in profiles:
        print(f"Erreur: Le profil '{nom}' n'existe pas")
        return

    print(f"\nProfil à supprimer: {nom_upper}")
    print(f"Valeurs: {profiles[nom_upper]}")

    confirmation = input("Confirmer la suppression? (o/n): ").strip().lower()
    if confirmation == "o":
        del profiles[nom_upper]
        if sauvegarder_profiles(profiles):
            print(f"\nSuccès: Profil '{nom}' supprimé")
            print(f"Total restant: {len(profiles)} profil(s)")
        else:
            print("\nErreur: Échec de la suppression")
    else:
        print("Suppression annulée")


def menu():
    """Menu principal"""
    while True:
        print("\n" + "=" * 40)
        print("GESTION DES PROFILS")
        print("=" * 40)
        print("1. Ajouter un profil")
        print("2. Voir tous les profils")
        print("3. Supprimer un profil")
        print("4. Quitter")
        print("=" * 40)

        choix = input("\nVotre choix: ").strip()

        if choix == "1":
            ajouter_profile()
        elif choix == "2":
            afficher_profiles()
        elif choix == "3":
            supprimer_profile()
        elif choix == "4":
            print("\nAu revoir!")
            break
        else:
            print("Erreur: Choix invalide")


if __name__ == "__main__":
    menu()
