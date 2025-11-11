from fastapi import FastAPI
from pydantic import BaseModel  # <-- 1. Importamos BaseModel para definir qué "pedidos" aceptamos

# 2. Importamos nuestra función "receta" desde el otro archivo
from src.scraper import analizar_url 

# 3. Definimos el formato del "pedido"
# Queremos que nos envíen un JSON como este: {"url": "http://ejemplo.com"}
class UrlRequest(BaseModel):
    url: str

# 4. Creamos la aplicación
app = FastAPI(
    title="API de Sentimiento Navarro",
    description="Un proyecto para analizar el sentimiento de reseñas."
)

# 5. Creamos el endpoint raíz (el mismo de antes)
@app.get("/")
def read_root():
    return {"message": "¡Bienvenido a la API de Sentimiento Navarro!"}

# 6. --- ¡EL NUEVO ENDPOINT! ---
# Usamos @app.post() porque el usuario nos "envía" (POST) datos (la URL)
@app.post("/analizar")
def analizar_sentimiento(request: UrlRequest):
    """
    Recibe una URL, la procesa con la función `analizar_url`
    y devuelve los resultados.
    """
    print(f"Recibido pedido para analizar: {request.url}")
    # 7. Llamamos a nuestra función "receta"
    resultados = analizar_url(request.url)
    
    # 8. Devolvemos los resultados
    return {"resultados_del_analisis": resultados}