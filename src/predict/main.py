import os

import numpy as np
import tensorflow as tf
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from preprocessing import preprocess_image
from models import PredictionResponse, HealthResponse, CLASS_NAMES_ES

CLASS_NAMES = [
    "Cardboard", "Food Organics", "Glass", "Metal",
    "Miscellaneous Trash", "Paper", "Plastic",
    "Textile Trash", "Vegetation",
]

model = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global model
    path = os.environ.get("MODEL_PATH", "/app/model/model_prd_colab.keras")
    model = tf.keras.models.load_model(path)
    yield


app = FastAPI(title="RealWaste Classifier", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", response_model=HealthResponse)
def health():
    return HealthResponse(status="ok", model_loaded=model is not None)


@app.post("/predict", response_model=PredictionResponse)
async def predict(file: UploadFile = File(...)):
    contents = await file.read()
    try:
        img = preprocess_image(contents)
    except tf.errors.InvalidArgumentError:
        raise HTTPException(status_code=400, detail="Invalid image file")

    preds = model.predict(img, verbose=0)
    idx = int(np.argmax(preds[0]))

    class_name = CLASS_NAMES[idx]
    return PredictionResponse(
        class_name=class_name,
        class_name_es=CLASS_NAMES_ES[class_name],
        confidence=round(float(preds[0][idx]), 4),
    )
