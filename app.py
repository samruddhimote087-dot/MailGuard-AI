from flask import Flask, render_template, request, jsonify
from spam_agent import EmailSpamAgent

app = Flask(__name__)
agent = EmailSpamAgent()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/analyze", methods=["POST"])
def analyze():
    data = request.get_json(silent=True) or {}
    subject = str(data.get("subject", ""))[:500]
    sender = str(data.get("sender", ""))[:300]
    body = str(data.get("body", ""))[:12000]
    if not (subject.strip() or sender.strip() or body.strip()):
        return jsonify({"error": "Enter an email subject, sender, or message first."}), 400
    return jsonify(agent.analyze(subject, sender, body))

if __name__ == "__main__":
    app.run(debug=True, port=5000)
