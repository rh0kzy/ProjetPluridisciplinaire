import sys
import re
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import serial
import serial.tools.list_ports
from PyQt6.QtGui import QAction, QFont, QPalette, QColor, QLinearGradient, QGradient
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QMessageBox, QFileDialog
from mpl_toolkits.mplot3d import Axes3D

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(600, 500)
        MainWindow.setMinimumSize(600, 500)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(9)

        # Palette de couleurs modernisée
        self.primary_color = "#2C3E50"  # Bleu foncé moderne
        self.secondary_color = "#3498DB"  # Bleu clair
        self.accent_color = "#E74C3C"  # Rouge vif
        self.text_color = "#ECF0F1"  # Blanc cassé
        self.background_color = "#F5F7FA"  # Gris très clair
        self.hover_color = "#2980B9"  # Bleu pour le survol
        self.success_color = "#2ECC71"  # Vert pour les actions positives

        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.centralwidget.setStyleSheet(f"""
            QWidget#centralwidget {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 {self.primary_color}, stop:1 #34495E);
                border-radius: 15px;
            }}
            QPushButton {{
                background-color: {self.secondary_color};
                color: {self.text_color};
                border-radius: 8px;
                padding: 12px 20px;
                font-weight: bold;
                border: none;
                min-width: 120px;
            }}
            QPushButton:hover {{
                background-color: {self.hover_color};
                border: 2px solid {self.accent_color};
            }}
            QPushButton:pressed {{
                background-color: {self.accent_color};
                border: 2px solid {self.hover_color};
            }}
            QLineEdit {{
                background-color: rgba(255, 255, 255, 0.9);
                border: 2px solid {self.secondary_color};
                border-radius: 8px;
                padding: 8px;
                color: {self.primary_color};
                font-weight: bold;
                min-height: 25px;
            }}
            QComboBox {{
                background-color: rgba(255, 255, 255, 0.9);
                border: 2px solid {self.secondary_color};
                border-radius: 8px;
                padding: 8px;
                color: {self.primary_color};
                font-weight: bold;
                min-height: 25px;
            }}
            QComboBox QAbstractItemView {{
                background-color: white;
                color: {self.primary_color};
                selection-background-color: {self.secondary_color};
                border: 1px solid {self.secondary_color};
                border-radius: 8px;
            }}
            QLabel {{
                color: {self.text_color};
                font-weight: bold;
                font-size: 12px;
            }}
            QGroupBox {{
                color: {self.text_color};
                border: 2px solid {self.secondary_color};
                border-radius: 12px;
                margin-top: 15px;
                padding-top: 15px;
                background-color: rgba(255, 255, 255, 0.1);
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: 15px;
                padding: 0 8px;
                color: {self.text_color};
                font-weight: bold;
            }}
            QStatusBar {{
                background-color: {self.primary_color};
                color: {self.text_color};
                font-weight: bold;
            }}
            QMenuBar {{
                background-color: {self.primary_color};
                color: {self.text_color};
            }}
            QMenuBar::item:selected {{
                background-color: {self.secondary_color};
            }}
            QMenu {{
                background-color: {self.primary_color};
                color: {self.text_color};
                border: 1px solid {self.secondary_color};
            }}
            QMenu::item:selected {{
                background-color: {self.secondary_color};
            }}
        """)

        self.main_layout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.main_layout.setContentsMargins(15, 10, 15, 10)  # Marges réduites
        self.main_layout.setSpacing(8)  # Espacement réduit entre les éléments

        # Section fichier avec icônes
        self.file_group = QtWidgets.QGroupBox("📂 Entrée des Données")
        self.file_group.setFont(font)
        self.file_group.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        
        self.file_layout = QtWidgets.QVBoxLayout(self.file_group)
        
        # Bouton charger fichier avec icône
        self.load_file_btn = QtWidgets.QPushButton("📂 Charger un fichier")
        self.load_file_btn.setFont(font)
        self.load_file_btn.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        self.file_layout.addWidget(self.load_file_btn)

        # Champ de saisie avec icône
        self.radii_layout = QtWidgets.QHBoxLayout()
        self.radii_label = QtWidgets.QLabel("📏 Rayons:")
        self.radii_label.setFont(font)
        self.radii_label.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        self.radii_layout.addWidget(self.radii_label)
        
        self.radii_input = QtWidgets.QLineEdit()
        self.radii_input.setFont(font)
        self.radii_input.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        self.radii_input.setPlaceholderText("Entrez les valeurs séparées par des virgules")
        self.radii_layout.addWidget(self.radii_input)
        self.file_layout.addLayout(self.radii_layout)

        # Info angles avec style amélioré
        self.angles_info = QtWidgets.QLabel("ℹ️ Les angles sont générés automatiquement selon le nombre de rayons")
        info_font = QtGui.QFont(font)
        info_font.setPointSize(9)
        info_font.setItalic(True)
        self.angles_info.setFont(info_font)
        self.angles_info.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        self.angles_info.setStyleSheet(f"color: {self.secondary_color};")
        self.file_layout.addWidget(self.angles_info)

        # Menu déroulant avec icône
        self.sections_layout = QtWidgets.QHBoxLayout()
        self.sections_label = QtWidgets.QLabel("📅 Sélection par date:")
        self.sections_label.setFont(font)
        self.sections_label.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        self.sections_layout.addWidget(self.sections_label)
        
        self.sections_combo = QtWidgets.QComboBox()
        self.sections_combo.setFont(font)
        self.sections_combo.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        self.sections_combo.setPlaceholderText("Sélectionnez une date")
        self.sections_layout.addWidget(self.sections_combo)
        self.file_layout.addLayout(self.sections_layout)

        self.main_layout.addWidget(self.file_group)

        # Section visualisation avec style moderne
        self.viz_group = QtWidgets.QGroupBox("📊 Visualisation")
        self.viz_group.setFont(font)
        self.viz_group.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        
        # Création d'une grille pour les boutons
        self.viz_layout = QtWidgets.QGridLayout(self.viz_group)
        self.viz_layout.setSpacing(10)
        
        # Boutons de visualisation avec icônes
        self.polar_btn = QtWidgets.QPushButton("📈 Tracer en polaire")
        self.polar_btn.setFont(font)
        self.polar_btn.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        self.polar_btn.setMinimumHeight(40)
        self.viz_layout.addWidget(self.polar_btn, 0, 0)
        
        self.sphere_btn = QtWidgets.QPushButton("🌐 Tracer en sphérique")
        self.sphere_btn.setFont(font)
        self.sphere_btn.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        self.sphere_btn.setMinimumHeight(40)
        self.viz_layout.addWidget(self.sphere_btn, 0, 1)
        
        self.all_graphs_btn = QtWidgets.QPushButton("📊 Tracer tous les graphes")
        self.all_graphs_btn.setFont(font)
        self.all_graphs_btn.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        self.all_graphs_btn.setMinimumHeight(40)
        self.viz_layout.addWidget(self.all_graphs_btn, 1, 0)
        
        self.combine_btn = QtWidgets.QPushButton("🌐 Tracer en sphérique combiné")
        self.combine_btn.setFont(font)
        self.combine_btn.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        self.combine_btn.setMinimumHeight(40)
        self.viz_layout.addWidget(self.combine_btn, 1, 1)
        
        # Ajuster les colonnes pour qu'elles aient la même largeur
        self.viz_layout.setColumnStretch(0, 1)
        self.viz_layout.setColumnStretch(1, 1)
        
        self.main_layout.addWidget(self.viz_group)

        # Barre d'état avec style moderne
        self.status_bar = QtWidgets.QStatusBar()
        self.status_bar.setFont(font)
        MainWindow.setStatusBar(self.status_bar)

        MainWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(MainWindow)
        
        # Définir les références
        self.input_rayons = self.radii_input
        self.barre_etat = self.status_bar
        
        # Variable pour stocker les sections de données
        self.sections_donnees = []

        # Connecter les boutons
        self.load_file_btn.clicked.connect(self.lire_fichier)
        self.polar_btn.clicked.connect(lambda: self.mettre_a_jour_graphique("polaire"))
        self.sphere_btn.clicked.connect(lambda: self.mettre_a_jour_graphique("spherique"))
        self.all_graphs_btn.clicked.connect(self.tracer_toutes_sections)
        self.sections_combo.currentIndexChanged.connect(self.charger_section_selectionnee)
        self.combine_btn.clicked.connect(self.tracer_graphique_combine)

        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Analyse de Diagramme de Rayonnement"))

    def detecter_sections_par_date(self, contenu):
        """Détecte les différentes sections de données par date et heure dans le fichier"""
        lignes = contenu.strip().split('\n')
        
        # Regex pour détecter les formats de date (MM-DD-YYYY ou DD-MM-YYYY)
        date_pattern = r'(\d{2}-\d{2}-\d{4})'
        
        sections = []
        dates = []
        section_courante = []
        date_courante = None
        heure_courante = None
        
        i = 0
        while i < len(lignes):
            ligne = lignes[i].strip()
            
            # Détection d'une date
            if re.match(date_pattern, ligne) and i + 1 < len(lignes):
                # Si nous avions déjà une section en cours, on l'enregistre
                if section_courante and date_courante:
                    sections.append((date_courante, heure_courante, section_courante))
                
                # Nouvelle date trouvée
                date_courante = ligne
                
                # Vérifie si la ligne suivante est une heure (HH:MM:SS)
                if i + 1 < len(lignes) and re.match(r'\d{2}:\d{2}:\d{2}', lignes[i+1].strip()):
                    heure_courante = lignes[i+1].strip()
                    i += 2  # On saute la date et l'heure
                else:
                    heure_courante = "00:00:00"
                    i += 1  # On saute seulement la date
                    
                dates.append(f"{date_courante} {heure_courante}")
                section_courante = []
                
            # Sinon, on ajoute la valeur à la section courante si c'est un nombre
            elif ligne and date_courante is not None:
                try:
                    valeur = float(ligne)
                    section_courante.append(valeur)
                except ValueError:
                    # Si ce n'est pas un nombre valide et pas une date/heure reconnue, on l'ignore
                    pass
                i += 1
            else:
                i += 1
        
        # N'oublions pas d'ajouter la dernière section
        if section_courante and date_courante:
            sections.append((date_courante, heure_courante, section_courante))
        
        return sections

    def lire_fichier(self):
        """Ouvre une boîte de dialogue pour charger un fichier de données"""
        options = QFileDialog.Option(0)
        file_name, _ = QFileDialog.getOpenFileName(
            None, "Choisir un fichier", "",
            "Fichiers de données (*.csv *.txt);;Tous les fichiers (*)",
            options=options
        )

        if file_name:
            try:
                # Lire le fichier
                if file_name.endswith('.txt'):
                    with open(file_name, 'r') as f:
                        contenu = f.read()
                        
                        # Vérifier si le fichier contient des sections par date
                        self.sections_donnees = self.detecter_sections_par_date(contenu)
                        
                        if self.sections_donnees:
                            # Mettre à jour le menu déroulant avec les dates
                            self.sections_combo.clear()
                            for date, heure, _ in self.sections_donnees:
                                self.sections_combo.addItem(f"{date} {heure}")
                            
                            # Charger la première section
                            if self.sections_donnees:
                                self.charger_section_selectionnee(0)
                                
                            self.barre_etat.showMessage(f"Fichier {file_name} chargé avec succès: {len(self.sections_donnees)} sections trouvées", 5000)
                        else:
                            # Comportement original si pas de sections par date
                            lignes = contenu.split('\n')
                            rayons = [float(ligne.strip()) for ligne in lignes if ligne.strip() and re.match(r'^-?\d+\.?\d*$', ligne.strip())]
                            self.input_rayons.setText(','.join(map(str, rayons)))
                            self.barre_etat.showMessage(f"Fichier {file_name} chargé avec succès", 3000)
                else:
                    df = pd.read_csv(file_name)
                    if 'rayon' in df.columns:
                        rayons = df['rayon'].values
                        self.input_rayons.setText(','.join(map(str, rayons)))
                        self.barre_etat.showMessage(f"Fichier {file_name} chargé avec succès", 3000)
                    else:
                        QMessageBox.critical(None, "Erreur", "Le fichier doit contenir une colonne 'rayon'")
                        return

            except Exception as e:
                QMessageBox.critical(None, "Erreur", f"Impossible de lire le fichier: {str(e)}")

    def charger_section_selectionnee(self, index):
        """Charge la section sélectionnée dans le champ de texte"""
        if index >= 0 and index < len(self.sections_donnees):
            _, _, rayons = self.sections_donnees[index]
            self.input_rayons.setText(','.join(map(str, rayons)))
            self.barre_etat.showMessage(f"Section '{self.sections_combo.currentText()}' chargée", 3000)

    def collecter_donnees(self):
        """Collecte et prépare les données pour le tracé"""
        try:
            rayons_str = self.input_rayons.text().strip()
            if not rayons_str:
                QMessageBox.critical(None, "Erreur", "Veuillez entrer des rayons.")
                return None

            # Séparer les valeurs et convertir en float
            rayons = []
            for val in rayons_str.split(','):
                val = val.strip()
                if val.endswith('dBi'):
                    val = val[:-3]  # Enlever 'dBi'
                try:
                    rayons.append(float(val))
                except ValueError:
                    QMessageBox.critical(None, "Erreur", f"Valeur invalide: {val}")
                    return None

            if not rayons:
                QMessageBox.critical(None, "Erreur", "La liste des rayons est vide.")
                return None

            rayons = np.array(rayons)

            # Générer les angles
            angles = np.linspace(0, 360, len(rayons), endpoint=False)

            return pd.DataFrame({'angle': angles, 'rayon': rayons})

        except ValueError:
            QMessageBox.critical(None, "Erreur",
                               "Format invalide. Entrez des nombres séparés par des virgules.")
            return None
        
    def tracer_polaire(self, donnees, titre=None):
        """Trace le diagramme polaire"""
        try:
            plt.style.use('seaborn-v0_8-darkgrid')
            fig = plt.figure(figsize=(8, 6))
            ax = plt.subplot(111, projection='polar')
            
            angles = np.deg2rad(donnees['angle'])
            rayons = donnees['rayon']
            
            ax.plot(angles, rayons, 
                   color=self.accent_color,
                   linewidth=2)
            
            if titre:
                ax.set_title(f"Diagramme Polaire - {titre}", pad=20)
            else:
                ax.set_title("Diagramme Polaire (dBi)", pad=20)
            ax.grid(True)
            
            # Fonction pour mettre à jour les ticks et labels
            def update_ticks():
                rmin, rmax = ax.get_ylim()
                # Générer 5 ticks entre les limites actuelles
                r_ticks = np.linspace(rmin, rmax, 5)
                ax.set_rticks(r_ticks)
                # Formater les labels avec 2 décimales et ajouter dBi
                ax.set_yticklabels([f"{tick:.2f} dBi" for tick in r_ticks])
            
            # Initialiser les ticks
            update_ticks()
            
            plt.tight_layout()
            plt.show()
            
        except Exception as e:
            QMessageBox.critical(None, "Erreur", f"Erreur dans le tracé polaire : {str(e)}")
            self.barre_etat.showMessage("Erreur lors du tracé polaire", 3000)
        
    def tracer_spherique(self, donnees, titre=None):
        """Trace le diagramme sphérique 3D"""
        try:
            plt.style.use('seaborn-v0_8-darkgrid')
            
            # Augmentation de la résolution
            resolution = 100  # Augmenté de 30 à 100
            
            theta = np.deg2rad(donnees['angle'].values)
            r = donnees['rayon'].values
            
            # Création d'une grille plus fine
            theta_grid = np.linspace(0, 2*np.pi, resolution)
            phi_grid = np.linspace(0, np.pi, resolution)
            theta_mesh, phi_mesh = np.meshgrid(theta_grid, phi_grid)
            
            # Interpolation plus précise
            r_grid = np.interp(theta_mesh.flatten(), 
                             np.linspace(0, 2*np.pi, len(r)), 
                             r).reshape(theta_mesh.shape)
            
            X = r_grid * np.sin(phi_mesh) * np.cos(theta_mesh)
            Y = r_grid * np.sin(phi_mesh) * np.sin(theta_mesh)
            Z = r_grid * np.cos(phi_mesh)
            
            # Configuration de la figure pour une meilleure qualité
            plt.rcParams['figure.dpi'] = 150  # Augmenté de 80 à 150
            plt.rcParams['savefig.dpi'] = 150
            plt.rcParams['figure.figsize'] = [12, 10]  # Taille de figure augmentée
            
            fig = plt.figure()
            ax = fig.add_subplot(111, projection='3d')
            
            # Normalisation des couleurs
            norm = plt.Normalize(np.min(r), np.max(r))
            
            # Tracé de la surface avec une meilleure qualité
            surf = ax.plot_surface(X, Y, Z, 
                                 cmap='viridis',
                                 norm=norm,
                                 alpha=0.8,
                                 rcount=resolution,
                                 ccount=resolution,
                                 antialiased=True,  # Activé l'antialiasing
                                 linewidth=0.5)  # Ajout de lignes de contour
            
            fig.colorbar(surf, ax=ax, shrink=0.5, label='dBi')
            
            if titre:
                ax.set_title(f"Diagramme 3D - {titre}", fontsize=12)
            else:
                ax.set_title("Diagramme 3D (dBi)", fontsize=12)
            ax.view_init(elev=30, azim=45)
            
            # Optimisations pour une meilleure qualité
            ax.set_axis_off()
            ax.grid(False)
            
            plt.tight_layout()
            plt.show(block=False)
            
        except Exception as e:
            QMessageBox.critical(None, "Erreur", f"Erreur dans le tracé sphérique : {str(e)}")
            self.barre_etat.showMessage("Erreur lors du tracé sphérique", 3000)

    def tracer_2d(self, donnees, titre=None):
        """Trace le diagramme en 2D"""
        try:
            plt.style.use('seaborn-v0_8-darkgrid')
            fig = plt.figure(figsize=(8, 6))
            ax = plt.subplot(111)
            
            angles = donnees['angle']
            rayons = donnees['rayon']
            
            ax.plot(angles, rayons, 
                   color=self.accent_color,
                   linewidth=2)
            
            if titre:
                ax.set_title(f"Diagramme 2D - {titre}", pad=20)
            else:
                ax.set_title("Diagramme 2D (dBi)", pad=20)
            
            ax.set_xlabel('Angle (degrés)')
            ax.set_ylabel('Gain (dBi)')
            ax.grid(True)
            
            # Ajuster les ticks de l'axe Y
            ymin, ymax = ax.get_ylim()
            y_ticks = np.linspace(ymin, ymax, 5)
            ax.set_yticks(y_ticks)
            ax.set_yticklabels([f"{tick:.2f} dBi" for tick in y_ticks])
            
            plt.tight_layout()
            plt.show()
            
        except Exception as e:
            QMessageBox.critical(None, "Erreur", f"Erreur dans le tracé 2D : {str(e)}")
            self.barre_etat.showMessage("Erreur lors du tracé 2D", 3000)

    def mettre_a_jour_graphique(self, mode):
        """Met à jour le graphique selon le mode sélectionné"""
        donnees = self.collecter_donnees()
        if donnees is not None:
            titre = self.sections_combo.currentText() if self.sections_combo.currentIndex() >= 0 else None
            
            if mode == "polaire":
                self.tracer_polaire(donnees, titre)
            elif mode == "spherique":
                self.tracer_spherique(donnees, titre)
            elif mode == "2d":
                self.tracer_2d(donnees, titre)
    
    def tracer_toutes_sections(self):
        """Trace les graphiques pour toutes les sections détectées"""
        if not self.sections_donnees:
            QMessageBox.information(None, "Information", "Aucune section par date détectée dans le fichier.")
            return
        
        try:
            plt.style.use('seaborn-v0_8-darkgrid')
            # Changer la disposition pour avoir les graphiques horizontalement
            fig, axs = plt.subplots(1, len(self.sections_donnees), figsize=(4*len(self.sections_donnees), 10), 
                                   subplot_kw={'projection': 'polar'})
            
            # Si une seule section, axs n'est pas un tableau
            if len(self.sections_donnees) == 1:
                axs = [axs]
                
            for i, (date, heure, rayons) in enumerate(self.sections_donnees):
                # Préparation des données
                rayons_arr = np.array(rayons)
                max_val = np.max(rayons_arr)
                rayons_normalises = rayons_arr - max_val
                angles = np.linspace(0, 2*np.pi, len(rayons_arr), endpoint=False)
                
                # Tracé
                axs[i].plot(angles, rayons_normalises, color=self.accent_color, linewidth=2)
                axs[i].set_title(f"{date} {heure}", pad=20)
                axs[i].grid(True)
                
                # Ajustement des ticks
                r_ticks = np.linspace(np.min(rayons_normalises), 0, 5)
                axs[i].set_rticks(r_ticks)
                axs[i].set_yticklabels([f"{tick:.1f}" for tick in r_ticks])
            
            plt.tight_layout()
            plt.subplots_adjust(wspace=0.5)  # Ajuster l'espacement horizontal
            plt.show()
            
            self.barre_etat.showMessage(f"Graphiques de toutes les sections tracés ({len(self.sections_donnees)} sections)", 3000)
            
        except Exception as e:
            QMessageBox.critical(None, "Erreur", f"Erreur lors du tracé des sections : {str(e)}")
            self.barre_etat.showMessage("Erreur lors du tracé des sections", 3000)

    def tracer_spherique_combine(self, donnees1, donnees2, titre1=None, titre2=None):
        """Trace deux diagrammes sphériques 3D combinés"""
        try:
            plt.style.use('seaborn-v0_8-darkgrid')
            
            # Augmentation de la résolution
            resolution = 100  # Augmenté de 30 à 100
            
            # Préparation des données pour le premier graphique
            theta1 = np.deg2rad(donnees1['angle'].values)
            r1 = donnees1['rayon'].values
            
            # Création d'une grille plus fine
            theta_grid1 = np.linspace(0, 2*np.pi, resolution)
            phi_grid1 = np.linspace(0, np.pi, resolution)
            theta_mesh1, phi_mesh1 = np.meshgrid(theta_grid1, phi_grid1)
            
            # Interpolation plus précise
            r_grid1 = np.interp(theta_mesh1.flatten(), 
                              np.linspace(0, 2*np.pi, len(r1)), 
                              r1).reshape(theta_mesh1.shape)
            
            X1 = r_grid1 * np.sin(phi_mesh1) * np.cos(theta_mesh1)
            Y1 = r_grid1 * np.sin(phi_mesh1) * np.sin(theta_mesh1)
            Z1 = r_grid1 * np.cos(phi_mesh1)
            
            # Préparation des données pour le deuxième graphique
            theta2 = np.deg2rad(donnees2['angle'].values)
            r2 = donnees2['rayon'].values
            
            # Utiliser la même grille pour les deux graphiques
            theta_mesh2, phi_mesh2 = np.meshgrid(theta_grid1, phi_grid1)
            
            r_grid2 = np.interp(theta_mesh2.flatten(), 
                              np.linspace(0, 2*np.pi, len(r2)), 
                              r2).reshape(theta_mesh2.shape)
            
            X2 = r_grid2 * np.sin(phi_mesh2) * np.cos(theta_mesh2)
            Y2 = r_grid2 * np.sin(phi_mesh2) * np.sin(theta_mesh2)
            Z2 = r_grid2 * np.cos(phi_mesh2)
            
            # Configuration de la figure pour une meilleure qualité
            plt.rcParams['figure.dpi'] = 150
            plt.rcParams['savefig.dpi'] = 150
            plt.rcParams['figure.figsize'] = [12, 10]
            
            fig = plt.figure()
            ax = fig.add_subplot(111, projection='3d')
            
            # Normalisation des couleurs
            norm1 = plt.Normalize(np.min(r1), np.max(r1))
            norm2 = plt.Normalize(np.min(r2), np.max(r2))
            
            # Tracé des surfaces avec une meilleure qualité
            surf1 = ax.plot_surface(X1, Y1, Z1, 
                                  cmap='viridis',
                                  norm=norm1,
                                  alpha=0.7,
                                  rcount=resolution,
                                  ccount=resolution,
                                  antialiased=True,
                                  linewidth=0.5)
            
            surf2 = ax.plot_surface(X2, Y2, Z2, 
                                  cmap='plasma',
                                  norm=norm2,
                                  alpha=0.7,
                                  rcount=resolution,
                                  ccount=resolution,
                                  antialiased=True,
                                  linewidth=0.5)
            
            # Optimisations pour une meilleure qualité
            ax.set_axis_off()
            ax.grid(False)
            
            # Titre simplifié
            if titre1 and titre2:
                ax.set_title(f"3D: {titre1} & {titre2}", fontsize=12)
            else:
                ax.set_title("Diagramme 3D Combiné", fontsize=12)
            
            plt.tight_layout()
            plt.show(block=False)
            
        except Exception as e:
            QMessageBox.critical(None, "Erreur", f"Erreur dans le tracé sphérique combiné : {str(e)}")
            self.barre_etat.showMessage("Erreur lors du tracé sphérique combiné", 3000)

    def tracer_graphique_combine(self):
        """Trace un graphique 3D combiné de deux sections"""
        if len(self.sections_donnees) < 2:
            QMessageBox.warning(None, "Attention", "Au moins deux sections sont nécessaires pour créer un graphique combiné.")
            return
            
        # Créer une boîte de dialogue pour sélectionner les deux sections
        dialog = QtWidgets.QDialog()
        dialog.setWindowTitle("Sélection des sections à combiner")
        layout = QtWidgets.QVBoxLayout()
        
        # Premier menu déroulant
        label1 = QtWidgets.QLabel("Première section:")
        combo1 = QtWidgets.QComboBox()
        for date, heure, _ in self.sections_donnees:
            combo1.addItem(f"{date} {heure}")
            
        # Deuxième menu déroulant
        label2 = QtWidgets.QLabel("Deuxième section:")
        combo2 = QtWidgets.QComboBox()
        for date, heure, _ in self.sections_donnees:
            combo2.addItem(f"{date} {heure}")
            
        # Bouton OK
        button = QtWidgets.QPushButton("Tracer")
        button.clicked.connect(dialog.accept)
        
        # Ajout des widgets à la boîte de dialogue
        layout.addWidget(label1)
        layout.addWidget(combo1)
        layout.addWidget(label2)
        layout.addWidget(combo2)
        layout.addWidget(button)
        
        dialog.setLayout(layout)
        
        if dialog.exec() == QtWidgets.QDialog.DialogCode.Accepted:
            index1 = combo1.currentIndex()
            index2 = combo2.currentIndex()
            
            if index1 == index2:
                QMessageBox.warning(None, "Attention", "Veuillez sélectionner deux sections différentes.")
                return
                
            # Récupérer les données des deux sections
            _, _, rayons1 = self.sections_donnees[index1]
            _, _, rayons2 = self.sections_donnees[index2]
            
            # Préparer les données pour le tracé
            angles1 = np.linspace(0, 360, len(rayons1), endpoint=False)
            angles2 = np.linspace(0, 360, len(rayons2), endpoint=False)
            
            donnees1 = pd.DataFrame({'angle': angles1, 'rayon': rayons1})
            donnees2 = pd.DataFrame({'angle': angles2, 'rayon': rayons2})
            
            # Tracer le graphique combiné
            self.tracer_spherique_combine(donnees1, donnees2, 
                                        combo1.currentText(),
                                        combo2.currentText())


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        # Ajouter un menu
        self.menu_bar = QtWidgets.QMenuBar(self)
        self.setMenuBar(self.menu_bar)
        
        # Menu Fichier
        self.menu_fichier = QtWidgets.QMenu("Fichier", self)
        self.menu_bar.addMenu(self.menu_fichier)
        
        # Actions pour le menu Fichier
        self.action_ouvrir = QAction("Ouvrir...", self)
        self.action_ouvrir.triggered.connect(self.ui.lire_fichier)
        self.menu_fichier.addAction(self.action_ouvrir)
        
        self.menu_fichier.addSeparator()
        
        self.action_quitter = QAction("Quitter", self)
        self.action_quitter.triggered.connect(self.close)
        self.menu_fichier.addAction(self.action_quitter)
        
        # Menu Aide
        self.menu_aide = QtWidgets.QMenu("Aide", self)
        self.menu_bar.addMenu(self.menu_aide)
        
    def afficher_aide(self):
        """Affiche la boîte de dialogue d'aide"""
        about_text = """
        
        <p>Version 1.0</p>
        <p>Cet outil permet d'analyser et de visualiser des diagrammes de rayonnement d'antennes.</p>
        <p>Fonctionnalités:</p>
        <ul>
            <li>Chargement de données à partir de fichiers</li>
            <li>Visualisation en diagramme polaire et 3D</li>
            <li>Analyse de multiples sections de données</li>
        </ul>
        <p>© 2025 Laboratoire d'Antennes</p>
        """
        
        QMessageBox.about(self, "À propos de l'Analyseur", about_text)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())