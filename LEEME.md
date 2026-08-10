# Gminayo — sitio corregido

## Qué se corrigió (verificado con evidencia, no solo revisión visual)

1. **Ruta del logo rota** — `src="assets/logo-lockup-notag.png"` (carpeta inexistente) →
   `src="logolockupnotag.png"` (archivo real, en la raíz). 36 apariciones en 17 páginas.
2. **Enlace de inicio roto** — `href="Home.html"` (no existe) → `href="index.html"`.
   34 apariciones en 17 páginas.
3. **`tokens.css` desconectado** — no lo cargaba ninguna página. Ahora se enlaza en las 17.
4. **Dependencia de un CDN externo (`unpkg.com`) para React/ReactDOM/Babel** — el sitio
   entero se queda en blanco si esa carga falla (comprobado leyendo `support.js`: el
   contenido vive oculto en `<x-dc>` hasta que el runtime arranca, y si React no carga,
   nunca se revela). Se resolvió vendorizando React 18.3.1, ReactDOM 18.3.1 y
   Babel Standalone 7.29.0 en `sitio/vendor/` (mismos archivos exactos: verificado por
   hash SHA-384 contra los que `support.js` esperaba) y usando el mecanismo de override
   `window.__resources` que el propio runtime ya soportaba.
5. **Dependencia de `fonts.googleapis.com`** — sustituida por Poppins e Inter
   autohospedadas en `sitio/vendor/fonts/` (subset latino, solo los pesos usados:
   Poppins 600/700/800, Inter 400/500/600/700).

El sitio ya no depende de ningún dominio externo para funcionar.

## Qué NO se tocó

La sintaxis `sc-if`, `sc-for`, `{{ }}` y los atributos `style-hover`/`style-focus` **no
son errores**: son el lenguaje de plantillas propio que `support.js` interpreta en
tiempo real (confirmado leyendo el propio runtime). Tocarlos habría roto el sitio.

## Estructura de la entrega

```
entrega/
├── LEEME.md                 (este archivo)
├── sitio/                   ← esto es lo que se sube al hosting estático
│   ├── index.html, Servicios.html, ... (17 páginas)
│   ├── support.js, image-slot.js
│   ├── tokens.css
│   ├── logolockupfull.png, logolockupnotag.png, logomark.png
│   └── vendor/
│       ├── react.production.min.js
│       ├── react-dom.production.min.js
│       ├── babel.min.js
│       └── fonts/  (fonts.css + 7 archivos .woff2)
└── verificacion/             ← herramientas para volver a comprobar (no se sube al hosting)
    ├── comprobar.sh
    ├── check_site.py
    └── verify_render.py
```

## Cómo volver a comprobarlo tú mismo

Necesitas Python 3 y, para la comprobación con navegador real, Playwright con Chromium:

```bash
pip install playwright --break-system-packages
playwright install chromium
```

Luego, desde la carpeta `verificacion/`:

```bash
bash comprobar.sh
```

Esto levanta un servidor local sobre `sitio/` en el puerto 8765 y ejecuta dos
comprobaciones:

1. `check_site.py` — navega las 17 páginas con Chromium real y reporta errores de
   consola, peticiones de red fallidas (404/403) y errores de JavaScript.
2. `verify_render.py` — confirma que React/ReactDOM cargaron, que el contenido es
   visible (no se queda oculto), que el logo se muestra y cuenta los enlaces internos.

El único "problema" que debería seguir apareciendo es un 404 de
`.image-slots.state.json` — es esperado y documentado en el propio `image-slot.js`
(un archivo complementario opcional que solo se usa fuera de este contexto de
despliegue estático); no afecta al funcionamiento del sitio.

Si prefieres comprobarlo sin Playwright, basta con:

```bash
cd sitio
python3 -m http.server 8765
```

y abrir `http://localhost:8765/index.html` en tu propio navegador con la consola de
DevTools abierta.
