import {observeReading} from './analytics-reading.mjs';
import {createKabitaEventValidator} from './analytics-events.mjs';
(() => {
  'use strict';
  const key = 'kabita-analytics-consent-v1';
  const denied = {analytics_storage:'denied', ad_storage:'denied', ad_user_data:'denied', ad_personalization:'denied'};
  let enabled = false, loaded = false, active = false, config, page, pageChoice, reading, ready = false, viewed = false, tag;
  const remember = value => { pageChoice = value; try { localStorage.setItem(key, value); return true; } catch { return false; } };
  const choice = () => { if (pageChoice) return pageChoice; try { return localStorage.getItem(key); } catch { return null; } };
  const status = text => { const el = document.getElementById('analytics-status'); if (el) el.textContent = text; };
  const privacyBlocked = () => window.navigator?.globalPrivacyControl === true ||
    window.navigator?.doNotTrack === '1' || window.doNotTrack === '1';
  function activate() {
    if (!enabled || active || choice() !== 'granted' || privacyBlocked()) return;
    active = ready;
    window['ga-disable-'+config.measurementId] = false;
    if (!loaded) {
      window.dataLayer = window.dataLayer || [];
      window.gtag = function () { window.dataLayer.push(arguments); };
      window.gtag('consent', 'default', denied);
      window.gtag('js', new Date());
      window.gtag('config', config.measurementId, {...page, send_page_view:false,
        allow_google_signals:false, allow_ad_personalization_signals:false,
        cookie_prefix:'kabita', cookie_domain:'none', cookie_path:config.basePath,
        cookie_flags:'SameSite=Lax;Secure', cookie_expires:60*60*24*30});
    }
    window.gtag('consent', 'update', {analytics_storage:'granted'});
    if (!loaded) {
      loaded = true;
      tag = document.createElement('script');
      tag.async = true;
      tag.src = 'https://www.googletagmanager.com/gtag/js?id=' + encodeURIComponent(config.measurementId);
      tag.onload = () => {
        ready = true;
        if (choice() !== 'granted' || privacyBlocked()) return;
        active = true;
        if (!viewed) { viewed = true; window.gtag('event', 'page_view', page); }
        reading?.refresh();
        status('Analytics is allowed. You can turn it off here at any time.');
      };
      tag.onerror = () => {
        active = false; ready = false; loaded = false;
        window['ga-disable-'+config.measurementId] = true;
        tag.remove(); window.dataLayer = [];
        status('Analytics could not load. Reading remains available; choose Allow to retry.');
      };
      document.head.append(tag);
    }
    if (active && !viewed) { viewed = true; window.gtag('event', 'page_view', page); }
    reading?.refresh();
    if (active) status('Analytics is allowed. You can turn it off here at any time.');
    else status('Analytics is loading. Reading remains available.');
  }
  function clearOwnCookies() {
    // Host-only, project-prefixed cookies; never touch other sites on the Pages host.
    for (const entry of (document.cookie || '').split(';')) {
      const name = entry.split('=')[0].trim();
      if (/^kabita_ga(?:_|$)/.test(name))
        document.cookie = name+'=; Max-Age=0; Path='+config.basePath+'; SameSite=Lax; Secure';
    }
  }
  window.kabitaAnalytics = {
    track(name, input) {
      if (!enabled || !active || choice() !== 'granted' || privacyBlocked()) return false;
      try {
        const event = createKabitaEventValidator(config.catalogue)(name, input);
        window.gtag('event', event.name, event.params);
        return true;
      } catch { return false; }
    }
  };
  fetch('runtime-config.json').then(r => r.ok ? r.json() : Promise.reject()).then(runtime => {
    config = runtime.analytics;
    // The public exporter supplies exact routes and fixed titles, including the deployment base.
    const title = config?.publicPages?.[location.pathname];
    enabled = config?.enabled === true && /^G-[A-Z0-9]{6,20}$/.test(config.measurementId) &&
      location.protocol === 'https:' && config.allowedHosts?.includes(location.hostname) &&
      !['localhost','127.0.0.1','[::1]'].includes(location.hostname) &&
      typeof title === 'string' && title.length > 0 && typeof config.basePath === 'string' &&
      config.basePath.startsWith('/') && config.basePath.endsWith('/') && !/[;\r\n]/.test(config.basePath) &&
      location.pathname.startsWith(config.basePath);
    if (!enabled) return;
    page = {page_location:location.origin+location.pathname, page_title:title, page_referrer:'', ignore_referrer:true};
    reading = observeReading(document, (name,input) => window.kabitaAnalytics.track(name,input));
    const settings = document.getElementById('analytics-settings');
    if (settings) settings.hidden = false;
    document.getElementById('allow-analytics')?.addEventListener('click', () => {
      if (privacyBlocked()) { status('Analytics is off because your browser requests privacy.'); return; }
      remember('granted'); activate();
    });
    function withdraw(persisted) {
      active = false;
      window['ga-disable-'+config.measurementId] = true;
      clearOwnCookies();
      if (loaded) {
        window.gtag('consent','update',denied);
        if (persisted) location.reload();
      }
      status('Analytics is off.');
    }
    document.getElementById('decline-analytics')?.addEventListener('click', () => withdraw(remember('denied')));
    // A different tab can withdraw or remove stored consent. Never grant from a storage event.
    window.addEventListener('storage', event => {
      if ((event.key !== key && event.key !== null) || (event.storageArea && event.storageArea !== localStorage)) return;
      if (event.newValue === 'granted') return;
      pageChoice = 'denied';
      withdraw(true);
    });
    status(privacyBlocked() ? 'Analytics is off because your browser requests privacy.' :
      choice() === 'granted' ? 'Analytics is allowed.' : 'Analytics is off.');
    activate();
  }).catch(() => {});
})();
