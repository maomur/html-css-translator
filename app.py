import os
from flask import Flask, request, jsonify, send_file
from dotenv import load_dotenv
import anthropic

load_dotenv()

app = Flask(__name__)
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

SYSTEM_PROMPT = """You are an HTML/CSS translator. Translate from {source_lang} to {target_lang}.

STRICT RULES:
1. Preserve ALL HTML tags, attribute names, class names, IDs, CSS selectors,
   CSS property names, CSS values, href, src, data-* attributes EXACTLY as-is.
2. Translate ONLY:
   - Visible text nodes between tags
   - Values of these attributes when present: alt, title, placeholder,
     aria-label, content (meta tags only)
3. Return ONLY the translated HTML — no explanation, no markdown fences."""


@app.route("/")
def index():
    return send_file("index.html")


@app.route("/translate", methods=["POST"])
def translate():
    data = request.get_json(force=True)
    html = (data.get("html") or "").strip()
    source_lang = data.get("source_lang", "English")
    target_lang = data.get("target_lang", "Spanish")

    if not html:
        return jsonify({"error": "No HTML/CSS provided."}), 400

    try:
        message = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=8192,
            system=SYSTEM_PROMPT.format(source_lang=source_lang, target_lang=target_lang),
            messages=[
                {
                    "role": "user",
                    "content": f"Translate the following from {source_lang} to {target_lang}:\n\n{html}",
                }
            ],
        )
        translated = message.content[0].text.strip()
        return jsonify({"translated_html": translated})
    except anthropic.AuthenticationError:
        return jsonify({"error": "Invalid API key. Check your .env file."}), 500
    except Exception as exc:
        return jsonify({"error": str(exc)}), 500


if __name__ == "__main__":
    app.run(debug=True, port=5000)
