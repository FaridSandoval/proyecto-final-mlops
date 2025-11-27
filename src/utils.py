import boto3
import os
import datetime

# Inicializar cliente S3
s3 = boto3.client('s3')

def download_model_if_not_exists(bucket_name, model_key, local_path):
    # Descarga el modelo desde S3 si no existe
    if not os.path.exists(local_path):
        print(f"Descargando modelo de S3: {bucket_name}/{model_key} ...")
        try:
            s3.download_file(bucket_name, model_key, local_path)
            print("Descarga exitosa.")
        except Exception as e:
            print(f"Error descargando el modelo: {e}")
            # No lanzamos error fatal aqui para permitir tests locales si es necesario
    else:
        print("El modelo ya existe localmente.")

def save_prediction_log(bucket_name, input_data, prediction):
    # Guarda un archivo de texto en S3 con la predicción
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S-%f')
    file_name = f"logs/pred_{timestamp}.txt"
    log_content = f"Input: {input_data} | Prediction: {prediction}\n"
    
    print(f"Guardando log en S3: {file_name}")
    try:
        s3.put_object(Body=log_content, Bucket=bucket_name, Key=file_name)
    except Exception as e:
        print(f"Error guardando log: {e}")