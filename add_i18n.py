import re
import codecs

with codecs.open('index.html', 'r', 'utf-8') as f:
    content = f.read()

# 1. Add CSS for Lang Switch & IG
css_to_add = """
  .lang-switch { display: flex; gap: 8px; align-items: center; border-left: 1px solid var(--c-border); padding-left: 20px; margin-left: -16px; }
  .lang-btn { background: none; border: none; color: var(--c-muted); font-family: var(--font-mono); font-size: 11px; cursor: pointer; transition: color 0.2s; padding: 0; }
  .lang-btn.active { color: var(--c-primary); font-weight: bold; }
  .lang-btn:hover { color: var(--c-text); }
  .ig-link { color: var(--c-muted); transition: color 0.2s; display: flex; align-items: center; }
  .ig-link:hover { color: var(--c-primary); }
"""
content = content.replace("  /* ── HAMBURGER ── */", css_to_add + "\n  /* ── HAMBURGER ── */")

# 2. Add Lang Switch to Nav
nav_insert = """
    <div class="lang-switch">
      <button class="lang-btn active" data-lang="lt" onclick="setLanguage('lt')">LT</button>
      <button class="lang-btn" data-lang="en" onclick="setLanguage('en')">EN</button>
    </div>
"""
content = re.sub(r'(<a href="https://www.treatwell.lt/salonas/cyberpunk-barbers/"[^>]*>Book Now</a>\s*)</nav>', r'\1' + nav_insert + r'  </nav>', content)

# Mobile Nav Lang switch
mob_nav_insert = """
  <div class="lang-switch" style="border:none; padding:0; margin:0; gap: 16px;">
    <button class="lang-btn active" style="font-size:18px;" data-lang="lt" onclick="setLanguage('lt')">LT</button>
    <button class="lang-btn" style="font-size:18px;" data-lang="en" onclick="setLanguage('en')">EN</button>
  </div>
"""
content = re.sub(r'(onclick="toggleMenu\(\)">[^\<]+</a>\s*</div>)', mob_nav_insert + r'\1', content)

# 3. Add JS Engine at end
js_engine = """
// ── I18N SYSTEM ──
let currentLang = localStorage.getItem('lang') || 'lt';
let i18nData = {};

async function initI18n() {
  document.documentElement.lang = currentLang;
  await loadTranslations(currentLang);
}

async function loadTranslations(lang) {
  try {
    const res = await fetch(`locales/${lang}.json`);
    i18nData = await res.json();
    populateTranslations();
    updateLangButtons();
  } catch (e) {
    console.error('Failed to load translations', e);
  }
}

function t(keyPath) {
  return keyPath.split('.').reduce((o, i) => (o ? o[i] : null), i18nData) || keyPath;
}

function populateTranslations() {
  document.querySelectorAll('[data-i18n]').forEach(el => {
    const translation = t(el.getAttribute('data-i18n'));
    if (translation !== el.getAttribute('data-i18n')) {
        el.innerHTML = translation;
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

window.setLanguage = async function(lang) {
  if (lang === currentLang) return;
  currentLang = lang;
  localStorage.setItem('lang', lang);
  document.documentElement.lang = lang;
  updateLangButtons();
  await loadTranslations(lang);
};

document.addEventListener('DOMContentLoaded', initI18n);
"""
content = content.replace("window.addEventListener('DOMContentLoaded', checkCookies);", js_engine + "\nwindow.addEventListener('DOMContentLoaded', checkCookies);")

with codecs.open('index_modified.html', 'w', 'utf-8') as f:
    f.write(content)
print("Done Phase 1")
