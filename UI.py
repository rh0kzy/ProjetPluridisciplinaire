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
        MainWindow.setObjectName("OptiGraph")
        MainWindow.setWindowIcon(QtGui.QIcon("C:/Users/PC/Desktop/POO/ProjetPluridisciplinaire/icon.png"))
        MainWindow.resize(620, 560)
        font = QtGui.QFont()
        font.setFamily("Montserrat")
        font.setPointSize(20)
        MainWindow.setFont(font)

        # Set background image
        MainWindow.setStyleSheet("""
            QMainWindow {
                background-image: url('C:/Users/PC/Desktop/12067355_4884273.jpg');
                background-repeat: no-repeat;
                background-position: center;
                background-size: cover;
            }
        """)

        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        
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
        self.lineEdit_3 = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.lineEdit_3.setGeometry(QtCore.QRect(275, 130, 310, 36))
        self.lineEdit_4 = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.lineEdit_4.setGeometry(QtCore.QRect(275, 180, 310, 36))
        self.lineEdit_5 = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.lineEdit_5.setGeometry(QtCore.QRect(275, 230, 310, 36))
        
        # Labels
        self.label = QtWidgets.QLabel("Angles 📐 :", parent=self.centralwidget)
        self.label.setGeometry(QtCore.QRect(85, 130, 171, 35))
        self.label.setFont(font)
        
        self.label_2 = QtWidgets.QLabel("Rayons 📏 :", parent=self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(85, 180, 171, 35))
        self.label_2.setFont(font)
        
        self.label_3 = QtWidgets.QLabel("Port USB 🔌:", parent=self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(90, 240, 181, 20))
        self.label_3.setFont(font)
        
        MainWindow.setCentralWidget(self.centralwidget)

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

    def collecter_donnees(self):
        try:
            angles_str = self.lineEdit_3.text().strip()
            rayons_str = self.lineEdit_4.text().strip()
            if not rayons_str:
                messagebox.showerror("Erreur", "Veuillez entrer des rayons.")
                return None
            rayons = list(map(float, rayons_str.split(',')))
            angles = [i * (360 / len(rayons)) for i in range(len(rayons))]
            return pd.DataFrame({'angle': angles, 'rayon': rayons})
        except ValueError:
            messagebox.showerror("Erreur", "Veuillez entrer des nombres valides.")
            return None

    def tracer_polaire(self, donnees):
        angles = np.deg2rad(donnees['angle'])
        rayons = donnees['rayon']
        plt.subplot(projection='polar')
        plt.plot(angles, rayons, 'r')
        plt.title("Graphique Polaire")
        plt.show()

    def tracer_spherique(self, donnees):
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        angles = np.deg2rad(donnees['angle'])
        rayons = donnees['rayon']
        x = rayons * np.cos(angles)
        y = rayons * np.sin(angles)
        z = np.linspace(0, len(rayons), len(rayons))
        ax.plot(x, y, z, 'r')
        plt.title("Graphique Sphérique")
        plt.show()

    def mettre_a_jour_graphique(self, mode):
        donnees = self.collecter_donnees()
        if donnees is not None:
            if mode == "polaire":
                self.tracer_polaire(donnees)
            elif mode == "spherique":
                self.tracer_spherique(donnees)

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
        finally:
            ser.close()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())
