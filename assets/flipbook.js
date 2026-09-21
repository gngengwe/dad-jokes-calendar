(function () {
  var stage = document.getElementById('bookStage');
  var prevBtn = document.getElementById('bookPrev');
  var nextBtn = document.getElementById('bookNext');
  var pageNum = document.getElementById('bookPageNum');
  if (!stage) return;

  var pages = Array.prototype.slice.call(stage.querySelectorAll('.flip-page'));
  var total = pages.length;
  var current = 0;

  // Deep link support: /#nov opens straight to that spread (no flip
  // animation on load -- transitions are suppressed for the first paint).
  var sections = window.__BOOK_SECTIONS__ || [];
  var hashTarget = sections.indexOf(location.hash.slice(1));
  if (hashTarget > -1) {
    current = hashTarget;
    stage.classList.add('no-anim');
  }

  // On-demand image loading: all 13 pages are stacked in the same screen
  // rect (that's how the flip effect works), so native loading="lazy"
  // can't tell most of them are "off-screen" and loads more than it
  // should. Only fetch the current spread's image plus one on each side.
  function loadImagesAround(idx) {
    [idx - 1, idx, idx + 1].forEach(function (i) {
      var page = pages[i];
      if (!page) return;
      var img = page.querySelector('img[data-src]');
      if (img) { img.src = img.dataset.src; img.removeAttribute('data-src'); }
    });
  }

  var monthsBtn = document.getElementById('monthsBtn');
  var monthMenu = document.getElementById('monthMenu');
  var artView = document.getElementById('artView');
  var artImg = artView ? artView.querySelector('img') : null;
  var artReturnFocus = null;

  function render() {
    pages.forEach(function (page) {
      var idx = Number(page.dataset.index);
      page.classList.toggle('turned', idx < current);
      // Only the visible page is reachable by keyboard / screen reader.
      var visible = idx === current;
      page.inert = !visible;
      page.setAttribute('aria-hidden', visible ? 'false' : 'true');
    });
    if (pageNum) pageNum.textContent = current + 1;
    if (prevBtn) prevBtn.disabled = current === 0;
    if (nextBtn) nextBtn.disabled = current === total - 1;
    if (monthMenu) {
      Array.prototype.forEach.call(monthMenu.querySelectorAll('[data-idx]'), function (b) {
        if (Number(b.dataset.idx) === current) b.setAttribute('aria-current', 'page');
        else b.removeAttribute('aria-current');
      });
    }
    loadImagesAround(current);

    // Keep the address bar on the page being viewed so the URL is shareable.
    var wantHash = current === 0 ? '' : '#' + sections[current];
    if (sections[current] && location.hash !== wantHash) {
      history.replaceState(null, '', location.pathname + location.search + wantHash);
    }
  }

  function goTo(idx) {
    idx = Math.max(0, Math.min(total - 1, idx));
    if (idx !== current) { current = idx; render(); }
  }
  function next() { goTo(current + 1); }
  function prev() { goTo(current - 1); }

  // Editing the hash by hand / following an in-page link switches the page.
  window.addEventListener('hashchange', function () {
    var i = location.hash ? sections.indexOf(location.hash.slice(1)) : 0;
    if (i > -1) goTo(i);
  });

  // Month picker.
  function setMenu(open) {
    if (!monthMenu || !monthsBtn) return;
    monthMenu.hidden = !open;
    monthsBtn.setAttribute('aria-expanded', open ? 'true' : 'false');
    if (open) {
      var cur = monthMenu.querySelector('[data-idx="' + current + '"]');
      if (cur) cur.focus();
    }
  }
  if (monthsBtn && monthMenu) {
    monthsBtn.addEventListener('click', function (e) { e.stopPropagation(); setMenu(monthMenu.hidden); });
    monthMenu.addEventListener('click', function (e) {
      var b = e.target.closest('[data-idx]');
      if (!b) return;
      goTo(Number(b.dataset.idx));
      setMenu(false);
      monthsBtn.focus();
    });
    document.addEventListener('click', function (e) {
      if (!monthMenu.hidden && !e.target.closest('#monthMenu') && !e.target.closest('#monthsBtn')) setMenu(false);
    });
  }

  // Full-illustration viewer.
  function openArt(page, trigger) {
    var src = page.querySelector('.art img');
    if (!artView || !artImg || !src || !src.getAttribute('src')) return;
    artImg.src = src.currentSrc || src.src;
    artImg.alt = src.alt;
    artReturnFocus = trigger;
    artView.hidden = false;
    var close = artView.querySelector('.art-view-close');
    if (close) close.focus();
  }
  function closeArt() {
    if (!artView || artView.hidden) return;
    artView.hidden = true;
    if (artReturnFocus) artReturnFocus.focus();
  }
  if (artView) artView.addEventListener('click', closeArt);

  if (prevBtn) prevBtn.addEventListener('click', prev);
  if (nextBtn) nextBtn.addEventListener('click', next);
  var coverStart = document.getElementById('coverStart');
  if (coverStart) coverStart.addEventListener('click', function (e) { e.stopPropagation(); next(); });

  stage.setAttribute('tabindex', '0');
  stage.addEventListener('click', function (e) {
    if (e.target.closest('.book-nav') || e.target.closest('.pin') || e.target.closest('.book-right') || e.target.closest('.book-reveal') || e.target.closest('.art-expand')) return;
    var rect = stage.getBoundingClientRect();
    var x = e.clientX - rect.left;
    if (x > rect.width / 2) next(); else prev();
  });

  // Each spread has its own pins/notes/reveal button -- wire them per page
  // rather than globally, since the flipbook holds 12 separate sets in one
  // document (unlike the single-spread month detail pages).
  pages.forEach(function (page) {
    var pagePins = Array.prototype.slice.call(page.querySelectorAll('.pin'));
    var pageNotes = Array.prototype.slice.call(page.querySelectorAll('.note'));
    var revealBtn = page.querySelector('.book-reveal-btn');
    var revealCard = page.querySelector('.book-reveal');
    var closeBtn = page.querySelector('.book-reveal-close');
    var expandBtn = page.querySelector('.art-expand');
    if (expandBtn) expandBtn.addEventListener('click', function (e) { e.stopPropagation(); openArt(page, expandBtn); });

    function reveal() {
      if (revealCard && revealCard.hidden) {
        revealCard.hidden = false;
        if (revealBtn) revealBtn.setAttribute('aria-expanded', 'true');
      }
    }

    function hideStory() {
      if (revealCard && !revealCard.hidden) {
        revealCard.hidden = true;
        if (revealBtn) revealBtn.setAttribute('aria-expanded', 'false');
        highlight(-1);
      }
    }

    function highlight(i) {
      pagePins.forEach(function (p, idx) { p.classList.toggle('hi', idx === i); });
      pageNotes.forEach(function (n) { n.classList.toggle('hi', Number(n.dataset.idx) === i); });
    }

    pagePins.forEach(function (pin, i) {
      pin.addEventListener('click', function (e) { e.stopPropagation(); reveal(); highlight(i); });
      pin.addEventListener('focus', function () { reveal(); highlight(i); });
    });
    pageNotes.forEach(function (note, i) {
      note.addEventListener('mouseenter', function () { highlight(i); });
    });
    if (revealBtn) revealBtn.addEventListener('click', function (e) { e.stopPropagation(); reveal(); });
    if (closeBtn) closeBtn.addEventListener('click', function (e) { e.stopPropagation(); hideStory(); });
  });

  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') {
      if (artView && !artView.hidden) { closeArt(); e.preventDefault(); return; }
      if (monthMenu && !monthMenu.hidden) { setMenu(false); if (monthsBtn) monthsBtn.focus(); e.preventDefault(); return; }
    }
    // Arrow keys belong to the picker / viewer while either is open.
    if ((artView && !artView.hidden) || (monthMenu && !monthMenu.hidden)) return;
    if (e.key === 'ArrowRight' || e.key === 'PageDown') { next(); e.preventDefault(); }
    if (e.key === 'ArrowLeft' || e.key === 'PageUp') { prev(); e.preventDefault(); }
  });

  // Touch swipe. Only acts on a clearly horizontal drag past a distance
  // threshold, so it doesn't fight the vertical scroll inside .book-right.
  var touchStartX = 0, touchStartY = 0, touching = false;
  stage.addEventListener('touchstart', function (e) {
    if (e.target.closest('.book-nav')) return;
    var t = e.changedTouches[0];
    touchStartX = t.clientX; touchStartY = t.clientY; touching = true;
  }, { passive: true });
  stage.addEventListener('touchend', function (e) {
    if (!touching) return;
    touching = false;
    var t = e.changedTouches[0];
    var dx = t.clientX - touchStartX;
    var dy = t.clientY - touchStartY;
    if (Math.abs(dx) > 55 && Math.abs(dx) > Math.abs(dy) * 1.5) {
      if (dx < 0) next(); else prev();
    }
  }, { passive: true });

  render();
  if (stage.classList.contains('no-anim')) {
    requestAnimationFrame(function () {
      requestAnimationFrame(function () { stage.classList.remove('no-anim'); });
    });
  }
})();
