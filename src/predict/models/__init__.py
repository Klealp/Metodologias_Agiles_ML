from pydantic import BaseModel

CLASS_NAMES_ES = {
    "Cardboard": "Cartón",
    "Food Organics": "Residuos Orgánicos",
    "Glass": "Vidrio",
    "Metal": "Metal",
    "Miscellaneous Trash": "Basura Miscelánea",
    "Paper": "Papel",
    "Plastic": "Plástico",
    "Textile Trash": "Residuos Textiles",
    "Vegetation": "Vegetación",
}


class PredictionResponse(BaseModel):
    class_name: str
    class_name_es: str
    confidence: float


class HealthResponse(BaseModel):
    status: str
    model_loaded: bool
