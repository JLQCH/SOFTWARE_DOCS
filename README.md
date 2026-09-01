# SOFTWARE_DOCS

Documentación pública de las aplicaciones de Jose Luis Querido Chica.

Publicado con GitHub Pages: **https://jlqch.github.io/SOFTWARE_DOCS/**

## Múltiplo

Juego de cálculo mental para iPhone y iPad.

| Documento | URL pública | Dónde se usa |
|---|---|---|
| Soporte (ES) | https://jlqch.github.io/SOFTWARE_DOCS/multiplo/soporte.html | **URL de soporte** de App Store Connect (obligatoria) |
| Support (EN) | https://jlqch.github.io/SOFTWARE_DOCS/multiplo/support.html | — |
| Política de privacidad (ES) | https://jlqch.github.io/SOFTWARE_DOCS/multiplo/privacidad.html | **URL de política de privacidad** de App Store Connect (obligatoria) y **AdMob** |
| Privacy policy (EN) | https://jlqch.github.io/SOFTWARE_DOCS/multiplo/privacy.html | — |

Son **dos campos distintos** en App Store Connect y los dos son obligatorios.
La de soporte tiene que ofrecer ayuda de verdad (contacto y preguntas
frecuentes): poner ahí la política de privacidad es motivo de rechazo.

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

## Publicar el sitio (una sola vez)

Hay que hacer **dos cosas**, y la primera se olvida siempre:

1. **Hacer el repositorio público.** Settings → General → abajo del todo,
   Danger Zone → *Change repository visibility* → Public.

   > GitHub Pages **no funciona en repositorios privados** salvo con un plan
   > de pago. Con el repositorio privado, la URL da error aunque Pages esté
   > activado. Aquí no hay nada secreto: una política de privacidad y una
   > página de ayuda están hechas para ser públicas.

2. **Activar Pages.** Settings → Pages → Source: *Deploy from a branch* →
   Branch: `main` / `(root)` → Save.

En un par de minutos las URLs de arriba responden. Compruébalas antes de
pegarlas en App Store Connect.
