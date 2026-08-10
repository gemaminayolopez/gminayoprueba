#!/usr/bin/env bash
# Uso: bash comprobar.sh
# Levanta un servidor local sobre la carpeta ../sitio y ejecuta las dos
# comprobaciones (errores de consola/red + renderizado real) en un solo paso.
# Requiere: python3, y el paquete "playwright" con Chromium instalado
#   (pip install playwright --break-system-packages && playwright install chromium)

set -e
cd "$(dirname "$0")/../sitio"
PORT=8765

(python3 -m http.server "$PORT" > /tmp/gminayo-server.log 2>&1 &)
sleep 1.5

cd "$(dirname "$0")"
echo "=== 1) Errores de consola / recursos rotos ==="
python3 check_site.py

echo ""
echo "=== 2) Renderizado real (React cargado, contenido visible, logo, enlaces) ==="
python3 verify_render.py
