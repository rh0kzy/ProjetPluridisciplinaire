import sys
import re
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import serial
import serial.tools.list_ports
from PyQt6.QtGui import QAction 
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QMessageBox, QFileDialog
from mpl_toolkits.mplot3d import Axes3D

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
            }}
            QComboBox {{
                background-color: rgba(255, 255, 255, 0.9);
                border: 2px solid {self.secondary_color};
                border-radius: 8px;
                padding: 5px;
                color: {self.primary_color};
            }}
            QComboBox QAbstractItemView {{
                background-color: white;
                color: {self.primary_color};
                selection-background-color: {self.secondary_color};
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
        self.title_label.setStyleSheet(f"color: {self.text_color};")
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
        self.radii_label.setStyleSheet(f"color: {self.text_color};")
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
        self.angles_info.setFont(info_font)
        self.angles_info.setStyleSheet(f"color: {self.secondary_color};")
        self.file_layout.addWidget(self.angles_info)

        # Menu déroulant pour les sections par date
        self.sections_layout = QtWidgets.QHBoxLayout()
        self.sections_label = QtWidgets.QLabel("Sélection par date 📅:")
        self.sections_label.setFont(font)
        self.sections_label.setStyleSheet(f"color: {self.text_color};")
        self.sections_layout.addWidget(self.sections_label)
        
        self.sections_combo = QtWidgets.QComboBox()
        self.sections_combo.setFont(font)
        self.sections_combo.setPlaceholderText("Sélectionnez une date")
        self.sections_layout.addWidget(self.sections_combo)
        self.file_layout.addLayout(self.sections_layout)

        self.main_layout.addWidget(self.file_group)

        # Section USB
        self.usb_group = QtWidgets.QGroupBox("Connexion USB")
        self.usb_group.setFont(font)
        self.usb_group.setStyleSheet(f"""
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
        
        self.usb_layout = QtWidgets.QVBoxLayout(self.usb_group)
        
        # Sélection port
        self.port_layout = QtWidgets.QHBoxLayout()
        self.port_label = QtWidgets.QLabel("Port USB 🔌:")
        self.port_label.setFont(font)
        self.port_label.setStyleSheet(f"color: {self.text_color};")
        self.port_layout.addWidget(self.port_label)
        
        self.port_combo = QtWidgets.QComboBox()
        self.port_combo.setFont(font)
        self.port_layout.addWidget(self.port_combo)
        
        self.refresh_btn = QtWidgets.QPushButton("🔄")
        self.refresh_btn.setFixedSize(40, 40)
        self.refresh_btn.setToolTip("Rafraîchir la liste des ports")
        self.port_layout.addWidget(self.refresh_btn)
        self.usb_layout.addLayout(self.port_layout)

        # Bouton lecture USB
        self.read_usb_btn = QtWidgets.QPushButton("Lire depuis USB 💾")
        self.read_usb_btn.setFont(font)
        self.usb_layout.addWidget(self.read_usb_btn)

        self.main_layout.addWidget(self.usb_group)

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
        
        self.viz_layout = QtWidgets.QHBoxLayout(self.viz_group)
        
        # Bouton polaire
        self.polar_btn = QtWidgets.QPushButton("Tracer en polaire 📊")
        self.polar_btn.setFont(font)
        self.viz_layout.addWidget(self.polar_btn)
        
        # Bouton sphérique
        self.sphere_btn = QtWidgets.QPushButton("Tracer en sphérique 🌐")
        self.sphere_btn.setFont(font)
        self.viz_layout.addWidget(self.sphere_btn)
        
        # Bouton pour tracer tous les graphiques
        self.all_graphs_btn = QtWidgets.QPushButton("Tracer tout les graphes 📈")
        self.all_graphs_btn.setFont(font)
        self.viz_layout.addWidget(self.all_graphs_btn)
        
        self.main_layout.addWidget(self.viz_group)

        # Barre d'état
        self.status_bar = QtWidgets.QStatusBar()
        self.status_bar.setFont(font)
        self.status_bar.setStyleSheet(f"color: {self.text_color};")
        MainWindow.setStatusBar(self.status_bar)

        MainWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(MainWindow)
        
        # Initialiser la liste des ports
        self.actualiser_ports_serie()

        # Définir les références
        self.input_rayons = self.radii_input
        self.barre_etat = self.status_bar
        
        # Variable pour stocker les sections de données
        self.sections_donnees = []

        # Connecter les boutons
        self.load_file_btn.clicked.connect(self.lire_fichier)
        self.refresh_btn.clicked.connect(self.actualiser_ports_serie)
        self.read_usb_btn.clicked.connect(self.lire_port_usb)
        self.polar_btn.clicked.connect(lambda: self.mettre_a_jour_graphique("polaire"))
        self.sphere_btn.clicked.connect(lambda: self.mettre_a_jour_graphique("spherique"))
        self.all_graphs_btn.clicked.connect(self.tracer_toutes_sections)
        self.sections_combo.currentIndexChanged.connect(self.charger_section_selectionnee)

        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Analyse de Diagramme de Rayonnement"))

    def actualiser_ports_serie(self):
        """Met à jour la liste des ports série disponibles"""
        self.port_combo.clear()
        ports = serial.tools.list_ports.comports()
        for port in ports:
            self.port_combo.addItem(port.device)

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
        """Trace le diagramme sphérique 3D"""
        try:
            plt.style.use('seaborn-v0_8-darkgrid')
            
            theta = np.deg2rad(donnees['angle'].values)
            phi = np.linspace(0, np.pi, len(theta))
            r = donnees['rayon'].values
            
            theta_grid, phi_grid = np.meshgrid(theta, phi)
            r_grid = np.tile(r, (len(phi), 1))
            
            X = r_grid * np.sin(phi_grid) * np.cos(theta_grid)
            Y = r_grid * np.sin(phi_grid) * np.sin(theta_grid)
            Z = r_grid * np.cos(phi_grid)
            
            fig = plt.figure(figsize=(10, 8))
            ax = fig.add_subplot(111, projection='3d')
            
            # Normalisation des couleurs
            norm = plt.Normalize(np.min(r), 0)
            
            surf = ax.plot_surface(X, Y, Z, 
                                 cmap='viridis',
                                 norm=norm,
                                 alpha=0.8)
            
            fig.colorbar(surf, ax=ax, shrink=0.5, label='Intensité Normalisée')
            
            if titre:
                ax.set_title(f"Diagramme 3D - {titre}")
            else:
                ax.set_title("Diagramme 3D Normalisé")
            ax.view_init(elev=30, azim=45)
            
            plt.tight_layout()
            plt.show()
            
        except Exception as e:
            QMessageBox.critical(None, "Erreur", f"Erreur dans le tracé sphérique : {str(e)}")
            self.barre_etat.showMessage("Erreur lors du tracé sphérique", 3000)

    def mettre_a_jour_graphique(self, mode):
        """Met à jour le graphique selon le mode sélectionné"""
        donnees = self.collecter_donnees()
        if donnees is not None:
            titre = self.sections_combo.currentText() if self.sections_combo.currentIndex() >= 0 else None
            
            if mode == "polaire":
                self.tracer_polaire(donnees, titre)
            elif mode == "spherique":
                self.tracer_spherique(donnees, titre)
    
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

    def lire_port_usb(self):
        """Lit les données depuis le port USB sélectionné"""
        port_selectionne = self.port_combo.currentText()
        
        if not port_selectionne:
            QMessageBox.critical(None, "Erreur", "Aucun port USB sélectionné.")
            return
            
        try:
            # Configuration du port série
            ser = serial.Serial(
                port=port_selectionne,
                baudrate=9600,
                timeout=1
            )
            
            self.barre_etat.showMessage(f"Connexion au port {port_selectionne}...", 3000)
            
            # Attente de la stabilisation de la connexion
            import time
            time.sleep(2)
            
            # Lecture des données (timeout après 30 secondes)
            debut = time.time()
            donnees = []
            
            while time.time() - debut < 30:
                if ser.in_waiting > 0:
                    ligne = ser.readline().decode('utf-8').strip()
                    try:
                        valeur = float(ligne)
                        donnees.append(valeur)
                        self.barre_etat.showMessage(f"Lecture en cours... ({len(donnees)} valeurs reçues)", 1000)
                    except ValueError:
                        # Ignorer les lignes qui ne sont pas des nombres
                        pass
                        
                # Si on a reçu beaucoup de données, on peut arrêter
                if len(donnees) > 100:
                    break
                    
                # Petite pause pour éviter de surcharger le CPU
                time.sleep(0.1)
                
            # Fermeture du port
            ser.close()
            
            if not donnees:
                QMessageBox.warning(None, "Attention", "Aucune donnée numérique reçue du port USB.")
                return
                
            # Mise à jour du champ de saisie
            self.input_rayons.setText(','.join(map(str, donnees)))
            
            # Enregistrer comme une nouvelle section avec la date et l'heure actuelles
            from datetime import datetime
            date_actuelle = datetime.now().strftime("%d-%m-%Y")
            heure_actuelle = datetime.now().strftime("%H:%M:%S")
            
            self.sections_donnees.append((date_actuelle, heure_actuelle, donnees))
            self.sections_combo.addItem(f"{date_actuelle} {heure_actuelle}")
            self.sections_combo.setCurrentIndex(self.sections_combo.count() - 1)
            
            self.barre_etat.showMessage(f"Lecture terminée : {len(donnees)} valeurs lues depuis {port_selectionne}", 5000)
            
        except serial.SerialException as e:
            QMessageBox.critical(None, "Erreur", f"Erreur de communication série : {str(e)}")
        except Exception as e:
            QMessageBox.critical(None, "Erreur", f"Erreur lors de la lecture USB : {str(e)}")

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
            <li>Acquisition de données via port USB</li>
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