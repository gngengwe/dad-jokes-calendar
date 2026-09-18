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

  function render() {
    pages.forEach(function (page) {
      var idx = Number(page.dataset.index);
      page.classList.toggle('turned', idx < current);
    });
    if (pageNum) pageNum.textContent = current + 1;
    if (prevBtn) prevBtn.disabled = current === 0;
    if (nextBtn) nextBtn.disabled = current === total - 1;
    loadImagesAround(current);
  }

  function next() { if (current < total - 1) { current++; render(); } }
  function prev() { if (current > 0) { current--; render(); } }

  if (prevBtn) prevBtn.addEventListener('click', prev);
  if (nextBtn) nextBtn.addEventListener('click', next);

  stage.setAttribute('tabindex', '0');
  stage.addEventListener('click', function (e) {
    if (e.target.closest('.book-nav')) return;
    var rect = stage.getBoundingClientRect();
    var x = e.clientX - rect.left;
    if (x > rect.width / 2) next(); else prev();
  });

  document.addEventListener('keydown', function (e) {
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
