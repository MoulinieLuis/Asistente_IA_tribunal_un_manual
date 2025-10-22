# 🧠 Guía para Cambiar el Manual PDF – Asistente IA con NLTK

Esta guía explica los pasos que debes seguir cada vez que quieras reemplazar el PDF por un nuevo manual en tu proyecto. Sigue esta checklist para evitar errores en el procesamiento y mantener el sistema sincronizado correctamente.

---

## 📌 1. Sustituir el PDF

- Coloca el nuevo PDF en la carpeta correspondiente (por ejemplo, `Backend/pdf` o donde guardes tus manuales originales).
- Usa un nombre claro y sin espacios, por ejemplo:  
  `manual_nuevo.pdf`

---

## 📝 2. Convertir PDF a TXT

- Utiliza tu script de conversión (o el paso que ya tengas integrado) para generar el archivo `.txt`.
- Verifica que el archivo `.txt` se haya creado correctamente y tenga contenido legible.  
  Ejemplo:  
  `manual_nuevo.txt`

---

## 📁 3. Mover el archivo TXT

- Mueve el archivo `.txt` generado a la carpeta:  
  `Backend/embeddings/`
- Asegúrate de no sobrescribir accidentalmente los archivos de índices existentes (`.faiss` y `.pkl`) si quieres conservarlos.

---

## ⚙️ 4. Actualizar la Ruta en el Script

- Abre `procesamiento_manual.py`.
- Busca la línea donde defines `manual_path`.
- Cambia la ruta para que apunte al nuevo `.txt`, por ejemplo:

import os

embeddings_folder = "Backend/embeddings"
manual_path = os.path.join(embeddings_folder, "manual_nuevo.txt")

text

---

## 🧠 5. Procesar el Nuevo Manual

- Ejecuta el script para generar los nuevos embeddings e índices FAISS:

python procesamiento_manual.py

text

- Verifica en la consola que aparezcan mensajes como:  
  - Embeddings generados correctamente  
  - Índices FAISS creados y guardados

---

## 🚀 6. Levantar la API / Servidor

- Ejecuta tu backend normalmente, por ejemplo:

python main.py

text

- A partir de este momento, el asistente utilizará la información del nuevo manual.

---

## 🧪 7. Probar

- Abre el frontend.
- Realiza preguntas de prueba para confirmar que el asistente responde en función del nuevo contenido.

---