# 📦 Lab Data Service: Multi-Source Pipeline

Este proyecto automatiza la extracción de datos de múltiples archivos Excel compartidos y los expone como archivos JSON estructurados. Optimizado para minimizar ejecuciones innecesarias mediante detección de cambios.

## 🚀 Cómo funciona
1.  **Detección**: El script verifica si el archivo en la nube ha cambiado comparando su "hash" (huella digital) contra el registro local (`registry.json`).
2.  **Extracción**: Si hay cambios, descarga el Excel y genera un JSON en una subcarpeta dedicada en `outputs/`.
3.  **Registro**: Cada actualización se anota en el [**`changelog.md`**](changelog.md).

## 📂 Estructura de Salida
- `outputs/`
  - `id-del-proyecto/`
    - `data.json`

## ➕ Cómo agregar un nuevo Excel
Para agregar una nueva fuente de datos, simplemente edita el archivo [**`sources.json`**](sources.json) agregando un nuevo objeto:

```json
{
    "id": "nombre-carpeta",
    "name": "Nombre Visual",
    "url": "LINK_DESCARGA_DIRECTA",
    "sheet": "NombreHoja",
    "skiprows": 3
}
```

## 🛠️ Configuración en GitHub
1. Sube este repositorio a GitHub.
2. Asegúrate de que el `GITHUB_TOKEN` tenga permisos de **Lectura y Escritura** (`Settings > Actions > General > Workflow permissions`).
3. El script se encargará de crear las carpetas y el changelog automáticamente.

## 💻 Consumo desde WordPress
Usa el link de GitHub Raw:
`https://raw.githubusercontent.com/USUARIO/REPO/main/outputs/id-del-proyecto/data.json`
