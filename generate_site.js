const fs = require('fs');
const path = require('path');

// ── CONFIGURATION ──
const locales = {
    lt: JSON.parse(fs.readFileSync('./locales/lt.json', 'utf8')),
    en: JSON.parse(fs.readFileSync('./locales/en.json', 'utf8'))
};

const template = fs.readFileSync('./src/template.html', 'utf8');

const pages = [
    { id: 'home', lt: '', en: '' },
    { id: 'services', lt: 'paslaugos/', en: 'services/' },
    { id: 'about', lt: 'apie-mus/', en: 'about/' },
    { id: 'contact', lt: 'kontaktai/', en: 'contact/' }
];

const baseUrl = 'https://cyberpunkbarbers.lt';

// ── HELPERS ──
function getTranslation(obj, keyPath) {
    return keyPath.split('.').reduce((o, i) => (o ? o[i] : null), obj);
}

function copyRecursiveSync(src, dest) {
    const exists = fs.existsSync(src);
    const stats = exists && fs.statSync(src);
    const isDirectory = exists && stats.isDirectory();
    if (isDirectory) {
        if (!fs.existsSync(dest)) fs.mkdirSync(dest, { recursive: true });
        fs.readdirSync(src).forEach(childItemName => {
            copyRecursiveSync(path.join(src, childItemName), path.join(dest, childItemName));
        });
    } else {
        fs.copyFileSync(src, dest);
    }
}

function translateHtml(html, langData) {
    // 1. First, handle the simple one-line translations
    let updatedHtml = html.replace(/data-i18n="([^"]+)"([^>]*>)([^<]*)/g, (match, key, rest, existingContent) => {
        const translation = getTranslation(langData, key);
        // Only replace if it's the simple case (no nested tags indicated by the original regex)
        // If the key is for a bio, we skip it here and handle it in step 2
        if (key.includes('.bio')) return match; 
        return `data-i18n="${key}"${rest}${translation || existingContent}`;
    });

    // 2. Specifically handle the complex "bio" blocks with nested HTML
    // We look for the data-i18n attribute and match until the closing </div>
    updatedHtml = updatedHtml.replace(/data-i18n="(barbersDesc\.[^.]+\.bio)"([^>]*>)([\s\S]*?)(?=<\/div>)/g, (match, key, rest, existingContent) => {
        const translation = getTranslation(langData, key);
        return `data-i18n="${key}"${rest}${translation || existingContent}`;
    });

    return updatedHtml;
}

function generateSchema(lang, pageId) {
    // Simple LocalBusiness schema
    return `
    <script type="application/ld+json">
    {
      "@context": "https://schema.org",
      "@type": "BarberShop",
      "name": "Cyberpunk Barbers",
      "image": "${baseUrl}/assets/og-image.jpg",
      "@id": "${baseUrl}/${lang}/${pages.find(p => p.id === pageId)[lang]}",
      "url": "${baseUrl}/${lang}/${pages.find(p => p.id === pageId)[lang]}",
      "telephone": "+37000000000",
      "address": {
        "@type": "PostalAddress",
        "streetAddress": "Švitrigailos g. 36",
        "addressLocality": "Vilnius",
        "postalCode": "03228",
        "addressCountry": "LT"
      },
      "geo": {
        "@type": "GeoCoordinates",
        "latitude": 54.6738,
        "longitude": 25.2635
      },
      "openingHoursSpecification": [
        {
          "@type": "OpeningHoursSpecification",
          "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
          "opens": "10:00",
          "closes": "20:00"
        },
        {
          "@type": "OpeningHoursSpecification",
          "dayOfWeek": "Saturday",
          "opens": "10:00",
          "closes": "18:00"
        }
      ]
    }
    </script>`;
}

// ── GENERATION ──
pages.forEach(page => {
    ['lt', 'en'].forEach(lang => {
        let content = template;
        const langData = locales[lang];
        const seo = langData.seo[page.id];
        const otherLang = lang === 'lt' ? 'en' : 'lt';

        // 1. Calculate relative paths
        const depth = page[lang].split('/').filter(Boolean).length + 1; // +1 for the lang dir
        const assetPath = '../'.repeat(depth);
        content = content.replace(/{{ASSET_PATH}}/g, assetPath);

        // 2. Static SEO Tags
        content = content.replace('{{LANG}}', lang);
        content = content.replace('{{TITLE}}', seo.title);
        content = content.replace('{{DESCRIPTION}}', seo.description);
        content = content.replace('{{CANONICAL}}', `<link rel="canonical" href="${baseUrl}${seo.canonical}">`);
        
        // 3. Hreflang Tags
        const hreflang = `
    <link rel="alternate" hreflang="lt" href="${baseUrl}/lt/${pages.find(p => p.id === page.id).lt}">
    <link rel="alternate" hreflang="en" href="${baseUrl}/en/${pages.find(p => p.id === page.id).en}">
    <link rel="alternate" hreflang="x-default" href="${baseUrl}/lt/">`;
        content = content.replace('{{HREFLANG}}', hreflang.trim());

        // 4. OG Tags
        const ogTags = `
    <meta property="og:title" content="${seo.title}">
    <meta property="og:description" content="${seo.description}">
    <meta property="og:url" content="${baseUrl}${seo.canonical}">
    <meta property="og:type" content="${langData.seo.og.type}">
    <meta property="og:image" content="${baseUrl}${langData.seo.og.image}">
    <meta property="og:locale" content="${langData.seo.og.locale}">`;
        content = content.replace('{{OG_TAGS}}', ogTags.trim());

        // 5. Schema
        content = content.replace('{{SCHEMA}}', generateSchema(lang, page.id));

        // 6. Navigation Paths (Relative)
        pages.forEach(p => {
            const placeholder = `{{PATH_${p.id.toUpperCase()}}}`;
            const targetPath = `${assetPath}${lang}/${p[lang]}`;
            content = content.replace(new RegExp(placeholder, 'g'), targetPath);
        });

        // 7. Translation Injection
        content = translateHtml(content, langData);

        // 8. Language Switcher Logic (Relative Redirection)
        const switchLogic = `
        function switchLanguageLocally(targetLang) {
            const currentLang = '${lang}';
            if (targetLang === currentLang) return;
            const pageMap = ${JSON.stringify(pages.find(p => p.id === page.id))};
            // For the language switcher, we use the root redirect approach
            window.location.href = '/' + targetLang + '/' + pageMap[targetLang];
        }`;
        content = content.replace('// SWITCH_LOGIC_PLACEHOLDER', switchLogic);

        // 9. Write File
        const dir = path.join('./dist', lang, page[lang]);
        fs.mkdirSync(dir, { recursive: true });
        fs.writeFileSync(path.join(dir, 'index.html'), content);
        
        console.log(`Generated: ${lang}/${page[lang]}index.html`);
    });
});

// Generate root index.html (redirect to /lt/)
const rootIndex = `<!DOCTYPE html><html><head><meta http-equiv="refresh" content="0; url=/lt/"></head></html>`;
fs.writeFileSync('./dist/index.html', rootIndex);

// ── POST-PROCESSING ──
// 1. Copy Assets & Videos
['assets', 'Videos'].forEach(dir => {
    if (fs.existsSync(dir)) {
        console.log(`Copying directory: ${dir}`);
        copyRecursiveSync(dir, path.join('./dist', dir));
    }
});

// 2. Copy Global Media (Favicon, Barbers, Hero videos)
fs.readdirSync('.').forEach(file => {
    if (file.match(/\.(jpg|png|mp4)$/i)) {
        console.log(`Copying media file: ${file}`);
        fs.copyFileSync(file, path.join('./dist', file));
    }
});

console.log('Site generation complete!');
