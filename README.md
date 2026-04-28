# HTML/CSS Translator

A local web app that translates visible text in HTML/CSS between languages while preserving all markup, selectors, attribute names, class names, and IDs.

## Prerequisites

- Python 3.9 or newer
- An [Anthropic API key](https://console.anthropic.com/)

## Setup

1. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

2. **Create a `.env` file** in this directory with your API key:

   ```
   ANTHROPIC_API_KEY=sk-ant-...
   ```

3. **Run the server**

   ```bash
   python app.py
   ```

4. Open your browser at `http://localhost:5000`

## Usage

1. Paste HTML or CSS into the left panel.
2. Select the **source language** (what the content is written in) and the **target language** (what you want it translated to).
3. Click **Translate** (or press `Ctrl+Enter` / `Cmd+Enter`).
4. The translated HTML/CSS appears in the right panel.
   - **Code view** — shows the raw translated markup.
   - **Preview** — renders the translated HTML in a sandboxed iframe.
   - **Copy** — copies the translated output to your clipboard.

## What gets translated

| Translated | Preserved exactly |
|---|---|
| Visible text between tags | Tag names (`div`, `p`, `span`, …) |
| `alt` attribute values | Attribute names (`class`, `id`, `href`, …) |
| `title` attribute values | CSS selectors and property names |
| `placeholder` attribute values | CSS values (`#fff`, `1rem`, …) |
| `aria-label` attribute values | `class`, `id`, `data-*` values |
| `content` attribute on `<meta>` tags | `href`, `src`, `action` values |

## Model

Uses `claude-haiku-4-5-20251001` via the [Anthropic Python SDK](https://github.com/anthropics/anthropic-sdk-python). Haiku is fast and cost-efficient for translation tasks.
