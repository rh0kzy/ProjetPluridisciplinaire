import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import serial
import serial.tools.list_ports
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QMessageBox, QFileDialog
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import gridspec

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(620, 560)
        font = QtGui.QFont()
        font.setFamily("Montserrat")
        font.setPointSize(20)

        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # Background image
        self.centralwidget.setStyleSheet("""
            QWidget#centralwidget {
                border-image: url('./background2.jpg') 0 0 0 0 stretch stretch;
            }
        """)

        self.main_layout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.main_layout.setContentsMargins(80, 40, 80, 40)
        self.main_layout.setSpacing(15)
        self.main_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        # Buttons
        self.Charger = QtWidgets.QPushButton("Charger un fichier 📂", parent=self.centralwidget)
        self.Charger.setGeometry(QtCore.QRect(87, 53, 446, 58))
        self.Charger.setFont(font)
        self.Charger.setStyleSheet("background-color: white; color: #031045;")
        self.Charger.clicked.connect(self.lire_fichier)

        self.pushButton = QtWidgets.QPushButton("Tracer en polaire 📊", parent=self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(87, 290, 446, 56))
        self.pushButton.setFont(font)
        self.pushButton.setStyleSheet("background-color: white; color: #031045;")
        self.pushButton.clicked.connect(lambda: self.mettre_a_jour_graphique("polaire"))

        self.pushButton_2 = QtWidgets.QPushButton("Tracer en sphérique 🌐", parent=self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(87, 360, 446, 58))
        self.pushButton_2.setFont(font)
        self.pushButton_2.setStyleSheet("background-color: white; color: #031045;")
        self.pushButton_2.clicked.connect(lambda: self.mettre_a_jour_graphique("spherique"))

        self.pushButton_3 = QtWidgets.QPushButton("Lire depuis USB 💾", parent=self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(87, 430, 446, 58))
        self.pushButton_3.setFont(font)
        self.pushButton_3.setStyleSheet("background-color: white; color: #031045;")
        self.pushButton_3.clicked.connect(self.lire_port_usb)

        # Input fields
        self.lineEdit_4 = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.lineEdit_4.setGeometry(QtCore.QRect(275, 180, 310, 36))
        self.lineEdit_4.setStyleSheet("color: white; background-color: rgba(3, 20, 69, 128);")

        # Serial port selection
        self.combo_serial_ports = QtWidgets.QComboBox(parent=self.centralwidget)
        self.combo_serial_ports.setGeometry(QtCore.QRect(275, 230, 250, 36))
        self.combo_serial_ports.setStyleSheet("""
            QComboBox {
                color: white; 
                background-color: rgba(3, 20, 69, 128);
                padding: 5px;
            }
            QComboBox QAbstractItemView {
                color: white;
                background-color: rgba(3, 20, 69, 200);
            }
        """)

        self.btn_refresh_ports = QtWidgets.QPushButton("🔄", parent=self.centralwidget)
        self.btn_refresh_ports.setGeometry(QtCore.QRect(530, 230, 55, 36))
        self.btn_refresh_ports.setStyleSheet("""
            QPushButton {
                color: white;
                background-color: rgba(3, 20, 69, 128);
                border: none;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: rgba(3, 20, 69, 180);
            }
        """)
        self.btn_refresh_ports.setToolTip("Refresh port list")
        self.btn_refresh_ports.clicked.connect(self.refresh_serial_ports)

        # Labels
        bold_font = QtGui.QFont(font)
        bold_font.setBold(True)
        
        self.label_angles_info = QtWidgets.QLabel(
            "*Les angles sont générés automatiquement selon le nombre de rayons",
            parent=self.centralwidget
        )
        self.label_angles_info.setGeometry(QtCore.QRect(85, 147, 500, 15))
        angles_font = QtGui.QFont()
        angles_font.setPointSize(10)
        angles_font.setBold(True)
        self.label_angles_info.setFont(angles_font)
        self.label_angles_info.setStyleSheet("color: white; background-color: transparent;")  
        
        self.label_2 = QtWidgets.QLabel("Rayons 📏 :", parent=self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(85, 180, 171, 35))
        self.label_2.setFont(bold_font)
        self.label_2.setStyleSheet("color: white;background-color: transparent;")

        self.label_3 = QtWidgets.QLabel("Port USB 🔌:", parent=self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(85, 235, 181, 25))
        self.label_3.setFont(bold_font)
        self.label_3.setStyleSheet("color: white;background-color: transparent;")

        MainWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        
        # Initialize
        self.refresh_serial_ports()
        MainWindow.setFixedSize(MainWindow.size())

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle("Analyse de Diagramme de Rayonnement")

    def refresh_serial_ports(self):
        """Refresh list of connected USB devices"""
        self.combo_serial_ports.clear()
        ports = serial.tools.list_ports.comports()
        
        if not ports:
            self.combo_serial_ports.addItem("No USB devices found", None)
            return
        
        usb_devices = []
        for port in ports:
            if 'USB' in port.description.upper():
                device_name = port.description.split('(')[0].strip()
                usb_devices.append((device_name, port.device))
        
        if not usb_devices:
            self.combo_serial_ports.addItem("No USB devices found", None)
        else:
            usb_devices.sort(key=lambda x: x[0])
            for name, port in usb_devices:
                self.combo_serial_ports.addItem(name, port)

    def lire_fichier(self):
        """Read data file with 720 values and date/time stamp"""
        file_dialog = QFileDialog()
        file_dialog.setNameFilter("Text files (*.txt)")
        if file_dialog.exec():
            chemin_fichier = file_dialog.selectedFiles()[0]
            if not chemin_fichier:
                return
            
            try:
                with open(chemin_fichier, 'r') as f:
                    lines = [line.strip() for line in f if line.strip()]
                
                values = []
                date_time = ""
                
                # Process file to extract values and date/time
                for line in lines:
                    if '/' in line or '-' in line:  # Date format detection
                        if ':' in line:  # Time part
                            date_time = line
                    else:
                        try:
                            values.append(float(line))
                        except ValueError:
                            pass
                
                if len(values) != 720:
                    QMessageBox.warning(self.centralwidget, "Attention", 
                                      f"Le fichier devrait contenir 720 valeurs, mais {len(values)} ont été trouvées.")
                
                # Store values and date for plotting
                self.rayons_data = np.array(values)
                self.data_date_time = date_time
                self.lineEdit_4.setText(','.join(map(str, values)))
                
                QMessageBox.information(self.centralwidget, "Succès", 
                                       f"Fichier chargé avec succès\n{date_time}\n{len(values)} valeurs")
                
            except Exception as e:
                QMessageBox.critical(self.centralwidget, "Erreur", f"Impossible de lire le fichier : {e}")

    def lire_port_usb(self):
        """Read data from USB port"""
        if self.combo_serial_ports.currentData() is None:
            QMessageBox.critical(self.centralwidget, "Erreur", "Aucun port USB sélectionné!")
            return
            
        port = self.combo_serial_ports.currentData()
        baudrate = 9600
        
        try:
            with serial.Serial(port, baudrate, timeout=1) as ser:
                QMessageBox.information(self.centralwidget, "Succès", f"Connecté au port {port}")
                
                # Read data
                received_data = []
                while len(received_data) < 720:  # Read until we get 720 values
                    if ser.in_waiting:
                        line = ser.readline().decode('utf-8').strip()
                        try:
                            value = float(line)
                            received_data.append(value)
                            print(f"Donnée reçue: {value} ({len(received_data)}/720)")
                            
                            # Update the display
                            current_text = self.lineEdit_4.text()
                            if current_text:
                                self.lineEdit_4.setText(f"{current_text},{line}")
                            else:
                                self.lineEdit_4.setText(line)
                                
                        except ValueError:
                            print(f"Ignoring non-numeric data: {line}")
                
                # Store the received data
                self.rayons_data = np.array(received_data)
                self.data_date_time = "Données USB - " + QtCore.QDateTime.currentDateTime().toString()
                
                QMessageBox.information(self.centralwidget, "Succès", 
                                       f"720 valeurs reçues avec succès!\n{self.data_date_time}")
                        
        except serial.SerialException as e:
            QMessageBox.critical(self.centralwidget, "Erreur", f"Problème avec le port USB : {e}")
        except Exception as e:
            QMessageBox.critical(self.centralwidget, "Erreur", f"Erreur inattendue : {e}")

    def collecter_donnees(self):
        """Collect data from input field or loaded file"""
        try:
            if hasattr(self, 'rayons_data'):
                rayons = self.rayons_data
            else:
                rayons_str = self.lineEdit_4.text().strip()
                if not rayons_str:
                    QMessageBox.critical(self.centralwidget, "Erreur", "Veuillez entrer des rayons.")
                    return None
                rayons = list(map(float, rayons_str.split(',')))
            
            val_max = max(rayons)  
            rayons = [r - val_max for r in rayons]
            return pd.DataFrame({'rayon': rayons})
            
        except ValueError:
            QMessageBox.critical(self.centralwidget, "Erreur", "Veuillez entrer des nombres valides.")
            return None

    def tracer_polaire(self, donnees):
        """Create polar plot"""
        plt.figure(figsize=(8, 6))
        angles = np.linspace(0, 2*np.pi, len(donnees['rayon']), endpoint=False)
        plt.subplot(projection='polar')
        plt.plot(angles, donnees['rayon'], 'r-', linewidth=1.5, alpha=0.7)
        plt.title(f"Diagramme Polaire\n{getattr(self, 'data_date_time', '')}", pad=20)
        plt.grid(True)
        plt.tight_layout()
        plt.show()
        
    def tracer_spherique(self, donnees):
        """Create 3D spherical plot"""
        try:
            angles = np.linspace(0, 2*np.pi, len(donnees['rayon']), endpoint=False)
            phi = np.linspace(0, np.pi, len(donnees['rayon']))
            r_normalized = (donnees['rayon'] - np.min(donnees['rayon'])) / (np.max(donnees['rayon']) - np.min(donnees['rayon']))
            
            X = r_normalized * np.outer(np.sin(phi), np.cos(angles))
            Y = r_normalized * np.outer(np.sin(phi), np.sin(angles))
            Z = r_normalized * np.outer(np.cos(phi), np.ones_like(angles))
            
            fig = plt.figure(figsize=(10, 8))
            ax = fig.add_subplot(111, projection='3d')
            surf = ax.plot_surface(X, Y, Z, cmap='jet', 
                                 rstride=1, cstride=1, 
                                 linewidth=0, antialiased=True)
            
            fig.colorbar(surf, ax=ax, shrink=0.5, aspect=5)
            ax.set_title(f"Diagramme de Rayonnement 3D\n{getattr(self, 'data_date_time', '')}", pad=20)
            ax.set_xlabel("X")
            ax.set_ylabel("Y")
            ax.set_zlabel("Z")
            plt.tight_layout()
            plt.show()
        except Exception as e:
            QMessageBox.critical(self.centralwidget, "Erreur", f"Erreur dans le tracé sphérique : {e}")

    def mettre_a_jour_graphique(self, mode):
        """Update the graph based on selected mode"""
        donnees = self.collecter_donnees()
        if donnees is not None:
            if mode == "polaire":
                self.tracer_polaire(donnees)
            elif mode == "spherique":
                self.tracer_spherique(donnees)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())