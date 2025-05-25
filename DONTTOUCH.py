import sys
import re
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mayavi import mlab
from PyQt6.QtGui import QAction 
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QMessageBox, QFileDialog
from reconstruct_3d_pattern import reconstruct_3d_pattern, plot_3d_pattern

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 700)
        font = QtGui.QFont()
        font.setFamily("Montserrat")
        font.setPointSize(12)

        # Palette de couleurs
        self.primary_color = "#031045"
        self.secondary_color = "#4ECDC4"
        self.accent_color = "#FF6B6B"
        self.text_color = "#FFFFFF"
        self.background_color = "#F5F7FA"

        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.centralwidget.setStyleSheet(f"""
            QWidget#centralwidget {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 {self.primary_color}, stop:1 #1a3a8f);
                border-radius: 15px;
            }}
            QPushButton {{
                background-color: {self.text_color};
                color: {self.primary_color};
                border-radius: 10px;
                padding: 10px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {self.secondary_color};
                color: {self.text_color};
            }}
            QLineEdit {{
                background-color: rgba(255, 255, 255, 0.9);
                border: 2px solid {self.secondary_color};
                border-radius: 8px;
                padding: 5px;
                color: {self.primary_color};
                font-weight: bold;
            }}
            QComboBox {{
                background-color: rgba(255, 255, 255, 0.9);
                border: 2px solid {self.secondary_color};
                border-radius: 8px;
                padding: 5px;
                color: {self.primary_color};
                font-weight: bold;
            }}
            QComboBox QAbstractItemView {{
                background-color: white;
                color: {self.primary_color};
                selection-background-color: {self.secondary_color};
                font-weight: bold;
            }}
            QLabel {{
                font-weight: bold;
            }}
            QGroupBox {{
                color: {self.text_color};
                border: 2px solid {self.secondary_color};
                border-radius: 10px;
                margin-top: 10px;
                font-weight: bold;
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
                font-weight: bold;
            }}
            QStatusBar {{
                font-weight: bold;
            }}
        """)

        self.main_layout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.main_layout.setContentsMargins(40, 30, 40, 30)
        self.main_layout.setSpacing(20)

        # En-tête
        self.header = QtWidgets.QHBoxLayout()
        self.title_label = QtWidgets.QLabel("Analyse de Diagramme de Rayonnement")
        title_font = QtGui.QFont(font)
        title_font.setPointSize(18)
        title_font.setBold(True)
        self.title_label.setFont(title_font)
        self.title_label.setStyleSheet(f"color: {self.text_color}; font-weight: bold;")
        self.header.addWidget(self.title_label)
        self.header.addStretch()
        self.main_layout.addLayout(self.header)

        # Section fichier
        self.file_group = QtWidgets.QGroupBox("Entrée des Données")
        self.file_group.setFont(font)
        self.file_group.setStyleSheet(f"""
            QGroupBox {{
                color: {self.text_color};
                border: 2px solid {self.secondary_color};
                border-radius: 10px;
                margin-top: 10px;
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }}
        """)
        
        self.file_layout = QtWidgets.QVBoxLayout(self.file_group)
        
        # Bouton charger fichier
        self.load_file_btn = QtWidgets.QPushButton("Charger un fichier 📂")
        self.load_file_btn.setFont(font)
        self.file_layout.addWidget(self.load_file_btn)

        # Champ de saisie
        self.radii_layout = QtWidgets.QHBoxLayout()
        self.radii_label = QtWidgets.QLabel("Rayons 📏:")
        self.radii_label.setFont(font)
        self.radii_label.setStyleSheet(f"color: {self.text_color}; font-weight: bold;")
        self.radii_layout.addWidget(self.radii_label)
        
        self.radii_input = QtWidgets.QLineEdit()
        self.radii_input.setFont(font)
        self.radii_input.setPlaceholderText("Entrez les valeurs séparées par des virgules")
        self.radii_layout.addWidget(self.radii_input)
        self.file_layout.addLayout(self.radii_layout)

        # Info angles
        self.angles_info = QtWidgets.QLabel("*Les angles sont générés automatiquement selon le nombre de rayons")
        info_font = QtGui.QFont(font)
        info_font.setPointSize(10)
        info_font.setItalic(True)
        info_font.setBold(True)
        self.angles_info.setFont(info_font)
        self.angles_info.setStyleSheet(f"color: {self.secondary_color}; font-weight: bold;")
        self.file_layout.addWidget(self.angles_info)

        # Menu déroulant pour les sections par date
        self.sections_layout = QtWidgets.QHBoxLayout()
        self.sections_label = QtWidgets.QLabel("Sélection par date 📅:")
        self.sections_label.setFont(font)
        self.sections_label.setStyleSheet(f"color: {self.text_color}; font-weight: bold;")
        self.sections_layout.addWidget(self.sections_label)
        
        self.sections_combo = QtWidgets.QComboBox()
        self.sections_combo.setFont(font)
        self.sections_combo.setPlaceholderText("Sélectionnez une date")
        self.sections_layout.addWidget(self.sections_combo)
        self.file_layout.addLayout(self.sections_layout)

        self.main_layout.addWidget(self.file_group)

        # Section visualisation
        self.viz_group = QtWidgets.QGroupBox("Visualisation")
        self.viz_group.setFont(font)
        self.viz_group.setStyleSheet(f"""
            QGroupBox {{
                color: {self.text_color};
                border: 2px solid {self.secondary_color};
                border-radius: 10px;
                margin-top: 10px;
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }}
        """)
        
        # Changer le layout en GridLayout pour une meilleure organisation des boutons
        self.viz_layout = QtWidgets.QGridLayout(self.viz_group)
        
        # Bouton polaire
        self.polar_btn = QtWidgets.QPushButton("Tracer en polaire 📊")
        self.polar_btn.setFont(font)
        self.viz_layout.addWidget(self.polar_btn, 0, 0)
        
        # Bouton sphérique
        self.sphere_btn = QtWidgets.QPushButton("Tracer en sphérique 🌐")
        self.sphere_btn.setFont(font)
        self.viz_layout.addWidget(self.sphere_btn, 0, 1)
        
        # Bouton 2D
        self.twod_btn = QtWidgets.QPushButton("Tracer en 2D 📈")
        self.twod_btn.setFont(font)
        self.viz_layout.addWidget(self.twod_btn, 1, 0)
        
        # Bouton combiné
        self.combine_btn = QtWidgets.QPushButton("Tracer combiné 🔄")
        self.combine_btn.setFont(font)
        self.viz_layout.addWidget(self.combine_btn, 1, 1)
        
        # Bouton pour tracer tous les graphiques
        self.all_graphs_btn = QtWidgets.QPushButton("Tracer tout les graphes 📉")
        self.all_graphs_btn.setFont(font)
        self.viz_layout.addWidget(self.all_graphs_btn, 2, 0, 1, 2)
        
        # Ajuster les colonnes pour qu'elles aient la même largeur
        self.viz_layout.setColumnStretch(0, 1)
        self.viz_layout.setColumnStretch(1, 1)
        
        self.main_layout.addWidget(self.viz_group)        # Barre d'état
        self.status_bar = QtWidgets.QStatusBar()
        self.status_bar.setFont(font)
        self.status_bar.setStyleSheet(f"color: {self.text_color}; font-weight: bold;")
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
        self.twod_btn.clicked.connect(lambda: self.mettre_a_jour_graphique("2d"))
        self.combine_btn.clicked.connect(lambda: self.mettre_a_jour_graphique("combine"))
        self.all_graphs_btn.clicked.connect(self.tracer_toutes_sections)
        self.sections_combo.currentIndexChanged.connect(self.charger_section_selectionnee)

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

            rayons = list(map(float, rayons_str.split(',')))
            if not rayons:
                QMessageBox.critical(None, "Erreur", "La liste des rayons est vide.")
                return None

            rayons = np.array(rayons)

            # Normalisation: valeurs - max
            max_val = np.max(rayons)
            rayons_normalises = rayons - max_val

            # Générer les angles
            angles = np.linspace(0, 360, len(rayons), endpoint=False)

            return pd.DataFrame({'angle': angles, 'rayon': rayons_normalises})

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
                ax.set_title("Diagramme Polaire Normalisé", pad=20)
            ax.grid(True)
            
            # Ajustement des ticks
            r_ticks = np.linspace(np.min(rayons), 0, 5)
            ax.set_rticks(r_ticks)
            ax.set_yticklabels([f"{tick:.1f}" for tick in r_ticks])
            
            plt.tight_layout()
            plt.show()
            
        except Exception as e:
            QMessageBox.critical(None, "Erreur", f"Erreur dans le tracé polaire : {str(e)}")
            self.barre_etat.showMessage("Erreur lors du tracé polaire", 3000)
        
    def tracer_spherique(self, donnees, titre=None):
        """Trace un pattern sphérique 3D à partir des données chargées."""
        try:
            # Récupération des données exactes (sans normalisation pour l'export)
            angles_deg = donnees['angle'].values
            rayons = donnees['rayon'].values

            # Conversion en radians
            angles_rad = np.deg2rad(angles_deg)

            # Conversion des rayons en valeurs linéaires (si les fonctions 3D attendent cela)
            # Si les valeurs de rayons sont déjà linéaires, commenter la ligne ci-dessous
            rayons_lin = 10 ** (rayons / 20) # Convertir dB en linéaire

            # Reconstruction du pattern 3D
            # Assurez-vous que reconstruct_3d_pattern peut gérer vos données d'angle
            pattern_3d, theta_grid, phi_grid = reconstruct_3d_pattern(rayons_lin, angles_rad)

            # Création du titre
            plot_title = f"Diagramme Sphérique 3D - {titre}" if titre else "Diagramme Sphérique 3D"

            # Tracé du pattern 3D
            plot_3d_pattern(pattern_3d, theta_grid, phi_grid, title=plot_title)
            
            self.barre_etat.showMessage("Tracé sphérique effectué avec succès", 3000)

        except Exception as e:
            QMessageBox.critical(None, "Erreur", f"Erreur dans le tracé sphérique : {str(e)}")
            self.barre_etat.showMessage("Erreur lors du tracé sphérique", 3000)

    def tracer_2d(self, donnees, titre=None):
        """Trace le diagramme en 2D"""
        try:
            plt.style.use('seaborn-v0_8-darkgrid')
            fig, ax = plt.subplots(figsize=(8, 6))
            
            ax.plot(donnees['angle'], donnees['rayon'], 
                   color=self.accent_color,
                   linewidth=2)
            
            if titre:
                ax.set_title(f"Diagramme 2D - {titre}", pad=20)
            else:
                ax.set_title("Diagramme 2D Normalisé", pad=20)
            ax.set_xlabel("Angle (degrés)", fontsize=12, fontweight='bold')
            ax.set_ylabel("Intensité Normalisée", fontsize=12, fontweight='bold')
            ax.grid(True)
            
            plt.tight_layout()
            plt.show()
            
        except Exception as e:
            QMessageBox.critical(None, "Erreur", f"Erreur dans le tracé 2D : {str(e)}")
            self.barre_etat.showMessage("Erreur lors du tracé 2D", 3000)

    def tracer_combine(self, donnees, titre=None):
        """Affiche une fenêtre de dialogue pour choisir deux dates à comparer et trace les graphiques sphériques côte à côte"""
        try:
            if not self.sections_donnees:
                QMessageBox.information(None, "Information", "Aucune section par date détectée dans le fichier.")
                return

            # Création de la boîte de dialogue
            dialog = QtWidgets.QDialog()
            dialog.setWindowTitle("Sélection des dates")
            dialog.setMinimumWidth(500)

            # Layout principal
            layout = QtWidgets.QVBoxLayout()

            # Section de sélection des dates
            date_group = QtWidgets.QGroupBox("Sélection des dates à comparer")
            date_group.setStyleSheet(f"""
                QGroupBox {{
                    color: {self.primary_color};
                    font-weight: bold;
                    border: 2px solid {self.secondary_color};
                    border-radius: 10px;
                    margin-top: 10px;
                }}
                QGroupBox::title {{
                    subcontrol-origin: margin;
                    left: 10px;
                    padding: 0 5px;
                }}
            """
            )

            date_layout = QtWidgets.QVBoxLayout()

            # Premier ComboBox pour la première date
            first_date_label = QtWidgets.QLabel("Première date :")
            first_date_label.setStyleSheet(f"color: {self.primary_color}; font-weight: bold;")
            first_date_combo = QtWidgets.QComboBox()

            # Deuxième ComboBox pour la deuxième date
            second_date_label = QtWidgets.QLabel("Deuxième date :")
            second_date_label.setStyleSheet(f"color: {self.primary_color}; font-weight: bold;")
            second_date_combo = QtWidgets.QComboBox()

            # Style commun pour les ComboBox
            combo_style = f"""
                QComboBox {{
                    background-color: white;
                    border: 2px solid {self.secondary_color};
                    border-radius: 5px;
                    padding: 5px;
                    color: {self.primary_color};
                    font-weight: bold;
                }}
                QComboBox::drop-down {{
                    border: none;
                }}
                QComboBox::down-arrow {{
                    image: url(down_arrow.png);
                    width: 12px;
                    height: 12px;
                }}
            """
            first_date_combo.setStyleSheet(combo_style)
            second_date_combo.setStyleSheet(combo_style)

            # Remplir les ComboBox avec les dates disponibles
            for date, heure, _ in self.sections_donnees:
                date_str = f"{date} {heure}"
                first_date_combo.addItem(date_str)
                second_date_combo.addItem(date_str)

            # Ajouter les widgets au layout des dates
            date_layout.addWidget(first_date_label)
            date_layout.addWidget(first_date_combo)
            date_layout.addWidget(second_date_label)
            date_layout.addWidget(second_date_combo)

            date_group.setLayout(date_layout)
            layout.addWidget(date_group)

            # Boutons
            button_layout = QtWidgets.QHBoxLayout()

            ok_button = QtWidgets.QPushButton("Tracer")
            cancel_button = QtWidgets.QPushButton("Annuler")

            # Style des boutons
            button_style = f"""
                QPushButton {{
                    background-color: {self.primary_color};
                    color: {self.text_color};
                    border-radius: 5px;
                    padding: 8px 15px;
                    font-weight: bold;
                }}
                QPushButton:hover {{
                    background-color: {self.secondary_color};
                }}
            """
            ok_button.setStyleSheet(button_style)
            cancel_button.setStyleSheet(button_style)

            button_layout.addWidget(ok_button)
            button_layout.addWidget(cancel_button)
            layout.addLayout(button_layout)

            dialog.setLayout(layout)

            # Connexion des boutons
            ok_button.clicked.connect(dialog.accept)
            cancel_button.clicked.connect(dialog.reject)

            # Affichage de la boîte de dialogue
            if dialog.exec() == QtWidgets.QDialog.DialogCode.Accepted:
                # Récupérer les indices des dates sélectionnées
                first_index = first_date_combo.currentIndex()
                second_index = second_date_combo.currentIndex()

                if first_index >= 0 and second_index >= 0:
                    # Charger les données des deux sections sélectionnées
                    _, _, rayons1 = self.sections_donnees[first_index]
                    _, _, rayons2 = self.sections_donnees[second_index]

                    # Préparation des données pour le premier graphique
                    angles_rad1 = np.deg2rad(np.linspace(0, 360, len(rayons1), endpoint=False))
                    rayons_lin1 = 10 ** (np.array(rayons1) / 20)
                    pattern_3d_1, theta_grid1, phi_grid1 = reconstruct_3d_pattern(rayons_lin1, angles_rad1)

                    # Préparation des données pour le deuxième graphique
                    angles_rad2 = np.deg2rad(np.linspace(0, 360, len(rayons2), endpoint=False))
                    rayons_lin2 = 10 ** (np.array(rayons2) / 20)
                    pattern_3d_2, theta_grid2, phi_grid2 = reconstruct_3d_pattern(rayons_lin2, angles_rad2)

                    # Création de la figure avec deux sous-graphiques pour les surfaces 3D
                    mlab.figure("Comparaison des diagrammes sphériques", size=(1200, 600))
                    
                    # Premier graphique (à gauche)
                    mlab.subplot(121)
                    x1 = pattern_3d_1 * np.sin(theta_grid1) * np.cos(phi_grid1)
                    y1 = pattern_3d_1 * np.sin(theta_grid1) * np.sin(phi_grid1)
                    z1 = pattern_3d_1 * np.cos(theta_grid1)
                    surf1 = mlab.mesh(x1, y1, z1, scalars=pattern_3d_1, colormap='viridis')
                    mlab.colorbar(surf1, title='Magnitude')
                    mlab.title(first_date_combo.currentText())
                    mlab.xlabel('X')
                    mlab.ylabel('Y')
                    mlab.zlabel('Z')
                    
                    # Deuxième graphique (à droite)
                    mlab.subplot(122)
                    x2 = pattern_3d_2 * np.sin(theta_grid2) * np.cos(phi_grid2)
                    y2 = pattern_3d_2 * np.sin(theta_grid2) * np.sin(phi_grid2)
                    z2 = pattern_3d_2 * np.cos(theta_grid2)
                    surf2 = mlab.mesh(x2, y2, z2, scalars=pattern_3d_2, colormap='viridis')
                    mlab.colorbar(surf2, title='Magnitude')
                    mlab.title(second_date_combo.currentText())
                    mlab.xlabel('X')
                    mlab.ylabel('Y')
                    mlab.zlabel('Z')
                    
                    # Afficher la figure
                    mlab.show()
                    
                    self.barre_etat.showMessage("Tracé des graphiques sphériques effectué avec succès", 3000)

        except Exception as e:
            QMessageBox.critical(None, "Erreur", f"Erreur dans le tracé combiné : {str(e)}")
            self.barre_etat.showMessage("Erreur lors du tracé combiné", 3000)

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
            elif mode == "combine":
                self.tracer_combine(donnees, titre)
    
    def tracer_toutes_sections(self):
        """Trace les graphiques pour toutes les sections détectées"""
        if not self.sections_donnees:
            QMessageBox.information(None, "Information", "Aucune section par date détectée dans le fichier.")
            return
        
        try:
            plt.style.use('seaborn-v0_8-darkgrid')
            fig, axs = plt.subplots(len(self.sections_donnees), 1, figsize=(10, 4*len(self.sections_donnees)), 
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
            plt.subplots_adjust(hspace=0.5)
            plt.show()
            
            self.barre_etat.showMessage(f"Graphiques de toutes les sections tracés ({len(self.sections_donnees)} sections)", 3000)
            
        except Exception as e:
            QMessageBox.critical(None, "Erreur", f"Erreur lors du tracé des sections : {str(e)}")
            self.barre_etat.showMessage("Erreur lors du tracé des sections", 3000)

    def exporter_donnees(self):
        """Exporte les données actuelles vers un fichier CSV"""
        donnees = self.collecter_donnees()
        if donnees is None:
            return
            
        options = QFileDialog.Option(0)
        file_name, _ = QFileDialog.getSaveFileName(
            None, "Enregistrer les données", "",
            "Fichiers CSV (*.csv);;Tous les fichiers (*)",
            options=options
        )
            
        if file_name:
            try:
                # Ajouter l'extension .csv si nécessaire
                if not file_name.endswith('.csv'):
                    file_name += '.csv'
                    
                donnees.to_csv(file_name, index=False)
                self.barre_etat.showMessage(f"Données exportées vers {file_name}", 3000)
                
            except Exception as e:
                QMessageBox.critical(None, "Erreur", f"Erreur lors de l'exportation : {str(e)}")


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
        self.action_ouvrir = QAction("Ouvrir...", self)  # Utilisez QAction importé
        self.action_ouvrir.triggered.connect(self.ui.lire_fichier)
        self.menu_fichier.addAction(self.action_ouvrir)
        
        self.action_exporter = QAction("Exporter...", self)  # Utilisez QAction importé
        self.action_exporter.triggered.connect(self.ui.exporter_donnees)
        self.menu_fichier.addAction(self.action_exporter)
        
        self.menu_fichier.addSeparator()
        
        self.action_quitter = QAction("Quitter", self)  # Utilisez QAction importé
        self.action_quitter.triggered.connect(self.close)
        self.menu_fichier.addAction(self.action_quitter)
        
        # Menu Aide
        self.menu_aide = QtWidgets.QMenu("Aide", self)
        self.menu_bar.addMenu(self.menu_aide)
        
    def afficher_aide(self):
        """Affiche la boîte de dialogue d'aide"""
        about_text = """
        <h2>Analyseur de Diagramme de Rayonnement</h2>
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