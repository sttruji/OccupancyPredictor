# occupancy_api.py
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
import joblib
import numpy as np
import pandas as pd
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn

# Load trained model and feature order
model = joblib.load("occupancy_predictor.pkl")
classes = model.classes_
feature_order = joblib.load("feature_order.pkl")

# Initialize app and templates
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Organize feature inputs
state_options = [f.replace("state_postal_", "") for f in feature_order if f.startswith("state_postal_")]
climate_options = [f.replace("BA_climate_", "") for f in feature_order if f.startswith("BA_climate_")]
iecc_options = [f.replace("IECC_climate_code_", "") for f in feature_order if f.startswith("IECC_climate_code_")]

descriptive_labels = {
    "KWH": "Electricity Usage (kWh)",
    "BTUEL": "Total Site Energy (BTU)",
    "HDD65": "Heating Degree Days (HDD65)",
    "CDD65": "Cooling Degree Days (CDD65)",
    "TOTHSQFT": "Heated Square Footage",
    "TOTROOMS": "Total Number of Rooms",
    "BEDROOMS": "Number of Bedrooms",
    "NUMFRIG": "Number of Refrigerators",
    "NUMFREEZ": "Number of Standalone Freezers",
    "NUMTABLET": "Number of Tablets"
}

core_inputs = list(descriptive_labels.keys())

@app.get("/", response_class=HTMLResponse)
def get_form(request: Request):
    return templates.TemplateResponse("form.html", {
        "request": request,
        "core_inputs": core_inputs,
        "labels": descriptive_labels,
        "state_options": state_options,
        "climate_options": climate_options,
        "iecc_options": iecc_options
    })

@app.post("/predict", response_class=HTMLResponse)
def predict(
    request: Request,
    expected_people: str = Form(...),
    state: str = Form(...),
    climate: str = Form(...),
    iecc: str = Form(...),
    KWH: float = Form(0),
    BTUEL: float = Form(0),
    HDD65: float = Form(0),
    CDD65: float = Form(0),
    TOTHSQFT: float = Form(0),
    TOTROOMS: float = Form(0),
    BEDROOMS: float = Form(0),
    NUMFRIG: float = Form(0),
    NUMFREEZ: float = Form(0),
    NUMTABLET: float = Form(0),
):
    try:
        input_dict = {col: 0.0 for col in feature_order}  # initialize all to zero

        # Set core inputs
        input_dict.update({
            "KWH": KWH,
            "BTUEL": BTUEL,
            "HDD65": HDD65,
            "CDD65": CDD65,
            "TOTHSQFT": TOTHSQFT,
            "TOTROOMS": TOTROOMS,
            "BEDROOMS": BEDROOMS,
            "NUMFRIG": NUMFRIG,
            "NUMFREEZ": NUMFREEZ,
            "NUMTABLET": NUMTABLET,
        })

        # Set one-hot selections
        input_dict[f"state_postal_{state}"] = 1.0
        input_dict[f"BA_climate_{climate}"] = 1.0
        input_dict[f"IECC_climate_code_{iecc}"] = 1.0

        # Create DataFrame in correct order
        df_input = pd.DataFrame([input_dict[col] for col in feature_order], index=feature_order).T

        # Predict
        probs = model.predict_proba(df_input)[0]
        class_probs = dict(zip(classes, probs))
        top_class = max(class_probs, key=class_probs.get)
        top_prob = class_probs[top_class]

        if top_prob >= 0.5:
            result_text = top_class
        else:
            result_text = "Model not confident enough to make a prediction."

        return templates.TemplateResponse("result.html", {
            "request": request,
            "result": result_text,
            "confidence": f"{top_prob*100:.1f}%",
            "class_probs": class_probs,
            "expected": expected_people
        })

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

if __name__ == "__main__":
    uvicorn.run("occupancy_api:app", host="0.0.0.0", port=8000, reload=True)
