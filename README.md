# 📊 Polar & Spherical Data Visualizer

A professional-grade Python application for analyzing and visualizing radiation patterns in polar and spherical coordinate systems. Designed for researchers, engineers, and antenna designers, this tool offers advanced features for data processing, visualization, and export.

---

## 🚀 Features

### **Data Import**
- Import `.txt` or `.csv` files containing radiation pattern data.
- Automatic detection of date-based sections for organized analysis.

### **Visualization Modes**
- **Polar Coordinates** 📊: Generate 2D polar plots with customizable styles.
- **Spherical Coordinates** 🌐: Create 3D spherical plots with advanced shading and lighting.
- **Combined Visualization** 🔄: Compare multiple datasets side-by-side.
- **2D Cartesian Plots** 📈: Visualize normalized data in 2D.

### **Data Processing**
- Apply moving averages for data smoothing.
- Normalize data for accurate comparisons.
- Export processed data to `.csv` files.

### **Interactive UI**
- Modern design using **PyQt6**.
- Intuitive controls for loading, processing, and visualizing data.
- Real-time feedback via status bar messages.

### **Error Handling**
- Comprehensive error messages for invalid inputs or file formats.

---

## 📦 Dependencies

Ensure you have the following Python libraries installed:

```bash
pip install pyqt6 pandas numpy matplotlib pyvista
```

---

## 🛠 Installation & Usage

### **Installation**

1️⃣ **Clone this repository:**
```bash
git clone https://github.com/rh0kzy/ProjetPluridisciplinaire.git
cd ProjetPluridisciplinaire
```

2️⃣ **Install dependencies:**
```bash
pip install -r requirements.txt
```

### **Run the Application**
```bash
python DONTTOUCH.py
```

---

## 📁 File Structure

```
📂 ProjetPluridisciplinaire
 ├── 📜 DONTTOUCH.py         # Main application script
 ├── 📜 debug_import.py      # Debugging script
 ├── 📜 README.md            # Original documentation
 ├── 📜 README_PRO.md        # Professional documentation
 ├── 📜 requirements.txt     # Required dependencies
 ├── 🖼️ IMG_4627.png          # Logo (blue marine version)
 ├── 🖼️ IMG_4627_white.png    # Logo (white version)
 ├── 📜 DONTTOUCH.spec       # PyInstaller spec file
 ├── 📂 build/               # Build artifacts
 └── 📂 __pycache__/         # Compiled Python files
```

---

## 📌 Usage Guide

### **Loading a File**
- Click **"Charger un fichier 📂"** and select a `.csv` or `.txt` file.
- Data will be displayed in the UI.

### **Plotting Data**
- Click **"Tracer en polaire 📊"** to generate a **2D polar plot**.
- Click **"Tracer en sphérique 🌐"** to generate a **3D spherical plot**.
- Click **"Tracer combiné 🔄"** to compare datasets side-by-side.

### **Exporting Data**
- Processed data can be exported to `.csv` files for further analysis.

---

## 👨‍💻 Collaborators

This project is developed by:
- **Hiba Daghbouj**
- **Rachid Hamdaoui**
- **Aymen Belkadi**
- **Guemaz Reda**

---

## 🛡️ License

This project is **private**. No external contributions are accepted.

---

### ✨ Author
**Aymen Belkadi**  
📧 Contact: [@rh0kzy]
