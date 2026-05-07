# Estándar de Excel para lab-data-service

Para que el script procese correctamente tus archivos, asegúrate de seguir estas reglas:

1. **Ubicación**: Los encabezados deben comenzar en la celda **A1** (primera fila, primera columna).
2. **Estructura**: No debe haber filas en blanco antes de los encabezados.
3. **Contenido**: El script leerá todas las columnas presentes y las convertirá a JSON automáticamente.
4. **Hojas**: El script procesará siempre la **primera hoja** del libro de Excel.

## Ejemplo de Estructura:

| A | B | C |
|---|---|---|
| **codigo** | **nombre** | **stock** |
| 001 | Item 1 | 10 |
| 002 | Item 2 | 5 |
