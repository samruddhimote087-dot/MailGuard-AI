# MailGuard AI — Interactive Email Spam Detection

A more user-friendly Streamlit app for a **single intelligent email-analysis agent**. The interface includes a sidebar guide, quick-fill sample emails, clear input fields, color-coded classification, risk score, signal explanations, and an expandable explanation panel. The on-screen privacy notice and bottom disclaimer have been removed.

## Files
- `app.py` — Streamlit interface and agent logic in one file.
- `requirements.txt` — required dependency.
- `README.md` — project instructions.

## Run locally
```bash
pip install -r requirements.txt
streamlit run app.py
```
Open the local address printed by Streamlit, usually `http://localhost:8501`.

## Deploy on Streamlit Community Cloud
1. Upload `app.py`, `requirements.txt`, and `README.md` to a GitHub repository.
2. Create an app in Streamlit Community Cloud.
3. Select the repository and set **Main file path** to `app.py`.
4. Deploy.

## How it works
The single agent checks for configured suspicious phrases, multiple links, unusual punctuation, excessive capital letters, and selected sender-domain indicators. It adds risk points and labels an email SPAM if the score is 3 or higher; otherwise, it labels it LIKELY LEGITIMATE. The dashboard explains detected signals.

## Important limitations
This is an educational rule-based prototype, not a trained machine-learning model. Its confidence indicator is heuristic, not a calibrated probability. It does not connect to Gmail, verify sender identity, inspect attachments, or open links. A message classified as legitimate may still be harmful.
