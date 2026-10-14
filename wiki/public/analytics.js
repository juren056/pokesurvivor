'use strict';
(() => {
  // Keep development and Pages preview traffic out of the production property.
  if (!['pokemonsurvivorwiki.com', 'www.pokemonsurvivorwiki.com'].includes(location.hostname)) {
    document.querySelector('[data-analytics-settings]')?.setAttribute('hidden', '');
    return;
  }
  const id = 'G-GEQDCG9L1K';
  const key = 'psw-analytics-consent-v1';
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
  panel.setAttribute('aria-label', 'Optional analytics');
  panel.innerHTML = '<strong>Help improve this Wiki?</strong><p>Allow Google Analytics to measure page visits. Your search terms are excluded. <a href="/privacy/">Privacy details</a></p><div><button type="button" class="button secondary" data-analytics="denied">Decline</button><button type="button" class="button" data-analytics="granted">Allow analytics</button></div>';
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
  if (choice === 'granted') start();
})();
