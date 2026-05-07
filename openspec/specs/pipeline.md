# Specification: Data Pipeline

## Overview
Automated ETL pipeline that fetches data from a Master Excel (Google Sheets/OneDrive) and generates structured JSON outputs for multiple projects.

## Components

### 1. Source Discovery
- **Master Excel**: Controlled via `MASTER_EXCEL_URL`. Only requires `id` and `url` columns.
- **Local Fallback**: `sources.json` is used if the master URL is unavailable.
- **Normalization**: URLs are automatically converted to direct download links.

### 2. Processing Logic (`main.py`)
- **A1 Convention**: The script assumes headers are in the first row and first column (A1).
- **Generic Processing**: No specific column names (like "CODIGO") are required. All table data is converted to JSON.
- **Change Detection**: Uses MD5 hashes stored in `registry.json`.
- **Dependencies**: Requires `pandas`, `openpyxl`, `python-dotenv`, and `requests`.

### 3. Output Structure
- **Data**: Saved as `outputs/{project_id}/data.json`.
- **Logs**: Appends update history to `changelog.md`.
- **State**: Persists current file hashes in `registry.json`.

## Automation
- **Platform**: GitHub Actions.
- **Frequency**: Every 30 minutes (`*/30 * * * *`).
- **Trigger**: Schedule and Manual (`workflow_dispatch`).

## Consumption
- **Generic**: Any frontend can consume the resulting JSON.
- **Next.js Frontend**: Consumes via GitHub Raw links pointing to `outputs/{id}/data.json`.
