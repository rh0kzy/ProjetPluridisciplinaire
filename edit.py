import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import serial
import serial.tools.list_ports
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QMessageBox
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

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
        self.load_file_btn.clicked.connect(self.lire_fichier)
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
        self.refresh_btn.clicked.connect(self.actualiser_ports_serie)
        self.port_layout.addWidget(self.refresh_btn)
        self.usb_layout.addLayout(self.port_layout)

        # Bouton lecture USB
        self.read_usb_btn = QtWidgets.QPushButton("Lire depuis USB 💾")
        self.read_usb_btn.setFont(font)
        self.read_usb_btn.clicked.connect(self.lire_port_serie)
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
        self.polar_btn.clicked.connect(lambda: self.mettre_a_jour_graphique("polaire"))
        self.viz_layout.addWidget(self.polar_btn)
        
        # Bouton sphérique
        self.sphere_btn = QtWidgets.QPushButton("Tracer en sphérique 🌐")
        self.sphere_btn.setFont(font)
        self.sphere_btn.clicked.connect(lambda: self.mettre_a_jour_graphique("spherique"))
        self.viz_layout.addWidget(self.sphere_btn)

        self.main_layout.addWidget(self.viz_group)

        # Barre d'état
        self.status_bar = QtWidgets.QStatusBar()
        self.status_bar.setFont(font)
        self.status_bar.setStyleSheet(f"color: {self.text_color};")
        MainWindow.setStatusBar(self.status_bar)

        MainWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        
        # Initialiser la liste des ports
        self.actualiser_ports_serie()

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle("Analyse de Diagramme de Rayonnement")

    def actualiser_ports_serie(self):
        """Actualiser la liste des ports série disponibles"""
        self.port_combo.clear()
        ports = serial.tools.list_ports.comports()
        
        if not ports:
            self.port_combo.addItem("Aucun port trouvé")
            self.status_bar.showMessage("Aucun port USB détecté", 3000)
        else:
            for port, desc, hwid in sorted(ports):
                self.port_combo.addItem(f"{port}: {desc}", port)
            self.status_bar.showMessage(f"{len(ports)} ports USB trouvés", 3000)

    def lire_fichier(self):
        file_dialog = QtWidgets.QFileDialog()
        file_dialog.setNameFilter("Fichiers texte (*.txt *.csv)")
        if file_dialog.exec():
            chemin_fichier = file_dialog.selectedFiles()[0]
            if not chemin_fichier:
                return
            try:
                # Lire le fichier
                with open(chemin_fichier, 'r') as f:
                    content = f.read().strip()
                    # Gérer les séparateurs
                    rayons = [float(x) for x in content.replace('\n', ',').split(',') if x.strip()]
                
                self.radii_input.setText(','.join(map(str, rayons)))
                QMessageBox.information(self.centralwidget, "Succès", 
                                      f"{len(rayons)} valeurs chargées avec succès!")
                
            except Exception as e:
                QMessageBox.critical(self.centralwidget, "Erreur", 
                                   f"Erreur de lecture: {str(e)}\nAssurez-vous que le fichier contient uniquement des nombres séparés par des virgules.")

    def collecter_donnees(self):
        try:
            rayons_str = self.radii_input.text().strip()
            if not rayons_str:
                QMessageBox.critical(self.centralwidget, "Erreur", "Veuillez entrer des rayons.")
                return None
            
            # Convertir en liste de floats
            rayons = list(map(float, rayons_str.split(',')))
            
            # Normalisation des données
            rayons = np.array(rayons)
            min_val = np.min(rayons)
            max_val = np.max(rayons)
            
            # Option 1: Conserver l'échelle mais commencer à 0
            rayons = rayons - min_val
            
            # Générer les angles
            angles = np.linspace(0, 360, len(rayons), endpoint=False)
            
            return pd.DataFrame({'angle': angles, 'rayon': rayons})
            
        except ValueError:
            QMessageBox.critical(self.centralwidget, "Erreur", 
                               "Format invalide. Entrez des nombres séparés par des virgules.")
            return None
        
    def tracer_polaire(self, donnees):
        try:
            plt.style.use('seaborn-v0_8-darkgrid')
            fig = plt.figure(figsize=(10, 8))
            ax = plt.subplot(111, projection='polar')
            
            angles = np.deg2rad(donnees['angle'])
            rayons = donnees['rayon']
            
            # Tracé principal sans marqueurs
            ax.plot(angles, rayons, 
                   color=self.accent_color,
                   linewidth=3,
                   label='Données')
            
            # Personnalisation
            ax.set_title("Diagramme Polaire\nAnalyse de Rayonnement", 
                        fontsize=18, 
                        fontweight='bold', 
                        pad=20,
                        color=self.primary_color)
            
            # Grille et axes
            ax.grid(True, linestyle='--', alpha=0.7, color='gray')
            ax.set_thetagrids(np.arange(0, 360, 45), 
                           labels=np.arange(0, 360, 45),
                           fontsize=12)
            
            # Graduations radiales
            r_ticks = np.linspace(0, np.max(rayons), 5)
            ax.set_rticks(r_ticks)
            ax.set_yticklabels([f"{tick:.1f}" for tick in r_ticks], 
                             fontsize=10,
                             color='gray')
            
            # Légende
            ax.legend(loc='upper right', bbox_to_anchor=(1.15, 1.15),
                     frameon=True, shadow=True, facecolor='white')
            
            # Barre de couleur
            sm = plt.cm.ScalarMappable(cmap=plt.cm.viridis, 
                                     norm=plt.Normalize(vmin=np.min(rayons), vmax=np.max(rayons)))
            sm.set_array([])
            cbar = plt.colorbar(sm, ax=ax, pad=0.1)
            cbar.set_label('Intensité', rotation=270, labelpad=20)
            
            plt.tight_layout()
            plt.show()
            
        except Exception as e:
            QMessageBox.critical(self.centralwidget, "Erreur", f"Erreur dans le tracé polaire : {str(e)}")
            self.status_bar.showMessage("Erreur lors du tracé polaire", 3000)
        
    def tracer_spherique(self, donnees):
        try:
            plt.style.use('seaborn-v0_8-darkgrid')
            
            theta = np.deg2rad(donnees['angle'].values)
            phi = np.linspace(0, np.pi, len(theta))
            r = donnees['rayon'].values
            
            # Coordonnées sphériques
            theta_grid, phi_grid = np.meshgrid(theta, phi)
            r_grid = np.tile(r, (len(phi), 1))
            
            # Conversion en coordonnées cartésiennes
            X = r_grid * np.sin(phi_grid) * np.cos(theta_grid)
            Y = r_grid * np.sin(phi_grid) * np.sin(theta_grid)
            Z = r_grid * np.cos(phi_grid)
            
            fig = plt.figure(figsize=(12, 10))
            ax = fig.add_subplot(111, projection='3d')
            
            # Surface 3D
            surf = ax.plot_surface(X, Y, Z, 
                                 cmap='viridis',
                                 edgecolor='none',
                                 alpha=0.8,
                                 rstride=1,
                                 cstride=1)
            
            # Barre de couleur
            cbar = fig.colorbar(surf, ax=ax, shrink=0.6, aspect=10)
            cbar.set_label('Intensité', rotation=270, labelpad=20)
            
            # Labels
            ax.set_xlabel("X", fontsize=12, labelpad=10)
            ax.set_ylabel("Y", fontsize=12, labelpad=10)
            ax.set_zlabel("Z", fontsize=12, labelpad=10)
            ax.set_title("Diagramme de Rayonnement 3D", 
                        fontsize=18, 
                        fontweight='bold',
                        pad=20,
                        color=self.primary_color)
            
            # Angle de vue
            ax.view_init(elev=30, azim=45)
            
            plt.tight_layout()
            plt.show()
            
        except Exception as e:
            QMessageBox.critical(self.centralwidget, "Erreur", f"Erreur dans le tracé sphérique : {str(e)}")
            self.status_bar.showMessage("Erreur lors du tracé sphérique", 3000)
            
    def mettre_a_jour_graphique(self, mode):
        donnees = self.collecter_donnees()
        if donnees is not None:
            if mode == "polaire":
                self.tracer_polaire(donnees)
            elif mode == "spherique":
                self.tracer_spherique(donnees)
            self.status_bar.showMessage("Graphique généré avec succès", 3000)
                
    def lire_port_serie(self):
        if self.port_combo.currentData() is None:
            QMessageBox.critical(self.centralwidget, "Erreur", "Aucun port USB sélectionné!")
            self.status_bar.showMessage("Aucun port sélectionné", 3000)
            return
            
        port = self.port_combo.currentData()
        baudrate = 9600
        
        try:
            with serial.Serial(port, baudrate, timeout=1) as ser:
                QMessageBox.information(self.centralwidget, "Succès", f"Connecté au port {port}")
                self.status_bar.showMessage(f"Lecture en cours depuis {port}...", 3000)
                
                data_points = []
                start_time = QtCore.QDateTime.currentDateTime()
                
                while QtCore.QDateTime.currentDateTime().secsTo(start_time) < 5:
                    if ser.in_waiting:
                        line = ser.readline().decode('utf-8').strip()
                        if line:
                            try:
                                value = float(line)
                                data_points.append(value)
                                self.status_bar.showMessage(f"Valeur lue: {value}", 1000)
                            except ValueError:
                                continue
                
                if data_points:
                    self.radii_input.setText(','.join(map(str, data_points)))
                    self.status_bar.showMessage(f"{len(data_points)} valeurs lues depuis {port}", 5000)
                else:
                    self.status_bar.showMessage("Aucune donnée reçue", 3000)
                    
        except serial.SerialException as e:
            QMessageBox.critical(self.centralwidget, "Erreur", f"Problème avec le port USB : {str(e)}")
            self.status_bar.showMessage("Erreur de communication USB", 3000)
        except Exception as e:
            QMessageBox.critical(self.centralwidget, "Erreur", f"Erreur inattendue : {str(e)}")
            self.status_bar.showMessage("Erreur inattendue", 3000)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    
    # Style de l'application
    app.setStyle('Fusion')
    palette = QtGui.QPalette()
    palette.setColor(QtGui.QPalette.ColorRole.Window, QtGui.QColor(3, 16, 69))
    palette.setColor(QtGui.QPalette.ColorRole.WindowText, QtCore.Qt.GlobalColor.white)
    app.setPalette(palette)
    
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())