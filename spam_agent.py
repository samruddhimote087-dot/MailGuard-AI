import re
from urllib.parse import urlparse

class EmailSpamAgent:
    """
    A single, explainable rule-based intelligent agent.
    It observes email text and sender details, scores risk signals,
    then chooses SPAM or LEGITIMATE and explains its decision.
    This is a demo baseline, not a replacement for a trained production model.
    """
    SPAM_PHRASES = {
        "urgent action required": 2, "act now": 2, "claim your prize": 3,
        "you have won": 3, "winner": 1, "free gift": 2, "limited time": 1,
        "verify your account": 2, "password expires": 2, "click here": 1,
        "guaranteed": 1, "make money fast": 3, "risk-free": 2,
        "congratulations": 1, "wire transfer": 2, "bank details": 2,
        "investment opportunity": 1, "100% free": 2, "unsubscribe": 0
    }
    URL_RE = re.compile(r'https?://[^\s<>"\']+|www\.[^\s<>"\']+', re.I)
    EMAIL_RE = re.compile(r'[\w.+-]+@[\w-]+\.[\w.-]+')

    def analyze(self, subject, sender, body):
        text = f"{subject}\n{body}".lower()
        score = 0
        signals = []

        for phrase, points in self.SPAM_PHRASES.items():
            if phrase in text and points:
                score += points
                signals.append({"label": f'Contains phrase: “{phrase}”', "impact": f"+{points}", "kind": "risk"})

        urls = self.URL_RE.findall(subject + "\n" + body)
        if len(urls) >= 3:
            score += 2
            signals.append({"label": f"Contains {len(urls)} links", "impact": "+2", "kind": "risk"})
        elif urls:
            signals.append({"label": f"Contains {len(urls)} link(s)", "impact": "Review", "kind": "neutral"})

        if re.search(r'!{2,}|\${2,}|₨\s?\d+', subject + " " + body):
            score += 1
            signals.append({"label": "Unusual punctuation or money emphasis", "impact": "+1", "kind": "risk"})

        if len(re.findall(r'\b[A-Z]{4,}\b', subject + " " + body)) >= 3:
            score += 1
            signals.append({"label": "Excessive ALL-CAPS wording", "impact": "+1", "kind": "risk"})

        if sender:
            match = self.EMAIL_RE.search(sender)
            if not match:
                score += 1
                signals.append({"label": "Sender is not a recognizable email address", "impact": "+1", "kind": "risk"})
            else:
                domain = match.group(0).split("@")[-1].lower()
                if domain in {"example.com", "test.com", "mailinator.com", "tempmail.com"}:
                    score += 2
                    signals.append({"label": f"Disposable/test-style sender domain: {domain}", "impact": "+2", "kind": "risk"})
                elif domain.endswith((".xyz", ".top", ".click", ".work")):
                    score += 1
                    signals.append({"label": f"Less common sender domain: {domain}", "impact": "+1", "kind": "risk"})

        if not signals:
            signals.append({"label": "No common spam signals detected", "impact": "0", "kind": "good"})

        # Score is intentionally transparent and easy to explain.
        label = "SPAM" if score >= 3 else "LEGITIMATE"
        confidence = min(97, 58 + score * 8) if label == "SPAM" else max(62, 94 - score * 8)
        confidence = min(confidence, 97)
        reasons = [s["label"] for s in signals if s["kind"] == "risk"]
        summary = (
            "Several suspicious signals were found. Avoid clicking links or sharing personal information."
            if label == "SPAM" else
            "The message has few common spam indicators. Still verify unexpected requests before acting."
        )
        return {
            "label": label,
            "score": min(score, 10),
            "confidence": confidence,
            "summary": summary,
            "signals": signals,
            "reasons": reasons,
            "agent": "Single Email Analysis Agent"
        }
