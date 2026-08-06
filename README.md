# 🎓 Placement Prediction System

A Machine Learning powered web application that predicts student placement outcomes based on academic and personal attributes.

## 🚀 Features

- **ML-Powered Predictions** — Trained on real placement data using multiple ML/DL models
- **Interactive Web UI** — Beautiful, responsive interface for entering student details
- **REST API** — Flask backend serving predictions via API
- **Comprehensive Analysis** — Provides placement probability along with salary estimates

## 🛠️ Tech Stack

- **Backend**: Python, Flask
- **ML/DL**: scikit-learn, pandas, numpy, joblib
- **Frontend**: HTML, CSS, JavaScript
- **Dataset**: Placement_Data_Full_Class.csv

## 📁 Project Structure

```
Placement Prediction/
├── app.py                          # Flask web application
├── train_model.py                  # Model training script
├── placement_pipeline.joblib       # Trained ML pipeline
├── model_metadata.json             # Model metadata and feature info
├── Placement_Data_Full_Class.csv   # Dataset
├── static/
│   ├── index.html                  # Frontend UI
│   ├── style.css                   # Styling
│   └── script.js                   # Frontend logic
└── Placement_Prediction_ML_DL.ipynb  # Jupyter exploration notebook
```

## ⚙️ Setup & Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd "Placement Prediction"
   ```

2. **Install dependencies**
   ```bash
   pip install flask scikit-learn pandas numpy joblib
   ```

3. **Train the model** (optional — pre-trained model included)
   ```bash
   python train_model.py
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Open in browser**
   ```
   http://localhost:5000
   ```

## 📊 Dataset

The dataset (`Placement_Data_Full_Class.csv`) contains student academic records and placement outcomes from an MBA program, including:
- Secondary Education percentage
- Higher Secondary Education percentage
- Degree type and percentage
- Work experience
- MBA percentage
- Placement status and salary

## 🤖 Model

The prediction pipeline is trained using scikit-learn and saved as a joblib file for fast loading. The `model_metadata.json` contains feature names, encodings, and model performance metrics.

## 📄 License

This project is open source and available under the [MIT License](LICENSE).
