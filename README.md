# AI-Based Email Spam Detection — Single Agent

A small interactive web app demonstrating one explainable email-analysis agent. The user enters an email's sender, subject, and body; the agent evaluates text patterns and email characteristics, then returns a spam/legitimate decision with a risk score and explanation.

## Run locally

1. Install Python 3.10 or newer.
2. Open a terminal in this project folder.
3. Install dependencies:
   ```bash
   python -m venv .venv
   # Windows:
   .venv\Scripts\activate
   # macOS/Linux:
   source .venv/bin/activate
   pip install -r requirements.txt
   ```
4. Start the app:
   ```bash
   python app.py
   ```
5. Open http://127.0.0.1:5000 in your browser.

## How the single agent works

**Input → Observe → Score signals → Decide → Explain**

- Observes sender, subject, body, links, urgency phrases, punctuation, and capitalization.
- Calculates an explainable risk score.
- Score 3 or higher = SPAM; otherwise = LEGITIMATE.
- Returns confidence-style indicator and the signals that influenced the decision.

## Important limitations

This is an educational prototype using transparent rules, not a trained machine-learning model. The confidence indicator is a heuristic display, not a calibrated probability. It does not connect to an inbox, send email, or open links. For production, use a labeled dataset, train and validate a classifier, and add privacy/security controls.
