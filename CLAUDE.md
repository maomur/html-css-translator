# HTML/CSS Translator

Web app que traduce el texto visible de código HTML/CSS a otro idioma usando la API de Claude, preservando intacta toda la estructura del código.

## Stack

- **Backend**: Flask (Python) — `app.py`
- **Frontend**: Single-file SPA — `index.html` (todo CSS y JS inline)
- **IA**: Claude Haiku (`claude-haiku-4-5-20251001`) vía SDK de Anthropic
- **Deploy**: Railway (producción) — auto-despliega al hacer push a `master`

## Arrancar en local

```bash
pip install -r requirements.txt   # solo la primera vez
python app.py                     # http://localhost:5000
```

La API key se lee de `.env` (no está en el repo, solo en local y en Railway como variable de entorno).

## Estructura

```
app.py           # servidor Flask + lógica de traducción
index.html       # toda la UI (HTML + CSS + JS en un solo archivo)
requirements.txt # flask, anthropic, python-dotenv, gunicorn
render.yaml      # config legacy de Render (no se usa, Railway es el deploy activo)
.env             # ANTHROPIC_API_KEY (no commitear)
```

## Cómo funciona

1. El usuario pega HTML/CSS en el editor izquierdo y selecciona idiomas.
2. Al pulsar Translate (o Ctrl+Enter), el frontend hace POST a `/translate`.
3. `app.py` llama a la API de Claude con un system prompt estricto que preserva tags, clases, IDs, selectores CSS y traduce solo texto visible y atributos semánticos (`alt`, `title`, `placeholder`, `aria-label`).
4. El resultado se muestra en el panel derecho.

## Frontend — `index.html`

### Editor de código (panel izquierdo)
- **CodeMirror 5** con tema Dracula, modo `htmlmixed` (HTML + CSS + JS inline)
- Números de línea, resaltado de sintaxis, cierre automático de tags y brackets
- **Linting en tiempo real** con HTMLHint — subraya errores/warnings con línea ondulada
- **Botón Format** — usa js-beautify (`html_beautify`) para indentar y limpiar el código
- **Botón Preview** — muestra el HTML de entrada renderizado en un iframe
- `Ctrl+Shift+F` formatea el código; `Ctrl+Enter` lanza la traducción

### Panel derecho (output)
- Alterna entre vista de código y preview del HTML traducido
- Si hay error, muestra un panel explicativo con el mensaje del servidor y sugerencias de corrección categorizadas por tipo (rate limit, auth, tamaño, red, etc.)

### Layout
- Dos paneles side-by-side con flexbox (`flex: 1` en cada panel)
- `.panel-body` es un flex container columna; todos sus hijos usan `flex: 1 + min-height: 0` para llenar el espacio
- CodeMirror se dimensiona con `ResizeObserver` que lee el alto del wrapper y llama a `editor.setSize(null, h)`

## Idiomas soportados

English, Spanish, French, German, Italian, Portuguese, Dutch, Polish, Russian, Chinese, Japanese, Arabic, Catalan.

## Variables de entorno

| Variable | Descripción |
|---|---|
| `ANTHROPIC_API_KEY` | API key de Anthropic (requerida) |

## Deploy en Railway

El proyecto está conectado al repo de GitHub. Cada push a `master` dispara un redeploy automático. El start command es `gunicorn app:app`.

URL de producción: `https://html-css-translator-production.up.railway.app/`
