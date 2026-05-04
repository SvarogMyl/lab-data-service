# Design: Sync System and Fix Workflow

## 1. Frontend Update
- **File**: `lab-frontend-nextjs/src/app/api/catalogo/route.ts`
- **Change**: Update `filePath` from `.../data.json` to `.../outputs/botica-municipal/data.json`.
- **Reason**: `outputs/` is the authoritative location for project-specific data.

## 2. GitHub Workflow Update
- **File**: `lab-data-service/.github/workflows/update_data.yml`
- **Environment**: Update `EXCEL_SOURCE` to `MASTER_EXCEL_URL`.
- **Git Actions**: Change `git add data.json` to `git add outputs/ registry.json changelog.md`.
- **Cron**: Keep `*/30 * * * *` for now.

## 3. Data Integrity
- **Registry**: Ensure `registry.json` is always updated to prevent redundant downloads in CI/CD.
- **Legacy Cleanup**: Keep root `data.json` for one cycle then remove once verified.
