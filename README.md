  # PlacementIQ — AI Campus Placement & Skill Assessment Platform           

> **Developed by Ashwini Vishal** | AI-powered placement prediction system for students across Engineering, Science, Commerce, and Arts streams.

---

## 🚀 Live Demo

> Deployed on Render — see [render.com](https://render.com) for deployment steps.

---

## 📌 Features

- 🎓 Multi-stream placement prediction (B.Tech, B.Sc, BBA, B.Com, Arts, etc.)
- 📊 Real-time placement probability with animated gauge
- 💼 Estimated CTC package band calculation (in LPA)
- 🔗 Candidate profile link verification (GitHub, LinkedIn, Portfolio)
- 🤖 ML model: Logistic Regression, Random Forest, SVM, XGBoost
- ⚡ FastAPI backend with Scikit-Learn pipeline
- ✨ Premium Glassmorphic dark UI with particle animations

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend API | FastAPI + Uvicorn |
| ML Pipeline | Scikit-Learn + XGBoost + Joblib |
| Data Processing | Pandas + NumPy |
| Frontend | HTML5 + Vanilla CSS + JavaScript |
| Deployment | Render (Free Tier) |

---

## 📁 Project Structure

```
Placement-Prediction/
├── app.py                      # FastAPI application & prediction API
├── train_model.py              # ML model training pipeline
├── placement_pipeline.joblib   # Trained ML model (Logistic Regression)
├── model_metadata.json         # Model info & feature columns
├── requirements.txt            # Python dependencies
├── Procfile                    # Deployment start command (Render)
├── Placement_Data_Full_Class.csv  # Training dataset
└── static/
    ├── index.html              # Frontend UI
    ├── style.css               # Dark glassmorphic theme
    └── script.js               # Animations & API integration
```

---

## ⚙️ Local Development

```bash
# 1. Clone the repo
git clone https://github.com/Ashwinihebbali/Placement-Prediction.git
cd Placement-Prediction

# 2. Create virtual environment
python -m venv venv
venv\Scripts\activate          # Windows
source venv/bin/activate       # Mac/Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. (Optional) Retrain the model
python train_model.py

# 5. Start the server
uvicorn app:app --reload --port 8000

# 6. Open in browser
# http://localhost:8000
```

---

## 🌐 Deploy on Render (Free)

1. Go to [https://render.com](https://render.com) and sign in with GitHub
2. Click **New → Web Service**
3. Select this repository: `Ashwinihebbali/Placement-Prediction`
4. Configure:
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app:app --host 0.0.0.0 --port $PORT`
5. Click **Create Web Service** — live in ~2 minutes!

---

## 📡 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Web UI |
| `POST` | `/api/predict` | Placement Prediction |
| `GET` | `/api/model-info` | Model metadata |
| `GET` | `/docs` | Swagger API Docs |

---

## 📄 License

MIT License — Free to use for educational purposes.

---

*PlacementIQ — Campus Placement & Skill Assessment System © 2026. Developed by Ashwini Vishal.*
