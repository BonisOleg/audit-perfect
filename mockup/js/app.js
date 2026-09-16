(function () {
  function markActive() {
    const page = document.body.getAttribute("data-page") || "";
    document.querySelectorAll("[data-nav]").forEach(function (link) {
      if (link.getAttribute("data-nav") === page) {
        link.classList.add("is-active");
      }
    });
    const file = (location.pathname.split("/").pop() || "").split("?")[0];
    document.querySelectorAll(".nav-sub a, .drawer__panel a").forEach(function (link) {
      const href = (link.getAttribute("href") || "").split("?")[0];
      if (href && file && href === file) {
        link.classList.add("is-active");
      }
    });
  }

  function headerScroll() {
    const onScroll = function () {
      document.body.classList.toggle("is-scrolled", window.scrollY > 24);
    };
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
  }

  function drawer() {
    const menu = document.querySelector("[data-drawer]");
    const openBtn = document.querySelector("[data-menu-open]");
    const closeBtn = document.querySelector("[data-menu-close]");
    const backdrop = document.querySelector("[data-drawer-backdrop]");
    if (!menu || !openBtn) return;

    const open = function () {
      menu.classList.add("is-open");
      openBtn.setAttribute("aria-expanded", "true");
      document.body.style.overflow = "hidden";
    };
    const close = function () {
      menu.classList.remove("is-open");
      openBtn.setAttribute("aria-expanded", "false");
      document.body.style.overflow = "";
    };

    openBtn.addEventListener("click", open);
    closeBtn && closeBtn.addEventListener("click", close);
    backdrop && backdrop.addEventListener("click", close);
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape") close();
    });
  }

  function reveal() {
    const nodes = document.querySelectorAll(".reveal");
    if (!nodes.length) return;
    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
      nodes.forEach(function (el) { el.classList.add("is-visible"); });
      return;
    }
    const io = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            entry.target.classList.add("is-visible");
            io.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.12, rootMargin: "0px 0px -40px 0px" }
    );
    nodes.forEach(function (el) {
      var box = el.getBoundingClientRect();
      if (box.top < window.innerHeight * 0.9 && box.bottom > 64) {
        el.classList.add("is-visible");
        return;
      }
      io.observe(el);
    });
  }

  function share() {
    const root = document.querySelector("[data-share]");
    if (!root) return;
    const url = encodeURIComponent(window.location.href);
    const title = encodeURIComponent(document.title);
    const telegram = root.querySelector("[data-share-telegram]");
    const facebook = root.querySelector("[data-share-facebook]");
    const linkedin = root.querySelector("[data-share-linkedin]");
    const copy = root.querySelector("[data-share-copy]");
    if (telegram) {
      telegram.href = "https://t.me/share/url?url=" + url + "&text=" + title;
    }
    if (facebook) {
      facebook.href = "https://www.facebook.com/sharer/sharer.php?u=" + url;
    }
    if (linkedin) {
      linkedin.href = "https://www.linkedin.com/sharing/share-offsite/?url=" + url;
    }
    if (copy) {
      copy.addEventListener("click", function () {
        var label = copy.getAttribute("data-label") || copy.textContent;
        copy.setAttribute("data-label", label);
        var done = function () {
          copy.textContent = "Скопійовано";
          window.setTimeout(function () {
            copy.textContent = label;
          }, 2000);
        };
        if (navigator.clipboard && navigator.clipboard.writeText) {
          navigator.clipboard.writeText(window.location.href).then(done).catch(function () {});
        }
      });
    }
  }

  function servicesDrop() {
    const item = document.querySelector(".nav-desktop .nav-item");
    if (!item) return;
    let timer = 0;
    const open = function () {
      window.clearTimeout(timer);
      item.classList.add("is-open");
    };
    const close = function () {
      timer = window.setTimeout(function () {
        item.classList.remove("is-open");
      }, 160);
    };
    item.addEventListener("mouseenter", open);
    item.addEventListener("mouseleave", close);
    item.addEventListener("focusin", open);
    item.addEventListener("focusout", function (e) {
      if (!item.contains(e.relatedTarget)) close();
    });
  }

  function boot() {
    markActive();
    headerScroll();
    drawer();
    servicesDrop();
    reveal();
    share();
  }

  var started = false;
  function once() {
    if (started) return;
    started = true;
    boot();
  }

  document.addEventListener("partials:ready", once);
  if (!document.querySelector("[data-include]")) once();
  window.setTimeout(once, 800);
})();
