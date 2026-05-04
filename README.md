# 📦 Lab Data Service: Multi-Source Pipeline

Este proyecto automatiza la extracción de datos de múltiples archivos Excel (Google Sheets/OneDrive) definidos en un **Archivo Maestro** y los expone como archivos JSON estructurados.

## 🚀 Cómo funciona

1.  **Detección**: El script descarga el **Archivo Maestro** y recorre cada fuente definida.
2.  **Detección de Cambios**: Compara el hash del contenido actual contra el registrado en `registry.json`.
3.  **Procesamiento**: Si hay cambios, descarga el Excel, detecta automáticamente la cabecera (buscando la columna "CODIGO") y genera un JSON en `outputs/{id-del-proyecto}/data.json`.
4.  **Automatización**: Se ejecuta automáticamente en GitHub cada **30 minutos**.

## ⚙️ Configuración

### Local
1. Crea un archivo `.env` basado en el siguiente ejemplo:
   ```env
   MASTER_EXCEL_URL=tu_url_de_google_sheets_o_onedrive
   ```
2. Instala dependencias: `pip install -r requirements.txt`
3. Ejecuta: `python3 main.py`

### GitHub (Producción)
Para que la automatización funcione, debes configurar el siguiente **Secret** en el repositorio (`Settings > Secrets and variables > Actions`):
- `MASTER_EXCEL_URL`: La URL del Excel Maestro que contiene la lista de todos los proyectos.

## 📂 Estructura de Archivos
- `main.py`: Lógica principal del ETL.
- `outputs/`: Carpeta con los JSON resultantes (un subdirectorio por proyecto).
- `registry.json`: Registro de versiones/hashes para evitar descargas innecesarias.
- `changelog.md`: Historial de actualizaciones automáticas.
- `openspec/`: Documentación técnica avanzada y especificaciones de diseño.

## 🔄 Frecuencia de Sincronización
El proceso de GitHub está configurado para correr cada **30 minutos** (`*/30 * * * *`). También se puede disparar manualmente desde la pestaña **Actions** de GitHub usando el botón "Run workflow".

## 💻 Consumo de Datos
Los datos pueden consumirse directamente desde el sistema de archivos (si el proyecto está en la misma máquina) o vía GitHub Raw:
`https://raw.githubusercontent.com/SvarogMyl/lab-data-service/main/outputs/{id-proyecto}/data.json`

---
*Mantenido con ❤️ usando la metodología OpenSpec.*
