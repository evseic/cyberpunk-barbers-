const fs = require('fs');
const path = require('path');

let html = fs.readFileSync('index.html', 'utf-8');

// Read Translation Files
const en = JSON.parse(fs.readFileSync(path.join(__dirname, 'locales/en.json'), 'utf-8'));
const lt = JSON.parse(fs.readFileSync(path.join(__dirname, 'locales/lt.json'), 'utf-8'));

const SITE_TRANSLATIONS = { en, lt };

// 1. Ticker
const tickerMatches = ["Precision Cuts", "Sculpted Beards", "Premium Experience", "Vilnius' Finest", "Book Today", "Fade Specialists", "Hot Towel Treatment", "Since 2024"];
tickerMatches.forEach((t, i) => {
  if (!html.includes(`data-i18n="ticker.item${i+1}"`)) {
    html = html.replace(`<div class="ticker-item">${t}</div>`, `<div class="ticker-item" data-i18n="ticker.item${i+1}">${t}</div>`);
  }
});

// 2. Stats
const stats = [
  { text: 'Cuts Done', key: 'stats.cutsDone' },
  { text: 'Satisfaction Rate', key: 'stats.satisfaction' },
  { text: 'Master Barbers', key: 'stats.masterBarbers' },
  { text: 'Location — Vilnius', key: 'stats.location' }
];
stats.forEach(s => {
  if (!html.includes(`data-i18n="${s.key}"`)) {
    html = html.replace(`class="counter-label">${s.text}</div>`, `class="counter-label" data-i18n="${s.key}">${s.text}</div>`);
  }
});

// 3. BarbersHeader (Idempotent Replacement)
html = html.replace('<div class="section-eyebrow">The Crew</div>', '<div class="section-eyebrow" data-i18n="barbersHeader.eyebrow">The Crew</div>');

// 4. Barbers Descriptions (Idempotent)
const barbers = [
  { id: 'nedas', name: 'NEDAS', ig: 'https://www.instagram.com/nedasbarber/' },
  { id: 'denis', name: 'DENIS', ig: 'https://www.instagram.com/denio.laboratory/' },
  { id: 'erikas', name: 'ERIKAS', ig: 'https://www.instagram.com/evseicik/' },
  { id: 'vlad', name: 'VLAD', ig: 'https://www.instagram.com/vlad.arh/' },
  { id: 'martynas', name: 'MARTYNAS', ig: 'https://www.instagram.com/martynas_balaika/' },
  { id: 'evaldas', name: 'EVALDAS', ig: 'https://www.instagram.com/aktyvus/' },
];

barbers.forEach(b => {
  if (!html.includes(`data-i18n="barbersDesc.${b.id}.book"`)) {
    const bookRegex = new RegExp(`>Book with ${b.name.charAt(0) + b.name.slice(1).toLowerCase()}</a>`, 'g');
    html = html.replace(bookRegex, ` data-i18n="barbersDesc.${b.id}.book">Book with ${b.name.charAt(0) + b.name.slice(1).toLowerCase()}</a>\n          <a href="${b.ig}" target="_blank" class="ig-link"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="2" y="2" width="20" height="20" rx="5" ry="5"></rect><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"></path><line x1="17.5" y1="6.5" x2="17.51" y2="6.5"></line></svg></a>`);
  }
});

// 5. Services Header (Idempotent)
html = html.replace('<div class="section-eyebrow">What We Do</div>', '<div class="section-eyebrow" data-i18n="services.eyebrow">What We Do</div>');

// Prepare Inlined Script
const jsEngineStart = '<!-- I18N ENGINE START -->';
const jsEngineEnd = '<!-- I18N ENGINE END -->';

const jsEngine = `
${jsEngineStart}
<script>
// ── I18N SYSTEM ──
const SITE_TRANSLATIONS = ${JSON.stringify(SITE_TRANSLATIONS, null, 2)};

let currentLang = localStorage.getItem('lang') || 'lt';
let i18nData = SITE_TRANSLATIONS[currentLang] || SITE_TRANSLATIONS['lt'];

function initI18n() {
  document.documentElement.lang = currentLang;
  loadTranslations(currentLang);
}

function loadTranslations(lang) {
  i18nData = SITE_TRANSLATIONS[lang] || SITE_TRANSLATIONS['lt'];
  populateTranslations();
  updateLangButtons();
}

function t(keyPath) {
  return keyPath.split('.').reduce((o, i) => (o ? o[i] : null), i18nData) || null;
}

function populateTranslations() {
  // Update standard elements with data-i18n attribute
  document.querySelectorAll('[data-i18n]').forEach(el => {
    const key = el.getAttribute('data-i18n');
    const translation = t(key);
    if (translation && translation !== key) {
        el.innerHTML = translation;
    }
  });

  // Specifically handle the biographies in the barber cards/modal
  document.querySelectorAll('.barber-card').forEach(card => {
    const nameEl = card.querySelector('.barber-name');
    if (!nameEl) return;
    const nameStr = nameEl.innerText.trim().toLowerCase();
    const modalDesc = card.querySelector('.barber-modal-desc');
    // The bios are stored in i18nData.barbersDesc[nameStr].bio
    if (modalDesc && i18nData.barbersDesc && i18nData.barbersDesc[nameStr]) {
       modalDesc.innerHTML = i18nData.barbersDesc[nameStr].bio;
    }
  });
}

function updateLangButtons() {
  document.querySelectorAll('.lang-btn').forEach(btn => {
    if(btn.dataset.lang === currentLang) {
      btn.classList.add('active');
    } else {
      btn.classList.remove('active');
    }
  });
}

window.setLanguage = function(lang) {
  if (lang === currentLang) return;
  currentLang = lang;
  localStorage.setItem('lang', lang);
  document.documentElement.lang = lang;
  updateLangButtons();
  loadTranslations(lang);
};

// Also handle the dynamic content refresh if the modal is currently open
function refreshActiveModal() {
  const modal = document.getElementById('barber-modal');
  if (modal && modal.classList.contains('active')) {
    const activeName = document.getElementById('modal-name').textContent.toLowerCase();
    if (i18nData.barbersDesc && i18nData.barbersDesc[activeName]) {
       document.getElementById('modal-desc').innerHTML = i18nData.barbersDesc[activeName].bio;
       document.getElementById('modal-role').textContent = i18nData.barbersDesc[activeName].role;
    }
  }
}

// Intercept window.setLanguage to also refresh modal
const originalSetLanguage = window.setLanguage;
window.setLanguage = function(lang) {
  originalSetLanguage(lang);
  refreshActiveModal();
};

initI18n();
</script>
${jsEngineEnd}
`;

// Replace or Append the I18N Engine
if (html.includes(jsEngineStart)) {
  const markerRegex = new RegExp(`${jsEngineStart}[\\s\\S]*?${jsEngineEnd}`, 'g');
  html = html.replace(markerRegex, jsEngine.trim());
} else {
  html = html.replace('</body>', jsEngine.trim() + '\n</body>');
}

fs.writeFileSync('index.html', html, 'utf-8');
console.log('Update Complete: Translations Inlined.');
