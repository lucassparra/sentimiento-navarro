import requests
from bs4 import BeautifulSoup
from transformers import pipeline  # <-- 1. Importamos la 'pipeline' de Hugging Face

# --- CONFIGURACIÓN DEL MODELO DE IA ---
# 2. Cargamos un modelo de análisis de sentimiento
# "pipeline" es una forma fácil de usar un modelo complejo.
# Elegimos un modelo que ya está entrenado para español (aunque las citas estén en inglés,
# este modelo es multilingüe y nos servirá para el proyecto real).
print("Cargando modelo de IA (esto puede tardar la primera vez)...")
sentiment_pipeline = pipeline(
    "sentiment-analysis", 
    model="cardiffnlp/twitter-xlm-roberta-base-sentiment"
)
print("¡Modelo cargado!")
# -------------------------------------


# 1. URL
URL_EJEMPLO = "https://quotes.toscrape.com/"

# 2. Petición
print(f"Haciendo petición a: {URL_EJEMPLO}")
response = requests.get(URL_EJEMPLO)

# 3. Verificación
if response.status_code == 200:
    print("Petición exitosa (Código 200).")
    
    # 4. Creamos la "sopa"
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # 5. Buscamos los elementos
    print("\n--- CITAS Y ANÁLISIS DE SENTIMIENTO ---")
    citas_encontradas = soup.find_all('span', class_='text')
    
    # 6. Recorremos los resultados, los analizamos y los imprimimos
    for cita in citas_encontradas:
        texto_cita = cita.text
        
        # --- ¡Aquí usamos la IA! ---
        # 7. Pasamos el texto de la cita a nuestro modelo
        resultado_sentimiento = sentiment_pipeline(texto_cita)[0]
        
        # 8. Imprimimos el resultado de forma bonita
        etiqueta = resultado_sentimiento['label']
        confianza = resultado_sentimiento['score'] * 100  # Convertir a porcentaje
        
        print(f"\nCITA: {texto_cita}")
        print(f"SENTIMIENTO: {etiqueta} (Confianza: {confianza:.2f}%)")
    
    print("\n--- FIN DEL ANÁLISIS ---\n")

else:
    print(f"Error en la petición. Código: {response.status_code}")
