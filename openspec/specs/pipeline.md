# Specification: Data Pipeline

## Overview
Automated ETL pipeline that fetches data from a Master Excel (Google Sheets/OneDrive) and generates structured JSON outputs for multiple projects.

## Components

### 1. Source Discovery
- **Master Excel**: Controlled via `MASTER_EXCEL_URL` environment variable.
- **Local Fallback**: `sources.json` is used if the master URL is unavailable.
- **Normalization**: URLs are automatically converted to direct download links.

### 2. Processing Logic (`main.py`)
- **Change Detection**: Uses MD5 hashes stored in `registry.json`.
- **Header Detection**: Automatically searches for a "CODIGO" column within the first 20 rows if the specified `skiprows` fails.
- **Filtering**: Removes rows where the "CODIGO" column is empty.
- **Dependencies**: Requires `pandas`, `openpyxl`, `python-dotenv`, and `requests`.

### 3. Output Structure
- **Data**: Saved as `outputs/{project_id}/data.json`.
- **Logs**: Appends update history to `changelog.md`.
- **State**: Persists current file hashes in `registry.json`.

## Automation
- **Platform**: GitHub Actions.
- **Frequency**: Every 30 minutes (`*/30 * * * *`).
- **Trigger**: Schedule and Manual (`workflow_dispatch`).
- **Secrets**: Requires `MASTER_EXCEL_URL` configured in GitHub Repository Secrets.

## Consumption
- **Next.js Frontend**: Consumes via local filesystem at `/home/devSvarog/proyectos/lab-data-service/outputs/{id}/data.json`.
- **WordPress/Others**: Consumes via GitHub Raw links.
