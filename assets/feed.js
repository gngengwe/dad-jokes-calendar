(function () {
  var scroller = document.querySelector('.feed-scroller');
  var dotsWrap = document.querySelector('.feed-dots');
  var progressFill = document.getElementById('feedProgressFill');
  if (!scroller) return;

  var sectionIds = window.__FEED_SECTIONS__ || [];
  var sections = sectionIds.map(function (id) { return document.getElementById(id); }).filter(Boolean);
  var dots = dotsWrap ? Array.prototype.slice.call(dotsWrap.querySelectorAll('button')) : [];

  dots.forEach(function (dot) {
    dot.addEventListener('click', function () {
      var target = document.getElementById(dot.dataset.target);
      if (target) target.scrollIntoView({ behavior: 'smooth', block: 'start' });
    });
  });

  function setActive(id) {
    var idx = sectionIds.indexOf(id);
    if (idx === -1) return;
    dots.forEach(function (dot) {
      dot.classList.toggle('active', dot.dataset.target === id);
    });
    if (progressFill && sectionIds.length > 1) {
      var pct = (idx / (sectionIds.length - 1)) * 100;
      progressFill.style.width = pct + '%';
    }
  }

  var observer = new IntersectionObserver(
    function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting && entry.intersectionRatio > 0.6) {
          setActive(entry.target.id);
        }
      });
    },
    { root: scroller, threshold: [0.6] }
  );

  sections.forEach(function (section) { observer.observe(section); });
})();
