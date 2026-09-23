(function () {
  var root = document.querySelector(".hero-cine");
  if (!root) return;

  var reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var kind = root.getAttribute("data-hero-kind");

  if (kind === "video") {
    var video = root.querySelector("[data-hero-video]");
    if (!video) return;
    if (reduceMotion) {
      video.removeAttribute("autoplay");
      video.pause();
      return;
    }
    var started = video.play();
    if (started && typeof started.catch === "function") {
      started.catch(function () {});
    }
    return;
  }

  if (kind !== "slider") return;

  var slides = Array.prototype.slice.call(root.querySelectorAll("[data-hero-slide]"));
  if (slides.length < 2) return;

  var index = 0;
  var timer = 0;
  var startX = 0;
  var startY = 0;
  var tracking = false;

  function show(next) {
    index = (next + slides.length) % slides.length;
    slides.forEach(function (slide, slideIndex) {
      slide.classList.toggle("is-active", slideIndex === index);
    });
  }

  function stop() {
    if (!timer) return;
    window.clearInterval(timer);
    timer = 0;
  }

  function startAuto() {
    stop();
    if (reduceMotion) return;
    timer = window.setInterval(function () {
      show(index + 1);
    }, 6500);
  }

  root.addEventListener("touchstart", function (event) {
    if (event.target.closest("a, button")) return;
    var touch = event.changedTouches[0];
    startX = touch.clientX;
    startY = touch.clientY;
    tracking = true;
  }, { passive: true });

  root.addEventListener("touchend", function (event) {
    if (!tracking) return;
    tracking = false;
    if (event.target.closest("a, button")) return;
    var touch = event.changedTouches[0];
    var dx = touch.clientX - startX;
    var dy = touch.clientY - startY;
    if (Math.abs(dx) < 48 || Math.abs(dx) < Math.abs(dy)) return;
    show(index + (dx < 0 ? 1 : -1));
    startAuto();
  }, { passive: true });

  document.addEventListener("visibilitychange", function () {
    if (document.hidden) {
      stop();
    } else {
      startAuto();
    }
  });

  startAuto();
})();
