(function () {
  var scroller = document.querySelector('.feed-scroller');
  var dotsWrap = document.querySelector('.feed-dots');
  if (!scroller || !dotsWrap) return;

  var sections = Array.prototype.slice.call(scroller.querySelectorAll('.feed-page'));
  var dots = Array.prototype.slice.call(dotsWrap.querySelectorAll('button'));

  dots.forEach(function (dot) {
    dot.addEventListener('click', function () {
      var target = document.getElementById(dot.dataset.target);
      if (target) target.scrollIntoView({ behavior: 'smooth', block: 'start' });
    });
  });

  var observer = new IntersectionObserver(
    function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting && entry.intersectionRatio > 0.6) {
          var id = entry.target.id;
          dots.forEach(function (dot) {
            dot.classList.toggle('active', dot.dataset.target === id);
          });
        }
      });
    },
    { root: scroller, threshold: [0.6] }
  );

  sections.forEach(function (section) {
    if (section.id) observer.observe(section);
  });
})();
