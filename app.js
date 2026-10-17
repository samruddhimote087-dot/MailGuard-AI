const form = document.getElementById('emailForm');
const sender = document.getElementById('sender');
const subject = document.getElementById('subject');
const body = document.getElementById('body');
const analyzeBtn = document.getElementById('analyzeBtn');
const charCount = document.getElementById('charCount');
const emptyState = document.getElementById('emptyState');
const loadingState = document.getElementById('loadingState');
const resultState = document.getElementById('resultState');
const errorBox = document.getElementById('errorBox');

body.addEventListener('input', () => charCount.textContent = `${body.value.length.toLocaleString()} / 12,000`);

document.querySelectorAll('[data-sample]').forEach(button => {
  button.addEventListener('click', () => {
    if (button.dataset.sample === 'spam') {
      sender.value = 'prize-center@example.com';
      subject.value = 'URGENT! Congratulations, you have won a FREE gift';
      body.value = 'Act now! You have won a prize. Verify your account immediately and click here: http://claim-prize.example/verify. Limited time offer!!! Send your bank details to claim your guaranteed reward.';
    } else {
      sender.value = 'alex.morgan@company.com';
      subject.value = 'Project update for tomorrow';
      body.value = 'Hi team, I have attached the notes from today’s meeting. Please review the project timeline before our check-in tomorrow. Let me know if you have any questions. Thanks, Alex';
    }
    charCount.textContent = `${body.value.length.toLocaleString()} / 12,000`;
    hideResult();
  });
});

form.addEventListener('submit', async (event) => {
  event.preventDefault();
  if (!(sender.value.trim() || subject.value.trim() || body.value.trim())) {
    showError('Please enter a sender, subject, or message to analyze.');
    return;
  }
  errorBox.classList.add('hidden');
  emptyState.classList.add('hidden');
  resultState.classList.add('hidden');
  loadingState.classList.remove('hidden');
  analyzeBtn.disabled = true;
  try {
    const response = await fetch('/api/analyze', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({sender: sender.value, subject: subject.value, body: body.value})
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.error || 'Unable to analyze this email.');
    renderResult(data);
  } catch (error) {
    loadingState.classList.add('hidden');
    emptyState.classList.remove('hidden');
    showError(error.message || 'Could not connect to the analysis agent. Is the server running?');
  } finally {
    analyzeBtn.disabled = false;
  }
});

function renderResult(data) {
  loadingState.classList.add('hidden');
  resultState.classList.remove('hidden');
  const spam = data.label === 'SPAM';
  const verdict = document.getElementById('verdict');
  verdict.textContent = data.label;
  verdict.className = spam ? 'spam-text' : 'legit-text';
  document.getElementById('verdictIcon').textContent = spam ? '!' : '✓';
  document.getElementById('verdictIcon').className = `verdict-icon ${spam ? 'spam' : 'legit'}`;
  document.getElementById('verdictSummary').textContent = data.summary;
  document.getElementById('scoreText').textContent = `${data.score} / 10`;
  document.getElementById('meterFill').style.width = `${data.score * 10}%`;
  document.getElementById('confidenceText').textContent = `${data.confidence}%`;
  document.getElementById('signalCount').textContent = `${data.signals.length} signal${data.signals.length === 1 ? '' : 's'}`;
  const list = document.getElementById('signalsList');
  list.innerHTML = '';
  data.signals.forEach(signal => {
    const item = document.createElement('div');
    item.className = 'signal';
    const mark = document.createElement('span');
    mark.className = `signal-mark ${signal.kind}`;
    mark.textContent = signal.kind === 'risk' ? '!' : signal.kind === 'good' ? '✓' : 'i';
    const label = document.createElement('span');
    label.className = 'signal-label';
    label.textContent = signal.label;
    const impact = document.createElement('span');
    impact.className = `signal-impact ${signal.kind}`;
    impact.textContent = signal.impact;
    item.append(mark, label, impact);
    list.appendChild(item);
  });
  document.getElementById('whyText').textContent = data.reasons.length
    ? data.reasons.join('; ') + '.'
    : 'No strong common spam indicators were detected. Always use caution with unexpected requests.';
}

function showError(message) {
  errorBox.textContent = message;
  errorBox.classList.remove('hidden');
}
function hideResult() {
  loadingState.classList.add('hidden');
  resultState.classList.add('hidden');
  errorBox.classList.add('hidden');
  emptyState.classList.remove('hidden');
}
document.getElementById('clearBtn').addEventListener('click', () => {
  sender.value = ''; subject.value = ''; body.value = '';
  charCount.textContent = '0 / 12,000'; hideResult();
});
document.getElementById('analyzeAnother').addEventListener('click', () => {
  hideResult(); body.focus();
});
