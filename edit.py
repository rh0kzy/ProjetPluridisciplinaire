import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import serial
from PyQt6 import QtCore, QtGui, QtWidgets
from mpl_toolkits.mplot3d import Axes3D
from tkinter import filedialog, messagebox, Tk


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(620, 560)
        font = QtGui.QFont()
        font.setFamily("Montserrat")
        font.setPointSize(20)

        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # Appliquer une image de fond uniquement au centralwidget
        self.centralwidget.setStyleSheet("""
            QWidget#centralwidget {
                border-image: url('./background2.jpg') 0 0 0 0 stretch stretch;
            }
        """)

        self.main_layout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.main_layout.setContentsMargins(80, 40, 80, 40)
        self.main_layout.setSpacing(15)
        self.main_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)



        # Bouton : Charger un fichier
        self.Charger = QtWidgets.QPushButton("Charger un fichier 📂", parent=self.centralwidget)
        self.Charger.setGeometry(QtCore.QRect(87, 53, 446, 58))
        self.Charger.setFont(font)
        self.Charger.setStyleSheet("background-color: white; color: #031045;")
        self.Charger.clicked.connect(self.lire_fichier)

        # Bouton : Tracer en polaire
        self.pushButton = QtWidgets.QPushButton("Tracer en polaire 📊", parent=self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(87, 290, 446, 56))
        self.pushButton.setFont(font)
        self.pushButton.setStyleSheet("background-color: white; color: #031045;")
        self.pushButton.clicked.connect(lambda: self.mettre_a_jour_graphique("polaire"))

        # Bouton : Tracer en sphérique
        self.pushButton_2 = QtWidgets.QPushButton("Tracer en sphérique 🌐", parent=self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(87, 360, 446, 58))
        self.pushButton_2.setFont(font)
        self.pushButton_2.setStyleSheet("background-color: white; color: #031045;")
        self.pushButton_2.clicked.connect(lambda: self.mettre_a_jour_graphique("spherique"))

        # Bouton : Lire depuis USB
        self.pushButton_3 = QtWidgets.QPushButton("Lire depuis USB 💾", parent=self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(87, 430, 446, 58))
        self.pushButton_3.setFont(font)
        self.pushButton_3.setStyleSheet("background-color: white; color: #031045;")
        self.pushButton_3.clicked.connect(self.lire_port_usb)

        # Champs de texte
        
        

        self.lineEdit_4 = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.lineEdit_4.setGeometry(QtCore.QRect(275, 180, 310, 36))
        self.lineEdit_4.setStyleSheet("color: white; background-color: rgba(3, 20, 69, 128);")

        self.lineEdit_5 = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.lineEdit_5.setGeometry(QtCore.QRect(275, 230, 310, 36))
        self.lineEdit_5.setStyleSheet("color: white; background-color: rgba(3, 20, 69, 128);")

        bold_font = QtGui.QFont(font)
        bold_font.setBold(True)
        # Labels
        # Add a new label for the angles information
        self.label_angles_info = QtWidgets.QLabel(
            "Les angles seront automatiquement définis de 1 degré jusqu'à 360 degrés",
            parent=self.centralwidget
        )
        self.label_angles_info.setGeometry(QtCore.QRect(85, 147, 400, 15))
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


    # Start of fonctions


    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle("MainWindow")
        
     # Upload file

    def lire_fichier(self):
        root = Tk()
        root.withdraw()
        chemin_fichier = filedialog.askopenfilename(filetypes=[("Fichiers texte", "*.txt"), ("Fichiers CSV", "*.csv")])
        if not chemin_fichier:
            return
        try:
            data = pd.read_csv(chemin_fichier, delimiter=';', names=['rayon'])
            angles = np.arange(1, len(data) + 1)
            self.lineEdit_3.setText(','.join(map(str, angles.tolist())))
            self.lineEdit_4.setText(','.join(map(str, data['rayon'].tolist())))
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de lire le fichier : {e}")
            
     # Collect Data from text field
    
    def collecter_donnees(self):
        try:
            rayons_str = self.lineEdit_4.text().strip()
            if not rayons_str:
                messagebox.showerror("Erreur", "Veuillez entrer des rayons.")
                return None
            rayons = list(map(float, rayons_str.split(',')))
            val_max = max(rayons)  
            rayons = [r - val_max for r in rayons]
            angles = [i * (360 / len(rayons)) for i in range(len(rayons))]
            return pd.DataFrame({'angle': angles, 'rayon': rayons})
        except ValueError:
            messagebox.showerror("Erreur", "Veuillez entrer des nombres valides.")
            return None
        
    # Polar    
    
    def tracer_polaire(self, donnees):
        angles = np.deg2rad(donnees['angle'])
        rayons = donnees['rayon']
        plt.subplot(projection='polar')
        plt.plot(angles, rayons, 'r')
        plt.title("Graphique Polaire")
        plt.show()
        
    # Spherique    
    
    def tracer_spherique(self, donnees):
        try:
            theta = np.deg2rad(donnees['angle'].values)
            phi = np.linspace(0, np.pi, len(theta))
            r = donnees['rayon'].values
            X = r * np.sin(phi)[:, None] * np.cos(theta)
            Y = r * np.sin(phi)[:, None] * np.sin(theta)
            Z = r * np.cos(phi)[:, None]
            fig = plt.figure(figsize=(8, 6))
            ax = fig.add_subplot(111, projection='3d')
            surf = ax.plot_surface(X, Y, Z, cmap='jet', edgecolor='none')
            fig.colorbar(surf, ax=ax, shrink=0.6, aspect=10)
            ax.set_xlabel("X")
            ax.set_ylabel("Y")
            ax.set_zlabel("Z")
            ax.set_title("Diagramme de Rayonnement 3D")
            plt.show()
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur dans le tracé sphérique : {e}")
            
    # Update Graphique        
    
    def mettre_a_jour_graphique(self, mode):
        donnees = self.collecter_donnees()
        if donnees is not None:
            if mode == "polaire":
                self.tracer_polaire(donnees)
            elif mode == "spherique":
                self.tracer_spherique(donnees)
                
    # Read from USB port            
    
    def lire_port_usb(self):
        port = self.lineEdit_5.text()
        baudrate = 9600
        try:
            ser = serial.Serial(port, baudrate)
            while True:
                ligne = ser.readline().decode('utf-8').strip()
                print(f"Données reçues : {ligne}")
        except Exception as e:
            messagebox.showerror("Erreur", f"Problème avec le port USB : {e}")
            
 ## Main function to run the application           
        

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())
