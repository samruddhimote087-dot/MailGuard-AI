import re
import streamlit as st

st.set_page_config(page_title="MailGuard AI", page_icon="🛡️", layout="wide")

# Single intelligent agent: observe email signals, score risk, classify, explain.
class EmailSpamAgent:
    SPAM_PHRASES = {
        "urgent action required": 2,
        "act now": 2,
        "claim your prize": 3,
        "you have won": 3,
        "winner": 1,
        "free gift": 2,
        "limited time": 1,
        "verify your account": 2,
        "password expires": 2,
        "click here": 1,
        "guaranteed": 1,
        "make money fast": 3,
        "risk-free": 2,
        "congratulations": 1,
        "wire transfer": 2,
        "bank details": 2,
        "investment opportunity": 1,
        "100% free": 2,
    }
    URL_RE = re.compile(r'https?://[^\s<>"\']+|www\.[^\s<>"\']+', re.I)
    EMAIL_RE = re.compile(r'[\w.+-]+@[\w-]+\.[\w.-]+')

    def analyze(self, subject, sender, body):
        text = f"{subject}\n{body}".lower()
        combined = f"{subject}\n{body}"
        score = 0
        signals = []

        for phrase, points in self.SPAM_PHRASES.items():
            if phrase in text:
                score += points
                signals.append((f"Contains phrase: “{phrase}”", f"+{points}", "risk"))

        urls = self.URL_RE.findall(combined)
        if len(urls) >= 3:
            score += 2
            signals.append((f"Contains {len(urls)} links", "+2", "risk"))
        elif urls:
            signals.append((f"Contains {len(urls)} link(s)", "Review", "neutral"))

        if re.search(r'!{2,}|\${2,}|₨\s?\d+', combined):
            score += 1
            signals.append(("Unusual punctuation or money emphasis", "+1", "risk"))

        if len(re.findall(r'\b[A-Z]{4,}\b', combined)) >= 3:
            score += 1
            signals.append(("Excessive ALL-CAPS wording", "+1", "risk"))

        if sender.strip():
            match = self.EMAIL_RE.search(sender)
            if not match:
                score += 1
                signals.append(("Sender is not a recognizable email address", "+1", "risk"))
            else:
                domain = match.group(0).split("@")[-1].lower()
                if domain in {"example.com", "test.com", "mailinator.com", "tempmail.com"}:
                    score += 2
                    signals.append((f"Disposable/test-style sender domain: {domain}", "+2", "risk"))
                elif domain.endswith((".xyz", ".top", ".click", ".work")):
                    score += 1
                    signals.append((f"Less common sender domain: {domain}", "+1", "risk"))

        if not signals:
            signals.append(("No common spam signals detected", "0", "good"))

        label = "SPAM" if score >= 3 else "LEGITIMATE"
        confidence = min(97, 58 + score * 8) if label == "SPAM" else max(62, 94 - score * 8)
        confidence = min(confidence, 97)
        reasons = [s[0] for s in signals if s[2] == "risk"]
        summary = (
            "Several suspicious signals were found. Avoid clicking links or sharing personal information."
            if label == "SPAM" else
            "Few common spam indicators were found. Verify unexpected requests before acting."
        )
        return {
            "label": label,
            "score": min(score, 10),
            "confidence": confidence,
            "summary": summary,
            "signals": signals,
            "reasons": reasons,
        }

agent = EmailSpamAgent()

st.markdown("""
<style>
.stApp { background: #f4f6fa; }
.main-title { font-size: 2.7rem; font-weight: 800; color: #17213b; line-height: 1.1; }
.accent { color: #6558e8; }
.subtle { color: #78839b; }
div[data-testid="stMetric"] { background: white; padding: 16px; border: 1px solid #e8ebf2; border-radius: 14px; }
</style>
""", unsafe_allow_html=True)

st.caption("✦ INTELLIGENT EMAIL SECURITY")
st.markdown('<div class="main-title">Know what’s in your<br><span class="accent">inbox.</span></div>', unsafe_allow_html=True)
st.markdown('<p class="subtle">One intelligent agent. Every suspicious signal explained.</p>', unsafe_allow_html=True)
st.divider()

left, right = st.columns([1, 1], gap="large")

with left:
    st.subheader("✉️ Inspect an email")
    with st.form("email_form"):
        sender = st.text_input("Sender address", placeholder="e.g. support@company.com")
        subject = st.text_input("Email subject", placeholder="What is this email about?")
        body = st.text_area("Message content", height=220, placeholder="Paste the email message here...")
        submitted = st.form_submit_button("✦ Analyze email", type="primary", use_container_width=True)

    st.markdown("**Try a sample**")
    sample_col1, sample_col2 = st.columns(2)
    if sample_col1.button("Suspicious email", use_container_width=True):
        st.session_state["sample"] = "spam"
    if sample_col2.button("Work email", use_container_width=True):
        st.session_state["sample"] = "safe"

    if st.session_state.get("sample") == "spam":
        st.info("Sample: sender prize-center@example.com · subject: URGENT! Congratulations, you have won a FREE gift. Paste these values into the form to test.")
    elif st.session_state.get("sample") == "safe":
        st.info("Sample: sender alex.morgan@company.com · subject: Project update for tomorrow. Message: Hi team, please review the project timeline before tomorrow’s check-in.")

    st.caption("🔒 This demo analyzes only the text you enter. It does not connect to your inbox.")

with right:
    st.subheader("◈ Agent decision")
    if submitted:
        if not (sender.strip() or subject.strip() or body.strip()):
            st.warning("Enter a sender, subject, or message first.")
        else:
            result = agent.analyze(subject, sender, body)
            if result["label"] == "SPAM":
                st.error("🚨 SPAM DETECTED")
            else:
                st.success("✅ LIKELY LEGITIMATE")

            st.write(result["summary"])
            metric1, metric2 = st.columns(2)
            metric1.metric("Risk score", f'{result["score"]} / 10')
            metric2.metric("Confidence indicator", f'{result["confidence"]}%')
            st.progress(result["score"] / 10)
            st.caption("Low risk  ← Risk score →  High risk")

            st.markdown("### Signals detected")
            for label, impact, kind in result["signals"]:
                if kind == "risk":
                    st.warning(f"{impact} · {label}")
                elif kind == "good":
                    st.success(label)
                else:
                    st.info(f"{impact} · {label}")

            st.markdown("### Why this decision?")
            if result["reasons"]:
                st.write("; ".join(result["reasons"]) + ".")
            else:
                st.write("No strong common spam indicators were detected. Be careful with unexpected requests.")
    else:
        st.info("✨ Ready when you are")
        st.write("Your agent is waiting for an email to inspect.")
        st.markdown("1. Observe email content  \n2. Evaluate suspicious signals  \n3. Explain the decision")

st.divider()
st.caption("MAILGUARD AI · Explainable decisions · Educational prototype")
st.warning("This educational prototype uses transparent rules, not a trained machine-learning model. The confidence indicator is heuristic, not a calibrated probability.")
