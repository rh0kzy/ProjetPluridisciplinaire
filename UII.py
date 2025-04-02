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
        MainWindow.setFont(font)
        MainWindow.setStyleSheet("background-color: #031045;\n""")
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.Charger = QtWidgets.QPushButton(parent=self.centralwidget)
        self.Charger.setGeometry(QtCore.QRect(87, 53, 446, 58))
        font = QtGui.QFont()
        font.setFamily("Montserrat")
        font.setPointSize(20)
        self.Charger.setFont(font)
        self.Charger.setStyleSheet("background-color: white;\n"
"color: #031045;")
        self.Charger.setObjectName("Charger")
        self.pushButton = QtWidgets.QPushButton(parent=self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(87, 290, 446, 56))
        font = QtGui.QFont()
        font.setFamily("Montserrat")
        font.setPointSize(20)
        font.setBold(False)
        self.pushButton.setFont(font)
        self.pushButton.setStyleSheet("color: #031045;\n"
"background-color: white;")
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(parent=self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(87, 360, 446, 58))
        font = QtGui.QFont()
        font.setFamily("Montserrat")
        font.setPointSize(20)
        font.setBold(False)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setStyleSheet("color: #031045;\n"
"background-color: white;\n"
"")
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_3 = QtWidgets.QPushButton(parent=self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(87, 430, 446, 58))
        font = QtGui.QFont()
        font.setFamily("Montserrat")
        font.setPointSize(20)
        self.pushButton_3.setFont(font)
        self.pushButton_3.setStyleSheet("color: #031045;\n"
"background-color: white;\n"
"")
        self.pushButton_3.setObjectName("pushButton_3")
        self.lineEdit_3 = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.lineEdit_3.setGeometry(QtCore.QRect(275, 130, 310, 36))
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.lineEdit_4 = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.lineEdit_4.setGeometry(QtCore.QRect(275, 180, 310, 36))
        self.lineEdit_4.setObjectName("lineEdit_4")
        self.lineEdit_5 = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.lineEdit_5.setGeometry(QtCore.QRect(275, 230, 310, 36))
        self.lineEdit_5.setObjectName("lineEdit_5")
        self.label = QtWidgets.QLabel(parent=self.centralwidget)
        self.label.setGeometry(QtCore.QRect(85, 130, 171, 35))
        font = QtGui.QFont()
        font.setFamily("Montserrat")
        font.setPointSize(20)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(parent=self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(85, 180, 171, 35))
        font = QtGui.QFont()
        font.setFamily("Montserrat")
        font.setPointSize(20)
        font.setBold(False)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(parent=self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(90, 240, 181, 20))
        font = QtGui.QFont()
        font.setFamily("Montserrat")
        font.setPointSize(18)
        font.setBold(False)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(parent=self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(0, 0, 620, 560))
        self.label_4.setText("")
        self.label_4.setObjectName("label_4")
        self.label_4.raise_()
        self.pushButton.raise_()
        self.pushButton_2.raise_()
        self.pushButton_3.raise_()
        self.lineEdit_3.raise_()
        self.lineEdit_4.raise_()
        self.lineEdit_5.raise_()
        self.label.raise_()
        self.label_2.raise_()
        self.label_3.raise_()
        self.Charger.raise_()
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(parent=MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 620, 33))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(parent=MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.Charger.setText(_translate("MainWindow", "Charger un fichier 📂"))
        self.pushButton.setText(_translate("MainWindow", "Tracer en polaire 📊"))
        self.pushButton_2.setText(_translate("MainWindow", "Tracer en spherique 🌐"))
        self.pushButton_3.setText(_translate("MainWindow", "Lire depuis USB 💾"))
        self.label.setText(_translate("MainWindow", "Angles 📐 :"))
        self.label_2.setText(_translate("MainWindow", "Rayons 📏 :"))
        self.label_3.setText(_translate("MainWindow", "Port USB🔌;"))

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
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())
