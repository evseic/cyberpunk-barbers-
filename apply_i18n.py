import re
import codecs

def run():
    with codecs.open('index.html', 'r', 'utf-8') as f:
        html = f.read()

    # 1. Add CSS
    css_to_add = """
  .lang-switch { display: flex; gap: 8px; align-items: center; border-left: 1px solid var(--c-border); padding-left: 20px; margin-left: -16px; }
  .lang-btn { background: none; border: none; color: var(--c-muted); font-family: var(--font-mono); font-size: 11px; cursor: pointer; transition: color 0.2s; padding: 0; }
  .lang-btn.active { color: var(--c-primary); font-weight: bold; }
  .lang-btn:hover { color: var(--c-text); }
  .ig-link { color: var(--c-muted); transition: color 0.2s; display: inline-flex; align-items: center; margin-left: 12px; }
  .ig-link:hover { color: var(--c-primary); }
  @media (max-width: 768px) {
    .lang-switch { border: none; padding: 0; margin: 0; }
    .lang-btn { font-size: 14px; }
  }
"""
    if '.lang-switch' not in html:
        html = html.replace("  /* ── HAMBURGER ── */", css_to_add + "  /* ── HAMBURGER ── */")

    # 2. Add Lang Switch to Desktop Nav
    if 'data-lang="lt"' not in html:
        nav_insert = """
    <div class="lang-switch">
      <button class="lang-btn active" data-lang="lt" onclick="setLanguage('lt')">LT</button>
      <button class="lang-btn" data-lang="en" onclick="setLanguage('en')">EN</button>
    </div>
"""
        html = re.sub(r'(<a[^>]*class="btn-primary"[^>]*>.*?</a\s*>)\s*(\n\s*</nav>)', r'\n    \1' + nav_insert + r'\2', html)

        mob_nav_insert = """
  <div class="lang-switch" style="border:none; padding:0; margin:0; gap: 16px;">
    <button class="lang-btn active" style="font-size:18px;" data-lang="lt" onclick="setLanguage('lt')">LT</button>
    <button class="lang-btn" style="font-size:18px;" data-lang="en" onclick="setLanguage('en')">EN</button>
  </div>
"""
        html = re.sub(r'(<a[^>]*class="btn-primary"[^>]*onclick="toggleMenu\(\)"[^>]*>.*?</a\s*>)\s*(\n\s*</div>)', r'\n  \1' + mob_nav_insert + r'\2', html)

    # 3. Add IG Links and data-i18n attributes
    # Nav
    html = html.replace('href="#barbers">Barbers</a>', 'href="#barbers" data-i18n="nav.barbers">Barbers</a>')
    html = html.replace('href="#services">Services</a>', 'href="#services" data-i18n="nav.services">Services</a>')
    html = html.replace('href="#gallery">Gallery</a>', 'href="#gallery" data-i18n="nav.gallery">Gallery</a>')
    html = html.replace('href="#reviews">Reviews</a>', 'href="#reviews" data-i18n="nav.reviews">Reviews</a>')
    html = html.replace('class="btn-primary">Book Now</a>', 'class="btn-primary" data-i18n="nav.book">Book Now</a>')
    html = html.replace('onclick="toggleMenu()">Barbers</a>', 'onclick="toggleMenu()" data-i18n="nav.barbers">Barbers</a>')
    html = html.replace('onclick="toggleMenu()">Services</a>', 'onclick="toggleMenu()" data-i18n="nav.services">Services</a>')
    html = html.replace('onclick="toggleMenu()">Gallery</a>', 'onclick="toggleMenu()" data-i18n="nav.gallery">Gallery</a>')
    html = html.replace('onclick="toggleMenu()">Reviews</a>', 'onclick="toggleMenu()" data-i18n="nav.reviews">Reviews</a>')
    html = html.replace('onclick="toggleMenu()">Book Appointment</a>', 'onclick="toggleMenu()" data-i18n="nav.bookMobile">Book Appointment</a>')

    # Hero
    html = html.replace('class="hero-eyebrow">Established 2024', 'class="hero-eyebrow" data-i18n="hero.eyebrow">Established 2024')
    html = html.replace('class="hero-title">YOU DON\'T JUST GET A</div>', 'class="hero-title" data-i18n="hero.title1">YOU DON\'T JUST GET A</div>')
    html = html.replace('class="hero-title-accent">HAIRCUT HERE.</div>', 'class="hero-title-accent" data-i18n="hero.title2">HAIRCUT HERE.</div>')
    html = html.replace('class="hero-sub">You get the whole upgrade', 'class="hero-sub" data-i18n="hero.sub">You get the whole upgrade')
    html = html.replace('class="btn-primary">Book Appointment</a>', 'class="btn-primary" data-i18n="hero.ctaBook">Book Appointment</a>')
    html = html.replace('class="btn-outline">See The Vibe</a>', 'class="btn-outline" data-i18n="hero.ctaSee">See The Vibe</a>')
    html = html.replace('<span>Scroll</span>', '<span data-i18n="hero.scroll">Scroll</span>')

    # Ticker
    for i, t in enumerate(["Precision Cuts", "Sculpted Beards", "Premium Experience", "Vilnius' Finest", "Book Today", "Fade Specialists", "Hot Towel Treatment", "Since 2024"]):
        html = html.replace(f'<div class="ticker-item">{t}</div>', f'<div class="ticker-item" data-i18n="ticker.item{i+1}">{t}</div>')

    # Stats
    html = html.replace('class="counter-label">Cuts Done</div>', 'class="counter-label" data-i18n="stats.cutsDone">Cuts Done</div>')
    html = html.replace('class="counter-label">Satisfaction Rate</div>', 'class="counter-label" data-i18n="stats.satisfaction">Satisfaction Rate</div>')
    html = html.replace('class="counter-label">Master Barbers</div>', 'class="counter-label" data-i18n="stats.masterBarbers">Master Barbers</div>')
    html = html.replace('class="counter-label">Location — Vilnius</div>', 'class="counter-label" data-i18n="stats.location">Location — Vilnius</div>')

    # Barbers
    html = html.replace('class="section-eyebrow">The Crew</div>', 'class="section-eyebrow" data-i18n="barbersHeader.eyebrow">The Crew</div>')
    html = html.replace('class="section-title">MEET THE<br><em>OPERATIVES</em></h2>', 'class="section-title"><span data-i18n="barbersHeader.title1">MEET THE</span><br><em data-i18n="barbersHeader.title2">OPERATIVES</em></h2>')
    html = html.replace('class="section-sub">Six distinct personalities.', 'class="section-sub" data-i18n="barbersHeader.sub">Six distinct personalities.')

    # Exact Barbers mapping:
    # NEDAS
    html = html.replace('class="barber-role" style="color: var(--c-primary);">Senior Barber</div>', 'class="barber-role" style="color: var(--c-primary);" data-i18n="barbersDesc.nedas.role">Senior Barber</div>')
    html = html.replace('class="barber-desc">Always sharp, always on point. Nedas gets the details right every time.</div>', 'class="barber-desc" data-i18n="barbersDesc.nedas.short">Always sharp, always on point. Nedas gets the details right every time.</div>')
    html = html.replace('>Book with Nedas</a>', ' data-i18n="barbersDesc.nedas.book">Book with Nedas</a>\n          <a href="https://www.instagram.com/nedasbarber/" target="_blank" class="ig-link"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="2" y="2" width="20" height="20" rx="5" ry="5"></rect><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"></path><line x1="17.5" y1="6.5" x2="17.51" y2="6.5"></line></svg></a>')

    # DENIS
    html = html.replace('class="barber-role" style="color: var(--c-secondary);">Style Engineer</div>', 'class="barber-role" style="color: var(--c-secondary);" data-i18n="barbersDesc.denis.role">Style Engineer</div>')
    html = html.replace('class="barber-desc">Brings the energy and the finest fades. Denis knows exactly what suits you.</div>', 'class="barber-desc" data-i18n="barbersDesc.denis.short">Brings the energy and the finest fades. Denis knows exactly what suits you.</div>')
    html = html.replace('>Book with Denis</a>', ' data-i18n="barbersDesc.denis.book">Book with Denis</a>\n          <a href="https://www.instagram.com/denio.laboratory/" target="_blank" class="ig-link"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="2" y="2" width="20" height="20" rx="5" ry="5"></rect><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"></path><line x1="17.5" y1="6.5" x2="17.51" y2="6.5"></line></svg></a>')

    # ERIKAS
    html = html.replace('class="barber-role" style="color: var(--c-tertiary);">Precision Specialist</div>', 'class="barber-role" style="color: var(--c-tertiary);" data-i18n="barbersDesc.erikas.role">Precision Specialist</div>')
    html = html.replace('class="barber-desc">Clean lines and classic cuts. Erikas executes the craft with pure focus.</div>', 'class="barber-desc" data-i18n="barbersDesc.erikas.short">Clean lines and classic cuts. Erikas executes the craft with pure focus.</div>')
    html = html.replace('>Book with Erikas</a>', ' data-i18n="barbersDesc.erikas.book">Book with Erikas</a>\n          <a href="https://www.instagram.com/evseicik/" target="_blank" class="ig-link"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="2" y="2" width="20" height="20" rx="5" ry="5"></rect><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"></path><line x1="17.5" y1="6.5" x2="17.51" y2="6.5"></line></svg></a>')

    # VLAD
    html = html.replace('class="barber-role" style="color: var(--c-primary);">Detail Master</div>', 'class="barber-role" style="color: var(--c-primary);" data-i18n="barbersDesc.vlad.role">Detail Master</div>')
    html = html.replace('class="barber-desc">Quiet precision. Vlad lets the results speak for themselves.</div>', 'class="barber-desc" data-i18n="barbersDesc.vlad.short">Quiet precision. Vlad lets the results speak for themselves.</div>')
    html = html.replace('>Book with Vlad</a>', ' data-i18n="barbersDesc.vlad.book">Book with Vlad</a>\n          <a href="https://www.instagram.com/vlad.arh/" target="_blank" class="ig-link"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="2" y="2" width="20" height="20" rx="5" ry="5"></rect><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"></path><line x1="17.5" y1="6.5" x2="17.51" y2="6.5"></line></svg></a>')

    # MARTYNAS
    html = html.replace('class="barber-role" style="color: var(--c-secondary);">Creative Lead</div>', 'class="barber-role" style="color: var(--c-secondary);" data-i18n="barbersDesc.martynas.role">Creative Lead</div>')
    html = html.replace('class="barber-desc">Next-level scissor work. Martynas turns every cut into a masterpiece.</div>', 'class="barber-desc" data-i18n="barbersDesc.martynas.short">Next-level scissor work. Martynas turns every cut into a masterpiece.</div>')
    html = html.replace('>Book with Martynas</a>', ' data-i18n="barbersDesc.martynas.book">Book with Martynas</a>\n          <a href="https://www.instagram.com/martynas_balaika/" target="_blank" class="ig-link"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="2" y="2" width="20" height="20" rx="5" ry="5"></rect><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"></path><line x1="17.5" y1="6.5" x2="17.51" y2="6.5"></line></svg></a>')

    # EVALDAS
    html = html.replace('class="barber-role" style="color: var(--c-tertiary);">Classic Specialist</div>', 'class="barber-role" style="color: var(--c-tertiary);" data-i18n="barbersDesc.evaldas.role">Classic Specialist</div>')
    html = html.replace('class="barber-desc">Old school craft meets modern edge. Good vibes guaranteed.</div>', 'class="barber-desc" data-i18n="barbersDesc.evaldas.short">Old school craft meets modern edge. Good vibes guaranteed.</div>')
    html = html.replace('>Book with Evaldas</a>', ' data-i18n="barbersDesc.evaldas.book">Book with Evaldas</a>\n          <a href="https://www.instagram.com/aktyvus/" target="_blank" class="ig-link"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="2" y="2" width="20" height="20" rx="5" ry="5"></rect><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"></path><line x1="17.5" y1="6.5" x2="17.51" y2="6.5"></line></svg></a>')

    # Bios
    html = re.sub(r'(<div class="barber-modal-desc" style="display: none;">).*?(</div>)', r'\1\n            <!-- Translated Bio goes here securely -->\n          \2', html, flags=re.DOTALL)

    # Services
    html = html.replace('class="section-eyebrow">What We Do</div>', 'class="section-eyebrow" data-i18n="services.eyebrow">What We Do</div>')
    html = html.replace('class="section-title">THE<br><em>MENU</em></h2>', 'class="section-title"><span data-i18n="services.title1">THE</span><br><em data-i18n="services.title2">MENU</em></h2>')
    html = html.replace('class="section-sub">No complicated packages', 'class="section-sub" data-i18n="services.sub">No complicated packages')

    html = html.replace('class="service-badge">Most Popular</div>', 'class="service-badge" data-i18n="services.cards.1.badge">Most Popular</div>')
    html = html.replace('class="service-name">PRECISION CUT</div>', 'class="service-name" data-i18n="services.cards.1.name">PRECISION CUT</div>')
    html = html.replace('class="service-desc">Custom fade, wash, and style tailored to your skull structure, face shape, and lifestyle.</p>', 'class="service-desc" data-i18n="services.cards.1.desc">Custom fade, wash, and style tailored to your skull structure, face shape, and lifestyle.</p>')
    html = html.replace('class="service-duration">45 MIN</span>', 'class="service-duration" data-i18n="services.cards.1.duration">45 MIN</span>')
    html = html.replace('class="service-price">from 30 EUR</span>', 'class="service-price" data-i18n="services.cards.1.price">from 30 EUR</span>')

    html = html.replace('class="service-name">SCULPTED BEARD</div>', 'class="service-name" data-i18n="services.cards.2.name">SCULPTED BEARD</div>')
    html = html.replace('class="service-desc">Hot towel treatment, precision line-up, and oil infusion. We shape what you\'ve got into something you\'re proud to wear.</p>', 'class="service-desc" data-i18n="services.cards.2.desc">Hot towel treatment, precision line-up, and oil infusion. We shape what you\'ve got into something you\'re proud to wear.</p>')
    html = html.replace('class="service-duration">30 MIN</span>', 'class="service-duration" data-i18n="services.cards.2.duration">30 MIN</span>')
    html = html.replace('class="service-price">from 25 EUR</span>', 'class="service-price" data-i18n="services.cards.2.price">from 25 EUR</span>')

    html = html.replace('class="service-name">CYBER COMBO</div>', 'class="service-name" data-i18n="services.cards.3.name">CYBER COMBO</div>')
    html = html.replace('class="service-desc">Full haircut plus beard sculpt. Walk in looking like a draft, leave looking like the final version.</p>', 'class="service-desc" data-i18n="services.cards.3.desc">Full haircut plus beard sculpt. Walk in looking like a draft, leave looking like the final version.</p>')
    html = html.replace('class="service-duration">75 MIN</span>', 'class="service-duration" data-i18n="services.cards.3.duration">75 MIN</span>')
    html = html.replace('class="service-price">from 45 EUR</span>', 'class="service-price" data-i18n="services.cards.3.price">from 45 EUR</span>')

    html = html.replace('class="service-cta">Book This Service</a>', 'class="service-cta" data-i18n="services.cta">Book This Service</a>')

    # Gallery
    html = html.replace('class="section-eyebrow">The Vibe</div>', 'class="section-eyebrow" data-i18n="gallery.eyebrow">The Vibe</div>')
    html = html.replace('class="section-title">FEEL IT<br><em>BEFORE YOU COME</em></h2>', 'class="section-title"><span data-i18n="gallery.title1">FEEL IT</span><br><em data-i18n="gallery.title2">BEFORE YOU COME</em></h2>')
    html = html.replace('class="section-sub">The kind of place you want to stay a bit longer.</p>', 'class="section-sub" data-i18n="gallery.sub">The kind of place you want to stay a bit longer.</p>')
    html = html.replace('class="gallery-label">Interior Atmosphere</span>', 'class="gallery-label" data-i18n="gallery.labels.interior">Interior Atmosphere</span>')
    html = html.replace('class="gallery-label">ENJOY</span>', 'class="gallery-label" data-i18n="gallery.labels.craft">ENJOY</span>')
    html = html.replace('class="gallery-label">Detail & Craft</span>', 'class="gallery-label" data-i18n="gallery.labels.vibe">Detail & Craft</span>')
    html = html.replace('class="gallery-label">LOGO</span>', 'class="gallery-label" data-i18n="gallery.labels.interior">LOGO</span>')

    # Reviews & Booking
    html = html.replace('class="section-eyebrow">What They Say</div>', 'class="section-eyebrow" data-i18n="reviews.eyebrow">What They Say</div>')
    html = html.replace('class="section-title">REAL TALK<br><em>FROM THE CHAIR</em></h2>', 'class="section-title"><span data-i18n="reviews.title1">REAL TALK</span><br><em data-i18n="reviews.title2">FROM THE CHAIR</em></h2>')
    html = html.replace('class="section-sub">We let the clients do the talking.</p>', 'class="section-sub" data-i18n="reviews.sub">We let the clients do the talking.</p>')
    html = html.replace('Verify on Treatwell ↗</div>', '<span data-i18n="reviews.badgeText">Verify on Treatwell ↗</span></div>')

    html = html.replace('class="section-eyebrow">Secure the Spot</div>', 'class="section-eyebrow" data-i18n="booking.eyebrow">Secure the Spot</div>')
    html = html.replace('class="section-title">YOUR UPGRADE<br><em>AWAITS</em></h2>', 'class="section-title"><span data-i18n="booking.title1">YOUR UPGRADE</span><br><em data-i18n="booking.title2">AWAITS</em></h2>')
    html = html.replace('class="section-sub">No more waiting around.', 'class="section-sub" data-i18n="booking.sub">No more waiting around.')
    html = html.replace('class="btn-primary" style="padding: 24px 48px; font-size: 14px;">Book on Treatwell</a>', 'class="btn-primary" style="padding: 24px 48px; font-size: 14px;" data-i18n="booking.cta">Book on Treatwell</a>')

    # Footer & Cookie
    html = html.replace('<p style="color: var(--c-muted); line-height: 1.7;">Not just a haircut. An experience.<br>Come curious, leave upgraded.<br>Vilnius\' premier atmosphere-first barbershop.</p>', '<p style="color: var(--c-muted); line-height: 1.7;" data-i18n="footer.tagline">Not just a haircut. An experience.<br>Come curious, leave upgraded.<br>Vilnius\' premier atmosphere-first barbershop.</p>')
    html = html.replace('<div class="footer-title">Navigate</div>', '<div class="footer-title" data-i18n="footer.colNavigate">Navigate</div>')
    html = html.replace('<div class="footer-title">Hours</div>', '<div class="footer-title" data-i18n="footer.colHours">Hours</div>')
    html = html.replace('Mon – Fri: 10:00 – 20:00<br>', '<span data-i18n="footer.hours1">Mon – Fri: 10:00 – 20:00</span><br>')
    html = html.replace('Saturday: 10:00 – 18:00<br>', '<span data-i18n="footer.hours2">Saturday: 10:00 – 18:00</span><br>')
    html = html.replace('Sunday: Closed', '<span data-i18n="footer.hours3">Sunday: Closed</span>')
    html = html.replace('<div class="footer-title">Location</div>', '<div class="footer-title" data-i18n="footer.colLocation">Location</div>')
    html = html.replace('Švitrigailos g. 36<br>', '<span data-i18n="footer.loc1">Švitrigailos g. 36</span><br>')
    html = html.replace('Vilnius, LT-03228<br>', '<span data-i18n="footer.loc2">Vilnius, LT-03228</span><br>')
    html = html.replace('Lithuania', '<span data-i18n="footer.loc3">Lithuania</span>')

    # JS I18n Engine
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
    if (translation && translation !== el.getAttribute('data-i18n')) {
        el.innerHTML = translation;
    }
  });

  // Dynamic modal injection wrapper
  document.querySelectorAll('.barber-card').forEach(card => {
    const name = card.querySelector('.barber-name').innerText.trim().toLowerCase();
    const modalDesc = card.querySelector('.barber-modal-desc');
    if (modalDesc && i18nData.barbersDesc && i18nData.barbersDesc[name]) {
       modalDesc.innerHTML = i18nData.barbersDesc[name].bio;
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

// Start I18n as early as possible
initI18n();
"""
    if 'let currentLang =' not in html:
        html = html.replace("window.addEventListener('DOMContentLoaded', checkCookies);", js_engine + "\nwindow.addEventListener('DOMContentLoaded', checkCookies);")

    with codecs.open('index.html', 'w', 'utf-8') as f:
        f.write(html)

if __name__ == '__main__':
    run()
