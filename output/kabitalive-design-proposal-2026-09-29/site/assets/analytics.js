(() => {
  'use strict';
  const key = 'kabita-analytics-consent-v1';
  const denied = {analytics_storage:'denied', ad_storage:'denied', ad_user_data:'denied', ad_personalization:'denied'};
  let enabled = false, loaded = false, active = false, config, page, pageChoice;
  const remember = value => { pageChoice = value; try { localStorage.setItem(key, value); return true; } catch { return false; } };
  const choice = () => { if (pageChoice) return pageChoice; try { return localStorage.getItem(key); } catch { return null; } };
  const status = text => { const el = document.getElementById('analytics-status'); if (el) el.textContent = text; };
  function activate() {
    if (!enabled || active || choice() !== 'granted') return;
    active = true;
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
      window.gtag('event', 'page_view', page);
      const tag = document.createElement('script');
      tag.async = true;
      tag.src = 'https://www.googletagmanager.com/gtag/js?id=' + encodeURIComponent(config.measurementId);
      document.head.append(tag);
    }
    status('Analytics is allowed. You can turn it off here at any time.');
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
    track(event, fields = {}) {
      if (!enabled || !active || choice() !== 'granted' || event !== 'share') return;
      if (!['copy_link','copy_caption','native','whatsapp','facebook'].includes(fields.method)) return;
      if (!/^\d{1,8}$/.test(String(fields.item_id))) return;
      window.gtag('event', 'share', {method:fields.method, content_type:'poem', item_id:String(fields.item_id)});
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
    const settings = document.getElementById('analytics-settings');
    if (settings) settings.hidden = false;
    document.getElementById('allow-analytics')?.addEventListener('click', () => { remember('granted'); activate(); });
    document.getElementById('decline-analytics')?.addEventListener('click', () => {
      const persisted = remember('denied'); active = false;
      window['ga-disable-'+config.measurementId] = true;
      clearOwnCookies();
      if (loaded) {
        window.gtag('consent','update',denied);
        if (persisted) location.reload();
      }
      status('Analytics is off.');
    });
    status(choice() === 'granted' ? 'Analytics is allowed.' : 'Analytics is off.');
    activate();
  }).catch(() => {});
})();
