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

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 1280, "height": 900})

    for name in PAGES:
        page.goto(f"{BASE}/{name}", wait_until="networkidle", timeout=15000)
        page.wait_for_timeout(400)

        react_loaded = page.evaluate("() => typeof window.React !== 'undefined' && typeof window.ReactDOM !== 'undefined'")
        xdc_hidden = page.evaluate("""() => {
            const el = document.querySelector('x-dc');
            if (!el) return 'no-x-dc-element';
            return getComputedStyle(el).display === 'none';
        }""")
        body_text_len = page.evaluate("() => document.body.innerText.trim().length")
        logo_visible = page.evaluate("""() => {
            const img = document.querySelector("img[src*='logolockup']");
            if (!img) return 'sin-logo';
            return img.naturalWidth > 0 && img.getBoundingClientRect().width > 0;
        }""")
        nav_links = page.evaluate("() => document.querySelectorAll('a[href$=\".html\"]').length")

        print(f"{name}: React/ReactDOM cargados={react_loaded} | x-dc oculto={xdc_hidden} | texto visible={body_text_len} chars | logo visible={logo_visible} | enlaces .html en página={nav_links}")

    browser.close()
