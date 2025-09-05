# 📚 Asistente Inteligente de Consulta Jurídica

## 📌 Descripción General
Este proyecto es un **asistente de consultas jurídicas** que combina:
1. **Un motor semántico** que busca información relevante en manuales oficiales del tribunal.
2. **Un modelo de IA** que genera respuestas completas y coherentes basadas en la información encontrada y en la pregunta del usuario.

El objetivo es proporcionar respuestas precisas y fundamentadas, integrando **conocimiento humano (manuales)** con **capacidad generativa de IA**.

---

## ⚙️ Funcionamiento General

1. **Recepción de la pregunta**
   - Un usuario envía su consulta a la API del proyecto.

2. **Búsqueda semántica**
   - El motor semántico analiza la pregunta y encuentra fragmentos relevantes en los manuales del tribunal.
    - Los fragmentos e los manuales ya se encunetran disponibles en el GitHub, fuern creados a parir del uso de FAISS junto con SentenceTransformer
   - Además se utiliza **FAISS** como índice vectorial para buscar por similitud de significado.

3. **Generación de respuesta**
   - El contexto relevante (texto de manuales) y la pregunta se envían al **modelo de IA local**.
   - La IA combina la información encontrada con su propio conocimiento para generar una respuesta clara.

4. **Devolución al usuario**
   - La respuesta final se envía en formato JSON.

---

## 🧩 Componentes del Proyecto

- **`main.py`**  
  Contiene la API desarrollada en **FastAPI**.  
  Expone los endpoints para recibir consultas y devolver respuestas.

- **`semantic_engine.py`**  
  Módulo que maneja la búsqueda semántica usando FAISS y embeddings.

- **`ia_connector.py`**  
  Módulo que gestiona la conexión con el modelo de IA local.

- **`procesamiento_manual.py`**  
  Módulo que procesa nuevos manuales que quieran ser integrados o utilizados una única vez.
  *Se debe ejcutar el siguiente comando antes de utilizar el módulo y el nuevo o los nuevos manuales ya deben existir en la carpeta personalized_manuals*
      **pip install sentence-transformers faiss-cpu**


- **`requirements.txt`**  
  Lista de dependencias necesarias para instalar el entorno.

- **`data/`**
  Carpeta donde se almacenan los manuales del tribunal en **texto plano** para ser indexados.

- **`personalized_manuals/`** *(Solo si se usará el módulo proesamiento_manual)*
  Carpeta donde se almacenan nuevos manuales del tribunal en **texto plano** para ser indexados que no existen en la carpeta data.
---
## 🖥️ Requerimientos del Sistema

- **Python** 3.9 o superior  
- **FastAPI** y **Uvicorn** para la API  
- **FAISS** para búsqueda semántica  
- **SentenceTransformers** para embeddings  
- **Transformers** y modelo local compatible  
- Sistema operativo: Windows  
- Al menos **8 GB de RAM** (recomendado 16 GB si se utiliza un modelo superior o más potente)  
- GPU con soporte CUDA *(opcional pero recomendado)*

---
## Estructura de proyecto
Backend
├── main.py                   # API FastAPI
├── procesamiento_manual.py   # Documento que prepara la información que el asistente luego usa para responder.
├── semantic_engine.py        # Motor semántico (FAISS + embeddings)
├── ia_connector.py           # Conector a Ollama (IA local)
├── requirements.txt          # Dependencias del proyecto
├── data/                     # Carpeta con manuales o documentos
├── requirements.txt          # Dependencias del proyecto
├── embeddings/               # Transformación de los manuales data en archivos de texto plano, procesados por FAISS
├── img/                      # Imagen que representa el flujo de trabajo de la API main   
└── __pycache__/              # Carpeta generada por Python que contiene el código compilado en bytecode
Frontend            
└── index.html                #Página web de prueba local, puede ejecutarse con la extención VS code 'Live Preview'
README.md                     # Documentación general


---
## 📦 Instalación

1. **Clonar el repositorio**
   Desde gitbash

   git clone https://github.com/MoulinieLuis/Asistente_IA_Tribunal.git
   cd asistente-juridico

2. **Crear entorno virtual**
  python -m venv venv
  source venv/bin/activate   # En Windows: venv\Scripts\activate

3. **Instalar dependencias**
  pip install -r requirements.txt


4. **Indexar manuales (opcional si ya existe el índice)**
  python semantic_engine.py --index


---
## 🚀 Ejecución principal

1. **Iniciar la API con recarga automática:**
  uvicorn main:app --reload


**La API de IA existe cuando se descaga la aplicación Ollama y se instala la IA "Mistral"**
  Puerto (localhost): http://127.0.0.1:8000


---
## 🚀 Ejecución para procesamiento manual

1. **Ejeuta el script:**
  python manual_processor.py

  *Los nuevos manuales ya deben existir en la carpeta personalized_manuals*


**La API de IA existe cuando se descaga la aplicación Ollama y se instala la IA "Mistral"**
  Puerto (localhost): http://127.0.0.1:8000



---
**Respuesta en formato JSON:**

{
  "answer": "Según el manual del tribunal, el procedimiento para apelar...",
  "source": "Manual de Procedimientos, Capítulo 4"
}

---
## 👥 Colaboración

**Para contribuir:**

Crear una nueva rama.

Realizar cambios y pruebas.

Hacer un Pull Request con una descripción clara de las modificaciones.

---
## 🔀 Flujo general del proyecto

![Arquitectura del Proyecto](/Backend/img/arquitectura_proyecto_asistente.png)