# 📦 lab-data-service — Multi-Source Excel → JSON Pipeline

Pipeline ETL automatizado que convierte archivos Excel alojados en Google Drive u OneDrive en archivos JSON estructurados, sincronizando cambios cada 30 minutos vía GitHub Actions.

**Estado**: ✅ Operativo en producción  
**Último run**: automático cada 30 min  
**Proyectos activos**: `botica-municipal`, `animales`, `otros-datos`

---

## 🚀 Cómo funciona

```
Excel Maestro (Google Drive / OneDrive)
        │
        ▼  GitHub Actions (cron cada 30 min)
[main.py]
   ├── Descarga Excel Maestro (lista de proyectos)
   ├── Por cada proyecto:
   │    ├── Descarga el Excel fuente
   │    ├── Compara hash MD5 con registry.json
   │    ├── Si hay cambios → convierte a JSON
   │    └── Guarda en outputs/{id}/data.json
   └── Actualiza registry.json y changelog.md
```

1. **Descubrimiento**: Descarga el Excel Maestro y lee todos los proyectos (`id` + `url`).
2. **Detección de cambios**: Compara el hash MD5 del archivo descargado con el registrado en `registry.json`. Si no hubo cambios, omite el procesamiento.
3. **Conversión**: Lee el Excel genéricamente desde A1 (todas las columnas, sin depender de nombres específicos) y genera `outputs/{id}/data.json`.
4. **Automatización**: Se ejecuta en GitHub Actions cada 30 minutos. También puede dispararse manualmente.

---

## ⚙️ Configuración

### Formato del Excel Maestro

El Excel Maestro es la lista de proyectos/fuentes que el pipeline debe procesar. Solo requiere dos columnas:

| id | url |
|---|---|
| botica-municipal | https://docs.google.com/spreadsheets/d/... |
| animales | https://onedrive.live.com/... |

- `id`: Identificador del proyecto. Define el nombre de la carpeta en `outputs/`.
- `url`: URL del archivo Excel. Puede ser un link de visualización de Google Drive o OneDrive — el script los normaliza automáticamente a links de descarga directa.

### Formato del Excel de datos

Cada Excel fuente debe seguir la convención A1:

- Los encabezados deben estar en la **primera fila**.
- No debe haber filas vacías antes de los encabezados.
- El script procesa siempre la **primera hoja** del libro.
- Todas las columnas son leídas y exportadas — no hay restricción de nombres.

Ver `examples/template.csv` como referencia.

### Ejecución local

1. Crea un archivo `.env`:
   ```env
   MASTER_EXCEL_URL=https://docs.google.com/spreadsheets/d/TU_ID/export?format=xlsx
   ```
2. Instala dependencias:
   ```bash
   pip install -r requirements.txt
   ```
3. Ejecuta:
   ```bash
   python3 main.py
   ```

**Alternativa sin Excel Maestro**: Si no defines `MASTER_EXCEL_URL`, el script usa `sources.json` como fallback local. Útil para pruebas:

```json
[
  { "id": "mi-proyecto", "url": "https://..." }
]
```

### GitHub Actions (Producción)

El workflow `update_data.yml` necesita un único secret configurado en `Settings > Secrets and variables > Actions` del repositorio:

| Secret | Descripción |
|---|---|
| `MASTER_EXCEL_URL` | URL de descarga directa del Excel Maestro ✅ Configurado |

---

## ➕ Cómo agregar un nuevo proyecto

1. Abre el Excel Maestro en Google Drive.
2. Añade una nueva fila con un `id` único y la URL del Excel fuente.
3. En el siguiente run (máximo 30 min), el pipeline detectará el nuevo proyecto y generará `outputs/{id}/data.json` automáticamente.

No se requiere ningún cambio en el código.

---

## 💻 Consumo de datos

### Vía GitHub Raw (desde cualquier frontend)

```
https://raw.githubusercontent.com/SvarogMyl/lab-data-service/main/outputs/{id}/data.json
```

Ejemplo real:
```
https://raw.githubusercontent.com/SvarogMyl/lab-data-service/main/outputs/botica-municipal/data.json
```

### Ejemplo de registro en el JSON resultante

```json
{
  "CODIGO": "BM 0001",
  "MEDICAMENTO": "AC ALENDRONICO 70 MG",
  "PRESENTACIÓN": "ALDROX 70 MG x 10 COMPRIMIDOS",
  "ESTADO": "Con stock",
  "ÚLTIMA ACTUALIZACIÓN": "01/05/2026"
}
```

Los nombres de campo en el JSON reflejan exactamente los encabezados del Excel original.

---

## 🔄 Auto-normalización de URLs

El script convierte automáticamente links de compartir en links de descarga directa. No es necesario buscar la URL "correcta" manualmente.

| Origen | Input del usuario | Resultado |
|---|---|---|
| Google Drive | `https://docs.google.com/spreadsheets/d/ID/edit` | `https://docs.google.com/spreadsheets/d/ID/export?format=xlsx` |
| OneDrive | `https://1drv.ms/x/...` | Añade `?download=1` automáticamente |

---

## 📂 Estructura del proyecto

```
lab-data-service/
├── main.py                  # Lógica principal del ETL
├── registry.json            # Hashes MD5 por proyecto (evita descargas redundantes)
├── changelog.md             # Historial de actualizaciones automáticas
├── requirements.txt         # Dependencias Python
├── outputs/
│   ├── botica-municipal/
│   │   └── data.json        # JSON generado del catálogo de medicamentos
│   ├── animales/
│   │   └── data.json
│   └── {id}/
│       └── data.json
├── examples/
│   ├── README.md            # Estándar de formato para los Excel fuente
│   └── template.csv         # Plantilla de ejemplo
└── openspec/
    └── specs/pipeline.md    # Especificación técnica del pipeline
```

---

## 🛠️ Dependencias

| Librería | Uso |
|---|---|
| `pandas` | Lectura y conversión de Excel a estructuras de datos |
| `openpyxl` | Engine de lectura de archivos `.xlsx` |
| `requests` | Descarga de archivos desde URLs remotas |
| `python-dotenv` | Carga de variables de entorno desde `.env` local |

---

## 🔗 Integración con el ecosistema

- **`lab-frontend-nextjs`**: Consume `outputs/botica-municipal/data.json` vía API Route interno para el catálogo de medicamentos.
- **`lab-core-node`** *(pendiente)*: Endpoint `/api/sync` para disparar el pipeline manualmente desde el backend central.

---

*Mantenido bajo la metodología OpenSpec — ver `openspec/` para especificaciones técnicas detalladas.*
