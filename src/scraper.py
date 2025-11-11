import requests
from bs4 import BeautifulSoup
from transformers import pipeline

# --- ¡CAMBIO IMPORTANTE! ---
# 1. Cargamos el modelo de IA UNA SOLA VEZ, cuando el programa se inicia.
# Esto es crucial para la velocidad. No queremos cargarlo con cada "pedido".
print("Cargando modelo de IA (esto solo pasa una vez al iniciar)...")
try:
    sentiment_pipeline = pipeline(
        "sentiment-analysis", 
        model="cardiffnlp/twitter-xlm-roberta-base-sentiment"
    )
    print("¡Modelo de IA cargado con éxito!")
except Exception as e:
    print(f"Error cargando el modelo de IA: {e}")
    sentiment_pipeline = None

# 2. Creamos la función principal que usará nuestra API
def analizar_url(url: str):
    """
    Esta función recibe una URL, la scrapea, analiza el sentimiento
    y devuelve una lista de resultados.
    """
    
    if sentiment_pipeline is None:
        return {"error": "El modelo de IA no está disponible."}
        
    print(f"Iniciando análisis para: {url}")
    
    # --- LÓGICA DEL SCRAPER (Fase 2) ---
    try:
        response = requests.get(url)
        if response.status_code != 200:
            return {"error": f"Error en la petición. Código: {response.status_code}"}
        
        soup = BeautifulSoup(response.text, 'html.parser')
        citas_encontradas = soup.find_all('span', class_='text')
        
        if not citas_encontradas:
            return {"error": "No se encontraron citas ('span', class_='text') en la URL."}

        # --- LÓGICA DE IA (Fase 3) ---
        resultados = []
        for cita in citas_encontradas:
            texto_cita = cita.text
            
            # Analizamos el sentimiento
            resultado_sentimiento = sentiment_pipeline(texto_cita)[0]
            
            # Guardamos un diccionario limpio
            resultados.append({
                "texto": texto_cita,
                "sentimiento": resultado_sentimiento['label'],
                "confianza": resultado_sentimiento['score']
            })
        
        print(f"Análisis completado. Encontradas {len(resultados)} citas.")
        return resultados

    except Exception as e:
        print(f"Ha ocurrido un error durante el scraping o análisis: {e}")
        return {"error": f"Ha ocurrido un error interno: {e}"}

# --- FIN DE LOS CAMBIOS ---
# Ya no hay código "suelto". Todo está dentro de una función
# o es parte de la configuración inicial.
