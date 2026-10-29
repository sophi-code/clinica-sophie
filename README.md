# Clínica Citas API 🏥

**Sistema de gestión de citas médicas**  
Proyecto de Desarrollo de Software  
FastAPI · Pydantic · Persistencia en CSV · pytest · Git/GitHub

---

## 📋 Descripción

API REST desarrollada en **FastAPI** para la gestión de pacientes, médicos y citas médicas. Evita que un mismo médico tenga dos citas agendadas a la misma hora y almacena los datos de forma persistente en archivos CSV.

---

## 🚀 Pasos para ejecutar en Visual Studio Code

1. Extrae el archivo comprimido.
2. Abre la carpeta `clinica_citas` en **Visual Studio Code**.
3. Abre la terminal (`Ctrl + ~` o `Cmd + ~`) y ejecuta:

```bash
# 1. Crear el entorno virtual
python -m venv .venv

# 2. Activar el entorno virtual
# En Windows (PowerShell):
.venv\Scripts\activate
# En macOS / Linux:
source .venv/bin/activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Iniciar el servidor
uvicorn main:app --reload
```

4. **Probar la API:**  
   Accede en tu navegador a [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) para interactuar con Swagger UI.

---

## 🧪 Ejecutar pruebas unitarias

En la terminal con el entorno virtual activado:

```bash
pytest
```
