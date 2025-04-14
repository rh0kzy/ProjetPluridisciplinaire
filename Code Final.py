import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import serial
import serial.tools.list_ports
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

        # Connecter les boutons
        self.load_file_btn.clicked.connect(self.lire_fichier)
        self.refresh_btn.clicked.connect(self.actualiser_ports_serie)
        self.read_usb_btn.clicked.connect(self.lire_port_usb)
        self.polar_btn.clicked.connect(lambda: self.mettre_a_jour_graphique("polaire"))
        self.sphere_btn.clicked.connect(lambda: self.mettre_a_jour_graphique("spherique"))

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
                        lines = f.readlines()
                        rayons = [float(line.strip()) for line in lines if line.strip()]
                else:
                    df = pd.read_csv(file_name)
                    if 'rayon' in df.columns:
                        rayons = df['rayon'].values
                    else:
                        QMessageBox.critical(None, "Erreur", "Le fichier doit contenir une colonne 'rayon'")
                        return

                self.input_rayons.setText(','.join(map(str, rayons)))
                self.barre_etat.showMessage(f"Fichier {file_name} chargé avec succès", 3000)

            except Exception as e:
                QMessageBox.critical(None, "Erreur", f"Impossible de lire le fichier: {str(e)}")

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
        
    def tracer_polaire(self, donnees):
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
        
    def tracer_spherique(self, donnees):
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
            if mode == "polaire":
                self.tracer_polaire(donnees)
            elif mode == "spherique":
                self.tracer_spherique(donnees)
    
    def lire_port_usb(self):
        """Lit les données depuis le port USB sélectionné"""
        port = self.port_combo.currentText()
        if not port:
            QMessageBox.critical(None, "Erreur", "Aucun port sélectionné")
            return
            
        try:
            with serial.Serial(port, 9600, timeout=2) as ser:
                data = ser.readline().decode('utf-8').strip()
                if data:
                    self.input_rayons.setText(data)
                    self.barre_etat.showMessage(f"Données reçues de {port}", 3000)
                else:
                    QMessageBox.warning(None, "Avertissement", "Aucune donnée reçue")
        except Exception as e:
            QMessageBox.critical(None, "Erreur", f"Erreur de communication série: {str(e)}")

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