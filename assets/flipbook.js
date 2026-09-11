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

  function render() {
    pages.forEach(function (page) {
      var idx = Number(page.dataset.index);
      page.classList.toggle('turned', idx < current);
    });
    if (pageNum) pageNum.textContent = current + 1;
    if (prevBtn) prevBtn.disabled = current === 0;
    if (nextBtn) nextBtn.disabled = current === total - 1;
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

  render();
  if (stage.classList.contains('no-anim')) {
    requestAnimationFrame(function () {
      requestAnimationFrame(function () { stage.classList.remove('no-anim'); });
    });
  }
})();
