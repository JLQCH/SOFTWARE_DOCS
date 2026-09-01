# SOFTWARE_DOCS

Documentación pública de las aplicaciones de Jose Luis Querido Chica.

Publicado con GitHub Pages: **https://jlqch.github.io/SOFTWARE_DOCS/**

## Múltiplo

Juego de cálculo mental para iPhone y iPad.

| Documento | URL pública |
|---|---|
| Política de privacidad (ES) | https://jlqch.github.io/SOFTWARE_DOCS/multiplo/privacidad.html |
| Privacy policy (EN) | https://jlqch.github.io/SOFTWARE_DOCS/multiplo/privacy.html |

La primera es la que hay que pegar en **App Store Connect → Información de la
app → Política de privacidad** y en la configuración de **Google AdMob**.

## Cómo se edita

La fuente es Markdown; el HTML se genera y **no se edita a mano**:

```bash
# 1. Cambiar el texto
vi multiplo/privacidad.md

# 2. Regenerar las páginas
python3 build.py

# 3. Publicar
git add -A && git commit -m "Actualiza la política de privacidad" && git push
```

`build.py` no necesita instalar nada: lleva su propio conversor de Markdown.

> **Importante:** el texto de `multiplo/privacidad.md` tiene que coincidir con
> el que muestra la app en Ajustes → Privacidad (`PrivacyPolicyView`, en
> `Multiplo/Views/SettingsView.swift` del repositorio MULTIPLO). Si se cambia
> uno, hay que cambiar el otro, y actualizar la fecha en los dos sitios.

## Activar GitHub Pages (una sola vez)

En este repositorio: **Settings → Pages → Source: Deploy from a branch →
Branch: `main` / `(root)` → Save**. En un par de minutos las URLs de arriba
responden.
