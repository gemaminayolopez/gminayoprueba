import sys
from playwright.sync_api import sync_playwright

BASE = "http://localhost:8765"
PAGES = [
    "index.html", "Servicios.html", "Paquetes.html", "Casos-de-Exito.html",
    "Sobre-Nosotros.html", "Blog.html", "Contacto.html", "Landing-Diagnostico.html",
    "Aviso-Legal.html", "Politica-Privacidad.html", "Politica-Cookies.html",
    "Articulo.html", "Articulo-Calendario-Contenido.html", "Articulo-Lead-MQL-SQL.html",
    "Articulo-Refresco-Marca.html", "Articulo-Video-IA.html", "Articulo-Automatizar-Primero.html",
    "Articulo-Marca-Personal.html",
]

results = {}

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 1280, "height": 900})

    for name in PAGES:
        console_errors = []
        failed_requests = []
        page_errors = []

        def on_console(msg):
            if msg.type == "error":
                console_errors.append(msg.text)

        def on_requestfailed(req):
            failed_requests.append(f"{req.method} {req.url} -> {req.failure}")

        def on_response(resp):
            if resp.status >= 400:
                failed_requests.append(f"{resp.status} {resp.url}")

        def on_pageerror(exc):
            page_errors.append(str(exc))

        page.on("console", on_console)
        page.on("requestfailed", on_requestfailed)
        page.on("response", on_response)
        page.on("pageerror", on_pageerror)

        try:
            page.goto(f"{BASE}/{name}", wait_until="networkidle", timeout=15000)
            page.wait_for_timeout(500)
        except Exception as e:
            page_errors.append(f"NAVIGATION ERROR: {e}")

        # Comprobar que el logo cargó realmente (naturalWidth > 0)
        logo_ok = None
        try:
            logo_ok = page.eval_on_selector("img[src*='logolockup']", "img => img.naturalWidth > 0")
        except Exception:
            logo_ok = "no-logo-element-found"

        results[name] = {
            "console_errors": console_errors,
            "failed_requests": failed_requests,
            "page_errors": page_errors,
            "logo_loaded": logo_ok,
        }

        page.remove_listener("console", on_console)
        page.remove_listener("requestfailed", on_requestfailed)
        page.remove_listener("response", on_response)
        page.remove_listener("pageerror", on_pageerror)

    browser.close()

# Reporte
total_issues = 0
for name, r in results.items():
    issues = r["console_errors"] + r["failed_requests"] + r["page_errors"]
    if r["logo_loaded"] is False:
        issues.append("LOGO NO CARGÓ (naturalWidth=0)")
    status = "OK" if not issues else f"{len(issues)} problema(s)"
    print(f"[{status}] {name}")
    for i in issues:
        print(f"    - {i}")
    total_issues += len(issues)

print(f"\nTOTAL incidencias en las {len(PAGES)} páginas: {total_issues}")
