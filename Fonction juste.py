import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import serial
import serial.tools.list_ports
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import (QMessageBox, QFileDialog, 
                            QMainWindow, QApplication, 
                            QVBoxLayout, QHBoxLayout,
                            QGroupBox, QPushButton,
                            QLabel, QLineEdit,
                            QComboBox, QStatusBar)
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class RadiationPatternAnalyzer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setup_ui()
        self.donnees = None
        
    def setup_ui(self):
        self.setWindowTitle("Analyse de Diagramme de Rayonnement")
        self.resize(1000, 800)
        
        # Color scheme
        self.primary_color = "#031045"
        self.secondary_color = "#4ECDC4"
        self.accent_color = "#FF6B6B"
        self.text_color = "#FFFFFF"
        self.background_color = "#F5F7FA"
        
        # Main widget and layout
        self.central_widget = QtWidgets.QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(30, 20, 30, 20)
        self.main_layout.setSpacing(15)
        
        # Apply stylesheet
        self.setStyleSheet(f"""
            QMainWindow {{
                background-color: {self.primary_color};
            }}
            QWidget {{
                font-family: 'Segoe UI';
                font-size: 12pt;
            }}
            QPushButton {{
                background-color: {self.text_color};
                color: {self.primary_color};
                border-radius: 8px;
                padding: 8px 16px;
                min-width: 120px;
            }}
            QPushButton:hover {{
                background-color: {self.secondary_color};
                color: {self.text_color};
            }}
            QLineEdit, QComboBox {{
                background-color: white;
                border: 2px solid {self.secondary_color};
                border-radius: 6px;
                padding: 6px;
            }}
            QGroupBox {{
                border: 2px solid {self.secondary_color};
                border-radius: 10px;
                margin-top: 10px;
                padding-top: 15px;
                color: {self.text_color};
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }}
        """)
        
        # Create UI sections
        self.create_header()
        self.create_file_input_section()
        self.create_usb_section()
        self.create_visualization_section()
        self.create_status_bar()
        
        # Initialize serial ports
        self.update_serial_ports()
        
    def create_header(self):
        header = QHBoxLayout()
        title = QLabel("Analyse de Diagramme de Rayonnement")
        title.setStyleSheet(f"font-size: 20pt; font-weight: bold; color: {self.text_color};")
        header.addWidget(title)
        header.addStretch()
        self.main_layout.addLayout(header)
        
    def create_file_input_section(self):
        group = QGroupBox("Entrée des Données")
        layout = QVBoxLayout()
        
        # File load button
        self.load_file_btn = QPushButton("Charger un fichier (CSV/TXT)")
        self.load_file_btn.clicked.connect(self.load_file)
        layout.addWidget(self.load_file_btn)
        
        # Manual input
        input_layout = QHBoxLayout()
        input_layout.addWidget(QLabel("Rayons:"))
        
        self.radii_input = QLineEdit()
        self.radii_input.setPlaceholderText("Entrez les valeurs séparées par des virgules")
        input_layout.addWidget(self.radii_input)
        
        layout.addLayout(input_layout)
        
        # Info label
        info = QLabel("*Les angles sont générés automatiquement selon le nombre de rayons")
        info.setStyleSheet(f"font-size: 10pt; font-style: italic; color: {self.secondary_color};")
        layout.addWidget(info)
        
        group.setLayout(layout)
        self.main_layout.addWidget(group)
        
    def create_usb_section(self):
        group = QGroupBox("Connexion USB")
        layout = QVBoxLayout()
        
        # Port selection
        port_layout = QHBoxLayout()
        port_layout.addWidget(QLabel("Port COM:"))
        
        self.port_combo = QComboBox()
        port_layout.addWidget(self.port_combo)
        
        self.refresh_btn = QPushButton("🔄")
        self.refresh_btn.setFixedSize(40, 40)
        self.refresh_btn.setToolTip("Rafraîchir les ports")
        self.refresh_btn.clicked.connect(self.update_serial_ports)
        port_layout.addWidget(self.refresh_btn)
        
        layout.addLayout(port_layout)
        
        # Read button
        self.read_usb_btn = QPushButton("Lire depuis le port série")
        self.read_usb_btn.clicked.connect(self.read_serial_port)
        layout.addWidget(self.read_usb_btn)
        
        group.setLayout(layout)
        self.main_layout.addWidget(group)
        
    def create_visualization_section(self):
        group = QGroupBox("Visualisation")
        layout = QHBoxLayout()
        
        # Plot buttons
        self.polar_btn = QPushButton("Diagramme Polaire")
        self.polar_btn.clicked.connect(lambda: self.update_plot("polar"))
        
        self.spherical_btn = QPushButton("Diagramme 3D")
        self.spherical_btn.clicked.connect(lambda: self.update_plot("3d"))
        
        layout.addWidget(self.polar_btn)
        layout.addWidget(self.spherical_btn)
        
        group.setLayout(layout)
        self.main_layout.addWidget(group)
        
    def create_status_bar(self):
        self.status_bar = QStatusBar()
        self.status_bar.setStyleSheet(f"color: {self.text_color};")
        self.setStatusBar(self.status_bar)
        
    def update_serial_ports(self):
        """Update the list of available serial ports"""
        self.port_combo.clear()
        ports = serial.tools.list_ports.comports()
        for port in ports:
            self.port_combo.addItem(port.device)
            
    def load_file(self):
        """Load data from CSV or TXT file"""
        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "Ouvrir un fichier de données",
            "",
            "Fichiers de données (*.csv *.txt);;Tous les fichiers (*)"
        )
        
        if file_name:
            try:
                if file_name.endswith('.txt'):
                    # Read TXT file with one value per line
                    with open(file_name, 'r') as f:
                        lines = f.readlines()
                        rayons = [float(line.strip()) for line in lines if line.strip()]
                else:
                    # Read CSV file
                    df = pd.read_csv(file_name)
                    if 'rayon' in df.columns:
                        rayons = df['rayon'].values
                    else:
                        QMessageBox.critical(self, "Erreur", "Le fichier CSV doit contenir une colonne 'rayon'")
                        return
                
                self.radii_input.setText(','.join(map(str, rayons)))
                self.prepare_data()
                self.status_bar.showMessage(f"Fichier chargé: {file_name}", 3000)
                
            except ValueError as ve:
                QMessageBox.critical(self, "Erreur", f"Format de nombre invalide dans le fichier: {str(ve)}")
            except Exception as e:
                QMessageBox.critical(self, "Erreur", f"Erreur de lecture: {str(e)}")
                
    def read_serial_port(self):
        """Read data from serial port"""
        port = self.port_combo.currentText()
        if not port:
            QMessageBox.critical(self, "Erreur", "Aucun port sélectionné")
            return
            
        try:
            with serial.Serial(port, 9600, timeout=2) as ser:
                data = ser.readline().decode('utf-8').strip()
                if data:
                    self.radii_input.setText(data)
                    self.prepare_data()
                    self.status_bar.showMessage(f"Données reçues de {port}", 3000)
                else:
                    QMessageBox.warning(self, "Avertissement", "Aucune donnée reçue")
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Erreur série: {str(e)}")
            
    def prepare_data(self):
        """Prepare data for plotting"""
        try:
            radii_str = self.radii_input.text().strip()
            if not radii_str:
                raise ValueError("Aucune donnée entrée")
                
            radii = np.array([float(x) for x in radii_str.split(',')])
            angles = np.linspace(0, 360, len(radii), endpoint=False)
            
            # Normalize data (values - max)
            radii_normalized = radii - np.max(radii)
            
            self.donnees = pd.DataFrame({
                'angle': angles,
                'rayon': radii_normalized
            })
            
            return True
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Données invalides: {str(e)}")
            return False
            
    def update_plot(self, plot_type):
        """Update the plot based on selected type"""
        if not self.prepare_data():
            return
            
        plt.style.use('seaborn-v0_8-darkgrid')
        
        if plot_type == "polar":
            self.plot_polar()
        elif plot_type == "3d":
            self.plot_3d()
            
    def plot_polar(self):
        """Create polar plot"""
        try:
            fig = plt.figure(figsize=(8, 6))
            ax = fig.add_subplot(111, projection='polar')
            
            angles = np.deg2rad(self.donnees['angle'])
            radii = self.donnees['rayon']
            
            ax.plot(angles, radii, color=self.accent_color, linewidth=2)
            ax.set_title("Diagramme Polaire Normalisé", pad=20)
            ax.grid(True)
            
            # Adjust radial ticks
            r_ticks = np.linspace(np.min(radii), 0, 5)
            ax.set_rticks(r_ticks)
            ax.set_yticklabels([f"{tick:.1f}" for tick in r_ticks])
            
            plt.tight_layout()
            plt.show()
            
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Erreur de tracé polaire: {str(e)}")
            self.status_bar.showMessage("Erreur lors du tracé polaire", 3000)
        
    def plot_3d(self):
        """Create 3D spherical plot"""
        try:
            fig = plt.figure(figsize=(10, 8))
            ax = fig.add_subplot(111, projection='3d')
            
            theta = np.deg2rad(self.donnees['angle'])
            phi = np.linspace(0, np.pi, len(theta))
            r = self.donnees['rayon'].values
            
            theta_grid, phi_grid = np.meshgrid(theta, phi)
            r_grid = np.tile(r, (len(phi), 1))
            
            X = r_grid * np.sin(phi_grid) * np.cos(theta_grid)
            Y = r_grid * np.sin(phi_grid) * np.sin(theta_grid)
            Z = r_grid * np.cos(phi_grid)
            
            norm = plt.Normalize(np.min(r), 0)
            surf = ax.plot_surface(X, Y, Z, cmap='viridis', norm=norm, alpha=0.8)
            
            fig.colorbar(surf, ax=ax, shrink=0.5, label='Intensité Normalisée')
            ax.set_title("Diagramme 3D Normalisé")
            ax.view_init(elev=30, azim=45)
            
            plt.tight_layout()
            plt.show()
            
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Erreur de tracé 3D: {str(e)}")
            self.status_bar.showMessage("Erreur lors du tracé 3D", 3000)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Set application style
    app.setStyle('Fusion')
    palette = QtGui.QPalette()
    palette.setColor(QtGui.QPalette.ColorRole.Window, QtGui.QColor(3, 16, 69))
    palette.setColor(QtGui.QPalette.ColorRole.WindowText, QtCore.Qt.GlobalColor.white)
    app.setPalette(palette)
    
    window = RadiationPatternAnalyzer()
    window.show()
    sys.exit(app.exec())