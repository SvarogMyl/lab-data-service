import os
import pandas as pd
import json
import requests
import hashlib
import re
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

def normalize_url(url):
    """Convierte links de compartir en links de descarga directa."""
    if not isinstance(url, str):
        return url
    url = url.strip()
    # Google Drive
    gd_match = re.search(r'https://docs\.google\.com/spreadsheets/d/([a-zA-Z0-9-_]+)', url)
    if gd_match:
        return f"https://docs.google.com/spreadsheets/d/{gd_match.group(1)}/export?format=xlsx"
    # OneDrive / SharePoint
    if any(domain in url for domain in ["onedrive.live.com", "1drv.ms", "sharepoint.com"]):
        if "download=1" not in url:
            return f"{url}{'&' if '?' in url else '?'}download=1"
    return url

# Configuración
MASTER_EXCEL_URL = normalize_url(os.getenv("MASTER_EXCEL_URL"))
SOURCES_FILE = "sources.json"
REGISTRY_FILE = "registry.json"
CHANGELOG_FILE = "changelog.md"
OUTPUT_DIR = "outputs"

def get_file_hash(content):
    return hashlib.md5(content).hexdigest()

def load_registry():
    if os.path.exists(REGISTRY_FILE):
        with open(REGISTRY_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_registry(registry):
    with open(REGISTRY_FILE, 'w') as f:
        json.dump(registry, f, indent=4)

def update_changelog(source_name, message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"| {timestamp} | {source_name} | {message} |\n"
    if not os.path.exists(CHANGELOG_FILE):
        with open(CHANGELOG_FILE, 'w', encoding='utf-8') as f:
            f.write("# 📜 Historial de Cambios (Changelog)\n\n| Fecha/Hora | Proyecto | Descripción |\n| --- | --- | --- |\n")
    with open(CHANGELOG_FILE, 'a', encoding='utf-8') as f:
        f.write(line)

def get_sources():
    """Obtiene la lista de fuentes (id, url) desde el Excel Maestro o archivo local."""
    sources = []
    if MASTER_EXCEL_URL:
        print(f"📥 Cargando configuración desde el Excel Maestro...")
        try:
            resp = requests.get(MASTER_EXCEL_URL)
            resp.raise_for_status()
            with open("master_config.xlsx", "wb") as f:
                f.write(resp.content)
            df_master = pd.read_excel("master_config.xlsx")
            df_master.columns = [str(c).strip().lower() for c in df_master.columns]
            
            # Solo nos interesan 'id' y 'url'
            if 'id' in df_master.columns and 'url' in df_master.columns:
                sources = df_master[['id', 'url']].dropna().to_dict(orient='records')
            else:
                print("⚠️ El Excel Maestro debe contener las columnas 'id' y 'url'.")
            
            os.remove("master_config.xlsx")
            return sources
        except Exception as e:
            print(f"⚠️ Error cargando Excel Maestro: {e}. Probando backup local...")
    
    if os.path.exists(SOURCES_FILE):
        with open(SOURCES_FILE, 'r') as f:
            return json.load(f)
    return []

def process_source(source, registry):
    source_id = str(source['id']).strip()
    url = normalize_url(source['url'])
    
    print(f"\n🔍 Procesando: {source_id}...")
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        content = response.content
        
        current_hash = get_file_hash(content)
        last_hash = registry.get(source_id, {}).get("hash")
        
        if current_hash == last_hash:
            print(f"⏩ Sin cambios para {source_id}.")
            return False

        temp_file = f"temp_{source_id}.xlsx"
        with open(temp_file, 'wb') as f:
            f.write(content)
            
        # Lectura Estándar (Cabecera en A1)
        df = pd.read_excel(temp_file)
        
        # Limpieza básica: quitar filas y columnas completamente vacías
        df = df.dropna(how='all').dropna(axis=1, how='all')
        
        target_dir = os.path.join(OUTPUT_DIR, source_id)
        os.makedirs(target_dir, exist_ok=True)
        
        output_path = os.path.join(target_dir, "data.json")
        data = df.to_dict(orient='records')
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
            
        registry[source_id] = {
            "hash": current_hash,
            "last_updated": datetime.now().isoformat()
        }
        update_changelog(source_id, f"Actualización genérica ({len(data)} registros)")
        
        print(f"✅ ¡Actualizado! {output_path}")
        
        if os.path.exists(temp_file):
            os.remove(temp_file)
        return True

    except Exception as e:
        print(f"❌ Error en {source_id}: {str(e)}")
        return False

def main():
    sources = get_sources()
    if not sources:
        print("❌ No se encontraron fuentes de datos para procesar.")
        return

    registry = load_registry()
    changes_made = False
    
    for source in sources:
        if process_source(source, registry):
            changes_made = True
            
    if changes_made:
        save_registry(registry)
        print("\n✨ Proceso finalizado con actualizaciones.")
    else:
        print("\n😴 Todo está al día.")

if __name__ == "__main__":
    main()
