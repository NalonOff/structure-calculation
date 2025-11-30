import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np

#from calcul import *

class CalculInterface:
    def __init__(self, root):
        self.root = root
        self.root.title("Interface de Calculs")
        self.root.geometry("1200x800")

        # Style
        style = ttk.Style()
        style.theme_use('clam')

        # Container principal
        main_container = ttk.PanedWindow(root, orient=tk.HORIZONTAL)
        main_container.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Panel gauche - Entrées
        left_panel = ttk.Frame(main_container)
        main_container.add(left_panel, weight=1)

        # Panel droit - Sorties
        right_panel = ttk.Frame(main_container)
        main_container.add(right_panel, weight=3)

        # Créer les widgets
        self.create_input_section(left_panel)
        self.create_output_section(right_panel)

    def create_input_section(self, parent):
        # Frame pour les paramètres
        params_frame = ttk.LabelFrame(parent, text="Paramètres d'entrée", padding=10)
        params_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Masse volumique du fluide
        ttk.Label(params_frame, text="Rho: ").grid(row=0, column=0, sticky=tk.W, pady=5, padx=5)
        self.rho = ttk.Entry(params_frame, width=15)
        self.rho.grid(row=0, column=1, pady=5, padx=5)
        self.rho.insert(0, "0")

        # Creux
        ttk.Label(params_frame, text="Creux (m): ").grid(row=1, column=0, sticky=tk.W, pady=5, padx=5)
        self.creux = ttk.Entry(params_frame, width=15)
        self.creux.grid(row=1, column=1, pady=5, padx=5)
        self.creux.insert(0, "0")

        # Bau
        ttk.Label(params_frame, text="Bau (m): ").grid(row=2, column=0, sticky=tk.W, pady=5, padx=5)
        self.bau = ttk.Entry(params_frame, width=15)
        self.bau.grid(row=2, column=1, pady=5, padx=5)
        self.bau.insert(0, "0")

        # Tirant d'eau
        ttk.Label(params_frame, text="Tirant d'eau (m): ").grid(row=3, column=0, sticky=tk.W, pady=5, padx=5)
        self.tirantEau = ttk.Entry(params_frame, width=15)
        self.tirantEau.grid(row=3, column=1, pady=5, padx=5)
        self.tirantEau.insert(0, "0")

        # Altitude de calcul pour les murailles
        ttk.Label(params_frame, text="Altitude de calcul pour les murailles (m):").grid(row=4, column=0, sticky=tk.W, pady=5, padx=5)
        self.altitude = ttk.Entry(params_frame, width=15)
        self.altitude.grid(row=4, column=1, pady=5, padx=5)
        self.altitude.insert(0, "0")

        # Inclinaison du fond
        ttk.Label(params_frame, text="Inclinaison du fond (°): ").grid(row=5, column=0, sticky=tk.W, pady=5, padx=5)
        self.inclinaison = ttk.Entry(params_frame, width=15)
        self.inclinaison.grid(row=5, column=1, pady=5, padx=5)
        self.inclinaison.insert(0, "0")

        # Methode de calcul
        ttk.Label(params_frame, text="Méthode de calcul:").grid(row=6, column=0, sticky=tk.W, pady=5, padx=5)
        self.calcType = ttk.Combobox(params_frame, width=13, state='readonly')
        self.calcType['values'] = ('BV', 'Hydro')
        self.calcType.current(0)
        self.calcType.grid(row=6, column=1, pady=5, padx=5)


        ttk.Separator(params_frame, orient='horizontal').grid(row=7, column=0, columnspan=2, sticky='ew', pady=10)


        # Portée des varangues
        ttk.Label(params_frame, text="Portée des varangues (m): ").grid(row=8, column=0, sticky=tk.W, pady=5, padx=5)
        self.varangueReach = ttk.Entry(params_frame, width=15)
        self.varangueReach.grid(row=8, column=1, pady=5, padx=5)
        self.varangueReach.insert(0, "0")

        # Espacement des varangues
        ttk.Label(params_frame, text="Espacement des varangues (m): ").grid(row=9, column=0, sticky=tk.W, pady=5, padx=5)
        self.varangueSpacing = ttk.Entry(params_frame, width=15)
        self.varangueSpacing.grid(row=9, column=1, pady=5, padx=5)
        self.varangueSpacing.insert(0, "0")

        # Re des varangues
        ttk.Label(params_frame, text="Re des varangues (MPa): ").grid(row=10, column=0, sticky=tk.W, pady=5, padx=5)
        self.varangueRe = ttk.Entry(params_frame, width=15)
        self.varangueRe.grid(row=10, column=1, pady=5, padx=5)
        self.varangueRe.insert(0, "0")


        ttk.Separator(params_frame, orient='horizontal').grid(row=11, column=0, columnspan=2, sticky='ew', pady=10)


        # Portée des lisses
        ttk.Label(params_frame, text="Portée des lisses (m): ").grid(row=12, column=0, sticky=tk.W, pady=5, padx=5)
        self.lisseReach = ttk.Entry(params_frame, width=15)
        self.lisseReach.grid(row=12, column=1, pady=5, padx=5)
        self.lisseReach.insert(0, "0")

        # Espacement des lisses
        ttk.Label(params_frame, text="Espacement des lisses (m): ").grid(row=13, column=0, sticky=tk.W, pady=5, padx=5)
        self.lisseSpacing = ttk.Entry(params_frame, width=15)
        self.lisseSpacing.grid(row=13, column=1, pady=5, padx=5)
        self.lisseSpacing.insert(0, "0")

        # Re des lisses
        ttk.Label(params_frame, text="Re des lisses (MPa): ").grid(row=14, column=0, sticky=tk.W, pady=5, padx=5)
        self.lisseRe = ttk.Entry(params_frame, width=15)
        self.lisseRe.grid(row=14, column=1, pady=5, padx=5)
        self.lisseRe.insert(0, "0")


        ttk.Separator(params_frame, orient='horizontal').grid(row=15, column=0, columnspan=2, sticky='ew', pady=10)


        # Re de la tôle
        ttk.Label(params_frame, text="Re du bordé (MPa): ").grid(row=16, column=0, sticky=tk.W, pady=5, padx=5)
        self.lisseRe = ttk.Entry(params_frame, width=15)
        self.lisseRe.grid(row=16, column=1, pady=5, padx=5)
        self.lisseRe.insert(0, "0")


        ttk.Separator(params_frame, orient='horizontal').grid(row=17, column=0, columnspan=2, sticky='ew', pady=10)


        # Facteur de sureté
        ttk.Label(params_frame, text="Facteur de sécurité global: ").grid(row=18, column=0, sticky=tk.W, pady=5, padx=5)
        self.securityFactor = ttk.Entry(params_frame, width=15)
        self.securityFactor.grid(row=18, column=1, pady=5, padx=5)
        self.securityFactor.insert(0, "0")


        ttk.Separator(params_frame, orient='horizontal').grid(row=19, column=0, columnspan=2, sticky='ew', pady=10)



        # Nombre de points
        ttk.Label(params_frame, text="Nombre de points:").grid(row=20, column=0, sticky=tk.W, pady=5, padx=5)
        self.nb_points = ttk.Spinbox(params_frame, from_=10, to=1000, width=12)
        self.nb_points.set(100)
        self.nb_points.grid(row=20, column=1, pady=5, padx=5)

        # Boutons
        button_frame = ttk.Frame(params_frame)
        button_frame.grid(row=21, column=0, columnspan=2, pady=20)

        ttk.Button(button_frame, text="Calculer", command=self.calculer, width=15).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Réinitialiser", command=self.reinitialiser, width=15).pack(side=tk.LEFT, padx=5)

        # Frame pour les options d'export
        export_frame = ttk.LabelFrame(parent, text="Export", padding=10)
        export_frame.pack(fill=tk.X, padx=5, pady=5)

        ttk.Button(export_frame, text="Exporter graphique", command=self.exporter_graphique).pack(fill=tk.X, pady=2)
        ttk.Button(export_frame, text="Exporter résultats", command=self.exporter_resultats).pack(fill=tk.X, pady=2)

    def create_output_section(self, parent):
        # Notebook pour organiser les sorties
        notebook = ttk.Notebook(parent)
        notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Onglet Résultats numériques
        results_tab = ttk.Frame(notebook)
        notebook.add(results_tab, text='Résultats')

        ttk.Label(results_tab, text="Valeurs calculées:", font=('Arial', 10, 'bold')).pack(pady=5)

        # Zone de texte avec scrollbar
        text_frame = ttk.Frame(results_tab)
        text_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        scrollbar = ttk.Scrollbar(text_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.result_text = tk.Text(text_frame, height=10, width=50, yscrollcommand=scrollbar.set)
        self.result_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.result_text.yview)

        # Onglet Graphique
        graph_tab = ttk.Frame(notebook)
        notebook.add(graph_tab, text='Graphique')

        # Toolbar frame pour les contrôles du graphique
        toolbar_frame = ttk.Frame(graph_tab)
        toolbar_frame.pack(fill=tk.X, padx=5, pady=5)

        ttk.Label(toolbar_frame, text="Type de graphique:").pack(side=tk.LEFT, padx=5)
        self.graph_type = ttk.Combobox(toolbar_frame, width=15, state='readonly')
        self.graph_type['values'] = ('Ligne', 'Points', 'Barres', 'Aire')
        self.graph_type.current(0)
        self.graph_type.pack(side=tk.LEFT, padx=5)
        self.graph_type.bind('<<ComboboxSelected>>', lambda e: self.actualiser_graphique())

        ttk.Button(toolbar_frame, text="Rafraîchir", command=self.actualiser_graphique).pack(side=tk.LEFT, padx=5)

        # Zone graphique
        self.fig = Figure(figsize=(8, 6), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.ax.set_title("Graphique des résultats")
        self.ax.grid(True, alpha=0.3)

        self.canvas = FigureCanvasTkAgg(self.fig, master=graph_tab)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Variables pour stocker les données
        self.current_x = None
        self.current_y = None

    def get_parametres(self):
        """Récupère tous les paramètres d'entrée sous forme de dictionnaire"""
        try:
            parametres = {
                'rho': float(self.rho.get()),
                'creux': float(self.creux.get()),
                'bau': float(self.bau.get()),
                'tirant d\'eau': float(self.tirantEau.get()),
                'altitude de calcul': float(self.altitude.get()),
                'inclinaison': float(self.inclinaison.get()),
                'facteur de securite': float(self.securityFactor.get()),
                'methode de calcul': self.calcType.get(),

                'nb_points': int(self.nb_points.get())
            }
            return parametres
        except ValueError as e:
            messagebox.showerror("Erreur", f"Valeur invalide: {str(e)}")
            return None

    def calculer(self):
        try:
            # Récupérer les paramètres via la méthode getter
            parametres = self.get_parametres()
            if parametres is None:
                return

            rho = parametres('rho')
            C = parametres('creux')
            B = parametres('bau')
            Te = parametres('tirant d\'eau')
            z = parametres('altitude de calcul')
            alpha = parametres('inclinaison')

            MC = app.get_parametres('type de calcul')


            # Stocker les données
            self.current_x = x
            self.current_y = y

            # Calculer des statistiques
            y_min = np.min(y)
            y_max = np.max(y)
            y_mean = np.mean(y)
            y_std = np.std(y)

            # Afficher les résultats
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, "="*50 + "\n")
            self.result_text.insert(tk.END, "RÉSULTATS DU CALCUL\n")
            self.result_text.insert(tk.END, "="*50 + "\n\n")
            self.result_text.insert(tk.END, f"Type de calcul: {calc_type}\n")
            self.result_text.insert(tk.END, f"Formule: {formule}\n\n")
            self.result_text.insert(tk.END, "Paramètres:\n")
            self.result_text.insert(tk.END, f"  - Paramètre 1: {p1}\n")
            self.result_text.insert(tk.END, f"  - Paramètre 2: {p2}\n")
            self.result_text.insert(tk.END, f"  - Paramètre 3: {p3}\n")
            self.result_text.insert(tk.END, f"  - Nombre de points: {n}\n\n")
            self.result_text.insert(tk.END, "Statistiques:\n")
            self.result_text.insert(tk.END, f"  - Minimum: {y_min:.4f}\n")
            self.result_text.insert(tk.END, f"  - Maximum: {y_max:.4f}\n")
            self.result_text.insert(tk.END, f"  - Moyenne: {y_mean:.4f}\n")
            self.result_text.insert(tk.END, f"  - Écart-type: {y_std:.4f}\n\n")
            self.result_text.insert(tk.END, "="*50 + "\n")

            # Afficher le graphique
            self.afficher_graphique()

            messagebox.showinfo("Succès", "Calcul effectué avec succès!")

        except ValueError as e:
            messagebox.showerror("Erreur", f"Valeurs invalides: {str(e)}")
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors du calcul: {str(e)}")

    def afficher_graphique(self):
        if self.current_x is None or self.current_y is None:
            return

        self.ax.clear()

        graph_type = self.graph_type.get()

        if graph_type == 'Ligne':
            self.ax.plot(self.current_x, self.current_y, 'b-', linewidth=2, label='Résultat')
        elif graph_type == 'Points':
            self.ax.scatter(self.current_x, self.current_y, c='red', s=20, alpha=0.6, label='Résultat')
        elif graph_type == 'Barres':
            # Sous-échantillonnage pour les barres
            step = max(1, len(self.current_x) // 50)
            self.ax.bar(self.current_x[::step], self.current_y[::step], width=0.2, alpha=0.7, label='Résultat')
        else:  # Aire
            self.ax.fill_between(self.current_x, self.current_y, alpha=0.4, label='Résultat')
            self.ax.plot(self.current_x, self.current_y, 'b-', linewidth=1)

        self.ax.set_xlabel('X', fontsize=11)
        self.ax.set_ylabel('Y', fontsize=11)
        self.ax.set_title(f'Graphique - {self.calc_type.get()}', fontsize=12, fontweight='bold')
        self.ax.grid(True, alpha=0.3, linestyle='--')
        self.ax.legend()

        self.fig.tight_layout()
        self.canvas.draw()

    def actualiser_graphique(self):
        if self.current_x is not None and self.current_y is not None:
            self.afficher_graphique()

    def reinitialiser(self):
        self.param1.delete(0, tk.END)
        self.param1.insert(0, "10")
        self.param2.delete(0, tk.END)
        self.param2.insert(0, "5")
        self.param3.delete(0, tk.END)
        self.param3.insert(0, "2")
        self.nb_points.set(100)
        self.calc_type.current(0)
        self.result_text.delete(1.0, tk.END)
        self.ax.clear()
        self.ax.set_title("Graphique des résultats")
        self.ax.grid(True, alpha=0.3)
        self.canvas.draw()
        self.current_x = None
        self.current_y = None

    def exporter_graphique(self):
        if self.current_x is None or self.current_y is None:
            messagebox.showwarning("Attention", "Aucun graphique à exporter. Effectuez d'abord un calcul.")
            return

        filename = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG", "*.png"), ("PDF", "*.pdf"), ("SVG", "*.svg"), ("Tous les fichiers", "*.*")]
        )
        if filename:
            self.fig.savefig(filename, dpi=300, bbox_inches='tight')
            messagebox.showinfo("Succès", f"Graphique exporté: {filename}")

    def exporter_resultats(self):
        contenu = self.result_text.get(1.0, tk.END)
        if not contenu.strip():
            messagebox.showwarning("Attention", "Aucun résultat à exporter. Effectuez d'abord un calcul.")
            return

        filename = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Fichier texte", "*.txt"), ("Tous les fichiers", "*.*")]
        )
        if filename:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(contenu)
            messagebox.showinfo("Succès", f"Résultats exportés: {filename}")

if __name__ == "__main__":
    root = tk.Tk()
    app = CalculInterface(root)
    root.mainloop()
