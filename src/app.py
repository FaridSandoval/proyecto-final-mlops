from fastapi import FastAPI
from pydantic import BaseModel
import onnxruntime as ort
import numpy as np
import os
# Importamos nuestras funciones del otro archivo
from .utils import download_model_if_not_exists, save_prediction_log

app = FastAPI()

# Configuración
BUCKET_NAME = os.getenv("S3_BUCKET_NAME")
MODEL_KEY = "models/iris.onnx" # Ruta dentro del bucket
LOCAL_MODEL_PATH = "iris.onnx"

# Variable global para el modelo
session = None

class IrisInput(BaseModel):
    sepal_length: float
    sepal_width: float
    petal_length: float
    petal_width: float

@app.on_event("startup")
async def startup_event():
    global session
    # 1. Intentar descargar modelo
    if BUCKET_NAME:
        download_model_if_not_exists(BUCKET_NAME, MODEL_KEY, LOCAL_MODEL_PATH)
    
    # 2. Cargar modelo en memoria
    if os.path.exists(LOCAL_MODEL_PATH):
        session = ort.InferenceSession(LOCAL_MODEL_PATH)
        print("Modelo cargado correctamente.")
    else:
        print("ADVERTENCIA: Modelo no encontrado.")

@app.get("/")
def read_root():
    return {"message": "API Iris MLOps Activa"}

@app.post("/predict")
def predict(iris_input: IrisInput):
    if session is None:
        return {"error": "Modelo no disponible"}
    
    # Preparar datos
    data = np.array([[
        iris_input.sepal_length,
        iris_input.sepal_width,
        iris_input.petal_length,
        iris_input.petal_width
    ]], dtype=np.float32)
    
    # Predecir
    input_name = session.get_inputs()[0].name
    output_name = session.get_outputs()[0].name
    result = session.run([output_name], {input_name: data})
    pred = int(result[0][0])
    
    # Guardar Log en S3
    if BUCKET_NAME:
        save_prediction_log(BUCKET_NAME, data.tolist(), pred)
    
    clases = ["Setosa", "Versicolor", "Virginica"]
    return {"clase": clases[pred], "id": pred}