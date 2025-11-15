import streamlit as st
import requests  # <-- 1. Importamos 'requests' para llamar a nuestra API

# --- Configuración de la Página ---
st.set_page_config(
    page_title="Sentimiento Navarro",
    page_icon="🍽️",  # Icono de la pestaña
    layout="centered"  # Centrar el contenido
)

# --- Títulos ---
st.title("Proyecto: Sentimiento Navarro 🍽️")
st.header("Análisis de Sentimiento de Reseñas de Hostelería")

st.write("""
    Esta herramienta utiliza un modelo de IA para analizar el sentimiento
    de las reseñas en una página de ejemplo.
""")
st.write("---")

# --- 2. Widgets Interactivos ---

# st.text_input() crea una caja de texto. El texto que el usuario escriba
# se guardará en la variable 'url_ingresada'
url_ingresada = st.text_input(
    "Pega la URL para analizar (ej: https://quotes.toscrape.com/)",
    value="https://quotes.toscrape.com/"  # Un valor por defecto
)

# st.button() crea un botón. El código dentro del 'if' solo se ejecuta
# cuando el usuario hace clic en el botón.
if st.button("Analizar Sentimiento"):
    
    # 3. --- Lógica de Conexión al Backend ---
    
    # Esta es la URL de nuestra "cocina" (FastAPI) que está corriendo en local
    API_URL = "http://127.0.0.1:8000/analizar"
    
    # El "pedido" que le hacemos a la cocina (el formato JSON que definimos)
    payload = {"url": url_ingresada}
    
    try:
        # Mostramos un mensaje de espera
        with st.spinner("Cargando modelo de IA y analizando reseñas... ¡Esto puede tardar un poco!"):
            
            # Usamos 'requests' para "llamar" a nuestra API
            response = requests.post(API_URL, json=payload)
            
            # Verificamos si la "cocina" nos respondió bien
            if response.status_code == 200:
                # Si todo va bien, mostramos los resultados
                resultados = response.json()
                
                st.write("---")
                st.subheader("🎉 ¡Análisis Completado!")
                
                # st.json() muestra el JSON de forma bonita e interactiva
                st.json(resultados["resultados_del_analisis"])
            
            else:
                # Si la API da un error
                st.error(f"Error desde la API: {response.text}")
                
    except requests.exceptions.ConnectionError:
        # Si el error es que no podemos conectar (ej: se nos olvidó encender la "cocina")
        st.error("¡Error de Conexión! No se pudo conectar con el Backend (FastAPI).")
        st.warning("¿Has encendido el servidor de FastAPI con 'uvicorn main:app --reload'?")
        
    except Exception as e:
        # Cualquier otro error
        st.error(f"Ha ocurrido un error inesperado: {e}")