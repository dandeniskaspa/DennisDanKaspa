#!/usr/bin/env python3
"""
סוכן תודעה - אפליקציית שיחה
Consciousness Agent - Web Chat Application
"""

import os
import json
from flask import Flask, render_template, request, stream_with_context, Response
from anthropic import Anthropic
from system_prompt import SYSTEM_PROMPT

app = Flask(__name__)

client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY", ""))


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    messages = data.get("messages", [])

    def generate():
        with client.messages.stream(
            model="claude-opus-4-6",
            max_tokens=2048,
            system=SYSTEM_PROMPT,
            messages=messages,
        ) as stream:
            for text in stream.text_stream:
                yield f"data: {json.dumps({'text': text})}\n\n"
        yield "data: [DONE]\n\n"

    return Response(
        stream_with_context(generate()),
        mimetype="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
        },
    )


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host="0.0.0.0", port=port)
