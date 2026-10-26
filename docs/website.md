# Manual web abierto

[Sitio público](https://hallacaitor-manual.rajmaliuk.chatgpt.site) · [Fuente](../web) · [Constructor](../scripts/build_site.py)

## Construir y consultar localmente

```bash
python scripts/build_site.py
python -m http.server 8000 --directory build/site
```

Abrir `http://localhost:8000`. No requiere Node, CDN, fuentes externas, cuenta ni base de datos. Las listas de lectura se guardan solo en el navegador. Sin JavaScript siguen disponibles los textos, catálogo completo, imágenes y descargas; búsqueda, filtros y calculadora necesitan JavaScript.

El constructor lee `web/content.json`, `config/parts.json`, `config/stations.json`, `config/references.json` e informes de geometría. Copia gráficos, STL y PDF y verifica cada destino local `href`/`src`. Las imágenes se generan con `scripts/illustrate_v3.py` a partir de los STL reales. No son fotos de pruebas.

## GitHub Pages

1. El propietario activa **Settings → Pages → Build and deployment → Source → GitHub Actions**.
2. Ejecutar **Actions → Build and publish manual → Run workflow**.
3. El flujo construye el sitio, conserva un artefacto y publica si Pages está habilitado. Futuros pushes a `main` lo actualizan.
4. Usar la URL que devuelve el paso Deploy, sin asumir que una dirección aún no activada ya funciona.

El conector de GitHub permite objetos Git y referencias, pero no administrar Pages. El token habitual de Actions no se usa para intentar crear esa configuración de administración. La web pública en Sites permite consultar el manual mientras se activa Pages.

## Otros alojamientos

Subir íntegro `build/site` a cualquier alojamiento estático. Enlaces relativos permiten alojarlo en una subcarpeta. Mantener `LICENSE.txt`, créditos y fuentes. Para una réplica, cambiar enlaces al repositorio y dirección pública en el constructor y documentos.
