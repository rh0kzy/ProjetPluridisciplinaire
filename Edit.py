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
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

class Ui_MainWindow(object):
    # Classe pour le widget matplotlib
    class MatplotlibCanvas(FigureCanvas):
        def __init__(self, parent=None, width=5, height=4, dpi=100):
            self.fig = Figure(figsize=(width, height), dpi=dpi)
            self.axes = self.fig.add_subplot(111)
            super(Ui_MainWindow.MatplotlibCanvas, self).__init__(self.fig)
            self.setParent(parent)
            self.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
            self.updateGeometry()
            
        def clear_plot(self):
            self.axes.clear()
            self.draw()
            
        def get_figure(self):
            return self.fig
            
    def setupUi(self, MainWindow):
        # Configuration de la fenêtre principale
        MainWindow.setObjectName("MainWindow")
        
        # Configurer la fenêtre pour être en plein écran
        screen = QtWidgets.QApplication.primaryScreen().geometry()
        MainWindow.setGeometry(0, 0, screen.width(), screen.height())
        MainWindow.setWindowState(QtCore.Qt.WindowState.WindowMaximized)
        
        # Taille minimale conservée pour les redimensionnements
        MainWindow.setMinimumSize(800, 600)
        
        # Police de caractères modernisée
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)  # Augmentation de la taille de police

        # Palette de couleurs professionnelle
        self.primary_color = "#1A2634"  # Bleu foncé professionnel
        self.secondary_color = "#2E86C1"  # Bleu clair moderne
        self.accent_color = "#E74C3C"  # Rouge vif
        self.text_color = "#FFFFFF"  # Blanc pur
        self.background_color = "#F8F9FA"  # Gris très clair
        self.hover_color = "#2471A3"  # Bleu pour le survol
        self.success_color = "#27AE60"  # Vert pour les actions positives
        self.card_color = "#FFFFFF"  # Blanc pour les cartes
        self.border_color = "#D6DBDF"  # Gris clair pour les bordures

        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.centralwidget.setStyleSheet(f"""
            QWidget#centralwidget {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 {self.primary_color}, stop:1 #1E3448);
            }}
            QPushButton {{
                background-color: {self.secondary_color};
                color: {self.text_color};
                border-radius: 8px;
                padding: 12px 20px;
                font-weight: bold;
                border: none;
                min-width: 140px;
                font-size: 12px;
                margin: 5px;
            }}
            QPushButton:hover {{
                background-color: {self.hover_color};
                border: 2px solid {self.accent_color};
                color: white;
            }}
            QPushButton:pressed {{
                background-color: {self.accent_color};
                border: 2px solid {self.hover_color};
            }}
            QLineEdit {{
                background-color: rgba(255, 255, 255, 0.9);
                border: 2px solid {self.secondary_color};
                border-radius: 8px;
                padding: 10px;
                color: {self.primary_color};
                font-weight: bold;
                min-height: 30px;
                font-size: 12px;
            }}
            QComboBox {{
                background-color: rgba(255, 255, 255, 0.9);
                border: 2px solid {self.secondary_color};
                border-radius: 8px;
                padding: 10px;
                color: {self.primary_color};
                font-weight: bold;
                min-height: 30px;
                font-size: 12px;
            }}
            QComboBox:hover {{
                border: 2px solid {self.accent_color};
                background-color: rgba(255, 255, 255, 0.95);
            }}
            QComboBox::drop-down {{
                border: none;
                width: 30px;
                border-radius: 0 8px 8px 0;
            }}
            QComboBox::down-arrow {{
                image: url(down_arrow.png);
                width: 12px;
                height: 12px;
            }}
            QComboBox QAbstractItemView {{
                background-color: white;
                color: {self.primary_color};
                selection-background-color: {self.secondary_color};
                border: 1px solid {self.secondary_color};
                border-radius: 8px;
                padding: 6px;
            }}
            QLabel {{
                color: {self.text_color};
                font-weight: bold;
                font-size: 13px;
                margin: 5px;
            }}
            QGroupBox {{
                color: {self.text_color};
                border: 2px solid {self.secondary_color};
                border-radius: 12px;
                margin-top: 20px;
                padding-top: 20px;
                padding: 15px;
                background-color: rgba(255, 255, 255, 0.05);
                font-size: 14px;
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: 20px;
                padding: 0 10px;
                color: {self.text_color};
                font-weight: bold;
                font-size: 14px;
            }}
            QStatusBar {{
                background-color: {self.primary_color};
                color: {self.text_color};
                font-weight: bold;
                min-height: 30px;
                padding: 5px;
                font-size: 12px;
            }}
            QMenuBar {{
                background-color: {self.primary_color};
                color: {self.text_color};
                padding: 5px;
                font-size: 13px;
            }}
            QMenuBar::item:selected {{
                background-color: {self.secondary_color};
            }}
            QMenu {{
                background-color: {self.primary_color};
                color: {self.text_color};
                border: 1px solid {self.secondary_color};
                padding: 5px;
            }}
            QMenu::item:selected {{
                background-color: {self.secondary_color};
            }}
            QScrollBar:vertical {{
                background: {self.primary_color};
                width: 12px;
                margin: 0px;
                border-radius: 6px;
            }}
            QScrollBar::handle:vertical {{
                background: {self.secondary_color};
                min-height: 20px;
                border-radius: 6px;
            }}
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
                height: 0px;
            }}
            QScrollBar:horizontal {{
                background: {self.primary_color};
                height: 12px;
                margin: 0px;
                border-radius: 6px;
            }}
            QScrollBar::handle:horizontal {{
                background: {self.secondary_color};
                min-width: 20px;
                border-radius: 6px;
            }}
            QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
                width: 0px;
            }}
        """)

        self.main_layout = QtWidgets.QHBoxLayout(self.centralwidget)  # Utilisation d'un layout horizontal pour diviser l'écran
        self.main_layout.setContentsMargins(20, 20, 20, 20)  # Marges augmentées
        self.main_layout.setSpacing(15)  # Espacement augmenté

        # Panneau de gauche (contrôles)
        self.left_panel = QtWidgets.QWidget()
        self.left_panel.setSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Expanding)
        self.left_panel.setMaximumWidth(600)  # Largeur maximale du panneau de gauche
        self.left_layout = QtWidgets.QVBoxLayout(self.left_panel)
        self.left_layout.setContentsMargins(10, 10, 10, 10)
        self.left_layout.setSpacing(15)

        # Logo et titre
        self.header_layout = QtWidgets.QHBoxLayout()
        self.logo_label = QtWidgets.QLabel()
        self.logo_label.setMaximumSize(100, 100)
        self.logo_label.setStyleSheet("background-color: transparent;")
        # Si vous avez un logo, décommentez et adaptez la ligne suivante
        # self.logo_label.setPixmap(QtGui.QPixmap("logo.png").scaled(80, 80, QtCore.Qt.AspectRatioMode.KeepAspectRatio))
        self.header_layout.addWidget(self.logo_label)
        
        self.title_label = QtWidgets.QLabel("Analyse de Diagramme de Rayonnement")
        title_font = QtGui.QFont("Segoe UI", 18, QtGui.QFont.Weight.Bold)
        self.title_label.setFont(title_font)
        self.title_label.setStyleSheet(f"color: {self.text_color}; margin-bottom: 10px;")
        self.header_layout.addWidget(self.title_label, 1)
        self.left_layout.addLayout(self.header_layout)

        # Section fichier avec style moderne
        self.file_group = QtWidgets.QGroupBox("📂 Entrée des Données")
        self.file_group.setFont(font)
        self.file_layout = QtWidgets.QVBoxLayout(self.file_group)
        self.file_layout.setSpacing(15)
        self.file_layout.setContentsMargins(20, 20, 20, 20)
        
        # Bouton charger fichier avec icône
        self.load_file_btn = QtWidgets.QPushButton("📂 Charger un fichier")
        self.load_file_btn.setFont(font)
        self.load_file_btn.setMinimumHeight(50)
        self.file_layout.addWidget(self.load_file_btn)

        # Champ de saisie avec icône
        self.radii_layout = QtWidgets.QHBoxLayout()
        self.radii_label = QtWidgets.QLabel("📏 Rayons:")
        self.radii_label.setFont(font)
        self.radii_layout.addWidget(self.radii_label, 1)
        
        self.radii_input = QtWidgets.QLineEdit()
        self.radii_input.setFont(font)
        self.radii_input.setPlaceholderText("Entrez les valeurs séparées par des virgules")
        self.radii_layout.addWidget(self.radii_input, 3)
        self.file_layout.addLayout(self.radii_layout)

        # Info angles avec style amélioré
        self.angles_info = QtWidgets.QLabel("ℹ️ Les angles sont générés automatiquement selon le nombre de rayons")
        info_font = QtGui.QFont(font)
        info_font.setPointSize(9)
        info_font.setItalic(True)
        self.angles_info.setFont(info_font)
        self.angles_info.setStyleSheet(f"color: {self.secondary_color}; padding: 5px;")
        self.file_layout.addWidget(self.angles_info)

        # Menu déroulant avec icône
        self.sections_layout = QtWidgets.QHBoxLayout()
        self.sections_label = QtWidgets.QLabel("📅 Sélection par date:")
        self.sections_label.setFont(font)
        self.sections_layout.addWidget(self.sections_label, 1)
        
        self.sections_combo = QtWidgets.QComboBox()
        self.sections_combo.setFont(font)
        self.sections_combo.setPlaceholderText("Sélectionnez une date")
        self.sections_layout.addWidget(self.sections_combo, 3)
        self.file_layout.addLayout(self.sections_layout)
        
        self.left_layout.addWidget(self.file_group)

        # Section visualisation avec style moderne
        self.viz_group = QtWidgets.QGroupBox("📊 Visualisation")
        self.viz_group.setFont(font)
        
        # Création d'une grille pour les boutons
        self.viz_layout = QtWidgets.QGridLayout(self.viz_group)
        self.viz_layout.setSpacing(15)
        self.viz_layout.setContentsMargins(20, 20, 20, 20)
        
        # Boutons de visualisation avec icônes et style modifié
        self.polar_btn = QtWidgets.QPushButton("📈 Tracer en polaire")
        self.polar_btn.setFont(font)
        self.polar_btn.setMinimumHeight(60)
        self.viz_layout.addWidget(self.polar_btn, 0, 0)
        
        self.sphere_btn = QtWidgets.QPushButton("🌐 Tracer en sphérique")
        self.sphere_btn.setFont(font)
        self.sphere_btn.setMinimumHeight(60)
        self.viz_layout.addWidget(self.sphere_btn, 0, 1)
        
        # Ajout d'un bouton 2D
        self.twod_btn = QtWidgets.QPushButton("📊 Tracer en 2D")
        self.twod_btn.setFont(font)
        self.twod_btn.setMinimumHeight(60)
        self.viz_layout.addWidget(self.twod_btn, 1, 0)
        
        self.combine_btn = QtWidgets.QPushButton("🔄 Tracer combiné")
        self.combine_btn.setFont(font)
        self.combine_btn.setMinimumHeight(60)
        self.viz_layout.addWidget(self.combine_btn, 1, 1)

        self.all_graphs_btn = QtWidgets.QPushButton("📊 Tracer tous les graphes")
        self.all_graphs_btn.setFont(font)
        self.all_graphs_btn.setMinimumHeight(60)
        self.all_graphs_btn.setStyleSheet(f"""
            background-color: {self.accent_color};
            color: {self.text_color};
            border-radius: 8px;
            padding: 12px 20px;
            font-weight: bold;
            border: none;
            min-width: 140px;
            font-size: 12px;
            margin: 5px;
        """)
        self.viz_layout.addWidget(self.all_graphs_btn, 2, 0, 1, 2)
        
        # Ajuster les colonnes pour qu'elles aient la même largeur
        self.viz_layout.setColumnStretch(0, 1)
        self.viz_layout.setColumnStretch(1, 1)
        
        self.left_layout.addWidget(self.viz_group)

        # Panneau de droite (aperçu du graphique)
        self.right_panel = QtWidgets.QWidget()
        self.right_panel.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        self.right_layout = QtWidgets.QVBoxLayout(self.right_panel)
        self.right_layout.setContentsMargins(10, 10, 10, 10)
          # Zone de prévisualisation du graphique
        self.preview_group = QtWidgets.QGroupBox("📊 Prévisualisation")
        self.preview_group.setFont(font)
        self.preview_layout = QtWidgets.QVBoxLayout(self.preview_group)
        
        # Créer le widget matplotlib et la barre d'outils
        self.canvas = self.MatplotlibCanvas(self.preview_group, width=5, height=4, dpi=100)
        self.toolbar = NavigationToolbar(self.canvas, self.preview_group)
        
        # Ajouter le widget et la barre d'outils au layout
        self.preview_layout.addWidget(self.toolbar)
        self.preview_layout.addWidget(self.canvas)
        
        self.right_layout.addWidget(self.preview_group)
        
        # Ajouter les panneaux au layout principal
        self.main_layout.addWidget(self.left_panel, 1)
        self.main_layout.addWidget(self.right_panel, 2)  # Le panneau droit prend plus de place
        
        # Barre d'état avec style moderne
        self.status_bar = QtWidgets.QStatusBar()
        self.status_bar.setFont(font)
        MainWindow.setStatusBar(self.status_bar)

        MainWindow.setCentralWidget(self.centralwidget)
        
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
        """Trace le diagramme polaire avec une esthétique professionnelle"""
        try:
            # Effacer la figure précédente
            self.canvas.axes.clear()
            
            # Utiliser un style moderne
            plt.style.use('ggplot')
            
            # Configuration de la figure pour une qualité professionnelle 
            self.canvas.fig.set_dpi(150)
            plt.rcParams['font.family'] = 'sans-serif'
            plt.rcParams['font.size'] = 12
            plt.rcParams['legend.fontsize'] = 12
            plt.rcParams['axes.titlesize'] = 14
            plt.rcParams['axes.labelsize'] = 12
            
            # Convertir l'axe en polar
            self.canvas.axes.remove()
            self.canvas.axes = self.canvas.fig.add_subplot(111, projection='polar')
            
            angles = np.deg2rad(donnees['angle'])
            rayons = donnees['rayon']
            
            # Tracé avec une ligne plus épaisse
            line, = self.canvas.axes.plot(angles, rayons, 
                   color=self.accent_color,
                   linewidth=3,
                   marker='o',
                   markersize=4,
                   markerfacecolor=self.secondary_color,
                   markeredgecolor=self.accent_color,
                   alpha=0.8)
                   
            # Remplir la zone sous la courbe pour une meilleure visualisation
            self.canvas.axes.fill(angles, rayons, alpha=0.3, color=self.accent_color)
            
            # Titres et étiquettes
            if titre:
                self.canvas.axes.set_title(f"Diagramme de Rayonnement Polaire - {titre}", pad=20, fontweight='bold')
            else:
                self.canvas.axes.set_title("Diagramme de Rayonnement Polaire (dBi)", pad=20, fontweight='bold')
            
            # Personnalisation de la grille
            self.canvas.axes.grid(True, linestyle='--', alpha=0.7, color='gray')
            
            # Configuration des ticks et labels
            rmin, rmax = self.canvas.axes.get_ylim()
            r_ticks = np.linspace(rmin, rmax, 5)
            self.canvas.axes.set_rticks(r_ticks)
            
            # Formater les labels avec 2 décimales et ajouter dBi
            self.canvas.axes.set_yticklabels([f"{tick:.2f} dBi" for tick in r_ticks])
              # Ajouter des lignes pour les angles de référence
            angles_deg = [0, 45, 90, 135, 180, 225, 270, 315]
            for angle_deg in angles_deg:
                self.canvas.axes.text(np.deg2rad(angle_deg), rmax*1.05, f"{angle_deg}°", 
                       ha='center', va='center', fontsize=10, color='gray')
            
            # Ajouter une légende
            self.canvas.axes.legend([line], ["Gain d'antenne"], loc='upper right', bbox_to_anchor=(0.1, 0.1))
            
            # Mettre à jour la figure
            self.canvas.fig.tight_layout()
            self.canvas.draw()
            
            # Mise à jour du statut
            self.barre_etat.showMessage(f"Diagramme polaire tracé avec succès", 3000)
            
        except Exception as e:
            QMessageBox.critical(None, "Erreur", f"Erreur dans le tracé polaire : {str(e)}")
            self.barre_etat.showMessage("Erreur lors du tracé polaire", 3000)

    def tracer_spherique(self, donnees, titre=None):
        """Trace le diagramme sphérique 3D avec une qualité professionnelle"""
        try:
            # Effacer la figure précédente
            self.canvas.axes.clear()
            
            # Utiliser un style moderne
            plt.style.use('ggplot')
            
            # Configuration pour une qualité professionnelle
            self.canvas.fig.set_dpi(180)  # Résolution encore plus élevée
            plt.rcParams['font.family'] = 'sans-serif'
            plt.rcParams['font.size'] = 12
            plt.rcParams['axes.titlesize'] = 14
            
            # Augmentation de la résolution pour un rendu plus lisse
            resolution = 120  
            
            theta = np.deg2rad(donnees['angle'].values)
            r = donnees['rayon'].values
            
            # Création d'une grille plus fine pour un rendu professionnel
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
            
            # Remplacer l'axe actuel par un axe 3D
            self.canvas.axes.remove()
            self.canvas.axes = self.canvas.fig.add_subplot(111, projection='3d')
              # Normalisation des couleurs pour un gradient professionnel
            cmap = plt.cm.viridis
            norm = plt.Normalize(np.min(r), np.max(r))
            
            # Tracé de la surface avec une meilleure qualité
            surf = self.canvas.axes.plot_surface(X, Y, Z, 
                                 cmap=cmap,
                                 norm=norm,
                                 alpha=0.9,
                                 rcount=resolution,
                                 ccount=resolution,
                                 antialiased=True,
                                 linewidth=0.3)
            
            # Barre de couleur personnalisée
            cbar = self.canvas.fig.colorbar(surf, ax=self.canvas.axes, shrink=0.5, pad=0.1, label='Gain (dBi)')
            cbar.ax.yaxis.label.set_weight('bold')
            
            # Titre en gras
            if titre:
                self.canvas.axes.set_title(f"Diagramme de Rayonnement 3D - {titre}", fontweight='bold', pad=20)
            else:
                self.canvas.axes.set_title("Diagramme de Rayonnement 3D (dBi)", fontweight='bold', pad=20)
            
            # Vue initiale optimisée
            self.canvas.axes.view_init(elev=35, azim=45)
            
            # Enlever les axes pour un rendu plus esthétique
            self.canvas.axes.set_axis_off()
            self.canvas.axes.grid(False)
              # Améliorer le contraste entre les axes et l'arrière-plan
            self.canvas.axes.xaxis.pane.fill = False
            self.canvas.axes.yaxis.pane.fill = False
            self.canvas.axes.zaxis.pane.fill = False
            
            # Ajouter une référence aux axes pour l'orientation
            max_range = np.max([np.abs(X).max(), np.abs(Y).max(), np.abs(Z).max()]) * 1.2
            self.canvas.axes.set_xlim(-max_range, max_range)
            self.canvas.axes.set_ylim(-max_range, max_range)
            self.canvas.axes.set_zlim(-max_range, max_range)
            
            # Mettre à jour la figure
            self.canvas.fig.tight_layout()
            self.canvas.draw()
            
            # Mise à jour du statut
            self.barre_etat.showMessage(f"Diagramme sphérique 3D tracé avec succès", 3000)
            
        except Exception as e:
            QMessageBox.critical(None, "Erreur", f"Erreur dans le tracé sphérique : {str(e)}")
            self.barre_etat.showMessage("Erreur lors du tracé sphérique", 3000)

    def tracer_2d(self, donnees, titre=None):
        """Trace le diagramme en 2D avec un style professionnel"""
        try:
            # Effacer la figure précédente
            self.canvas.axes.clear()
            
            # Utiliser un style moderne
            plt.style.use('ggplot')
            
            # Configuration pour une qualité professionnelle
            self.canvas.fig.set_dpi(150)
            plt.rcParams['font.family'] = 'sans-serif'
            plt.rcParams['font.size'] = 12
            plt.rcParams['legend.fontsize'] = 12
            plt.rcParams['axes.titlesize'] = 14
            plt.rcParams['axes.labelsize'] = 12
            
            # S'assurer que l'axe n'est pas en 3D ou polaire
            self.canvas.axes.remove()
            self.canvas.axes = self.canvas.fig.add_subplot(111)
            
            angles = donnees['angle']
            rayons = donnees['rayon']
              # Tracer la ligne avec un style plus élaboré
            line, = self.canvas.axes.plot(angles, rayons, 
                   color=self.accent_color,
                   linewidth=2.5,
                   marker='o',
                   markersize=4,
                   markerfacecolor=self.secondary_color,
                   markeredgecolor=self.accent_color,
                   alpha=0.8)
            
            # Remplir la zone sous la courbe pour une meilleure visualisation
            self.canvas.axes.fill_between(angles, rayons, min(rayons), alpha=0.15, color=self.accent_color)
            
            # Titre et étiquettes
            if titre:
                self.canvas.axes.set_title(f"Diagramme de Rayonnement 2D - {titre}", fontweight='bold', pad=20)
            else:
                self.canvas.axes.set_title("Diagramme de Rayonnement 2D (dBi)", fontweight='bold', pad=20)
            
            self.canvas.axes.set_xlabel('Angle (degrés)', fontweight='bold')
            self.canvas.axes.set_ylabel('Gain (dBi)', fontweight='bold')
            
            # Grille plus subtile
            self.canvas.axes.grid(True, linestyle='--', alpha=0.6)
            
            # Personnalisation des ticks et limites
            ymin, ymax = self.canvas.axes.get_ylim()
            y_range = ymax - ymin
            self.canvas.axes.set_ylim(ymin - y_range*0.05, ymax + y_range*0.05)  # Ajouter une marge
            y_ticks = np.linspace(ymin, ymax, 6)
            self.canvas.axes.set_yticks(y_ticks)
            self.canvas.axes.set_yticklabels([f"{tick:.2f} dBi" for tick in y_ticks])
            
            # Limites de l'axe X (de 0 à 360 degrés)
            self.canvas.axes.set_xlim(0, 360)
            x_ticks = np.arange(0, 361, 45)  # Tous les 45 degrés
            self.canvas.axes.set_xticks(x_ticks)
            
            # Ajouter une légende
            self.canvas.axes.legend([line], ["Gain d'antenne"], loc='upper right')
            
            # Barre d'information pour la valeur maximale
            max_gain = np.max(rayons)
            max_angle = angles[np.argmax(rayons)]
            self.canvas.axes.axhline(y=max_gain, linestyle='--', color=self.secondary_color, alpha=0.5)
            self.canvas.axes.axvline(x=max_angle, linestyle='--', color=self.secondary_color, alpha=0.5)
            self.canvas.axes.annotate(f"Max: {max_gain:.2f} dBi à {max_angle:.1f}°", 
                       xy=(max_angle, max_gain),
                       xytext=(max_angle + 20, max_gain + 0.5),
                       arrowprops=dict(facecolor=self.secondary_color, shrink=0.05),
                       fontsize=10,
                       backgroundcolor='white',
                       alpha=0.8)
            
            # Mettre à jour la figure
            self.canvas.fig.tight_layout()
            self.canvas.draw()
            
            # Mise à jour du statut
            self.barre_etat.showMessage(f"Diagramme 2D tracé avec succès", 3000)
            
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
        """Trace les graphiques pour toutes les sections détectées avec un style professionnel"""
        if not self.sections_donnees:
            QMessageBox.information(None, "Information", "Aucune section par date détectée dans le fichier.")
            return
        
        try:
            # Utiliser un style moderne
            plt.style.use('ggplot')
            
            # Configuration pour une qualité professionnelle
            plt.rcParams['figure.dpi'] = 150
            plt.rcParams['savefig.dpi'] = 150
            plt.rcParams['font.family'] = 'sans-serif'
            plt.rcParams['font.size'] = 12
            plt.rcParams['axes.titlesize'] = 14
            plt.rcParams['axes.labelsize'] = 12
            
            # Adapter la taille de la figure en fonction du nombre de sections
            sections_count = len(self.sections_donnees)
            
            if sections_count <= 3:
                # Pour 1 à 3 sections, disposition horizontale
                fig, axs = plt.subplots(1, sections_count, 
                                      figsize=(6*sections_count, 6),
                                      subplot_kw={'projection': 'polar'})
            else:
                # Pour 4 sections ou plus, utiliser une grille
                rows = (sections_count + 1) // 2  # Arrondi au supérieur
                cols = min(2, sections_count)
                fig, axs = plt.subplots(rows, cols, 
                                      figsize=(12, 6*rows),
                                      subplot_kw={'projection': 'polar'})
            
            # Si une seule section, axs n'est pas un tableau
            if sections_count == 1:
                axs = [axs]
            else:
                # Convertir axs en tableau 1D pour simplifier le traitement
                axs = axs.flatten() if hasattr(axs, 'flatten') else axs
                
            # Couleurs différentes pour chaque section
            colors = [self.primary_color, self.secondary_color, self.accent_color, 
                    self.success_color, '#9B59B6', '#F1C40F', '#2C3E50', '#E67E22']
            
            # Garantir suffisamment de couleurs
            while len(colors) < sections_count:
                colors.extend(colors)
                
            for i, (date, heure, rayons) in enumerate(self.sections_donnees):
                # Préparation des données
                rayons_arr = np.array(rayons)
                max_val = np.max(rayons_arr)
                rayons_normalises = rayons_arr - max_val
                angles = np.linspace(0, 2*np.pi, len(rayons_arr), endpoint=False)
                
                # Utiliser une couleur différente pour chaque section
                color = colors[i % len(colors)]
                
                # Tracé amélioré
                axs[i].plot(angles, rayons_normalises, 
                          color=color, 
                          linewidth=2.5,
                          marker='o',
                          markersize=3,
                          markerfacecolor='white',
                          markeredgecolor=color,
                          alpha=0.9)
                
                # Remplir la zone pour un meilleur rendu visuel
                axs[i].fill(angles, rayons_normalises, alpha=0.2, color=color)
                
                # Titre informatif
                axs[i].set_title(f"{date}\n{heure}", fontweight='bold', fontsize=12)
                
                # Grille améliorée
                axs[i].grid(True, linestyle='--', alpha=0.7, color='gray')
                
                # Ajustement des ticks pour une meilleure lisibilité
                r_ticks = np.linspace(np.min(rayons_normalises), 0, 5)
                axs[i].set_rticks(r_ticks)
                axs[i].set_yticklabels([f"{tick:.1f}" for tick in r_ticks])
                
                # Ajouter une annotation pour la valeur maximale
                max_angle_idx = np.argmax(rayons_normalises)
                max_angle = angles[max_angle_idx]
                max_r = rayons_normalises[max_angle_idx]
                axs[i].annotate("Max", 
                             xy=(max_angle, max_r),
                             xytext=(max_angle, max_r - 0.5),
                             arrowprops=dict(facecolor='black', shrink=0.05, width=1.5),
                             fontsize=9,
                             horizontalalignment='center',
                             verticalalignment='bottom')
            
            # Ajuster la mise en page
            plt.tight_layout()
            plt.subplots_adjust(wspace=0.3, hspace=0.4)
            
            # Ajouter un titre global
            fig.suptitle("Comparaison des Diagrammes de Rayonnement", 
                       fontsize=16, fontweight='bold', y=0.98)
            
            # Ajouter une annotation explicative
            fig.text(0.5, 0.01, 
                    "Chaque diagramme est normalisé à sa valeur maximale (0 dBi)",
                    ha='center', fontsize=10, style='italic', color='gray')
            
            plt.show()
            
            # Mise à jour du statut
            self.barre_etat.showMessage(f"Comparaison des {sections_count} sections tracée avec succès", 3000)
            
        except Exception as e:
            QMessageBox.critical(None, "Erreur", f"Erreur lors du tracé des sections : {str(e)}")
            self.barre_etat.showMessage("Erreur lors du tracé des sections", 3000)

    def tracer_graphique_combine(self):
        """Trace un graphique 3D combiné de deux sections avec un style professionnel"""
        if len(self.sections_donnees) < 2:
            QMessageBox.warning(None, "Attention", "Au moins deux sections sont nécessaires pour créer un graphique combiné.")
            return
            
        # Créer une boîte de dialogue professionnelle pour sélectionner les deux sections
        dialog = QtWidgets.QDialog()
        dialog.setWindowTitle("Sélection des sections à combiner")
        dialog.setMinimumWidth(400)
        dialog.setStyleSheet(f"""
            QDialog {{
                background-color: {self.primary_color};
                border-radius: 8px;
                padding: 10px;
            }}
            QLabel {{
                color: {self.text_color};
                font-weight: bold;
                font-size: 12px;
                margin-bottom: 5px;
            }}
            QComboBox {{
                background-color: white;
                border: 2px solid {self.secondary_color};
                border-radius: 5px;
                padding: 8px;
                color: {self.primary_color};
                min-height: 30px;
                font-size: 11px;
            }}
            QPushButton {{
                background-color: {self.secondary_color};
                color: {self.text_color};
                border-radius: 5px;
                padding: 10px;
                font-weight: bold;
                min-width: 100px;
                font-size: 12px;
                margin-top: 15px;
            }}
            QPushButton:hover {{
                background-color: {self.hover_color};
                border: 2px solid {self.accent_color};
            }}
        """)
        
        layout = QtWidgets.QVBoxLayout()
        layout.setSpacing(15)
        
        # En-tête explicatif
        header = QtWidgets.QLabel("Sélectionnez deux sections de données à comparer dans un graphique 3D combiné.")
        header.setWordWrap(True)
        layout.addWidget(header)
        
        # Premier menu déroulant avec étiquette
        label1 = QtWidgets.QLabel("Première section:")
        combo1 = QtWidgets.QComboBox()
        combo1.setMaxVisibleItems(10)
        for date, heure, _ in self.sections_donnees:
            combo1.addItem(f"{date} {heure}")
            
        # Deuxième menu déroulant avec étiquette
        label2 = QtWidgets.QLabel("Deuxième section:")
        combo2 = QtWidgets.QComboBox()
        combo2.setMaxVisibleItems(10)
        for date, heure, _ in self.sections_donnees:
            combo2.addItem(f"{date} {heure}")
        
        # Si plus de 2 sections, sélectionner la première et la deuxième par défaut
        if len(self.sections_donnees) > 1:
            combo2.setCurrentIndex(1)
            
        # Disposition des éléments
        layout.addWidget(label1)
        layout.addWidget(combo1)
        layout.addWidget(label2)
        layout.addWidget(combo2)
        
        # Options supplémentaires
        options_group = QtWidgets.QGroupBox("Options")
        options_group.setStyleSheet(f"""
            QGroupBox {{
                color: {self.text_color};
                border: 1px solid {self.secondary_color};
                border-radius: 5px;
                margin-top: 15px;
                padding: 10px;
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }}
            QCheckBox {{
                color: {self.text_color};
                font-size: 11px;
            }}
        """)
        options_layout = QtWidgets.QVBoxLayout()
        
        # Checkbox pour la rotation automatique
        rotation_check = QtWidgets.QCheckBox("Ajouter une rotation automatique")
        rotation_check.setChecked(True)
        options_layout.addWidget(rotation_check)
        
        options_group.setLayout(options_layout)
        layout.addWidget(options_group)
        
        # Bouton avec une disposition horizontale pour le centrage
        button_layout = QtWidgets.QHBoxLayout()
        button = QtWidgets.QPushButton("Tracer")
        button.clicked.connect(dialog.accept)
        button_layout.addStretch()
        button_layout.addWidget(button)
        button_layout.addStretch()
        layout.addLayout(button_layout)
        
        dialog.setLayout(layout)
        
        # Exécution de la boîte de dialogue
        if dialog.exec() == QtWidgets.QDialog.DialogCode.Accepted:
            index1 = combo1.currentIndex()
            index2 = combo2.currentIndex()
            
            if index1 == index2:
                QMessageBox.warning(None, "Attention", "Veuillez sélectionner deux sections différentes.")
                return
                
            # Récupérer les données des deux sections
            date1, heure1, rayons1 = self.sections_donnees[index1]
            date2, heure2, rayons2 = self.sections_donnees[index2]
            
            # Préparer les données pour le tracé
            angles1 = np.linspace(0, 360, len(rayons1), endpoint=False)
            angles2 = np.linspace(0, 360, len(rayons2), endpoint=False)
            
            donnees1 = pd.DataFrame({'angle': angles1, 'rayon': rayons1})
            donnees2 = pd.DataFrame({'angle': angles2, 'rayon': rayons2})
            
            # Option de rotation
            rotation = rotation_check.isChecked()
            
            # Tracer le graphique combiné
            self.tracer_spherique_combine(
                donnees1, donnees2, 
                f"{date1} {heure1}", 
                f"{date2} {heure2}",
                rotation=rotation
            )
            
    def tracer_spherique_combine(self, donnees1, donnees2, titre1=None, titre2=None, rotation=False):
        """Trace deux diagrammes sphériques 3D combinés avec un style professionnel"""
        try:
            # Utiliser un style moderne
            plt.style.use('ggplot')
            
            # Configuration pour une qualité professionnelle
            plt.rcParams['figure.dpi'] = 180
            plt.rcParams['savefig.dpi'] = 180
            plt.rcParams['font.family'] = 'sans-serif'
            plt.rcParams['font.size'] = 12
            plt.rcParams['axes.titlesize'] = 14
            
            # Augmentation de la résolution pour un rendu professionnel
            resolution = 130
            
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
            
            # Création de la figure avec une taille adaptée aux écrans larges
            fig = plt.figure(figsize=(14, 10))
            ax = fig.add_subplot(111, projection='3d')
            
            # Utiliser des colormaps contrastés pour différencier les surfaces
            cmap1 = plt.cm.viridis
            cmap2 = plt.cm.plasma
            
            # Normalisation des couleurs
            norm1 = plt.Normalize(np.min(r1), np.max(r1))
            norm2 = plt.Normalize(np.min(r2), np.max(r2))
            
            # Traces des surfaces avec styles améliorés
            surf1 = ax.plot_surface(X1, Y1, Z1, 
                                  cmap=cmap1,
                                  norm=norm1,
                                  alpha=0.7,
                                  rcount=resolution,
                                  ccount=resolution,
                                  antialiased=True,
                                  linewidth=0.2,
                                  label=titre1 if titre1 else "Section 1")
            
            surf2 = ax.plot_surface(X2, Y2, Z2, 
                                  cmap=cmap2,
                                  norm=norm2,
                                  alpha=0.7,
                                  rcount=resolution,
                                  ccount=resolution,
                                  antialiased=True,
                                  linewidth=0.2,
                                  label=titre2 if titre2 else "Section 2")
            
            # Ajout des barres de couleur
            cbar1 = fig.colorbar(surf1, ax=ax, shrink=0.4, pad=0.02, aspect=10, location='left')
            cbar1.ax.set_ylabel(f"{titre1 if titre1 else 'Section 1'} (dBi)", rotation=90, va='bottom', fontweight='bold')
            
            cbar2 = fig.colorbar(surf2, ax=ax, shrink=0.4, pad=0.1, aspect=10)
            cbar2.ax.set_ylabel(f"{titre2 if titre2 else 'Section 2'} (dBi)", rotation=90, va='bottom', fontweight='bold')
            
            # Titre général avec plus d'informations
            ax.set_title("Comparaison des Diagrammes de Rayonnement 3D", fontweight='bold', pad=25, fontsize=16)
            
            # Enlever les axes pour un rendu plus esthétique
            ax.set_axis_off()
            ax.grid(False)
            
            # Améliorer le contraste entre les axes et l'arrière-plan
            ax.xaxis.pane.fill = False
            ax.yaxis.pane.fill = False
            ax.zaxis.pane.fill = False
            
            # Ajouter une référence aux axes pour l'orientation
            max_range = np.max([np.abs(X1).max(), np.abs(Y1).max(), np.abs(Z1).max(), 
                             np.abs(X2).max(), np.abs(Y2).max(), np.abs(Z2).max()]) * 1.1
            ax.set_xlim(-max_range, max_range)
            ax.set_ylim(-max_range, max_range)
            ax.set_zlim(-max_range, max_range)
            
            # Légende pour indiquer quelle surface est associée à quelle section
            # Hack pour créer une légende pour les plot_surface
            surf1_proxy = plt.Rectangle((0, 0), 1, 1, fc=cmap1(0.7))
            surf2_proxy = plt.Rectangle((0, 0), 1, 1, fc=cmap2(0.7))
            ax.legend([surf1_proxy, surf2_proxy], 
                     [titre1 if titre1 else "Section 1", 
                      titre2 if titre2 else "Section 2"],
                     loc='upper right',
                     bbox_to_anchor=(0.95, 0.95))
            
            # Ajouter des informations statistiques
            info_text = f"Max {titre1 if titre1 else 'Section 1'}: {np.max(r1):.2f} dBi\n"
            info_text += f"Max {titre2 if titre2 else 'Section 2'}: {np.max(r2):.2f} dBi\n"
            info_text += f"Différence: {np.max(r1) - np.max(r2):.2f} dBi"
            
            fig.text(0.02, 0.02, info_text, 
                   fontsize=10, 
                   bbox=dict(facecolor='white', alpha=0.8, boxstyle='round,pad=0.5'))
            
            # Animation de rotation si demandée
            if rotation:
                def rotate(angle):
                    ax.view_init(elev=30, azim=angle)
                    return [ax]
                
                # Créer l'animation
                from matplotlib.animation import FuncAnimation
                ani = FuncAnimation(fig, rotate, frames=np.arange(0, 360, 2), interval=50, blit=True)
                plt.show()
            else:
                # Vue initiale optimisée
                ax.view_init(elev=30, azim=45)
                plt.tight_layout()
                plt.show()
            
            # Mise à jour du statut
            self.barre_etat.showMessage(f"Diagramme combiné tracé avec succès", 3000)
            
        except Exception as e:
            QMessageBox.critical(None, "Erreur", f"Erreur dans le tracé sphérique combiné : {str(e)}")
            self.barre_etat.showMessage("Erreur lors du tracé sphérique combiné", 3000)

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        # Création du menu avec style moderne
        self.menu_bar = self.menuBar()
        self.menu_bar.setStyleSheet(f"""
            QMenuBar {{
                background-color: {self.ui.primary_color};
                color: {self.ui.text_color};
                padding: 5px;
                font-size: 13px;
            }}
            QMenuBar::item:selected {{
                background-color: {self.ui.secondary_color};
            }}
        """)
        
        # Menu Fichier
        self.menu_fichier = self.menu_bar.addMenu("Fichier")
        
        # Action pour charger un fichier
        self.action_charger = QAction("Charger un fichier...", self)
        self.action_charger.setShortcut("Ctrl+O")
        self.action_charger.triggered.connect(self.ui.lire_fichier)
        self.menu_fichier.addAction(self.action_charger)
        
        # Action pour exporter les résultats
        self.action_exporter = QAction("Exporter les résultats...", self)
        self.action_exporter.setShortcut("Ctrl+S")
        self.action_exporter.triggered.connect(self.exporter_resultats)
        self.menu_fichier.addAction(self.action_exporter)
        
        self.menu_fichier.addSeparator()
        
        # Action pour quitter
        self.action_quitter = QAction("Quitter", self)
        self.action_quitter.setShortcut("Ctrl+Q")
        self.action_quitter.triggered.connect(self.close)
        self.menu_fichier.addAction(self.action_quitter)
        
        # Menu Visualisation
        self.menu_visualisation = self.menu_bar.addMenu("Visualisation")
        
        # Actions pour les différents types de graphiques
        self.action_polaire = QAction("Diagramme Polaire", self)
        self.action_polaire.setShortcut("Ctrl+P")
        self.action_polaire.triggered.connect(lambda: self.ui.mettre_a_jour_graphique("polaire"))
        self.menu_visualisation.addAction(self.action_polaire)
        
        self.action_spherique = QAction("Diagramme Sphérique 3D", self)
        self.action_spherique.setShortcut("Ctrl+3")
        self.action_spherique.triggered.connect(lambda: self.ui.mettre_a_jour_graphique("spherique"))
        self.menu_visualisation.addAction(self.action_spherique)
        
        self.action_2d = QAction("Diagramme 2D", self)
        self.action_2d.setShortcut("Ctrl+2")
        self.action_2d.triggered.connect(lambda: self.ui.mettre_a_jour_graphique("2d"))
        self.menu_visualisation.addAction(self.action_2d)
        
        self.menu_visualisation.addSeparator()
        
        self.action_tous = QAction("Tracer Toutes les Sections", self)
        self.action_tous.setShortcut("Ctrl+T")
        self.action_tous.triggered.connect(self.ui.tracer_toutes_sections)
        self.menu_visualisation.addAction(self.action_tous)
        
        self.action_combine = QAction("Graphique Combiné", self)
        self.action_combine.setShortcut("Ctrl+C")
        self.action_combine.triggered.connect(self.ui.tracer_graphique_combine)
        self.menu_visualisation.addAction(self.action_combine)
        
        # Menu Aide
        self.menu_aide = self.menu_bar.addMenu("Aide")
        
        # Action pour afficher l'aide
        self.action_aide = QAction("À propos", self)
        self.action_aide.triggered.connect(self.afficher_aide)
        self.menu_aide.addAction(self.action_aide)
        
        # Action pour les raccourcis
        self.action_raccourcis = QAction("Raccourcis clavier", self)
        self.action_raccourcis.triggered.connect(self.afficher_raccourcis)
        self.menu_aide.addAction(self.action_raccourcis)
        
        # Configuration supplémentaire
        self.setWindowTitle("Analyse de Diagramme de Rayonnement - Projet Professionnel")
        self.setWindowIcon(QtGui.QIcon("icon.ico"))  # Utiliser l'icône si disponible
    
    def exporter_resultats(self):
        """Exporte les résultats actuels"""
        if not self.ui.input_rayons.text().strip():
            QMessageBox.warning(self, "Attention", "Aucune donnée à exporter.")
            return
            
        options = QFileDialog.Option(0)
        file_name, selected_filter = QFileDialog.getSaveFileName(
            self, "Exporter les Résultats", "",
            "Fichiers CSV (*.csv);;Fichiers texte (*.txt);;Tous les fichiers (*)", 
            options=options
        )
        
        if not file_name:
            return
            
        try:
            # Récupérer les données
            donnees = self.ui.collecter_donnees()
            if donnees is not None:
                if file_name.endswith('.csv'):
                    donnees.to_csv(file_name, index=False)
                else:
                    # Format texte simple
                    with open(file_name, 'w') as f:
                        f.write("# Données du diagramme de rayonnement\n")
                        f.write("# Format: angle,rayon\n")
                        for _, row in donnees.iterrows():
                            f.write(f"{row['angle']},{row['rayon']}\n")
                            
                self.ui.barre_etat.showMessage(f"Données exportées vers {file_name}", 3000)
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Erreur lors de l'exportation : {str(e)}")
            
    def afficher_aide(self):
        """Affiche la boîte de dialogue d'aide"""
        about_text = """
        <div style="text-align: center; margin-bottom: 15px;">
            <h2 style="color: #2E86C1;">Analyseur de Diagramme de Rayonnement</h2>
            <p style="font-size: 12px;">Version 2.0</p>
        </div>
        
        <p style="margin-bottom: 10px;">Cette application professionnelle permet d'analyser et de visualiser les diagrammes de rayonnement d'antennes avec des graphiques de haute qualité.</p>
        
        <h3 style="color: #2E86C1;">Fonctionnalités:</h3>
        <ul>
            <li>Chargement de données à partir de fichiers texte ou CSV</li>
            <li>Détection automatique des sections par date/heure</li>
            <li>Visualisation en diagramme polaire, 2D et 3D</li>
            <li>Comparaison de multiples sections de données</li>
            <li>Graphiques combinés pour analyses comparatives</li>
            <li>Export des résultats</li>
        </ul>
        
        <p style="margin-top: 15px; font-style: italic; font-size: 11px;">Développé dans le cadre du projet de fin de cycle préparatoire 2024-2025.</p>
        """
        
        QMessageBox.about(self, "À propos de l'Analyseur", about_text)
    
    def afficher_raccourcis(self):
        """Affiche la liste des raccourcis clavier"""
        raccourcis_text = """
        <div style="text-align: center; margin-bottom: 15px;">
            <h2 style="color: #2E86C1;">Raccourcis Clavier</h2>
        </div>
        
        <table style="width: 100%; border-collapse: collapse;">
            <tr style="background-color: #ECF0F1;">
                <th style="padding: 8px; text-align: left; border: 1px solid #BDC3C7;">Action</th>
                <th style="padding: 8px; text-align: left; border: 1px solid #BDC3C7;">Raccourci</th>
            </tr>
            <tr>
                <td style="padding: 8px; border: 1px solid #BDC3C7;">Charger un fichier</td>
                <td style="padding: 8px; border: 1px solid #BDC3C7;">Ctrl+O</td>
            </tr>
            <tr style="background-color: #ECF0F1;">
                <td style="padding: 8px; border: 1px solid #BDC3C7;">Exporter les résultats</td>
                <td style="padding: 8px; border: 1px solid #BDC3C7;">Ctrl+S</td>
            </tr>
            <tr>
                <td style="padding: 8px; border: 1px solid #BDC3C7;">Diagramme Polaire</td>
                <td style="padding: 8px; border: 1px solid #BDC3C7;">Ctrl+P</td>
            </tr>
            <tr style="background-color: #ECF0F1;">
                <td style="padding: 8px; border: 1px solid #BDC3C7;">Diagramme Sphérique 3D</td>
                <td style="padding: 8px; border: 1px solid #BDC3C7;">Ctrl+3</td>
            </tr>
            <tr>
                <td style="padding: 8px; border: 1px solid #BDC3C7;">Diagramme 2D</td>
                <td style="padding: 8px; border: 1px solid #BDC3C7;">Ctrl+2</td>
            </tr>
            <tr style="background-color: #ECF0F1;">
                <td style="padding: 8px; border: 1px solid #BDC3C7;">Tracer Toutes les Sections</td>
                <td style="padding: 8px; border: 1px solid #BDC3C7;">Ctrl+T</td>
            </tr>
            <tr>
                <td style="padding: 8px; border: 1px solid #BDC3C7;">Graphique Combiné</td>
                <td style="padding: 8px; border: 1px solid #BDC3C7;">Ctrl+C</td>
            </tr>
            <tr style="background-color: #ECF0F1;">
                <td style="padding: 8px; border: 1px solid #BDC3C7;">Quitter</td>
                <td style="padding: 8px; border: 1px solid #BDC3C7;">Ctrl+Q</td>
            </tr>
        </table>
        """
        
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("Raccourcis Clavier")
        msg_box.setTextFormat(QtCore.Qt.TextFormat.RichText)
        msg_box.setText(raccourcis_text)
        msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg_box.exec()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())