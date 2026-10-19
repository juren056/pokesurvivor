'use strict';
(() => {
  // Keep development and Pages preview traffic out of the production property.
  if (!['pokemonsurvivorwiki.com', 'www.pokemonsurvivorwiki.com'].includes(location.hostname)) {
    document.querySelector('[data-analytics-settings]')?.setAttribute('hidden', '');
    return;
  }
  const id = 'G-GEQDCG9L1K';
  const key = 'psw-analytics-consent-v1';
  const locale = window.WIKI_LOCALE || 'en';
  const consentCopy = {
    en: {label: 'Optional analytics', title: 'Help improve this Wiki?', body: 'Allow Google Analytics to measure page visits. Your search terms are excluded.', details: 'Privacy details', decline: 'Decline', allow: 'Allow analytics', privacy: '/privacy/'},
    es: {label: 'Analítica opcional', title: '¿Ayudas a mejorar esta wiki?', body: 'Permite que Google Analytics mida las visitas. Tus términos de búsqueda quedan excluidos.', details: 'Detalles de privacidad', decline: 'Rechazar', allow: 'Permitir analítica', privacy: '/es/privacy/'},
    it: {label: 'Statistiche facoltative', title: 'Vuoi aiutarci a migliorare la wiki?', body: 'Consenti a Google Analytics di misurare le visite. I termini cercati restano esclusi.', details: 'Dettagli sulla privacy', decline: 'Rifiuta', allow: 'Consenti statistiche', privacy: '/it/privacy/'},
    'zh-hant': {label: '選用分析資料', title: '協助改善本站？', body: '允許 Google Analytics 統計頁面瀏覽；搜尋內容不會送出。', details: '隱私權說明', decline: '拒絕', allow: '允許分析', privacy: '/zh-hant/privacy/'}
  };
  const copy = consentCopy[locale] || consentCopy.en;
  let choice = null;
  try { choice = localStorage.getItem(key); } catch (_) {}
  let started = false;
  const start = () => {
    if (navigator.globalPrivacyControl) return;
    window['ga-disable-' + id] = false;
    if (started) {
      gtag('consent', 'update', {analytics_storage: 'granted'});
      return;
    }
    started = true;
    window.dataLayer = window.dataLayer || [];
    window.gtag = function () { window.dataLayer.push(arguments); };
    gtag('consent', 'default', {analytics_storage: 'granted', ad_storage: 'denied', ad_user_data: 'denied', ad_personalization: 'denied'});
    gtag('js', new Date());
    gtag('config', id, {
      page_location: location.origin + location.pathname,
      page_referrer: document.referrer ? (() => { try { const u = new URL(document.referrer); return u.origin + u.pathname; } catch (_) { return ''; } })() : '',
      allow_google_signals: false,
      allow_ad_personalization_signals: false
    });
    const script = document.createElement('script');
    script.async = true;
    script.src = 'https://www.googletagmanager.com/gtag/js?id=' + id;
    document.head.append(script);
  };
  const panel = document.createElement('section');
  panel.className = 'analytics-choice';
  panel.setAttribute('aria-label', copy.label);
  panel.innerHTML = `<strong>${copy.title}</strong><p>${copy.body} <a href="${copy.privacy}">${copy.details}</a></p><div><button type="button" class="button secondary" data-analytics="denied">${copy.decline}</button><button type="button" class="button" data-analytics="granted">${copy.allow}</button></div>`;
  panel.hidden = choice !== null || !!navigator.globalPrivacyControl;
  document.body.append(panel);
  panel.addEventListener('click', e => {
    const button = e.target.closest('[data-analytics]');
    if (!button) return;
    choice = button.dataset.analytics;
    try { localStorage.setItem(key, choice); } catch (_) {}
    panel.hidden = true;
    if (choice === 'granted') start();
    else {
      window['ga-disable-' + id] = true;
      if (window.gtag) gtag('consent', 'update', {analytics_storage: 'denied'});
      document.cookie.split(';').forEach(c => {
        const name = c.split('=')[0].trim();
        if (!/^_ga(?:_|$)/.test(name)) return;
        for (const domain of ['', '; Domain=' + location.hostname, '; Domain=.pokemonsurvivorwiki.com']) {
          document.cookie = name + '=; Max-Age=0; Path=/' + domain + '; SameSite=Lax; Secure';
        }
      });
    }
  });
  document.querySelector('[data-analytics-settings]')?.addEventListener('click', () => {
    panel.hidden = false;
    panel.querySelector('button').focus();
  });
  const event = (name, params = {}) => {
    if (choice === 'granted' && started && window.gtag) gtag('event', name, params);
  };
  window.wikiTrack = event;
  document.addEventListener?.('click', e => {
    const link = e.target.closest('a');
    if (link?.href?.startsWith('https://pokesurvivor.com/')) event('official_game_click', {link_domain: 'pokesurvivor.com'});
    if (link?.closest('.related')) event('guide_navigation', {destination_path: new URL(link.href).pathname});
    if (e.target.closest('[data-diagnostic-run]')) event('diagnosis_complete', {tool_name: 'save_recovery'});
    if (e.target.closest('[data-report-copy]')) event('report_copy', {tool_name: 'save_recovery'});
  });
  document.querySelectorAll?.('.guide-video video').forEach(video => video.addEventListener('play', () => event('video_start', {video_id: video.closest('[data-video-id]')?.dataset.videoId || 'guide'}), {once: true}));
  if (choice === 'granted') start();
})();
