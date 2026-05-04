# Proposal: Sync System and Fix Workflow

## Problem
1. **Frontend Desync**: The Next.js frontend reads from a legacy `data.json` in the root, while the pipeline generates fresh data in `outputs/`.
2. **Workflow Desync**: GitHub Actions uses an old environment variable (`EXCEL_SOURCE`) and doesn't push the new output files.
3. **Implicit Dependencies**: The system relies on a manual `data.json` file that is no longer the primary output.

## Goals
- Align frontend to consume from `outputs/botica-municipal/data.json`.
- Synchronize GitHub Actions with `main.py` environment variables and output paths.
- Ensure all artifacts (`registry.json`, `changelog.md`, `outputs/`) are version-controlled automatically.
