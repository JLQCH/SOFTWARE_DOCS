#!/usr/bin/env python3
"""Genera las paginas HTML del sitio a partir de los Markdown.

Sin dependencias: un conversor Markdown minimo, suficiente para documentos
legales (encabezados, parrafos, listas, negrita, enlaces y tablas).

Uso:  python3 build.py
"""
import html
import re
from pathlib import Path

RAIZ = Path(__file__).parent

PLANTILLA = """<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{titulo}</title>
<meta name="description" content="{desc}">
<style>
  :root {{
    --tinta: #1b1830; --suave: #5c5870; --fondo: #ffffff; --panel: #f6f5fa;
    --acento: #4a3fd4; --borde: #e3e1ee;
  }}
  @media (prefers-color-scheme: dark) {{
    :root {{
      --tinta: #eceaf6; --suave: #a8a4bd; --fondo: #14121f; --panel: #1e1b2e;
      --acento: #9c93ff; --borde: #2c2842;
    }}
  }}
  * {{ box-sizing: border-box; }}
  body {{
    margin: 0; background: var(--fondo); color: var(--tinta);
    font: 17px/1.65 -apple-system, BlinkMacSystemFont, "Segoe UI", system-ui, sans-serif;
    -webkit-text-size-adjust: 100%;
  }}
  .envoltura {{ max-width: 720px; margin: 0 auto; padding: 32px 20px 80px; }}
  header.marca {{
    display: flex; align-items: center; gap: 12px;
    padding-bottom: 20px; margin-bottom: 28px; border-bottom: 1px solid var(--borde);
  }}
  .logo {{
    width: 42px; height: 42px; border-radius: 11px; flex: none;
    background: linear-gradient(135deg, #6C5CE7, #A29BFE);
    color: #fff; font-weight: 800; font-size: 21px;
    display: grid; place-items: center;
  }}
  .marca b {{ font-size: 17px; }}
  .marca span {{ display: block; color: var(--suave); font-size: 13px; }}
  h1 {{ font-size: 30px; line-height: 1.25; margin: 0 0 6px; letter-spacing: -0.02em; }}
  h2 {{
    font-size: 21px; margin: 38px 0 10px; letter-spacing: -0.01em;
    padding-top: 18px; border-top: 1px solid var(--borde);
  }}
  h2:first-of-type {{ border-top: 0; padding-top: 0; }}
  h3 {{ font-size: 17px; margin: 26px 0 8px; }}
  p, li {{ color: var(--tinta); }}
  a {{ color: var(--acento); }}
  .fecha {{ color: var(--suave); font-size: 14px; margin: 0 0 26px; }}
  .resumen {{
    background: var(--panel); border: 1px solid var(--borde);
    border-radius: 14px; padding: 16px 18px; margin: 0 0 30px;
  }}
  .resumen p {{ margin: 0; }}
  table {{ border-collapse: collapse; width: 100%; margin: 14px 0; font-size: 15px; }}
  th, td {{ border: 1px solid var(--borde); padding: 8px 10px; text-align: left; }}
  th {{ background: var(--panel); }}
  code {{
    background: var(--panel); padding: 2px 6px; border-radius: 5px;
    font-size: 0.9em; font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
  }}
  footer {{
    margin-top: 56px; padding-top: 20px; border-top: 1px solid var(--borde);
    color: var(--suave); font-size: 14px;
  }}
  .idiomas {{ margin-bottom: 24px; font-size: 14px; }}
  .idiomas a {{ margin-right: 14px; }}
</style>
</head>
<body>
<div class="envoltura">
<header class="marca">
  <div class="logo">M</div>
  <div><b>Múltiplo</b><span>{sub}</span></div>
</header>
{idiomas}
{cuerpo}
<footer>{pie}</footer>
</div>
</body>
</html>
"""


def en_linea(t):
    """Negrita, codigo y enlaces dentro de un parrafo."""
    t = html.escape(t)
    t = re.sub(r"`([^`]+)`", r"<code>\1</code>", t)
    t = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", t)
    t = re.sub(r"\[([^\]]+)\]\((https?://[^)]+)\)", r'<a href="\2">\1</a>', t)
    # URLs sueltas
    t = re.sub(r"(?<!\")(?<!=)(https?://[^\s<]+)(?![^<]*</a>)", r'<a href="\1">\1</a>', t)
    return t


def a_html(md):
    salida, i = [], 0
    lineas = md.split("\n")
    while i < len(lineas):
        ln = lineas[i]
        if ln.startswith("### "):
            salida.append(f"<h3>{en_linea(ln[4:])}</h3>")
        elif ln.startswith("## "):
            salida.append(f"<h2>{en_linea(ln[3:])}</h2>")
        elif ln.startswith("# "):
            salida.append(f"<h1>{en_linea(ln[2:])}</h1>")
        elif ln.startswith("|"):
            filas = []
            while i < len(lineas) and lineas[i].startswith("|"):
                filas.append(lineas[i]); i += 1
            i -= 1
            celdas = [[c.strip() for c in f.strip("|").split("|")] for f in filas]
            cuerpo = [c for c in celdas if not set("".join(c).replace(" ", "")) <= set("-:")]
            if cuerpo:
                th = "".join(f"<th>{en_linea(c)}</th>" for c in cuerpo[0])
                trs = "".join(
                    "<tr>" + "".join(f"<td>{en_linea(c)}</td>" for c in fila) + "</tr>"
                    for fila in cuerpo[1:]
                )
                salida.append(f"<table><tr>{th}</tr>{trs}</table>")
        elif ln.startswith("- "):
            items = []
            while i < len(lineas) and (lineas[i].startswith("- ") or
                                       (lineas[i].startswith("  ") and items)):
                if lineas[i].startswith("- "):
                    items.append(lineas[i][2:])
                else:
                    items[-1] += " " + lineas[i].strip()
                i += 1
            i -= 1
            salida.append("<ul>" + "".join(f"<li>{en_linea(x)}</li>" for x in items) + "</ul>")
        elif ln.strip() == "---":
            pass
        elif ln.strip():
            parr = [ln]
            while i + 1 < len(lineas) and lineas[i + 1].strip() and \
                    not lineas[i + 1][0] in "#|-":
                i += 1; parr.append(lineas[i])
            texto = " ".join(parr).strip()
            if texto.startswith("**Última actualización") or texto.startswith("**Last updated"):
                salida.append(f'<p class="fecha">{en_linea(texto)}</p>')
            else:
                salida.append(f"<p>{en_linea(texto)}</p>")
        i += 1
    return "\n".join(salida)


def partir_idiomas(md):
    """El MD trae las dos versiones; se separan por sus encabezados.

    Al quitar el "## Version en espanol" que las envolvia, sus secciones (que
    en el documento son `###`) pasan a ser el nivel principal de la pagina, asi
    que se promocionan a `##`. Si no, el esquema del documento queda con un
    salto de h1 a h3 y los lectores de pantalla lo leen mal.
    """
    marca_es = "## Versión en español"
    marca_en = "## English version"
    es = md[md.index(marca_es) + len(marca_es):md.index(marca_en)].strip()
    en = md[md.index(marca_en) + len(marca_en):].strip()
    subir = lambda t: re.sub(r"^### ", "## ", t, flags=re.M)
    return subir(es), subir(en)


def main():
    md = (RAIZ / "multiplo" / "privacidad.md").read_text(encoding="utf-8")
    es, en = partir_idiomas(md)

    nav_es = ('<p class="idiomas"><strong>Español</strong> · '
              '<a href="privacy.html">English</a></p>')
    nav_en = ('<p class="idiomas"><a href="privacidad.html">Español</a> · '
              '<strong>English</strong></p>')
    pie_es = ("Múltiplo · Jose Luis Querido Chica · "
              '<a href="mailto:jlq.software@gmail.com">jlq.software@gmail.com</a>')
    pie_en = pie_es

    (RAIZ / "multiplo" / "privacidad.html").write_text(PLANTILLA.format(
        lang="es", titulo="Política de privacidad · Múltiplo",
        desc="Política de privacidad de Múltiplo. Tus datos de juego no salen del dispositivo.",
        sub="Política de privacidad", idiomas=nav_es,
        cuerpo="<h1>Política de privacidad</h1>\n" + a_html(es), pie=pie_es),
        encoding="utf-8")

    (RAIZ / "multiplo" / "privacy.html").write_text(PLANTILLA.format(
        lang="en", titulo="Privacy Policy · Múltiplo",
        desc="Privacy policy for Multiplo. Your game data never leaves your device.",
        sub="Privacy policy", idiomas=nav_en,
        cuerpo="<h1>Privacy Policy</h1>\n" + a_html(en), pie=pie_en),
        encoding="utf-8")

    indice = """<h1>Múltiplo</h1>
<div class="resumen"><p>Juego de calculo mental para iPhone y iPad. Tablas de
multiplicar convertidas en un juego de reflejos.</p></div>
<h2>Documentos</h2>
<ul>
<li><a href="multiplo/privacidad.html">Politica de privacidad</a> (espanol)</li>
<li><a href="multiplo/privacy.html">Privacy policy</a> (English)</li>
</ul>
<h2>Contacto</h2>
<p>Para cualquier duda: <a href="mailto:jlq.software@gmail.com">jlq.software@gmail.com</a></p>"""
    (RAIZ / "index.html").write_text(PLANTILLA.format(
        lang="es", titulo="Múltiplo · Documentación",
        desc="Documentacion publica de Multiplo.",
        sub="Documentación", idiomas="", cuerpo=indice,
        pie="Jose Luis Querido Chica"), encoding="utf-8")
    print("Generado: index.html, multiplo/privacidad.html, multiplo/privacy.html")


if __name__ == "__main__":
    main()
