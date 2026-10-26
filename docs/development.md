# Desarrollo y reproducción

[Inicio](../README.md)

## Herramientas

- OpenSCAD 2021.01 fue la versión utilizada para la comprobación inicial; CLI `-D` y exportación binaria STL.
- Python 3.10+; exportación, auditoría, cálculos y pruebas usan solo su biblioteca estándar.
- Para imágenes y PDFs: dependencias de [requirements-docs.txt](../requirements-docs.txt), fuentes DejaVu Sans y Poppler para revisar páginas.

```bash
python scripts/export.py
python -m unittest discover -s tests -v
python scripts/validate.py
python scripts/check_motion.py

# Opcional, redibujar documentación después de exportar:
pip install -r requirements-docs.txt
python scripts/illustrate_v3.py
python scripts/manual_v3.py
python scripts/manual.py
python scripts/build_site.py
```

En macOS se puede indicar el ejecutable sin agregarlo al PATH:

```bash
OPENSCAD=/Applications/OpenSCAD.app/Contents/MacOS/OpenSCAD python scripts/export.py
```

En Windows usar `openscad.com` si el instalador lo proporciona y configurar `OPENSCAD` antes de ejecutar Python. El exportador pasa argumentos como lista, sin shell intermedio.

Para generar gráficos/PDF fuera de Linux, instalar DejaVu Sans y definir `HALLACAITOR_FONT_DIR` con la carpeta que contiene `DejaVuSans.ttf` y `DejaVuSans-Bold.ttf`. Esto no afecta la exportación de STL ni los controles de geometría.

## Cambiar geometría

`config/parts.json` declara las piezas, sus kits y orientación. `cad/hallacaitor.scad` y `cad/modular.scad` definen el sólido y las vistas de conjunto. Los scripts de imagen transforman las mallas exportadas para representar esos conjuntos: si cambian los ejes o transformaciones de montaje, actualizar también los dibujos y comprobaciones que los describen.

La prueba de movimiento muestrea ángulos, no calcula toda trayectoria continua. Los informes llevan hashes para identificar los archivos exactos auditados. Los STL no incluyen unidades; el manifiesto y todas las cotas usan mm.

## CI

El flujo de GitHub Actions instala OpenSCAD, ejecuta pruebas de restricciones, reexporta todos los modelos a una carpeta temporal, compara envolventes/volúmenes con el informe y comprueba las intersecciones de movimiento y aguja. No publica ni cambia automáticamente archivos del repositorio. Los informes del trabajo se adjuntan como artefactos de CI.

No se exige igualdad binaria de STL entre versiones de CGAL: puede cambiar la triangulación sin cambiar el sólido. Se comparan topología, volúmenes y cotas. Regenerar `docs/validation/geometry.json` después de un cambio intencional y explicar la diferencia en el PR.
