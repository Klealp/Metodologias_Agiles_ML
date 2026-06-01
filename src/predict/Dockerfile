FROM tensorflow/tensorflow:2.19.0

WORKDIR /app

COPY src/predict/requirements.txt .
RUN pip install --no-cache-dir --upgrade keras
RUN pip install --no-cache-dir -r requirements.txt

COPY scripts/evaluation/model_prd_colab.keras /app/model/model_prd_colab.keras

COPY src/predict/main.py .
COPY src/predict/preprocessing/ ./preprocessing/
COPY src/predict/models/ ./models/

ENV MODEL_PATH=/app/model/model_prd_colab.keras

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
