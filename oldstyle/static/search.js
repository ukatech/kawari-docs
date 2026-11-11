/* サイト内検索。search-index.js（ビルド時に作る。大きいので、使うときに読み込む）の KAWARI_INDEX を、
   空白で区切った語の AND で部分一致検索する。旧 wiki の検索の代わり。
   - ヘッダの検索欄に打ち込むと、止まってから DEBOUNCE ミリ秒後に、ドロップダウンに上位の節を出す
   - ↑↓で選び、Enter で開く（選んでいなければ search/?q= へ）。Esc で閉じる
   - search/ は、ヒットした全項目を並べる（JavaScript が無いと、結果は出ない） */
(function () {
  'use strict';

  var DEBOUNCE = 250;      // 打ち込みが止まってから検索するまでの待ち（ミリ秒）
  var MAX_ITEMS = 8;       // ドロップダウンに並べる件数
  var MAX_PAGE = 100;      // search/ に並べる件数

  var ESC = { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' };
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return ESC[c]; }); }
  function norm(s) { return s.toLowerCase(); }
  // ページの深さによらず、サイトのルートからの相対パス（<body data-root="../../"> など）を前に付ける
  var ROOT = document.body.getAttribute('data-root') || './';
  function urlOf(u) { return ROOT + u; }
  function searchUrl(q) { return ROOT + 'search/' + (q ? '?q=' + encodeURIComponent(q) : ''); }

  /* ---- 索引と検索 ---- */

  var docs = null;
  var waiting = null;      // 索引の読み込み中に溜まった呼び出し

  function ensureIndex(cb) {
    if (docs) { cb(); return; }
    if (waiting) { waiting.push(cb); return; }
    waiting = [cb];
    function done(list) {
      docs = (list || []).map(function (e) {
        return { page: e[0], title: e[1], url: e[2], text: e[3], nt: norm(e[1]), nx: norm(e[3]) };
      });
      var calls = waiting;
      waiting = null;
      calls.forEach(function (f) { f(); });
    }
    if (window.KAWARI_INDEX) { done(window.KAWARI_INDEX); return; }
    var s = document.createElement('script');
    s.src = ROOT + 'search-index.js';
    s.onload = function () { done(window.KAWARI_INDEX); };
    s.onerror = function () { done([]); };
    document.head.appendChild(s);
  }

  function snippet(d, terms, len) {
    var pos = -1;
    terms.forEach(function (t) { var p = d.nx.indexOf(t); if (p >= 0 && (pos < 0 || p < pos)) pos = p; });
    var start = Math.max(0, pos - 30);
    var html = esc(d.text.slice(start, start + len));
    terms.forEach(function (t) {
      if (!t) return;
      var re = new RegExp(esc(t).replace(/[.*+?^${}()|[\]\\]/g, '\\$&'), 'gi');
      html = html.replace(re, function (m) { return '<mark>' + m + '</mark>'; });
    });
    return (start > 0 ? '…' : '') + html + (start + len < d.text.length ? '…' : '');
  }

  function find(q) {
    var terms = norm(q).split(/\s+/).filter(Boolean);
    var hits = [];
    if (!terms.length) return { terms: terms, hits: hits };
    docs.forEach(function (d) {
      var score = 0;
      for (var i = 0; i < terms.length; i++) {
        var inTitle = d.nt.indexOf(terms[i]) >= 0, inText = d.nx.indexOf(terms[i]) >= 0;
        if (!inTitle && !inText) return;
        score += inTitle ? (d.nt === terms[i] ? 100 : 10) : 1;
      }
      hits.push({ d: d, score: score });
    });
    hits.sort(function (a, b) { return b.score - a.score; });
    return { terms: terms, hits: hits };
  }

  /* ---- 検索頁（search/） ---- */

  function resultsPage() {
    var input = document.getElementById('search-q');
    var out = document.getElementById('search-results');
    var form = document.getElementById('search-form');
    if (!input || !out || !form) return;

    function run(q) {
      ensureIndex(function () {
        var r = find(q);
        if (!r.terms.length) { out.innerHTML = ''; return; }
        var shown = r.hits.slice(0, MAX_PAGE);
        var html = '<p>' + r.hits.length + ' 件' + (r.hits.length > shown.length ? '（上位 ' + shown.length + ' 件を表示）' : '') + '</p><ul>';
        shown.forEach(function (h) {
          html += '<li><a href="' + esc(urlOf(h.d.url)) + '">' + esc(h.d.title) + '</a> <span class="search-page">' + esc(h.d.page) + '</span><br>' + snippet(h.d, r.terms, 140) + '</li>';
        });
        out.innerHTML = html + '</ul>';
      });
    }

    var m = /[?&]q=([^&]*)/.exec(location.search);
    if (m) { input.value = decodeURIComponent(m[1].replace(/\+/g, ' ')); run(input.value); }
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      run(input.value);
      history.replaceState(null, '', '?q=' + encodeURIComponent(input.value));
    });
  }

  /* ---- 左上の検索欄とドロップダウン ---- */

  function dropdown(input) {
    var box = document.getElementById('search');
    var el = document.createElement('div');
    el.className = 'site-search__dropdown';
    el.id = 'search-dropdown';
    el.setAttribute('role', 'listbox');
    el.setAttribute('translate', 'no');
    el.hidden = true;
    box.appendChild(el);

    var q = '', active = -1, count = 0, timer = null, composing = false;

    function items() { return el.querySelectorAll('a[data-i]'); }
    function setActive(i) {
      active = i;
      Array.prototype.forEach.call(items(), function (a) {
        var on = +a.dataset.i === i;
        a.classList.toggle('is-active', on);
        a.setAttribute('aria-selected', String(on));
        if (on) a.scrollIntoView({ block: 'nearest' });
      });
    }
    function hide() {
      clearTimeout(timer);
      q = '';
      active = -1;
      el.hidden = true;
      input.setAttribute('aria-expanded', 'false');
    }
    function render() {
      var r = find(q);
      var shown = r.hits.slice(0, MAX_ITEMS);
      var html = '';
      shown.forEach(function (h, i) {
        html += '<a class="site-search__item" role="option" data-i="' + i + '" href="' + esc(urlOf(h.d.url)) + '"><span class="site-search__title">' + esc(h.d.title) +
          '</span> <span class="site-search__page">' + esc(h.d.page) + '</span><span class="site-search__snippet">' + snippet(h.d, r.terms, 90) + '</span></a>';
      });
      if (!shown.length) html += '<p class="site-search__empty">見つかりませんでした。</p>';
      html += '<a class="site-search__all" role="option" data-i="' + shown.length + '" href="' + esc(searchUrl(q)) + '">' +
        (shown.length ? 'すべての結果を見る（' + r.hits.length + ' 件）' : '検索ページで探す') + '</a>';
      el.innerHTML = html;
      count = shown.length + 1;
      active = -1;
      el.hidden = false;
      input.setAttribute('aria-expanded', 'true');
    }
    // 打ち込みが止まってから検索する。空なら閉じる
    function query(value) {
      clearTimeout(timer);
      value = value.trim();
      if (!value) { hide(); return; }
      timer = setTimeout(function () {
        ensureIndex(function () {
          if (value === q) return;
          q = value;
          render();
        });
      }, DEBOUNCE);
    }

    // 項目を押してもフォーカス（入力欄）を動かさない。動くと blur で閉じて、押した項目に届かない
    el.addEventListener('mousedown', function (e) { e.preventDefault(); });
    el.addEventListener('mouseover', function (e) {
      var a = e.target.closest('a[data-i]');
      if (a) setActive(+a.dataset.i);
    });
    input.addEventListener('compositionstart', function () { composing = true; });
    input.addEventListener('compositionend', function () { composing = false; query(input.value); });
    input.addEventListener('input', function () { if (!composing) query(input.value); });
    input.addEventListener('focus', function () { if (input.value.trim()) query(input.value); });
    input.addEventListener('blur', hide);
    input.addEventListener('keydown', function (e) {
      if (e.isComposing) return;
      if (e.key === 'ArrowDown' || e.key === 'ArrowUp') {
        if (el.hidden) return;
        e.preventDefault();
        setActive(Math.max(-1, Math.min(count - 1, active + (e.key === 'ArrowDown' ? 1 : -1))));
      } else if (e.key === 'Enter') {
        var a = active >= 0 && !el.hidden ? el.querySelector('a[data-i="' + active + '"]') : null;
        if (a) { e.preventDefault(); location.href = a.getAttribute('href'); }
        // 選んでいなければ、フォームの送信（search/?q=）に任せる
      } else if (e.key === 'Escape') {
        hide();
      }
    });
  }

  /* ---- 起動 ---- */

  resultsPage();
  var input = document.getElementById('query');
  if (input) dropdown(input);
})();
