/*
 * Medição do site (Google Tag Manager) e texto do WhatsApp conforme a origem da visita.
 * Arquivo compartilhado por todas as páginas. NUNCA envie dados pessoais (nome, telefone,
 * e-mail) para o dataLayer, para a URL ou para o armazenamento do navegador.
 */
(function () {
  'use strict';
  var w = window, d = document;
  w.dataLayer = w.dataLayer || [];
  function push(o) { w.dataLayer.push(o); }
  function sessao(k, v) {
    try {
      if (v === undefined) return sessionStorage.getItem(k);
      sessionStorage.setItem(k, v);
    } catch (e) { /* navegação anônima ou armazenamento bloqueado */ }
    return null;
  }

  /* ---------- 1. Origem da visita (sitelink e anúncio), guardada na sessão ---------- */
  var CHAVES = ['utm_content', 'gclid', 'gbraid', 'wbraid', 'gad_source'];
  var params = null;
  try { params = new URLSearchParams(w.location.search); } catch (e) { /* navegador antigo */ }
  var ctx = {};
  CHAVES.forEach(function (k) {
    var v = params && params.get(k);
    if (v) { v = String(v).slice(0, 200); sessao('ml_' + k, v); }
    else { v = sessao('ml_' + k); }
    if (v) ctx[k] = v;
  });
  var servico = String(ctx.utm_content || '').toLowerCase().replace(/[^a-z0-9_-]/g, '').slice(0, 40) || 'geral';
  var anuncio = !!(ctx.gclid || ctx.gbraid || ctx.wbraid || ctx.gad_source);
  var origem = anuncio ? 'google_ads' : 'organico';

  /* ---------- 2. Texto pré-preenchido do WhatsApp ---------- */
  var MENSAGENS = {
    sl_limpeza: 'Olá! Gostaria de agendar uma limpeza 😊',
    sl_clareamento: 'Olá! Gostaria de saber sobre clareamento dental 😊',
    sl_urgencia: 'Olá! Estou com uma urgência odontológica, podem me atender? 🙏',
    sl_alinhadores: 'Olá! Gostaria de saber sobre alinhadores SouSmile 😊',
    sl_restauracoes: 'Olá! Gostaria de agendar uma avaliação para restauração 😊'
  };
  function ehWhatsApp(a) { return /(^|\/\/)(api\.)?wa\.me\//i.test(a.getAttribute('href') || ''); }
  function ajustaWhatsApp(a) {
    try {
      var u = new URL(a.href);
      if (!a.hasAttribute('data-wa-texto')) a.setAttribute('data-wa-texto', u.searchParams.get('text') || '');
      var texto = MENSAGENS[servico] || a.getAttribute('data-wa-texto');
      if (anuncio) texto += ' (vim pelo Google)';
      a.href = u.origin + u.pathname + '?text=' + encodeURIComponent(texto);
    } catch (e) { /* mantém o link original */ }
  }
  function ajustaTodos() {
    Array.prototype.forEach.call(d.querySelectorAll('a[href*="wa.me"]'), ajustaWhatsApp);
  }

  /* ---------- 3. Rolar até o serviço do sitelink ---------- */
  var DESTINOS = {
    sl_limpeza: '.svc-media[data-slug="limpeza"]',
    sl_clareamento: '.svc-media[data-slug="clareamento"]',
    sl_alinhadores: '.svc-media[data-slug="sousmile"]',
    sl_restauracoes: '.svc-media[data-slug="restauracoes"]',
    sl_avaliacoes: '.depoimentos'
  };
  function rolaAteServico() {
    // Só na chegada pelo link do anúncio, uma vez, e só se a pessoa ainda não mexeu na página.
    if (!params || !params.get('utm_content') || !DESTINOS[servico]) return;
    var alvo = d.querySelector(DESTINOS[servico]);
    if (!alvo) return;
    alvo = alvo.closest('.svc') || alvo;
    var mexeu = false;
    var marca = function () { mexeu = true; };
    ['wheel', 'touchstart', 'keydown', 'mousedown'].forEach(function (ev) { w.addEventListener(ev, marca, { once: true, passive: true }); });
    setTimeout(function () {
      if (mexeu || w.scrollY > 80) return;
      var css = d.createElement('style');
      css.textContent = '.ml-destaque{box-shadow:0 0 0 3px #E8825A,0 10px 30px rgba(28,28,28,.12)!important;transition:box-shadow .6s ease}';
      d.head.appendChild(css);
      var topo = alvo.getBoundingClientRect().top + w.scrollY - 16;
      w.scrollTo({ top: Math.max(0, topo), behavior: 'smooth' });
      if (alvo.classList.contains('svc')) {
        alvo.classList.add('ml-destaque');
        setTimeout(function () { alvo.classList.remove('ml-destaque'); }, 4000);
      }
    }, 900);
  }

  /* ---------- 4. Eventos de clique (delegação no document) ---------- */
  function nomeBotao(a) {
    return a.getAttribute('data-botao') || a.id || (a.textContent || '').replace(/\s+/g, ' ').trim().slice(0, 60) ||
      a.getAttribute('aria-label') || a.getAttribute('title') || 'sem_nome';
  }
  d.addEventListener('click', function (e) {
    var a = e.target && e.target.closest ? e.target.closest('a[href]') : null;
    if (!a) return;
    var href = a.getAttribute('href') || '';
    if (ehWhatsApp(a)) {
      ajustaWhatsApp(a); // vale também para links que aparecerem depois
      push({ event: 'clique_whatsapp', botao: nomeBotao(a), servico: servico, origem: origem });
    } else if (/^tel:/i.test(href)) {
      push({ event: 'clique_telefone', botao: nomeBotao(a) });
    } else if (/(google\.[a-z.]+\/maps|maps\.google\.|maps\.app\.goo\.gl|goo\.gl\/maps)/i.test(href)) {
      push({ event: 'clique_mapa', destino: 'google_maps' });
    } else if (/waze\.com/i.test(href)) {
      push({ event: 'clique_mapa', destino: 'waze' });
    }
  });

  /* ---------- 5. Interação com os carrosséis de casos (uma vez por carrossel por visita) ---------- */
  d.addEventListener('scroll', function (e) {
    var t = e.target;
    if (!t || !t.classList || !t.classList.contains('svc-track') || t.scrollLeft < 10) return;
    var box = t.closest('.svc-media');
    var nome = (box && box.getAttribute('data-slug')) || 'desconhecido';
    if (sessao('ml_casos_' + nome)) return;
    sessao('ml_casos_' + nome, '1');
    if (t.getAttribute('data-ml-casos')) return; // reserva caso a sessão esteja bloqueada
    t.setAttribute('data-ml-casos', '1');
    push({ event: 'interacao_casos', servico: nome });
  }, { capture: true, passive: true });

  /* ---------- 6. Seção de depoimentos apareceu na tela ---------- */
  function observaDepoimentos() {
    var sec = d.querySelector('.depoimentos');
    if (!sec || !('IntersectionObserver' in w)) return;
    var io = new IntersectionObserver(function (itens) {
      if (!itens.some(function (i) { return i.isIntersecting; })) return;
      io.disconnect();
      push({ event: 'viu_depoimentos' });
    }, { threshold: 0.25 });
    io.observe(sec);
  }

  function inicia() { ajustaTodos(); rolaAteServico(); observaDepoimentos(); }
  if (d.readyState === 'loading') d.addEventListener('DOMContentLoaded', inicia); else inicia();
})();
