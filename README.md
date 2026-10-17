# MailGuard AI — Single Intelligent Agent for Email Spam Detection

MailGuard AI is an interactive Streamlit application that analyzes an email's sender address, subject, and body. One explainable, rule-based intelligent agent checks for suspicious phrases, links, unusual punctuation, excessive capitalization, and selected sender-domain indicators. It then classifies the email as **SPAM** or **LEGITIMATE**, displays a risk score, and explains the signals behind its decision.

## Files in this project

- `app.py` — complete Streamlit user interface and single-agent logic.
- `requirements.txt` — Python dependency list.
- `README.md` — setup and project documentation.

## Run locally

1. Install Python 3.10 or newer.
2. Open a terminal in this folder.
3. Install the dependency:

   ```bash
   pip install -r requirements.txt
   ```

4. Start the app:

   ```bash
   streamlit run app.py
   ```

5. Open the local URL shown in the terminal, usually `http://localhost:8501`.

## Deploy on Streamlit Community Cloud

1. Upload these three files to a GitHub repository.
2. Create a new app in Streamlit Community Cloud and select that repository.
3. Set **Main file path** to `app.py`.
4. Deploy the app.

## How the agent works

1. **Observe:** receives sender, subject, and message text.
2. **Analyze:** checks configured phrases and selected email characteristics.
3. **Score:** adds risk points for detected indicators.
4. **Decide:** score of 3 or higher is classified as SPAM; lower scores are classified as LEGITIMATE.
5. **Explain:** shows the detected signals and summary in the dashboard.

## Important limitations

This is an educational prototype using hand-written rules, not a trained machine-learning model. It may miss sophisticated spam or flag legitimate messages that contain suspicious wording. The percentage shown as a confidence indicator is a heuristic, not a calibrated probability. The app does not connect to Gmail, open links, inspect attachments, or automatically block email. Do not use the result as the only basis for cybersecurity decisions.
