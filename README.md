# 📊 Polar & Spherical Data Visualizer

A Python GUI application built with **PyQt6**, **Matplotlib**, and **Pandas** for loading, processing, and visualizing data in **polar** and **spherical** coordinate systems. The application also supports **serial communication via USB** for real-time data acquisition.

---

## 🚀 Features

✅ **Load Data from File**: Import `.txt` or `.csv` files containing data points.
✅ **Plot in Polar Coordinates** 📊: Generate 2D polar graphs.
✅ **Plot in Spherical Coordinates** 🌐: Generate 3D spherical graphs.
✅ **USB Data Acquisition** 🔌: Read real-time data from a serial port (e.g., Arduino sensors).
✅ **Interactive UI** 🎨: Designed using **PyQt6** with a modern look.

---

## 📦 Dependencies
Ensure you have the following Python libraries installed:

```bash
pip install pyqt6 pandas numpy matplotlib pyserial
```

---

## 🛠 Installation & Usage

1️⃣ **Clone this repository:**
```bash
git clone https://github.com/your-username/your-repo.git
cd your-repo
```

2️⃣ **Run the application:**
```bash
python main.py
```

---

## 📁 File Structure
```
📂 Your Project Directory
 ├── 📜 main.py            # Main application script
 ├── 📜 README.md          # Documentation (this file)
 ├── 📜 requirements.txt   # Required dependencies
 ├── 🖼️ IMG_4627.png        # Logo (blue marine version)
 ├── 🖼️ IMG_4627_white.png  # Logo (white version)
 ├── 📜 UI.ui              # Qt Designer UI file
 ├── 📜 UI.py              # PyQt converted UI file
```

---

## 📌 Usage Guide

### 🗂 Loading a File
- Click **"Charger un fichier 📂"** and select a `.csv` or `.txt` file.
- Data will be displayed in the UI.

### 📊 Plotting Data
- Click **"Tracer en polaire 📊"** to generate a **2D polar plot**.
- Click **"Tracer en sphérique 🌐"** to generate a **3D spherical plot**.

### 🔌 Reading USB Data
- Enter the **USB port name** (e.g., `COM3` on Windows, `/dev/ttyUSB0` on Linux/Mac).
- Click **"Lire depuis USB 💾"** to start reading data.

---

## 👨‍💻 Collaborators
This project is developed by:
- **Hiba Daghbouj**
- **Rachid Hamdaoui**
- **Aymen Belkadi**
- **Guemaz Reda**
- **Korichi Hannane**

---

## 🛡️ License
This project is **private**. No external contributions are accepted.

---

### ✨ Author
**Aymen Belkadi**  
📧 Contact: [your email or GitHub profile]

