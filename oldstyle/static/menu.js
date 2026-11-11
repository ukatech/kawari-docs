/* 幅が狭いとき（767px 以下。style.css の @media と同じ）は、左のメニュー（#menubar）を、
   ヘッダの検索欄の左のボタンで開閉する引き出し（ドロワー）にする（yaya-docs の menu.js を移したもの）。
   - この script は head で同期に読み込み、<html> に js-drawer を付ける。CSS は js-drawer があるときだけメニューを畳む
     （JavaScript が動かなければ、メニューは従来どおり本文の下に出る）
   - 開いているときは <html> に drawer-open。引き出しは、ヘッダの下から出る（--drawer-top。ヘッダが画面の外なら画面の上から）
   - 背景の暗幕・Esc・メニューの中のリンクで閉じる。広い画面に戻ると閉じる
   また、上端に残るヘッダの高さを測って、CSS の --header-h に入れる */
(function () {
  'use strict';

  var root = document.documentElement;
  root.classList.add('js-drawer');

  var LABELS = ['メニューを開く', 'メニューを閉じる'];
  var ICON_OPEN = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" aria-hidden="true"><path d="M3 6h18v2H3zm0 5h18v2H3zm0 5h18v2H3z"/></svg>';
  var ICON_CLOSE = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" aria-hidden="true"><path d="M19 6.41 17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"/></svg>';
  var narrow = window.matchMedia('(max-width: 767px)');

  function init() {
    var drawer = document.getElementById('menubar');
    var bar = document.getElementById('search');
    var header = document.getElementById('header');
    if (!drawer || !bar || !header) return;

    // 広い画面では、ヘッダが上端に残る。その高さ（パンくずリストの折り返しで変わる）を --header-h に入れ、
    // 左のメニューの貼り付く位置と、#アンカーで飛んだ見出しの位置を、ヘッダの下に合わせる
    function measure() {
      root.style.setProperty('--header-h', header.getBoundingClientRect().height + 'px');
    }
    measure();
    if (window.ResizeObserver) new ResizeObserver(measure).observe(header);
    else window.addEventListener('resize', measure);

    var button = document.createElement('button');
    button.type = 'button';
    button.className = 'ukadoc-drawer-toggle';
    button.setAttribute('aria-controls', 'menubar');
    button.setAttribute('translate', 'no');
    bar.insertBefore(button, bar.firstChild);

    var backdrop = document.createElement('div');
    backdrop.className = 'ukadoc-drawer-backdrop';
    document.body.appendChild(backdrop);

    drawer.setAttribute('tabindex', '-1');

    function render(open) {
      button.innerHTML = open ? ICON_CLOSE : ICON_OPEN;
      button.title = LABELS[open ? 1 : 0];
      button.setAttribute('aria-label', LABELS[open ? 1 : 0]);
      button.setAttribute('aria-expanded', String(open));
    }

    function setOpen(open, restoreFocus) {
      if (open === root.classList.contains('drawer-open')) return;
      root.classList.toggle('drawer-open', open);
      render(open);
      if (open) {
        // 引き出しは、ヘッダの下から。いま見ているページの項目が見えるようにする
        root.style.setProperty('--drawer-top', Math.max(0, header.getBoundingClientRect().bottom) + 'px');
        drawer.scrollTop = 0;
        var cur = drawer.querySelector('[aria-current="page"]');
        if (cur) drawer.scrollTop += cur.getBoundingClientRect().top - drawer.getBoundingClientRect().top - drawer.clientHeight / 2;
        drawer.focus({ preventScroll: true });
      } else if (restoreFocus) {
        button.focus({ preventScroll: true });
      }
    }

    render(false);
    button.addEventListener('click', function () {
      setOpen(!root.classList.contains('drawer-open'), false);
    });
    backdrop.addEventListener('click', function () { setOpen(false, true); });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && root.classList.contains('drawer-open')) setOpen(false, true);
    });
    // 同じページの中の見出しへのリンクでも、選んだら閉じて本文を見せる
    drawer.addEventListener('click', function (e) {
      if (narrow.matches && e.target.closest && e.target.closest('a[href]')) setOpen(false, false);
    });
    var onChange = function () { if (!narrow.matches) setOpen(false, false); };
    if (narrow.addEventListener) narrow.addEventListener('change', onChange);
    else if (narrow.addListener) narrow.addListener(onChange);
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
