import tkinter as tk
from tkinter import ttk, scrolledtext
# from mes_calculs import *  # Importez vos fonctions ici

class CalculGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Application de Calcul de Structure")
        self.root.geometry("450x600")

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

    def create_base_tab(self):
        """Crée l'onglet Base"""
        base_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(base_frame, text="Base")

        # Canvas et scrollbar pour le défilement
        canvas = tk.Canvas(base_frame)
        scrollbar = ttk.Scrollbar(base_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Exemples de champs pour la base
        fields = [
            ("Rho (kg/m3)", "rho"),
            ("Creux (m)", "hollow"),
            ("Bau (m)", "bau"),
            ("Tirant d'eau (m)", "draft"),
            ("Inclinaison du fond (°)", "bottomInclination"),
            ("Méthode de calcul", "calculationMethod", "combobox", ["BV", "HYDRO"]),

            ("Facteur de securité global", "securityFactor")
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

        # Exemples de champs pour le fond
        fields = [
            ("Portée des varangues (m)", "varangueRange"),
            ("Espacement des varangues (m)", "varangueSpacing"),
            ("Re des varangues (Mpa)", "varangueRe"),
            'separator',
            ("Portée des lisses (m)", "lisseRange"),
            ("Espacement des lisses (m)", "lisseSpacing"),
            ("Re des lisses (Mpa)", "lisseRe"),
            'separator',
            ("Re du bordé (Mpa)", "platingRe")
        ]

        self.create_input_fields(scrollable_frame, fields, self.fond_values)

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

        # Exemples de champs pour la muraille

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

    def create_input_fields(self, parent, fields, value_dict):
        """Crée les champs de saisie pour un onglet"""
        row = 0
        for field_info in fields:
            # Gestion des séparateurs
            if field_info == "separator":
                separator = ttk.Separator(parent, orient='horizontal')
                separator.grid(row=row, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10, padx=5)
                row += 1
                continue

            # Support pour tuple simple ou avec options
            if len(field_info) == 2:
                label_text, key = field_info
                field_type = "entry"
                options = []
            elif len(field_info) == 3:
                label_text, key, field_type = field_info
                options = []
            else:  # len == 4
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
        """Récupère toutes les valeurs saisies"""
        base_data = {key: entry.get() for key, entry in self.base_values.items()}
        fond_data = {key: entry.get() for key, entry in self.fond_values.items()}
        muraille_data = {key: entry.get() for key, entry in self.muraille_values.items()}

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
            # Récupération des valeurs
            values = self.get_values()

            # Exemple d'affichage - Remplacez par vos vraies fonctions
            self.output_text.insert(tk.END, "="*58 + "\n")
            self.output_text.insert(tk.END, "RÉSULTATS DES CALCULS\n")
            self.output_text.insert(tk.END, "="*58 + "\n\n")

            # BASE
            self.output_text.insert(tk.END, "--- CALCULS BASE ---\n")
            for key, value in values['base'].items():
                if value:
                    self.output_text.insert(tk.END, f"{key}: {value}\n")
            # Ajoutez vos calculs ici
            # resultat_base = ma_fonction_base(values['base'])
            # self.output_text.insert(tk.END, f"Résultat: {resultat_base}\n")
            self.output_text.insert(tk.END, "\n")

            # FOND
            self.output_text.insert(tk.END, "--- CALCULS FOND ---\n")
            for key, value in values['fond'].items():
                if value:
                    self.output_text.insert(tk.END, f"{key}: {value}\n")
            # Ajoutez vos calculs ici
            self.output_text.insert(tk.END, "\n")

            # MURAILLE
            self.output_text.insert(tk.END, "--- CALCULS MURAILLE ---\n")
            for key, value in values['muraille'].items():
                if value:
                    self.output_text.insert(tk.END, f"{key}: {value}\n")
            # Ajoutez vos calculs ici
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
