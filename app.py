import re
import streamlit as st
from datetime import datetime

st.set_page_config(page_title="MailGuard AI", page_icon="🛡️", layout="wide", initial_sidebar_state="expanded")

# ---------- Single intelligent agent ----------
class EmailSpamAgent:
    PHRASES = {
        "urgent action required": 2, "act now": 2, "claim your prize": 3,
        "you have won": 3, "winner": 1, "free gift": 2, "limited time": 1,
        "verify your account": 2, "password expires": 2, "click here": 1,
        "guaranteed": 1, "make money fast": 3, "risk-free": 2,
        "congratulations": 1, "wire transfer": 2, "bank details": 2,
        "investment opportunity": 1, "100% free": 2, "urgent": 1,
        "act immediately": 2, "confirm your password": 3
    }
    URL_RE = re.compile(r'https?://[^\s<>"\']+|www\.[^\s<>"\']+', re.I)
    EMAIL_RE = re.compile(r'[\w.+-]+@[\w-]+\.[\w.-]+')

    def analyze(self, subject, sender, body):
        combined = f"{subject}\n{body}"
        lower = combined.lower()
        score, signals = 0, []

        for phrase, points in self.PHRASES.items():
            if phrase in lower:
                score += points
                signals.append({"label": f"Suspicious phrase: “{phrase}”", "points": points, "kind": "risk"})

        urls = self.URL_RE.findall(combined)
        if len(urls) >= 3:
            score += 2
            signals.append({"label": f"Contains multiple links ({len(urls)})", "points": 2, "kind": "risk"})
        elif urls:
            signals.append({"label": f"Contains {len(urls)} link(s)", "points": 0, "kind": "neutral"})

        if re.search(r'!{2,}|\${2,}|₨\s?\d+', combined):
            score += 1
            signals.append({"label": "Unusual punctuation or money emphasis", "points": 1, "kind": "risk"})

        if len(re.findall(r'\b[A-Z]{4,}\b', combined)) >= 3:
            score += 1
            signals.append({"label": "Excessive ALL-CAPS wording", "points": 1, "kind": "risk"})

        if sender.strip():
            match = self.EMAIL_RE.search(sender)
            if not match:
                score += 1
                signals.append({"label": "Sender is not a recognizable email address", "points": 1, "kind": "risk"})
            else:
                domain = match.group(0).split("@")[-1].lower()
                if domain in {"example.com", "test.com", "mailinator.com", "tempmail.com"}:
                    score += 2
                    signals.append({"label": f"Test/disposable-style domain: {domain}", "points": 2, "kind": "risk"})
                elif domain.endswith((".xyz", ".top", ".click", ".work")):
                    score += 1
                    signals.append({"label": f"Less common sender domain: {domain}", "points": 1, "kind": "risk"})

        if not signals:
            signals.append({"label": "No common spam indicators detected", "points": 0, "kind": "good"})

        label = "SPAM" if score >= 3 else "LIKELY LEGITIMATE"
        reasons = [s["label"] for s in signals if s["kind"] == "risk"]
        # This is an illustrative heuristic, not calibrated probability.
        confidence = min(97, 58 + score * 8) if label == "SPAM" else max(62, 94 - score * 8)
        summary = (
            "This message contains several warning signs. Avoid clicking links or sharing sensitive information."
            if label == "SPAM" else
            "Few common spam indicators were detected. Still verify unexpected requests before taking action."
        )
        return {"label": label, "score": min(score, 10), "confidence": min(confidence, 97),
                "signals": signals, "reasons": reasons, "summary": summary}

agent = EmailSpamAgent()

# ---------- Styling ----------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap');
:root { --purple:#6759e8; --ink:#1b2440; }
.stApp { background: linear-gradient(135deg,#f7f8fc 0%,#f0f2fb 100%); color:var(--ink); }
.block-container { max-width: 1450px; padding-top: 1.2rem; padding-bottom: 2rem; }
[data-testid="stSidebar"] { background: #171b35; }
[data-testid="stSidebar"] * { color:#eef0ff; }
.brand {font-family:'Space Grotesk',sans-serif;font-size:1.55rem;font-weight:700;letter-spacing:-.7px}
.brand span {color:#a69cff}
.hero {padding:1.1rem 0 .7rem}
.kicker {font-size:.75rem;font-weight:700;letter-spacing:2px;color:#6759e8;text-transform:uppercase}
.hero-title {font-family:'Space Grotesk',sans-serif;font-size:clamp(2.6rem,5vw,4rem);font-weight:700;letter-spacing:-2px;line-height:1.03;color:#1b2440;margin:.5rem 0}
.hero-title span {color:#6759e8}
.hero-copy {font-size:1.02rem;color:#7a849c;line-height:1.65;max-width:700px}
div[data-testid="stMetric"] {background:#fff;border:1px solid #e8eaf3;border-radius:17px;padding:17px 18px;box-shadow:0 6px 24px rgba(34,42,82,.04)}
div[data-testid="stMetricLabel"] p {font-size:.78rem;color:#7a849c}
div[data-testid="stMetricValue"] {font-family:'Space Grotesk',sans-serif;color:#20294a}
div[data-testid="stForm"] {background:#fff;border:1px solid #e6e9f2;border-radius:20px;padding:1.3rem 1.4rem}
.stTextInput input,.stTextArea textarea {border-radius:11px!important;background:#fbfbfe!important}
.stButton button,.stFormSubmitButton button {border-radius:11px!important;font-weight:650!important;min-height:2.8rem}
.stButton button[kind="primary"],.stFormSubmitButton button[kind="primary"] {background:#6759e8!important;border-color:#6759e8!important}
.panel-title {font-family:'Space Grotesk',sans-serif;font-size:1.4rem;font-weight:700;color:#20294a}
.panel-subtitle {font-size:.9rem;color:#7a849c}
.status-spam {padding:1.1rem 1.2rem;border-radius:15px;background:#fff0f2;border:1px solid #ffd9df;color:#b82f4a}
.status-safe {padding:1.1rem 1.2rem;border-radius:15px;background:#e7faf2;border:1px solid #c8f1e1;color:#147650}
.status-title {font-family:'Space Grotesk',sans-serif;font-size:1.6rem;font-weight:700;margin-bottom:.25rem}
.signal {background:#fff;border:1px solid #e8eaf2;border-radius:12px;padding:.75rem .9rem;margin:.45rem 0;color:#35405e}
.small-muted {color:#8993a8;font-size:.8rem}
div[data-testid="stTabs"] button {font-weight:650}
</style>
""", unsafe_allow_html=True)

# ---------- Sidebar ----------
with st.sidebar:
    st.markdown('<div class="brand">🛡️ MailGuard <span>AI</span></div>', unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("### Your workspace")
    st.markdown("**● Agent status:** Online")
    st.caption("One agent · Explainable analysis")
    st.markdown("---")
    st.markdown("### Quick start")
    st.markdown("1. Add email details\n2. Click **Analyze email**\n3. Review the decision")
    st.markdown("---")
    st.markdown("### Privacy")
    st.caption("Your text is processed by this app only. No inbox connection is made.")
    st.markdown("---")
    st.caption("MAILGUARD AI · Student project")

# ---------- Header ----------
st.markdown('<div class="hero"><div class="kicker">✦ Intelligent email security</div><div class="hero-title">A safer inbox<br><span>starts here.</span></div><div class="hero-copy">Paste an email. Let one intelligent agent check the warning signs and explain what it finds—in seconds.</div></div>', unsafe_allow_html=True)

# Sample controls outside form to make quick demo use easier
st.markdown("#### Try a sample")
sample_cols = st.columns([1, 1, 3])
with sample_cols[0]:
    if st.button("🚨 Suspicious email", use_container_width=True):
        st.session_state["sender"] = "prize-center@example.com"
        st.session_state["subject"] = "URGENT! Congratulations, you have won a FREE gift"
        st.session_state["body"] = "Act now! You have won a prize. Verify your account immediately and click here: http://claim-prize.example/verify. Limited time offer!!! Send your bank details to claim your guaranteed reward."
        st.rerun()
with sample_cols[1]:
    if st.button("✉️ Work email", use_container_width=True):
        st.session_state["sender"] = "alex.morgan@company.com"
        st.session_state["subject"] = "Project update for tomorrow"
        st.session_state["body"] = "Hi team, I have attached the notes from today’s meeting. Please review the project timeline before our check-in tomorrow. Let me know if you have any questions. Thanks, Alex"
        st.rerun()
with sample_cols[2]:
    st.markdown('<div class="small-muted" style="padding:.7rem 0">Choose a sample to fill the form automatically, or enter your own email below.</div>', unsafe_allow_html=True)

left, right = st.columns([1.03, .97], gap="large")

with left:
    st.markdown('<div class="panel-title">✉️ Inspect an email</div><div class="panel-subtitle">Add any details you have. All fields are optional, but more detail helps.</div><br>', unsafe_allow_html=True)
    with st.form("email_form", clear_on_submit=False):
        sender = st.text_input("SENDER ADDRESS", key="sender", placeholder="name@example.com")
        subject = st.text_input("EMAIL SUBJECT", key="subject", placeholder="e.g. Your account needs attention")
        body = st.text_area("MESSAGE CONTENT", key="body", height=210, placeholder="Paste the email text here...")
        submitted = st.form_submit_button("✨ Analyze this email", type="primary", use_container_width=True)
    st.caption("🔒 For this demo, analysis is limited to the text you paste. The app does not connect to Gmail.")

with right:
    st.markdown('<div class="panel-title">🔎 Your analysis</div><div class="panel-subtitle">Your agent’s decision and the reasons behind it.</div><br>', unsafe_allow_html=True)
    if submitted:
        if not (sender.strip() or subject.strip() or body.strip()):
            st.warning("Please enter a sender, subject, or message first.")
        else:
            result = agent.analyze(subject, sender, body)
            is_spam = result["label"] == "SPAM"
            if is_spam:
                st.markdown(f'<div class="status-spam"><div class="status-title">🚨 SPAM DETECTED</div>{result["summary"]}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="status-safe"><div class="status-title">✅ LIKELY LEGITIMATE</div>{result["summary"]}</div>', unsafe_allow_html=True)

            st.write("")
            m1, m2 = st.columns(2)
            m1.metric("Risk score", f'{result["score"]} / 10', help="Rule-based risk score. Higher means more configured warning signs were detected.")
            m2.metric("Confidence indicator", f'{result["confidence"]}%', help="Heuristic display, not a calibrated probability.")
            st.progress(result["score"] / 10, text="Email risk level")
            st.markdown("#### Signals we noticed")
            for signal in result["signals"]:
                if signal["kind"] == "risk":
                    st.markdown(f'<div class="signal">🔴 <b>+{signal["points"]}</b> &nbsp; {signal["label"]}</div>', unsafe_allow_html=True)
                elif signal["kind"] == "good":
                    st.markdown(f'<div class="signal">🟢 &nbsp; {signal["label"]}</div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="signal">🔵 &nbsp; {signal["label"]} <span class="small-muted">(review manually)</span></div>', unsafe_allow_html=True)

            with st.expander("💡 Why did the agent choose this result?", expanded=True):
                if result["reasons"]:
                    for reason in result["reasons"]:
                        st.write("• " + reason)
                else:
                    st.write("No strong common spam indicators were detected. This does not guarantee the email is safe.")
            st.caption("Analysis complete · Single intelligent agent")
    else:
        st.markdown("""
        <div style="background:#fff;border:1px solid #e6e9f2;border-radius:20px;padding:2rem 1.4rem;text-align:center;min-height:300px">
          <div style="font-size:3.1rem">🛡️</div>
          <div style="font-family:'Space Grotesk',sans-serif;font-size:1.3rem;font-weight:700;color:#20294a;margin:.7rem 0">Ready to check your email</div>
          <div style="color:#8993a8;line-height:1.6">Your results will appear here, with a risk score and a simple explanation.</div>
          <div style="display:flex;justify-content:center;gap:1rem;flex-wrap:wrap;margin-top:1.5rem;color:#6d7891;font-size:.85rem">
            <span>① Observe</span><span>② Analyze</span><span>③ Explain</span>
          </div>
        </div>
        """, unsafe_allow_html=True)

st.divider()
foot1, foot2 = st.columns([3, 2])
with foot1:
    st.caption("MailGuard AI · Single intelligent agent · Educational prototype")
with foot2:
    st.caption("Note: rule-based demo, not a trained ML model. Always verify unexpected requests.")
