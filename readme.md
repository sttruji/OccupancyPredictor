# Occupancy Predictor

A FastAPI-based machine learning web application designed to estimate the number of people living in a residential property. Built with a focus on utility for landlords, the app predicts household occupancy using real-world energy usage, appliance count, and geographic metadata, all through a clean and intuitive UI.

---

## 🔍 Project Overview

**Purpose**: Provide landlords and property managers with a tool to estimate actual occupancy versus lease-reported numbers, flagging potential over-occupancy or misuse.

**Core Features**:

* User-friendly web interface built using FastAPI, HTML/CSS, and Chart.js
* Inputs include:

  * Energy usage (kWh, BTU)
  * Square footage, rooms, appliance counts
  * State, climate, and IECC code (auto-encoded)
* Trained Gradient Boosting Classifier with SMOTE to handle class imbalance
* Real-time prediction with probabilistic confidence
* Doughnut chart visualization of predicted class breakdown

**ML Model Details**:

* Gradient Boosting Classifier
* Input features one-hot encoded per state/climate
* Target label: number of occupants, classified into bins (`1`, `2-3`, `4-5`, `6+`)

---

## 🚀 Deployment Options

### 1. **Render** (Recommended for simplicity)

* Connect GitHub repo
* Add `requirements.txt`, point to FastAPI app
* Automatic HTTPS, scalable

**render.yaml**:

```yaml
services:
  - type: web
    name: occupancy-predictor
    runtime: python
    buildCommand: "pip install -r requirements.txt"
    startCommand: "uvicorn occupancy_api:app --host 0.0.0.0 --port 10000"
    envVars:
      - key: PYTHON_VERSION
        value: 3.9
```

### 2. **Google Cloud Run** (Containerized, scalable)

* Package app using Docker
* Deploy from CLI or GitHub Actions

**Dockerfile**:

```Dockerfile
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy contents
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Run app
CMD ["uvicorn", "occupancy_api:app", "--host", "0.0.0.0", "--port", "8080"]
```

Deploy via:

```bash
gcloud run deploy occupancy-predictor \
  --source . \
  --region us-central1 \
  --platform managed \
  --allow-unauthenticated
```

### 3. **Ngrok (For Local Demos)**

* Spin up server on localhost
* Tunnel with `ngrok` to share URL

```bash
uvicorn occupancy_api:app --reload
ngrok http 8000
```

---

## 📁 File Structure

```
OccupancyPredictor/
├── occupancy_api.py         # Main FastAPI app
├── templates/
│   ├── form.html            # User input form
│   └── result.html          # Output visualization
├── static/                  # (Optional) Static assets
├── occupancy_predictor.pkl  # Trained model
├── feature_order.pkl        # Ordered list of model input features
├── requirements.txt         # App dependencies
├── Dockerfile               # For Google Cloud Run
├── render.yaml              # For Render deployment
└── README.md
```

---

## 🧠 Future Utilization

The current application is a proof-of-concept for small-scale use by property owners. But with broader data streams and model improvements, the vision expands:

### 📡 Next-Generation Smart Monitoring System

**Concept**: A national intelligence layer fed by real-time utility and IoT data from smart meters and city-level infrastructure.

**Potential Capabilities**:

* Estimate **current headcount** inside a building in near real-time
* Detect **suspicious congregation/movements** through spikes in energy, WiFi, or waste data
* Analyze **migration patterns** across cities due to work, weather, or other factors
* Track **daily human flow** patterns in/out of zones of interest
* Feed into **Homeland Security dashboards** for threat assessment

**Ethical Focus**: All of this would be **non-invasive**, respecting individual privacy while identifying anomalous patterns at an aggregate level. Like a smart census — continuous, decentralized, and respectful.

---

## 🛠 Tech Stack

* **FastAPI** + Jinja2 Templates
* **scikit-learn**, **pandas**, **joblib**
* **Chart.js** (client-side visualization)
* **SMOTE** from `imblearn` for balancing classes

---

## 📌 Final Notes

If you're a landlord, housing regulator, or data researcher — this tool can help you detect possible lease violations or trends in property usage. It is modular, extendable, and ready to scale into something much bigger.

Pull requests welcome. 🌍
