// JavaScript Logic for PlacementIQ Web Application

document.addEventListener('DOMContentLoaded', () => {
  initParticleCanvas();
  initFormBindings();
  initPresetButtons();

  const form = document.getElementById('prediction-form');
  if (form) {
    form.addEventListener('submit', handleFormSubmit);
  }
});

/* Canvas Particle Animation */
function initParticleCanvas() {
  const canvas = document.getElementById('bg-canvas');
  if (!canvas) return;
  const ctx = canvas.getContext('2d');

  let width = canvas.width = window.innerWidth;
  let height = canvas.height = window.innerHeight;

  window.addEventListener('resize', () => {
    width = canvas.width = window.innerWidth;
    height = canvas.height = window.innerHeight;
  });

  const particles = [];
  const particleCount = 45;

  for (let i = 0; i < particleCount; i++) {
    particles.push({
      x: Math.random() * width,
      y: Math.random() * height,
      vx: (Math.random() - 0.5) * 0.4,
      vy: (Math.random() - 0.5) * 0.4,
      radius: Math.random() * 2 + 1,
      alpha: Math.random() * 0.5 + 0.2
    });
  }

  function render() {
    ctx.clearRect(0, 0, width, height);

    for (let i = 0; i < particleCount; i++) {
      let p = particles[i];
      p.x += p.vx;
      p.y += p.vy;

      if (p.x < 0) p.x = width;
      if (p.x > width) p.x = 0;
      if (p.y < 0) p.y = height;
      if (p.y > height) p.y = 0;

      ctx.beginPath();
      ctx.arc(p.x, p.y, p.radius, 0, Math.PI * 2);
      ctx.fillStyle = `rgba(0, 242, 254, ${p.alpha})`;
      ctx.fill();

      for (let j = i + 1; j < particleCount; j++) {
        let p2 = particles[j];
        let dx = p.x - p2.x;
        let dy = p.y - p2.y;
        let dist = Math.sqrt(dx * dx + dy * dy);

        if (dist < 120) {
          ctx.beginPath();
          ctx.moveTo(p.x, p.y);
          ctx.lineTo(p2.x, p2.y);
          ctx.strokeStyle = `rgba(0, 242, 254, ${0.15 * (1 - dist / 120)})`;
          ctx.lineWidth = 0.8;
          ctx.stroke();
        }
      }
    }

    requestAnimationFrame(render);
  }

  render();
}

/* Slider & Input Bindings */
function initFormBindings() {
  const sliders = [
    { id: 'coding_score', suffix: '%' },
    { id: 'communication_score', suffix: '%' },
    { id: 'projects_count', suffix: ' Projects' },
    { id: 'certifications_count', suffix: ' Certs' },
    { id: 'ssc_p', suffix: '%' },
    { id: 'hsc_p', suffix: '%' },
    { id: 'degree_p', suffix: '%' },
    { id: 'etest_p', suffix: '%' }
  ];

  sliders.forEach(item => {
    const slider = document.getElementById(item.id);
    const badge = document.getElementById(`${item.id}-val`);
    if (slider && badge) {
      slider.addEventListener('input', (e) => {
        const val = parseFloat(e.target.value);
        badge.textContent = `${item.suffix === '%' ? val.toFixed(1) : val}${item.suffix}`;
      });
    }
  });
}

/* Preset Buttons */
function initPresetButtons() {
  const presets = {
    high: { full_name: 'Sophia Chen', target_role: 'Senior Software Engineer', github_url: 'https://github.com/sophiachen', linkedin_url: 'https://linkedin.com/in/sophiachen', portfolio_url: 'https://sophiachen.dev', coding_score: 92, communication_score: 88, projects_count: 4, certifications_count: 3, ssc_p: 88, hsc_p: 85, degree_p: 82, etest_p: 90, gender: 'F', ssc_b: 'Central', hsc_b: 'Central', hsc_s: 'Science', degree_t: 'Sci&Tech', workex: 'Yes' },
    average: { full_name: 'Rahul Sharma', target_role: 'Data Analyst', github_url: 'https://github.com/rahulsharma', linkedin_url: 'https://linkedin.com/in/rahulsharma', portfolio_url: '', coding_score: 70, communication_score: 74, projects_count: 2, certifications_count: 1, ssc_p: 68, hsc_p: 65, degree_p: 66, etest_p: 68, gender: 'M', ssc_b: 'Others', hsc_b: 'Others', hsc_s: 'Science', degree_t: 'Sci&Tech', workex: 'No' },
    experienced: { full_name: 'Marcus Vance', target_role: 'Full Stack Engineer', github_url: 'https://github.com/marcusvance', linkedin_url: 'https://linkedin.com/in/marcusvance', portfolio_url: 'https://marcusv.io', coding_score: 85, communication_score: 86, projects_count: 3, certifications_count: 2, ssc_p: 76, hsc_p: 74, degree_p: 75, etest_p: 78, gender: 'M', ssc_b: 'Central', hsc_b: 'Others', hsc_s: 'Commerce', degree_t: 'Comm&Mgmt', workex: 'Yes' },
    low: { full_name: 'Jordan Miller', target_role: 'Associate Analyst', github_url: '', linkedin_url: '', portfolio_url: '', coding_score: 48, communication_score: 52, projects_count: 1, certifications_count: 0, ssc_p: 55, hsc_p: 52, degree_p: 56, etest_p: 54, gender: 'M', ssc_b: 'Others', hsc_b: 'Others', hsc_s: 'Arts', degree_t: 'Others', workex: 'No' }
  };

  const suffixMap = {
    coding_score: '%', communication_score: '%', projects_count: ' Projects', certifications_count: ' Certs',
    ssc_p: '%', hsc_p: '%', degree_p: '%', etest_p: '%'
  };

  document.querySelectorAll('.btn-preset').forEach(btn => {
    btn.addEventListener('click', () => {
      const type = btn.getAttribute('data-preset');
      const data = presets[type];
      if (!data) return;

      Object.keys(data).forEach(key => {
        const input = document.getElementById(key);
        if (input) {
          if (input.type === 'range') {
            input.value = data[key];
            const badge = document.getElementById(`${key}-val`);
            if (badge) {
              const suf = suffixMap[key] || '%';
              badge.textContent = `${data[key]}${suf}`;
            }
          } else {
            input.value = data[key];
          }
        } else {
          const radio = document.querySelector(`input[name="${key}"][value="${data[key]}"]`);
          if (radio) radio.checked = true;
        }
      });
    });
  });
}

/* Handle Prediction Submission */
async function handleFormSubmit(e) {
  e.preventDefault();

  const getRadioVal = (name) => {
    const checked = document.querySelector(`input[name="${name}"]:checked`);
    return checked ? checked.value : '';
  };

  const payload = {
    full_name: document.getElementById('full_name').value || 'Candidate',
    target_role: document.getElementById('target_role').value || 'General Candidate',
    github_url: document.getElementById('github_url').value || '',
    linkedin_url: document.getElementById('linkedin_url').value || '',
    portfolio_url: document.getElementById('portfolio_url').value || '',
    coding_score: parseFloat(document.getElementById('coding_score').value),
    communication_score: parseFloat(document.getElementById('communication_score').value),
    projects_count: parseInt(document.getElementById('projects_count').value),
    certifications_count: parseInt(document.getElementById('certifications_count').value),
    ssc_p: parseFloat(document.getElementById('ssc_p').value),
    hsc_p: parseFloat(document.getElementById('hsc_p').value),
    degree_p: parseFloat(document.getElementById('degree_p').value),
    etest_p: parseFloat(document.getElementById('etest_p').value),
    gender: getRadioVal('gender') || 'M',
    ssc_b: getRadioVal('ssc_b') || 'Central',
    hsc_b: getRadioVal('hsc_b') || 'Central',
    hsc_s: document.getElementById('hsc_s').value,
    degree_t: document.getElementById('degree_t').value,
    workex: getRadioVal('workex') || 'No'
  };

  const submitBtn = document.getElementById('submit-btn');
  const originalText = submitBtn.innerHTML;
  submitBtn.disabled = true;
  submitBtn.innerHTML = `<i class="fas fa-spinner fa-spin"></i> Evaluating Candidate Profile & Skills...`;

  try {
    const res = await fetch('/api/predict', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });

    if (!res.ok) {
      const err = await res.json();
      throw new Error(err.detail || 'Prediction failed');
    }

    const result = await res.json();
    displayPredictionResult(result);
  } catch (err) {
    alert(`Error: ${err.message}`);
  } finally {
    submitBtn.disabled = false;
    submitBtn.innerHTML = originalText;
  }
}

/* Display Prediction Result Report */
function displayPredictionResult(data) {
  const container = document.getElementById('result-container');
  if (!container) return;

  const isPlaced = data.verdict === 'Placed';
  const prob = data.probability_placed;

  // Build profile badges HTML
  let profileBadges = '';
  if (data.github_url) {
    profileBadges += `<a href="${data.github_url}" target="_blank" class="profile-badge-link"><i class="fab fa-github"></i> GitHub</a>`;
  }
  if (data.linkedin_url) {
    profileBadges += `<a href="${data.linkedin_url}" target="_blank" class="profile-badge-link"><i class="fab fa-linkedin" style="color:#0077b5;"></i> LinkedIn</a>`;
  }
  if (data.portfolio_url) {
    profileBadges += `<a href="${data.portfolio_url}" target="_blank" class="profile-badge-link"><i class="fas fa-globe" style="color:var(--warning);"></i> Portfolio</a>`;
  }

  container.innerHTML = `
    <div class="fade-in">
      <div class="candidate-header">
        <h3 class="candidate-name">${data.full_name}</h3>
        <p class="candidate-role"><i class="fas fa-user-tie"></i> Target: ${data.target_role}</p>
      </div>

      ${profileBadges ? `<div class="profile-badges">${profileBadges}</div>` : ''}

      <div class="ctc-badge">
        <i class="fas fa-coins"></i> Estimated CTC: <strong>${data.estimated_ctc}</strong>
      </div>

      <div class="result-verdict ${isPlaced ? 'verdict-placed' : 'verdict-not-placed'}">
        <i class="fas ${isPlaced ? 'fa-check-circle' : 'fa-exclamation-triangle'}"></i>
        <span>${isPlaced ? 'Placement Likely' : 'Skill Upgrade Needed'}</span>
      </div>

      <p style="color: var(--text-muted); font-size: 0.85rem;">
        Model Confidence: <strong>${data.confidence_score}%</strong> | Skill Readiness Index: <strong style="color: var(--accent-cyan);">${data.skills_score}/100</strong>
      </p>

      <div class="gauge-wrapper">
        <svg class="gauge-svg" viewBox="0 0 200 200">
          <defs>
            <linearGradient id="gauge-gradient" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" stop-color="${isPlaced ? '#00f2fe' : '#ff1744'}" />
              <stop offset="100%" stop-color="${isPlaced ? '#00e676' : '#ffea00'}" />
            </linearGradient>
          </defs>
          <circle class="gauge-bg" cx="100" cy="100" r="90" />
          <circle id="gauge-progress" class="gauge-progress" cx="100" cy="100" r="90" />
        </svg>
        <div class="gauge-center-text">
          <span class="gauge-percent" id="counter-val">0%</span>
          <span class="gauge-label">Placement Probability</span>
        </div>
      </div>

      <div class="insight-box">
        <div class="insight-title"><i class="fas fa-star" style="color: var(--accent-cyan);"></i> Profile Strengths & Skill Assets</div>
        <ul class="insight-list">
          ${data.insights.map(item => `<li class="insight-item"><i class="fas fa-shield-alt" style="color: var(--success); margin-right: 6px;"></i> ${item}</li>`).join('')}
        </ul>
      </div>

      ${data.recommendations && data.recommendations.length > 0 ? `
      <div class="insight-box" style="margin-top: 0.8rem;">
        <div class="insight-title"><i class="fas fa-lightbulb" style="color: var(--warning);"></i> Recommendations to Boost Odds</div>
        <ul class="insight-list">
          ${data.recommendations.map(item => `<li class="insight-item rec"><i class="fas fa-arrow-circle-up" style="color: var(--warning); margin-right: 6px;"></i> ${item}</li>`).join('')}
        </ul>
      </div>
      ` : ''}

      <button type="button" class="btn-export" onclick="window.print()">
        <i class="fas fa-file-pdf"></i> Save / Print Placement Assessment
      </button>
    </div>
  `;

  setTimeout(() => {
    const circle = document.getElementById('gauge-progress');
    const counter = document.getElementById('counter-val');
    if (circle && counter) {
      const circumference = 2 * Math.PI * 90;
      const offset = circumference - (prob / 100) * circumference;
      circle.style.strokeDashoffset = offset;

      let start = 0;
      const duration = 1500;
      const startTime = performance.now();

      function updateCounter(now) {
        const elapsed = now - startTime;
        const progress = Math.min(elapsed / duration, 1);
        const current = Math.floor(progress * prob);
        counter.textContent = `${current}%`;

        if (progress < 1) {
          requestAnimationFrame(updateCounter);
        } else {
          counter.textContent = `${prob.toFixed(1)}%`;
        }
      }

      requestAnimationFrame(updateCounter);
    }
  }, 100);

  if (isPlaced) {
    triggerConfetti();
  }
}

/* Canvas Confetti Effect */
function triggerConfetti() {
  const count = 60;
  for (let i = 0; i < count; i++) {
    const div = document.createElement('div');
    div.style.position = 'fixed';
    div.style.width = '8px';
    div.style.height = '8px';
    div.style.backgroundColor = ['#00f2fe', '#00e676', '#4facfe', '#7f00ff', '#ffea00'][Math.floor(Math.random() * 5)];
    div.style.left = `${Math.random() * 100}vw`;
    div.style.top = '-10px';
    div.style.borderRadius = '50%';
    div.style.pointerEvents = 'none';
    div.style.zIndex = '9999';
    div.style.transition = `all ${Math.random() * 2 + 1.5}s cubic-bezier(0.25, 0.46, 0.45, 0.94)`;

    document.body.appendChild(div);

    setTimeout(() => {
      div.style.transform = `translate(${ (Math.random() - 0.5) * 200 }px, ${ window.innerHeight + 50 }px) rotate(${ Math.random() * 720 }deg)`;
      div.style.opacity = '0';
    }, 50);

    setTimeout(() => div.remove(), 3500);
  }
}
