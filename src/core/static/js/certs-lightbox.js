(function () {
  function certsLightbox() {
    var root = document.querySelector("[data-certs-lb]");
    if (!root || typeof root.showModal !== "function") return;

    var openers = Array.prototype.slice.call(
      document.querySelectorAll("[data-certs-open]")
    );
    if (!openers.length) return;

    var track = root.querySelector("[data-certs-track]");
    var viewport = root.querySelector("[data-certs-viewport]");
    var cap = root.querySelector("[data-certs-cap]");
    var prevBtn = root.querySelector("[data-certs-prev]");
    var nextBtn = root.querySelector("[data-certs-next]");
    var dots = Array.prototype.slice.call(
      root.querySelectorAll("[data-certs-dot]")
    );
    var slides = Array.prototype.slice.call(
      root.querySelectorAll("[data-certs-slide]")
    );
    var index = 0;
    var touchStartX = 0;
    var touchDeltaX = 0;
    var swiping = false;

    function clamp(i) {
      if (i < 0) return 0;
      if (i > slides.length - 1) return slides.length - 1;
      return i;
    }

    function render() {
      if (track) {
        track.style.transform = "translate3d(" + (-index * 100) + "%, 0, 0)";
      }
      slides.forEach(function (slide, i) {
        slide.setAttribute("aria-hidden", i === index ? "false" : "true");
      });
      dots.forEach(function (dot, i) {
        dot.classList.toggle("is-active", i === index);
        dot.setAttribute("aria-current", i === index ? "true" : "false");
      });
      if (cap) {
        var active = slides[index];
        cap.textContent = active
          ? active.getAttribute("data-caption") || ""
          : "";
      }
      if (prevBtn) prevBtn.disabled = index === 0;
      if (nextBtn) nextBtn.disabled = index === slides.length - 1;
    }

    function go(i) {
      index = clamp(i);
      render();
    }

    function openAt(i) {
      go(i);
      if (!root.open) root.showModal();
      document.body.classList.add("is-certs-lb-open");
      var closeBtn = root.querySelector("[data-certs-close]");
      if (closeBtn) closeBtn.focus();
    }

    function close() {
      if (root.open) root.close();
      document.body.classList.remove("is-certs-lb-open");
    }

    openers.forEach(function (btn) {
      btn.addEventListener("click", function () {
        var i = parseInt(btn.getAttribute("data-certs-open") || "0", 10);
        openAt(isNaN(i) ? 0 : i);
      });
    });

    root.querySelectorAll("[data-certs-close]").forEach(function (el) {
      el.addEventListener("click", function (e) {
        e.preventDefault();
        close();
      });
    });

    if (prevBtn) {
      prevBtn.addEventListener("click", function () {
        go(index - 1);
      });
    }
    if (nextBtn) {
      nextBtn.addEventListener("click", function () {
        go(index + 1);
      });
    }

    dots.forEach(function (dot) {
      dot.addEventListener("click", function () {
        var i = parseInt(dot.getAttribute("data-certs-dot") || "0", 10);
        go(isNaN(i) ? 0 : i);
      });
    });

    root.addEventListener("cancel", function () {
      document.body.classList.remove("is-certs-lb-open");
    });

    document.addEventListener("keydown", function (e) {
      if (!root.open) return;
      if (e.key === "ArrowLeft") {
        e.preventDefault();
        go(index - 1);
      } else if (e.key === "ArrowRight") {
        e.preventDefault();
        go(index + 1);
      }
    });

    if (viewport) {
      viewport.addEventListener(
        "touchstart",
        function (e) {
          if (!e.touches || !e.touches.length) return;
          swiping = true;
          touchStartX = e.touches[0].clientX;
          touchDeltaX = 0;
          if (track) track.style.transition = "none";
        },
        { passive: true }
      );

      viewport.addEventListener(
        "touchmove",
        function (e) {
          if (!swiping || !e.touches || !e.touches.length) return;
          touchDeltaX = e.touches[0].clientX - touchStartX;
          if (track) {
            var base = -index * 100;
            var offsetPct =
              (touchDeltaX / Math.max(viewport.clientWidth, 1)) * 100;
            track.style.transform =
              "translate3d(" + (base + offsetPct) + "%, 0, 0)";
          }
        },
        { passive: true }
      );

      viewport.addEventListener(
        "touchend",
        function () {
          if (!swiping) return;
          swiping = false;
          if (track) track.style.transition = "";
          var threshold = Math.min(72, viewport.clientWidth * 0.18);
          if (touchDeltaX > threshold) go(index - 1);
          else if (touchDeltaX < -threshold) go(index + 1);
          else render();
          touchDeltaX = 0;
        },
        { passive: true }
      );
    }

    render();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", certsLightbox);
  } else {
    certsLightbox();
  }
})();
