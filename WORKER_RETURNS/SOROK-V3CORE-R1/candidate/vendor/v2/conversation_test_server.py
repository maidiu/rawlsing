#!/usr/bin/env python3
"""
Local test server for the conversation engine. Run this, open http://127.0.0.1:5000
in your browser, type messages, and see the engine output (hooks, refraction, streams,
move) plus the prompt or persona reply. No ChatGPT needed—you see what we're building.

  cd /path/to/Rawlsing
  pip install flask   # if not installed
  python3 v2/conversation_test_server.py

  Then open http://127.0.0.1:5000

Optional: set OPENAI_API_KEY so the server calls the API and shows the persona reply.
"""

import json
import os
import sys

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

# Load .env from repo root so OPENAI_API_KEY is set without manual export
try:
    from dotenv import load_dotenv
    load_dotenv(os.path.join(_ROOT, ".env"))
except ImportError:
    pass

# Lazy load so we can show a clear error if deps missing
_history = None
_field = None


def _get_history():
    global _history
    if _history is not None:
        return _history
    from v2.run_conversation_chat import _load_persona_from_sheet, _minimal_persona
    # Prefer dev pipeline persona (full sim output) if present
    path = os.environ.get("DEV_PERSONA_JSON") or os.path.join(_ROOT, "dev_persona.json")
    if os.path.isfile(path):
        _history = _load_persona_from_sheet(path)
    else:
        path = os.path.join(_ROOT, "handoff_kid", "persona_sheet.json")
        if os.path.isfile(path):
            _history = _load_persona_from_sheet(path)
        else:
            _history = _minimal_persona()
    return _history


def run_turn(user_message: str):
    """Run one conversation turn; return dict with prompt, engine output, and optional reply."""
    global _field
    from v2 import prepare_conversation_turn, update_energetic_field
    history = _get_history()
    out = prepare_conversation_turn(
        history,
        user_message,
        date="2025-01-15",
        scenario_reason=None,
        rng=None,
        energetic_field=_field,
    )
    _field = out["energetic_field"]
    streams = getattr(_field, "active_streams", None) or []
    engine = {
        "selected_hooks": out.get("selected_hooks", []),
        "response_angles": out.get("response_angles", []),
        "refraction_strength": out.get("refraction_strength"),
        "ongoing_streams": [
            {"external": s.external_tag, "internal": s.internal_tag, "strength": round(s.strength, 2)}
            for s in streams[:4]
        ],
        "move_type": out.get("move", {}).get("move_type"),
        "max_sentences": out.get("move", {}).get("max_sentences"),
    }
    reply = ""
    if os.environ.get("OPENAI_API_KEY"):
        try:
            from openai import OpenAI
            r = OpenAI().chat.completions.create(
                model=os.environ.get("OPENAI_MODEL", "gpt-4o-mini"),
                messages=[{"role": "user", "content": out["prompt"]}],
                max_tokens=400,
            )
            reply = (r.choices[0].message.content or "").strip()
            if reply:
                _field = update_energetic_field(_field, reply, "persona", persona_effort="medium")
        except Exception as e:
            reply = f"(API error: {e})"
    return {
        "prompt": out["prompt"],
        "engine": engine,
        "reply": reply,
    }


INDEX_HTML = """
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>Conversation engine test</title>
  <style>
    body { font-family: system-ui, sans-serif; max-width: 900px; margin: 1rem auto; padding: 0 1rem; }
    h1 { font-size: 1.2rem; }
    .row { display: flex; gap: 1rem; margin: 0.5rem 0; }
    input[type="text"] { flex: 1; padding: 0.5rem; }
    button { padding: 0.5rem 1rem; cursor: pointer; }
    .panel { background: #f5f5f5; border-radius: 6px; padding: 0.75rem; margin: 0.75rem 0; }
    .panel h3 { margin: 0 0 0.5rem 0; font-size: 0.9rem; }
    pre { white-space: pre-wrap; font-size: 0.8rem; max-height: 300px; overflow: auto; }
    .error { color: #c00; }
  </style>
</head>
<body>
  <h1>Conversation engine test</h1>
  <p>Type a message and click Send. You'll see what the engine produced (hooks, refraction, streams, move) and the prompt or persona reply.</p>
  <p><strong>No JavaScript required:</strong> use the form below. Submit opens the result on the same page.</p>
  <form method="post" action="/turn" style="margin: 0.5rem 0;">
    <div class="row">
      <input type="text" name="message" placeholder="Your message..." style="flex: 1;" />
      <button type="submit">Send</button>
    </div>
  </form>
  <div id="out"></div>
  <script>
    function sendMsg() {
      var msg = document.getElementById("msg").value.trim();
      if (!msg) return;
      var out = document.getElementById("out");
      out.innerHTML = "<p>Sending...</p>";
      var url = (window.location.origin || "http://127.0.0.1:5001") + "/api/turn";
      fetch(url, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: msg })
      })
      .then(function(r) {
        if (!r.ok) return r.text().then(function(t) { throw new Error(r.status + " " + t); });
        return r.json();
      })
      .then(function(data) {
        if (data.error) {
          out.innerHTML = "<p class=\"error\">" + data.error + "</p>";
          return;
        }
        var html = "";
        html += "<div class=\"panel\"><h3>Engine this turn</h3>";
        html += "<p><strong>selected_hooks:</strong> " + JSON.stringify(data.engine.selected_hooks) + "</p>";
        html += "<p><strong>response_angles:</strong> " + JSON.stringify(data.engine.response_angles) + "</p>";
        html += "<p><strong>refraction_strength:</strong> " + data.engine.refraction_strength + "</p>";
        html += "<p><strong>ongoing_streams:</strong> " + JSON.stringify(data.engine.ongoing_streams) + "</p>";
        html += "<p><strong>move:</strong> " + data.engine.move_type + " (max " + data.engine.max_sentences + " sentences)</p></div>";
        if (data.reply) {
          html += "<div class=\"panel\"><h3>Persona reply</h3><pre>" + data.reply.replace(/</g, "&lt;").replace(/&/g, "&amp;") + "</pre></div>";
        }
        var promptText = (data.prompt || "").replace(/</g, "&lt;").replace(/&/g, "&amp;");
        html += "<div class=\"panel\"><h3>Prompt sent to LLM</h3><pre>" + promptText.substring(0, 8000) + (data.prompt.length > 8000 ? "\\n..." : "") + "</pre></div>";
        out.innerHTML = html;
      })
      .catch(function(e) {
        out.innerHTML = "<p class=\"error\">Request failed: " + e.message + "</p>";
      });
    }
    document.getElementById("send").onclick = sendMsg;
    document.getElementById("msg").onkeydown = function(e) { if (e.key === "Enter") sendMsg(); };
  </script>
</body>
</html>
"""


def main():
    try:
        from flask import Flask, request, jsonify, Response
    except ImportError:
        print("Flask required. Run: pip3 install flask")
        sys.exit(1)

    app = Flask(__name__)

    def _result_html(msg, result):
        engine = result.get("engine") or {}
        prompt = (result.get("prompt") or "").replace("<", "&lt;").replace("&", "&amp;")[:8000]
        reply = (result.get("reply") or "").replace("<", "&lt;").replace("&", "&amp;")
        parts = [
            "<!DOCTYPE html><html><head><meta charset='utf-8'><title>Result</title>",
            "<style>body{font-family:system-ui;max-width:900px;margin:1rem auto;padding:0 1rem;} .panel{background:#f5f5f5;border-radius:6px;padding:0.75rem;margin:0.75rem 0;} pre{white-space:pre-wrap;font-size:0.8rem;max-height:300px;overflow:auto;}</style></head><body>",
            "<h1>Conversation engine test</h1>",
            "<p><a href='/'>← Back to form</a></p>",
            "<div class='panel'><h3>You said</h3><p>" + msg.replace("<", "&lt;") + "</p></div>",
            "<div class='panel'><h3>Engine this turn</h3>",
            "<p><strong>selected_hooks:</strong> " + str(engine.get("selected_hooks", [])) + "</p>",
            "<p><strong>response_angles:</strong> " + str(engine.get("response_angles", [])) + "</p>",
            "<p><strong>refraction_strength:</strong> " + str(engine.get("refraction_strength")) + "</p>",
            "<p><strong>ongoing_streams:</strong> " + str(engine.get("ongoing_streams", [])) + "</p>",
            "<p><strong>move:</strong> " + str(engine.get("move_type")) + " (max " + str(engine.get("max_sentences")) + " sentences)</p></div>",
        ]
        if reply:
            parts.append("<div class='panel'><h3>Persona reply</h3><pre>" + reply + "</pre></div>")
        parts.append("<div class='panel'><h3>Prompt sent to LLM</h3><pre>" + prompt + "</pre></div>")
        parts.append("<p><a href='/'>Send another message</a></p></body></html>")
        return "".join(parts)

    @app.route("/")
    def index():
        return Response(INDEX_HTML, mimetype="text/html")

    @app.route("/turn", methods=["POST"])
    def turn_form():
        msg = (request.form.get("message") or request.form.get("msg") or "").strip()
        if not msg:
            return Response(INDEX_HTML, mimetype="text/html")
        try:
            result = run_turn(msg)
            return _result_html(msg, result)
        except Exception as e:
            return "<html><body><p style='color:red'>Error: " + str(e).replace("<", "&lt;") + "</p><p><a href='/'>Back</a></p></body></html>", 500

    @app.after_request
    def cors(resp):
        resp.headers["Access-Control-Allow-Origin"] = "*"
        resp.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
        resp.headers["Access-Control-Allow-Headers"] = "Content-Type"
        return resp

    @app.route("/api/turn", methods=["POST", "OPTIONS"])
    def turn():
        if request.method == "OPTIONS":
            return "", 204
        data = request.get_json() or {}
        msg = (data.get("message") or "").strip()
        if not msg:
            return jsonify({"error": "message required"}), 400
        try:
            result = run_turn(msg)
            return jsonify(result)
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    # Preload persona (5001: macOS often uses 5000 for AirPlay Receiver)
    _get_history()
    port = int(os.environ.get("PORT", 5001))
    print("Conversation engine test server")
    print("  Open http://127.0.0.1:{} in your browser.".format(port))
    print("  Type a message and click Send to see engine output + prompt (or reply if OPENAI_API_KEY set).")
    app.run(host="127.0.0.1", port=port, debug=False)


if __name__ == "__main__":
    main()
