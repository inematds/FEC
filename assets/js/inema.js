// inema.js — interações globais. Servido via 'self' (CSP-safe).
// (1) Toggle exclusivo de tópicos: abrir um fecha os irmãos do mesmo card.
// (2) Modais com iframe (botão "Ver em Modal" + fechar com X / Esc / clique no backdrop).

(function () {
  'use strict';

  // (1) Tópicos expansíveis: ao abrir um <details>, fechar os outros do mesmo
  //     card (.modulo-card). Comportamento "accordion" dentro do card.
  document.addEventListener('toggle', function (ev) {
    var d = ev.target;
    if (!(d instanceof HTMLDetailsElement)) return;
    if (!d.classList.contains('topico-expansivel')) return;
    if (!d.open) return;
    var card = d.closest('.modulo-card');
    if (!card) return;
    card.querySelectorAll('details.topico-expansivel[open]').forEach(function (other) {
      if (other !== d) other.open = false;
    });
  }, true);

  // (2) Modais
  function openModal(id) {
    var modal = document.getElementById(id);
    if (!modal) return;
    modal.classList.remove('hidden');
    modal.classList.add('flex');
    document.body.style.overflow = 'hidden';
  }

  function closeAllModals() {
    document.querySelectorAll('.fec-modal').forEach(function (m) {
      m.classList.add('hidden');
      m.classList.remove('flex');
    });
    document.body.style.overflow = '';
  }

  // Botões "Ver em Modal" (data-modal="<id>")
  document.addEventListener('click', function (ev) {
    var btn = ev.target.closest('[data-modal]');
    if (btn) {
      ev.preventDefault();
      openModal(btn.getAttribute('data-modal'));
      return;
    }
    // Botões de fechar (data-modal-close) e backdrop (clicou fora do conteúdo)
    if (ev.target.closest('[data-modal-close]')) {
      ev.preventDefault();
      closeAllModals();
      return;
    }
    var modal = ev.target.closest('[data-modal-backdrop]');
    if (modal && ev.target === modal) {
      closeAllModals();
    }
  });

  // Esc fecha qualquer modal aberto
  document.addEventListener('keydown', function (ev) {
    if (ev.key === 'Escape') closeAllModals();
  });
})();
