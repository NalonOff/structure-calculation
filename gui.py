import tkinter as tk
from tkinter import ttk, scrolledtext
from calculs import *
from profiles import charger_profiles, lister_profiles

class CalculGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Application de Calcul de Structure")
        self.root.geometry("450x600")

        # Charger les profils au démarrage
        self.profiles_data = charger_profiles()

        # Dictionnaires pour stocker les valeurs
        self.base_values = {}
        self.fond_values = {}
        self.muraille_values = {}

        # Frame principal
        main_frame = ttk.Frame(root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Configuration du redimensionnement
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(0, weight=3)
        main_frame.rowconfigure(1, weight=2)

        # Création du notebook (onglets)
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))

        # Création des onglets
        self.create_base_tab()
        self.create_fond_tab()
        self.create_muraille_tab()

        # Zone de sortie
        self.create_output_zone(main_frame)

        # Bouton de calcul
        calc_button = ttk.Button(main_frame, text="Lancer les Calculs", command=self.run_calculations)
        calc_button.grid(row=2, column=0, pady=10)

    def create_profile_selector(self, parent, row, label_text, key_prefix, value_dict):
        """Crée un sélecteur de profil HP (liste) ou MS (manuel)"""

        # Label principal
        label = ttk.Label(parent, text=label_text, font=('Arial', 9, 'bold'))
        label.grid(row=row, column=0, columnspan=2, sticky=tk.W, padx=5, pady=(10, 5))
        row += 1

        # Type de lisse (HP ou MS)
        type_var = tk.StringVar(value="HP")
        type_frame = ttk.Frame(parent)
        type_frame.grid(row=row, column=0, columnspan=2, padx=5, pady=5, sticky=tk.W)

        # Radio buttons
        rb_hp = ttk.Radiobutton(type_frame, text="HP (Profil JSON)", variable=type_var,
                                value="HP")
        rb_hp.pack(side=tk.LEFT, padx=5)

        rb_ms = ttk.Radiobutton(type_frame, text="MS (Manuel)", variable=type_var,
                                value="MS")
        rb_ms.pack(side=tk.LEFT, padx=5)

        row += 1

        # Frame pour la sélection HP (liste déroulante)
        hp_frame = ttk.Frame(parent)
        hp_frame.grid(row=row, column=0, columnspan=2, padx=5, pady=5, sticky=(tk.W, tk.E))

        hp_label = ttk.Label(hp_frame, text="Profil:")
        hp_label.pack(side=tk.LEFT, padx=(0, 5))

        profiles_list = lister_profiles()
        combo_hp = ttk.Combobox(hp_frame, width=18,
                                values=profiles_list,
                                state='readonly' if profiles_list else 'disabled')
        combo_hp.pack(side=tk.LEFT)

        if not profiles_list:
            no_profile_label = ttk.Label(hp_frame, text="(Aucun profil disponible)",
                                        foreground='gray')
            no_profile_label.pack(side=tk.LEFT, padx=5)

        # Stocker les références
        value_dict[f"{key_prefix}_type"] = type_var
        value_dict[f"{key_prefix}_combo"] = combo_hp
        value_dict[f"{key_prefix}_hp_frame"] = hp_frame

        # Lier les événements
        rb_hp.config(command=lambda: self.toggle_profile_type(type_var, hp_frame,
                                                              key_prefix, value_dict))
        rb_ms.config(command=lambda: self.toggle_profile_type(type_var, hp_frame,
                                                              key_prefix, value_dict))
        combo_hp.bind('<<ComboboxSelected>>',
                     lambda e: self.on_profile_selected(combo_hp.get(),
                                                       key_prefix, value_dict))

        row += 1

        # Champs pour les valeurs du profil
        profile_fields = [
            ("Hauteur (mm)", f"{key_prefix}_hauteur"),
            ("Section (mm²)", f"{key_prefix}_section"),
            ("Inertie (mm⁴)", f"{key_prefix}_inertie"),
            ("Centre de gravité (mm)", f"{key_prefix}_centre_gravite"),
        ]

        for field_label, field_key in profile_fields:
            field_label_widget = ttk.Label(parent, text=field_label)
            field_label_widget.grid(row=row, column=0, sticky=tk.W, padx=5, pady=2)

            field_entry = ttk.Entry(parent, width=20)
            field_entry.grid(row=row, column=1, padx=5, pady=2)

            value_dict[field_key] = field_entry
            row += 1

        # Initialement en mode HP : désactiver les champs et afficher la liste
        self.set_profile_fields_state(key_prefix, value_dict, 'disabled')
        hp_frame.grid()

        return row

    def toggle_profile_type(self, type_var, hp_frame, key_prefix, value_dict):
        """Gère le changement de type HP/MS"""
        if type_var.get() == "HP":
            # Mode HP : afficher la liste, désactiver les champs
            hp_frame.grid()
            self.set_profile_fields_state(key_prefix, value_dict, 'disabled')
            # Si un profil est déjà sélectionné, le charger
            combo = value_dict[f"{key_prefix}_combo"]
            if combo.get():
                self.on_profile_selected(combo.get(), key_prefix, value_dict)
            else:
                self.clear_profile_fields(key_prefix, value_dict)
        else:  # MS
            # Mode MS : cacher la liste, activer les champs pour saisie manuelle
            hp_frame.grid_remove()
            self.set_profile_fields_state(key_prefix, value_dict, 'normal')
            self.clear_profile_fields(key_prefix, value_dict)

    def set_profile_fields_state(self, key_prefix, value_dict, state):
        """Active/désactive les champs du profil"""
        fields = ['hauteur', 'section', 'inertie', 'centre_gravite']
        for field in fields:
            field_key = f"{key_prefix}_{field}"
            if field_key in value_dict:
                value_dict[field_key].config(state=state)

    def clear_profile_fields(self, key_prefix, value_dict):
        """Vide les champs du profil"""
        fields = ['hauteur', 'section', 'inertie', 'centre_gravite']
        for field in fields:
            field_key = f"{key_prefix}_{field}"
            if field_key in value_dict:
                value_dict[field_key].delete(0, tk.END)

    def on_profile_selected(self, profile_name, key_prefix, value_dict):
        """Remplit automatiquement les valeurs quand un profil JSON est sélectionné"""
        profile_data = self.profiles_data.get(profile_name)

        if profile_data:
            # Activer temporairement les champs pour les remplir
            self.set_profile_fields_state(key_prefix, value_dict, 'normal')

            # Remplir les champs
            mapping = {
                'hauteur': 'hauteur',
                'section': 'section',
                'inertie': 'inertie',
                'centre_gravite': 'centre_gravite'
            }

            for json_key, field_suffix in mapping.items():
                field_key = f"{key_prefix}_{field_suffix}"
                if field_key in value_dict and json_key in profile_data:
                    value_dict[field_key].delete(0, tk.END)
                    value_dict[field_key].insert(0, str(profile_data[json_key]))

            # Redésactiver les champs (mode custom)
            self.set_profile_fields_state(key_prefix, value_dict, 'disabled')

    def create_base_tab(self):
        """Crée l'onglet Base"""
        base_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(base_frame, text="Base")

        canvas = tk.Canvas(base_frame)
        scrollbar = ttk.Scrollbar(base_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        fields = [
            ("Rho (kg/m3)", "rho"),
            ("Creux (m)", "hollow"),
            ("Bau (m)", "bau"),
            ("Tirant d'eau (m)", "draft"),
            ("Inclinaison du fond (°)", "bottomInclination"),
            ("Altitude de calcul pour les murailles (m)", "wallCalculationAltitude"),
            ("Méthode de calcul", "calculationMethod", "combobox", ["BV", "HYDRO"]),
            ("Facteur de sécurité global", "securityFactor")
        ]

        self.create_input_fields(scrollable_frame, fields, self.base_values)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def create_fond_tab(self):
        """Crée l'onglet Fond"""
        fond_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(fond_frame, text="Fond")

        canvas = tk.Canvas(fond_frame)
        scrollbar = ttk.Scrollbar(fond_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        row = 0

        # Sélecteur de profil pour les lisses
        row = self.create_profile_selector(scrollable_frame, row,
                                           "Type de Lisse:", "lisse", self.fond_values)

        # Champs pour les lisses et autres
        fields = [
            'separator',
            ("Portée des lisses (m)", "lisseRange"),
            ("Espacement des lisses (m)", "lisseSpacing"),
            ("Re des lisses (Mpa)", "lisseRe"),
            'separator',
            ("Portée des varangues (m)", "varangueRange"),
            ("Espacement des varangues (m)", "varangueSpacing"),
            ("Re des varangues (Mpa)", "varangueRe"),
            'separator',
            ("Re du bordé (Mpa)", "platingRe")
        ]

        self.create_input_fields(scrollable_frame, fields, self.fond_values, start_row=row)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def create_muraille_tab(self):
        """Crée l'onglet Muraille"""
        muraille_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(muraille_frame, text="Muraille")

        canvas = tk.Canvas(muraille_frame)
        scrollbar = ttk.Scrollbar(muraille_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        fields = [
            ("Portée des murailles (m)", "wallRange"),
            ("Espacement des varangues (m)", "wallSpacing"),
            ("Re des varangues (Mpa)", "wallRe"),
            'separator',
            ("Portée des lisses (m)", "lisseRange"),
            ("Espacement des lisses (m)", "lisseSpacing"),
            ("Re des liesses (Mpa)", "lisseRe"),
            'separator',
            ("Re du bordé (Mpa)", "platingRe")
        ]

        self.create_input_fields(scrollable_frame, fields, self.muraille_values)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def create_input_fields(self, parent, fields, value_dict, start_row=0):
        """Crée les champs de saisie pour un onglet"""
        row = start_row
        for field_info in fields:
            if field_info == "separator":
                separator = ttk.Separator(parent, orient='horizontal')
                separator.grid(row=row, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10, padx=5)
                row += 1
                continue

            if len(field_info) == 2:
                label_text, key = field_info
                field_type = "entry"
                options = []
            elif len(field_info) == 3:
                label_text, key, field_type = field_info
                options = []
            else:
                label_text, key, field_type, options = field_info

            label = ttk.Label(parent, text=label_text)
            label.grid(row=row, column=0, sticky=tk.W, padx=5, pady=5)

            if field_type == "combobox":
                widget = ttk.Combobox(parent, width=18, values=options, state='readonly')
                widget.grid(row=row, column=1, padx=5, pady=5)
            else:
                widget = ttk.Entry(parent, width=20)
                widget.grid(row=row, column=1, padx=5, pady=5)

            value_dict[key] = widget
            row += 1

    def create_output_zone(self, parent):
        """Crée la zone d'affichage des résultats"""
        output_label = ttk.Label(parent, text="Résultats des Calculs:", font=('Arial', 12, 'bold'))
        output_label.grid(row=1, column=0, sticky=tk.W, pady=(10, 5))

        self.output_text = scrolledtext.ScrolledText(parent, width=80, height=10, wrap=tk.WORD, state='disabled')
        self.output_text.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

    def get_values(self):
        """Récupère toutes les valeurs saisies et les convertit en float (sauf combobox)"""
        def convert_value(widget):
            # Ignorer les frames et autres widgets non-input
            if isinstance(widget, (ttk.Frame, tk.Frame)):
                return None

            if isinstance(widget, tk.StringVar):
                return widget.get()

            value = widget.get()

            if isinstance(widget, ttk.Combobox):
                return value

            if value.strip() == '':
                return None

            try:
                return float(value)
            except ValueError:
                raise ValueError(f"Impossible de convertir '{value}' en nombre")

        base_data = {key: convert_value(entry) for key, entry in self.base_values.items()
                     if not isinstance(entry, (ttk.Frame, tk.Frame))}
        fond_data = {key: convert_value(entry) for key, entry in self.fond_values.items()
                     if not isinstance(entry, (ttk.Frame, tk.Frame))}
        muraille_data = {key: convert_value(entry) for key, entry in self.muraille_values.items()
                         if not isinstance(entry, (ttk.Frame, tk.Frame))}

        return {
            'base': base_data,
            'fond': fond_data,
            'muraille': muraille_data
        }

    def run_calculations(self):
        """Lance les calculs avec les valeurs saisies"""
        self.output_text.config(state='normal')
        self.output_text.delete(1.0, tk.END)

        try:
            values = self.get_values()

            self.output_text.insert(tk.END, "="*58 + "\n")
            self.output_text.insert(tk.END, "RÉSULTATS DES CALCULS\n")
            self.output_text.insert(tk.END, "="*58 + "\n\n")

            # BASE
            self.output_text.insert(tk.END, "--- CALCULS DES PRESSIONS ---\n")

            bottomPression = bottom_pression(values['base']['calculationMethod'],
                                            values['base']['draft'],
                                            values['base']['hollow'],
                                            values['base']['rho'])
            wallPression = wall_pression(values['base']['calculationMethod'],
                                        bottomPression,
                                        values['base']['wallCalculationAltitude'],
                                        values['base']['rho'],
                                        values['base']['draft'])

            self.output_text.insert(tk.END, f"Pressions considérées: Pfond = {bottomPression} Mpa et Pmuraille = {wallPression} MPa")
            self.output_text.insert(tk.END, "\n\n")

            # FOND
            self.output_text.insert(tk.END, "--- CALCULS FOND ---\n")

            sigma_adm_tole = sigma(values['fond']['platingRe'], values['base']['securityFactor'])
            sigma_adm_lisse = sigma(values['fond']['lisseRe'], values['base']['securityFactor'])
            sigma_adm_varangue = sigma(values['fond']['varangueRe'], values['base']['securityFactor'])

            sheetThickness = sheet_thickness(values['fond']['lisseSpacing'],
                                            values['fond']['lisseRange'],
                                            bottomPression,
                                            sigma_adm_tole)

            self.output_text.insert(tk.END, f"Épaisseur du bordé: {round(sheetThickness[0] * 10**3, 1)} mm (coeff: {round(sheetThickness[2], 3)})")
            self.output_text.insert(tk.END, "\n\n")

            # MURAILLE
            self.output_text.insert(tk.END, "--- CALCULS MURAILLE ---\n")
            for key, value in values['muraille'].items():
                if value:
                    self.output_text.insert(tk.END, f"{key}: {value}\n")
            self.output_text.insert(tk.END, "\n")

        except Exception as e:
            self.output_text.insert(tk.END, f"Erreur lors des calculs: {str(e)}\n")

        finally:
            self.output_text.config(state='disabled')

def main():
    root = tk.Tk()
    app = CalculGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
