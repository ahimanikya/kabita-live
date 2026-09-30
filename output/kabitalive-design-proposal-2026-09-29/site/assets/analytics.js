(() => {
  'use strict';
  const key = 'kabita-analytics-consent-v1';
  let enabled = false, loaded = false;
  let config;
  const remember = value => { try { localStorage.setItem(key, value); } catch {} };
  const choice = () => { try { return localStorage.getItem(key); } catch { return null; } };
  const status = text => { const el = document.getElementById('analytics-status'); if (el) el.textContent = text; };
  function activate() {
    if (!enabled || loaded || choice() !== 'granted') return;
    loaded = true;
    window.dataLayer = window.dataLayer || [];
    window.gtag = function () { window.dataLayer.push(arguments); };
    window.gtag('consent', 'default', {analytics_storage:'granted', ad_storage:'denied', ad_user_data:'denied', ad_personalization:'denied'});
    window.gtag('js', new Date());
    window.gtag('config', config.measurementId, {send_page_view:false, allow_google_signals:false, allow_ad_personalization_signals:false});
    let referrer = '';
    try { const ref = new URL(document.referrer); referrer = ref.origin + ref.pathname; } catch {}
    window.gtag('event', 'page_view', {page_location:location.origin+location.pathname, page_title:document.title, page_referrer:referrer});
    const tag = document.createElement('script');
    tag.async = true;
    tag.src = 'https://www.googletagmanager.com/gtag/js?id=' + encodeURIComponent(config.measurementId);
    document.head.append(tag);
    status('Analytics is allowed. You can turn it off here at any time.');
  }
  window.kabitaAnalytics = {
    track(event, fields = {}) {
      if (!enabled || !loaded || choice() !== 'granted' || event !== 'share') return;
      if (!['copy_link','copy_caption','native','whatsapp','facebook'].includes(fields.method)) return;
      if (!/^\d{1,8}$/.test(String(fields.item_id))) return;
      window.gtag('event', 'share', {method:fields.method, content_type:'poem', item_id:String(fields.item_id)});
    }
  };
  fetch('runtime-config.json').then(r => r.ok ? r.json() : Promise.reject()).then(runtime => {
    config = runtime.analytics;
    enabled = config?.enabled === true && /^G-[A-Z0-9]+$/.test(config.measurementId) &&
      location.protocol === 'https:' && config.allowedHosts?.includes(location.hostname) &&
      !['localhost','127.0.0.1','[::1]'].includes(location.hostname);
    if (!enabled) return;
    const settings = document.getElementById('analytics-settings');
    if (settings) settings.hidden = false;
    document.getElementById('allow-analytics')?.addEventListener('click', () => { remember('granted'); activate(); });
    document.getElementById('decline-analytics')?.addEventListener('click', () => {
      remember('denied');
      if (loaded) {
        window.gtag('consent','update',{analytics_storage:'denied',ad_storage:'denied',ad_user_data:'denied',ad_personalization:'denied'});
        window['ga-disable-'+config.measurementId] = true;
        location.reload();
      }
      status('Analytics is off.');
    });
    status(choice() === 'granted' ? 'Analytics is allowed.' : 'Analytics is off.');
    activate();
  }).catch(() => {});
})();
