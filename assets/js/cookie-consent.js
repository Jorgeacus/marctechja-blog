/* Consentimento de cookies — MarctechJA
 * Banner CMP ligeiro, sem dependências externas.
 * Guarda a escolha em localStorage; carrega conteúdo condicionado
 * a consentimento (anúncios/cookies) apenas após "Aceitar".
 */
(function () {
  'use strict';

  var KEY = 'marctechja_cookie_consent';
  var DEFAULTS = { analytics: true, ads: true };

  function getPrefs() {
    try {
      var raw = localStorage.getItem(KEY);
      if (!raw) return null;
      var p = JSON.parse(raw);
      return { analytics: !!p.analytics, ads: !!p.ads, at: p.at };
    } catch (e) { return null; }
  }

  function savePrefs(analytics, ads) {
    var p = { analytics: !!analytics, ads: !!ads, at: new Date().toISOString() };
    try { localStorage.setItem(KEY, JSON.stringify(p)); } catch (e) {}
    return p;
  }

  function applyConsent(p) {
    // Marca o documento como "consentido" para scripts condicionados
    document.documentElement.setAttribute('data-cookie-consent', p.ads ? 'accepted' : 'denied');
    // GTAgtm / dataLayer, se algum dia existir
    if (typeof dataLayer !== 'undefined') {
      dataLayer.push({ event: 'consent', consent: p });
    }
  }

  function buildBanner() {
    if (document.getElementById('cookie-consent-banner')) return;
    var banner = document.createElement('div');
    banner.id = 'cookie-consent-banner';
    banner.setAttribute('role', 'dialog');
    banner.setAttribute('aria-label', 'Consentimento de cookies');

    var text = document.createElement('p');
    text.innerHTML =
      'Este site utiliza cookies para melhorar a tua experiência e medir o tráfego. ' +
      'Lê a <a href="/politica-de-cookies/">Política de Cookies</a> e a ' +
      '<a href="/politica-de-privacidade/">Política de Privacidade</a>.';

    var accept = document.createElement('button');
    accept.type = 'button';
    accept.id = 'cookie-accept';
    accept.textContent = 'Aceitar';

    var decline = document.createElement('button');
    decline.type = 'button';
    decline.id = 'cookie-decline';
    decline.className = 'secondary';
    decline.textContent = 'Recusar';

    banner.appendChild(text);
    banner.appendChild(accept);
    banner.appendChild(decline);
    document.body.appendChild(banner);

    accept.addEventListener('click', function () {
      var p = savePrefs(true, true);
      applyConsent(p);
      banner.remove();
    });

    decline.addEventListener('click', function () {
      var p = savePrefs(false, false);
      applyConsent(p);
      banner.remove();
    });
  }

  function init() {
    var p = getPrefs();
    if (p) {
      applyConsent(p);
      return; // já decidiu — sem banner
    }
    buildBanner();
  }

  // API pública para reabrir o banner (link "Definições de cookies" no rodapé)
  window.MarctechJACookieConsent = {
    show: function () {
      if (getPrefs()) {
        // reabrir para permitir alterar a escolha
        localStorage.removeItem(KEY);
      }
      buildBanner();
    }
  };

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
