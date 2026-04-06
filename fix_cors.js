const fs = require('fs');

const en = fs.readFileSync('locales/en.json', 'utf-8');
const lt = fs.readFileSync('locales/lt.json', 'utf-8');

let html = fs.readFileSync('index.html', 'utf-8');

const newScript = `
// ── I18N SYSTEM ──
const SITE_TRANSLATIONS = {
  "en": ${en},
  "lt": ${lt}
};

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
`;

// regex to replace the old block natively
const oldBlockRegex = /\/\/ ── I18N SYSTEM ──[\s\S]*?async function loadTranslations\(lang\) \{[\s\S]*?catch \(e\) \{[\s\S]*?\}[\s\S]*?\}/g;

html = html.replace(oldBlockRegex, newScript.trim());

fs.writeFileSync('index.html', html, 'utf-8');
console.log('CORS Patch Complete.');
